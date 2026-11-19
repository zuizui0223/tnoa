#!/usr/bin/env python3
"""Independent natural Brassica floral-visitor guild wind analysis (exploratory).

Prior source-protocol frozen in PROTOCOL_2026-11-19.md; source CRC is published
Zenodo MD5. Weather association with actual recorded flower visits is NOT
causal and not an independent field intervention. Do not redistribute raw rows.
"""
from __future__ import annotations
from collections import Counter,defaultdict
from datetime import datetime
import argparse,hashlib,json,math
from pathlib import Path
import numpy as np
from scipy.optimize import minimize
from scipy.special import logsumexp
from intake import prepare, EXPECTED_MD5, num

SEED=20261119
FOUR=("honeybee","bumblebee","solitary","hoverfly")
def read_date(x):
    t=str(x).strip()
    forms=["%d-%m-%Y %H:%M","%d-%m-%y %H:%M","%d/%m/%Y %H:%M","%d/%m/%y %H:%M",
      "%Y-%m-%d %H:%M:%S","%Y-%m-%d %H:%M","%d-%m-%Y %H:%M:%S",
      "%d/%m/%Y %H:%M:%S","%m/%d/%Y %H:%M:%S","%m/%d/%Y %H:%M"]
    for f in forms:
        try:return datetime.strptime(t,f)
        except ValueError:pass
    try:return datetime.fromisoformat(t)
    except ValueError as exc:raise ValueError("UNPARSEABLE_SOURCE_DATE: "+repr(t)) from exc

def admitted():
    rows,cols,enc,sha,_=prepare()
    need=["site","location","datetimestart","datetimeend","secssincemidnight","meanwindspd",
        "honeybee","honeybee_pollen","bumblebee","bumblebee_pollen","solitary",
        "solitary_pollen"]
    missing=[x for x in need if x not in cols]
    hover=[c for c in cols if "hover" in c or "syrph" in c]
    if missing or len(hover)!=1:
        return {"gate":"HOLD_SCHEMA","missing":missing,"hover_candidates":hover,"n_rows":len(rows)},None
    data=[];bad=Counter();keys=set()
    for i,r in enumerate(rows):
        site=str(r["site"]).strip()
        start=read_date(r["datetimestart"])
        end=read_date(r["datetimeend"])
        clock=num(r["secssincemidnight"])
        wind=num(r["meanwindspd"])
        counts={}
        for k in FOUR:
            cols2= [k] if k=="hoverfly" else [k,k+"_pollen"]
            cols2=[hover[0]] if k=="hoverfly" else cols2
            values=[num(r.get(c)) for c in cols2]
            if any(v is None or not math.isfinite(v) or v<0 or abs(v-round(v))>1e-9 for v in values):
                bad["missing_or_noninteger_count"]+=1; counts=None;break
            counts[k]=int(sum(values))
        if counts is None:continue
        t=(end-start).total_seconds()/60.
        if t<0: t+=1440 # rollover
        key=(site,start.isoformat(),str(r["transect"]).strip())
        if key in keys:bad["duplicate_source_key"]+=1
        keys.add(key)
        if not (14.0<=t<=16.0):bad["not_15_min_effort"]+=1
        if clock is None or not math.isfinite(clock) or not (0<=clock<=86400):
            bad["missing_clock"]+=1;continue
        if wind is None or not math.isfinite(wind):
            bad["missing_wind"]+=1;continue
        if wind<0 or wind>45:
            bad["nonphysical_wind"]+=1;continue
        location=str(r["location"]).strip().lower()
        data.append({"source_row":i,"field":site,"location":location,
          "date":start.date().isoformat(),"clock":clock,
          "hour":clock/3600.,"wind":wind,"counts":counts,
          "temp":num(r.get("meantemp")),
          "solar":num(r.get("meansolar")),
          "rh":num(r.get("meanrh")),
          "rain":num(r.get("meanrain")),
          "minutes":t})
    if bad["duplicate_source_key"] or bad["not_15_min_effort"] or bad["nonphysical_wind"]:
        return {"gate":"HOLD_EFFORT_OR_KEYS","bad":dict(bad),"n_rows":len(rows)},None
    fields=sorted(set(r["field"] for r in data))
    dates=sorted(set(r["date"] for r in data))
    winds=np.array([r["wind"] for r in data])
    if len(data)<36 or len(fields)!=3 or len(dates)<6 or len(data)<.8*len(rows) or not len(winds):
        return {"gate":"HOLD_SAMPLE_OR_WEATHER","field_n":len(fields),
            "n_eligible":len(data),"date_n":len(dates),"n_rows":len(rows),"bad":dict(bad)},None
    iqr=float(np.quantile(winds,.75)-np.quantile(winds,.25))
    if iqr<=0.1:
        return {"gate":"HOLD_WIND_RANGE","wind_iqr":iqr,"min":float(winds.min()),
                "max":float(winds.max()),"n":len(data)},None
    tally=Counter();occ=defaultdict(lambda:{"rows":set(),"fields":set()})
    for i,r in enumerate(data):
        for k,v in r["counts"].items():
            tally[k]+=v
            if v>0:occ[k]["rows"].add(i);occ[k]["fields"].add(r["field"])
    strong=[g for g in FOUR if tally[g]>=25 and len(occ[g]["rows"])>=10 and len(occ[g]["fields"])>=2]
    if len(strong)<3:
        return {"gate":"HOLD_COMPOSITION_SUPPORT","eligible_guilds":strong,
                "guild_totals":dict(tally),"field_n":len(fields),"weather_iqr":iqr},None
    strata=defaultdict(list)
    for i,r in enumerate(data):
        hour=r["hour"]
        part="early" if hour<11 else "mid" if hour<16 else "late"
        strata[(r["field"],part)].append(i)
    per=sorted([g for g in strata.values() if len(g)>=2],key=lambda a:a[0])
    support=sum(len(g) for g in per)
    distinct=[len(set(r["wind"] for r in data if r["field"]==site)) for site in fields]
    if not (len(per)>=6 and support>=30 and sum(z>=3 for z in distinct)>=2):
        return {"gate":"HOLD_WEATHER_STRATA","strata":len(per),"permutable":support,
                "within_field_distinct_wind":distinct},None
    return {"gate":"PASS","source_sha256":sha,"source_rows":len(rows),
       "eligible_rows":len(data),"missing_cause":dict(bad),"fields":fields,
       "dates_n":len(dates),"wind_iqr":iqr,
       "wind_range":[float(winds.min()),float(winds.max())],
       "guild_totals":dict(tally),
       "guild_support":{g:{"visits":tally[g],"transects":len(occ[g]["rows"]),"fields":len(occ[g]["fields"])} for g in FOUR},
       "strong_guilds":strong,"strata_n":len(per),"permutable_n":support,
       "permutable_groups":per,
       "note":"observations of natural Brassica flower visitors; not randomized wind exposure"},data

def design(data,wind=None,weather=False):
    fields=sorted(set(r["field"] for r in data))
    locs=sorted(set(r["location"] for r in data))
    n=len(data)
    wind_raw=np.asarray([r["wind"] for r in data])
    wind_iqr=float(np.quantile(wind_raw,.75)-np.quantile(wind_raw,.25))
    w = wind_raw.copy() if wind is None else np.asarray(wind)
    wc=w.copy()
    for field in fields:
        ix=np.asarray([i for i,r in enumerate(data) if r["field"]==field])
        wc[ix]-=w[ix].mean()
    wc/=max(wind_iqr,0.1)
    clock=(np.asarray([r["clock"] for r in data])/3600.-14.)/5.
    Xcols=[np.ones(n)]+[np.asarray([r["field"]==field for r in data],float) for field in fields[1:]]
    Xcols += [np.asarray([r["location"]==loc for r in data],float) for loc in locs[1:]]
    Xcols += [clock,clock*clock]
    if weather:
        for k in ("temp","solar"):
            z=np.asarray([r[k] for r in data],float)
            if not np.isfinite(z).all() or np.std(z)<1e-6:
                return None,None
            Xcols += [(z-z.mean())/z.std()]
    X0=np.column_stack(Xcols)
    X1=np.column_stack(Xcols+[wc])
    if np.linalg.matrix_rank(X0)!=X0.shape[1] or np.linalg.matrix_rank(X1)!=X1.shape[1]:
        return None,None
    return X0,X1

def fit_count(X,y):
    def fn(b):
        z=X@b
        mu=np.exp(np.clip(z,-20,20))
        return float(np.sum(mu-y*z)),X.T@(mu-y)
    r=minimize(fn,np.zeros(X.shape[1]),jac=True,method="L-BFGS-B",
      options={"maxiter":700,"ftol":5e-12,"gtol":1e-7})
    v,g=fn(r.x)
    return {"ok":bool(r.success and np.isfinite(v) and np.linalg.norm(g)<.01),
       "nll":v,"coefficients":r.x,"gradient_norm":float(np.linalg.norm(g)),"message":str(r.message)}
def fit_comp(X,Y):
    n,p=X.shape;k=Y.shape[1]
    def fn(z):
        b=z.reshape((p,k-1))
        a=np.column_stack([X@b,np.zeros(n)])
        lp=a-logsumexp(a,axis=1,keepdims=True)
        P=np.exp(lp)
        v=-float(np.sum(Y*lp))
        g=X.T@(Y.sum(axis=1)[:,None]*P[:,:-1]-Y[:,:-1])
        return v,g.ravel()
    opt=minimize(fn,np.zeros(p*(k-1)),jac=True,method="L-BFGS-B",
       options={"maxiter":900,"ftol":5e-12,"gtol":1e-7})
    v,g=fn(opt.x)
    return {"ok":bool(opt.success and np.isfinite(v) and np.linalg.norm(g)<.03),
       "nll":v,"coefficients":opt.x,"gradient_norm":float(np.linalg.norm(g)),"message":str(opt.message)}
def run(data,gate,nperm):
    if gate["gate"]!="PASS":
        return {"status":gate["gate"],"source_gate":{k:v for k,v in gate.items() if k!="permutable_groups"}}
    X0,X1=design(data)
    if X0 is None:return {"status":"HOLD_DESIGN_RANK"}
    y=np.array([sum(r["counts"].values()) for r in data],float)
    Y=np.array([[r["counts"][k] for k in FOUR] for r in data],float)
    count0,count1=fit_count(X0,y),fit_count(X1,y)
    comp0,comp1=fit_comp(X0,Y),fit_comp(X1,Y)
    if not all(z["ok"] for z in [count0,count1,comp0,comp1]):
        return {"status":"HOLD_OPTIMIZER","fits":{k:{"ok":v["ok"],"gradient":v["gradient_norm"],"message":v["message"]} for k,v in
            [("count0",count0),("count1",count1),("comp0",comp0),("comp1",comp1)]}}
    obs_count=2*(count0["nll"]-count1["nll"])
    obs_comp=2*(comp0["nll"]-comp1["nll"])
    if obs_count<-1e-5 or obs_comp<-1e-5:return {"status":"HOLD_BAD_DEVIANCE"}
    perm_count=[];perm_comp=[];failed_count=0;failed_comp=0
    rng=np.random.default_rng(SEED)
    wind=np.array([r["wind"] for r in data])
    for b in range(nperm):
        ww=wind.copy()
        for g in gate["permutable_groups"]:
            ind=np.asarray(g,int)
            ww[ind]=wind[rng.permutation(ind)]
        _,Xp=design(data,ww)
        if Xp is None:raise ValueError("Unexpected permuted rank fail")
        a=fit_count(Xp,y); c=fit_comp(Xp,Y)
        if a["ok"]:perm_count.append(max(0.,2*(count0["nll"]-a["nll"])))
        else:failed_count+=1
        if c["ok"]:perm_comp.append(max(0.,2*(comp0["nll"]-c["nll"])))
        else:failed_comp+=1
    stable=failed_count==0 and failed_comp==0 and len(perm_count)==nperm and len(perm_comp)==nperm
    pp=lambda obs, arr:(1+sum(v>=obs-1e-8 for v in arr))/(nperm+1) if stable else None
    count_slope=float(count1["coefficients"][-1])
    comp_b=comp1["coefficients"].reshape(X1.shape[1],len(FOUR)-1)
    # linear predictions at ±half IQR on same nonzero composition rows
    active=np.where(Y.sum(axis=1)>0)[0]
    dx=np.zeros(X1.shape[1]);dx[-1]=.5
    def soft(z):
        v=np.column_stack([z,np.zeros(z.shape[0])])
        return np.exp(v-logsumexp(v,axis=1,keepdims=True))
    lo=soft((X1[active]-dx)@comp_b);hi=soft((X1[active]+dx)@comp_b)
    delta=dict(zip(FOUR,(hi-lo).mean(axis=0).tolist()))
    # not a significance comparison
    sensitivity={}
    xw0,xw1=design(data,weather=True)
    if xw0 is not None:
        b0,b1=fit_count(xw0,y),fit_count(xw1,y)
        c0,c1=fit_comp(xw0,Y),fit_comp(xw1,Y)
        sensitivity={"status":"ESTIMABLE" if all(a["ok"] for a in [b0,b1,c0,c1]) else "HOLD_OPTIMIZER",
          "count_delta_deviance":2*(b0["nll"]-b1["nll"]) if b0["ok"] and b1["ok"] else None,
          "guild_delta_deviance":2*(c0["nll"]-c1["nll"]) if c0["ok"] and c1["ok"] else None}
    else:sensitivity={"status":"HOLD_WEATHER_COVARIATE_DESIGN"}
    return {
      "schema":"tnoa-independent-natural-flower-visitor-wind-v1",
      "status":"EXPLORATORY_ESTIMATED" if stable else "HOLD_PERMUTATION_OPTIMIZER",
      "source":{"doi":"10.5061/dryad.jq2bvq8dw","zenodo_record":10869660,
          "published_md5":EXPECTED_MD5,"sha256":gate["source_sha256"]},
      "unit":"15-minute transect; field×date is the independent uncertainty context",
      "coverage":{k:v for k,v in gate.items() if k!="permutable_groups"},
      "response_labels":list(FOUR),
      "n_total_flower_visitors":int(y.sum()),
      "n_zero_transects":int(sum(y==0)),
      "count":{"baseline_nll":count0["nll"],"full_nll":count1["nll"],
          "deviance_gain":obs_count,"wind_scaled_coef":count_slope,
          "estimated_count_ratio_per_wind_iqr":float(np.exp(count_slope)),
          "permutation_p":pp(obs_count,perm_count),
          "null_exceedances":sum(v>=obs_count-1e-8 for v in perm_count),
          "pearson_overdispersion_warning":"Poisson model is working mean model, not independent-pollinator variance"},
      "guild_composition":{"baseline_nll":comp0["nll"],"full_nll":comp1["nll"],
          "deviance_gain":obs_comp,"permutation_p":pp(obs_comp,perm_comp),
          "null_exceedances":sum(v>=obs_comp-1e-8 for v in perm_comp),
          "estimated_guild_share_change_across_log_wind_iqr":delta,
          "model_limit":"Conditional on visitor observed; does not measure pollination effectiveness."},
      "permutation":{"n":nperm,"seed":SEED,"strata":"site×coarse daypart",
          "n_movable_strata":gate["strata_n"],"n_permutable_transects":gate["permutable_n"],
          "count_fit_failures":failed_count,"composition_fit_failures":failed_comp},
      "weather_sensitivity":sensitivity,
      "hard_limits":[
        "This is a post-publication reanalysis of original authors' natural flower data; not an untouched replication.",
        "Wind not randomized; relatively still/warm sampling days selected; exchangeability across site×daypart is unverified.",
        "Only three fields, limited external-generalization; transects within field-date are repeated.",
        "Main publication already demonstrated time-of-day differences in four visitor guilds.",
        "One weather logger was moved between fields; weather and survey effort/observer not experimentally separated.",
        "Two p values are not a formal statistical test that amount and identity effects differ.",
        "Visitation and pollen-load notation do not verify stigma contact, pollen transfer, plant fitness, or absolute pollinator population.",
        "No validated TNOA T/C/N/O/A- causal field observer states are inferred from this dataset."]
    }
def main():
    p=argparse.ArgumentParser()
    p.add_argument("--output",default="research/natural_flower_wind/RESULT_2026-11-19.json")
    p.add_argument("--permutations",type=int,default=999)
    args=p.parse_args()
    gate,data=admitted()
    report=run(data,gate,args.permutations)
    out=Path(args.output)
    out.parent.mkdir(parents=True,exist_ok=True)
    out.write_text(json.dumps(report,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
    print("NATURAL_FLOWER_WIND_RESULT",json.dumps({
      "status":report["status"],
      "n_rows":report.get("coverage",{}).get("eligible_rows"),
      "visitors":report.get("n_total_flower_visitors"),
      "amount_ratio":report.get("count",{}).get("estimated_count_ratio_per_wind_iqr"),
      "amount_p":report.get("count",{}).get("permutation_p"),
      "composition_p":report.get("guild_composition",{}).get("permutation_p"),
      "permutations":report.get("permutation",{}).get("n")}))
    if report["status"].startswith("HOLD_"):
        raise SystemExit("NATURAL_FLOWER_WIND_HOLD: "+report["status"])
if __name__=="__main__":main()
