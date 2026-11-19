#!/usr/bin/env python3
"""Exploratory within-field wind associations in three bee-guild floral visits.

This is a newly frozen analysis AFTER discovering a source exact-4x duplicate
and the missing hoverfly column. The original four-guild plan remains HOLD.
Original source bytes are never committed or uploaded as an artifact.

Requires numpy/scipy. Public source is verified via Zenodo MD5 in intake.py.
"""
from __future__ import annotations
from collections import Counter,defaultdict
from pathlib import Path
from scipy.optimize import minimize
import argparse,json,math
import numpy as np

from intake import prepare,num
from test_amount_vs_guild import read_date,design,fit_comp,SEED

GROUPS=("honeybee","bumblebee","solitary")
def build():
    original, cols,enc,sha,nbytes=prepare()
    if len(original)!=496:return {"status":"HOLD_ORIGINAL_ROW_COUNT","n":len(original)},None
    counts=Counter(tuple((k,str(r.get(k,""))) for k in cols) for r in original)
    if len(counts)!=124 or set(counts.values())!={4}:
        return {"status":"HOLD_NONEXACT_DUPLICATION",
            "rows":len(original),"unique":len(counts),
            "multiplicity":dict(Counter(counts.values()))},None
    seen=set();unique=[]
    for row in original:
        key=tuple((k,str(row.get(k,""))) for k in cols)
        if key in seen:continue
        seen.add(key);unique.append(row)
    assert len(unique)==124
    idkey=[(str(r.get("site","")).strip(),str(r.get("transect","")).strip(),
            str(r.get("datetimestart","")).strip(),
            str(r.get("location","")).strip()) for r in unique]
    if len(set(idkey))!=124:
        return {"status":"HOLD_NOT_UNIQUE_TRAVERSAL_IDS",
            "n_unique_rows":124,"n_distinct_ids":len(set(idkey))},None
    if "hoverfly" in cols or "syrphid" in cols or "syrph" in cols:
        return {"status":"HOLD_UNEXPECTED_SOURCE_SEMANTICS"},None
    if "butterfly" not in cols:
        return {"status":"HOLD_MISSING_BUTTERFLY_METADATA"},None
    data=[];discards=Counter();butterflies=0;weather_missing=0
    times=[]
    for i,r in enumerate(unique):
        dt=read_date(r["datetimestart"])
        end=read_date(r["datetimeend"])
        minutes=(end-dt).total_seconds()/60
        if minutes<0:minutes+=24*60
        times.append(minutes)
        cn={}
        valid=True
        for guild in GROUPS:
            vals=[num(r.get(guild)),num(r.get(guild+"_pollen"))]
            if any(v is None or not math.isfinite(v) or v<0 or abs(v-round(v))>1e-8 for v in vals):
                valid=False;break
            cn[guild]=int(sum(vals))
        butterfly=num(r.get("butterfly"))
        if butterfly is not None and butterfly>=0 and int(butterfly)==butterfly:
            butterflies+=int(butterfly)
        else:discards["invalid_butterfly_metadata"]+=1
        if not valid:
            discards["invalid_bee_count"]+=1;continue
        if not 10<=minutes<=25:
            discards["invalid_effort_duration"]+=1;continue
        wind=num(r.get("meanwindspd"))
        clock=num(r.get("secssincemidnight"))
        if wind is None or not math.isfinite(wind):
            discards["missing_wind"]+=1;weather_missing+=1;continue
        if wind<0 or wind>45 or clock is None or not (0<=clock<=86400):
            discards["invalid_weather_or_clock"]+=1;continue
        data.append({
            "source_unique_index":i,
            "field":str(r["site"]).strip(),
            "location":str(r["location"]).strip().lower(),
            "date":dt.date().isoformat(),
            "hour":clock/3600.,
            "clock":clock,
            "wind":wind,
            "counts":cn,
            "minutes":minutes,
            "temp":num(r.get("meantemp")),
            "solar":num(r.get("meansolar")),
            "rh":num(r.get("meanrh"))
        })
    durationgood=sum(14<=t<=16 for t in times)
    if durationgood/len(times)<.90:
        return {"status":"HOLD_INCONSISTENT_TRANSECT_EFFORT",
            "n_original_unique":len(times),"min_minutes":min(times),
            "max_minutes":max(times),"within_14_16_fraction":durationgood/len(times)},None
    fields=sorted(set(r["field"] for r in data))
    dates=sorted(set(r["date"] for r in data))
    if len(data)<.95*124 or len(fields)!=3 or len(dates)<6:
        return {"status":"HOLD_FIELD_OR_DATE_SUPPORT","eligible":len(data),
            "fields":len(fields),"dates":len(dates),"discard":dict(discards)},None
    w=np.array([r["wind"] for r in data],float)
    iqr=float(np.quantile(w,.75)-np.quantile(w,.25))
    if iqr<=.1 or sum(len(set(r["wind"] for r in data if r["field"]==f))>=3 for f in fields)<2:
        return {"status":"HOLD_WEATHER_SUPPORT","iqr":iqr,"range":[float(w.min()),float(w.max())]},None
    tally=Counter();pos=defaultdict(lambda:{"events":set(),"fields":set()})
    for i,r in enumerate(data):
        for g,n in r["counts"].items():
            tally[g]+=n
            if n:
                pos[g]["events"].add(i);pos[g]["fields"].add(r["field"])
    supported=[g for g in GROUPS if tally[g]>=25 and len(pos[g]["events"])>=10 and len(pos[g]["fields"])>=2]
    if len(supported)<3:
        return {"status":"HOLD_BEE_GUILD_SUPPORT","guilds":dict(tally),"supported":supported},None
    strata=defaultdict(list)
    for i,r in enumerate(data):
        t=r["hour"]
        part="early" if t<11 else "mid" if t<16 else "late"
        strata[(r["field"],part)].append(i)
    permutable=[a for a in strata.values() if len(a)>=2]
    if len(permutable)<6 or sum(map(len,permutable))<30:
        return {"status":"HOLD_WEATHER_PERMUTATION_SUPPORT",
            "n_groups":len(permutable),"n_rows":sum(map(len,permutable))},None
    return {
      "status":"PASS","source_sha256":sha,
      "source_rows":496,"exact_repetitions_per_unique_row":4,
      "unique_full_source_rows":124,"eligible_observations":len(data),
      "field_n":len(fields),"field_ids":fields,"n_dates":len(dates),
      "butterfly_original_events_excluded":butterflies,
      "weather_missing_unique_transects":weather_missing,
      "discarded_by_reason":dict(discards),
      "wind_iqr":iqr,"wind_range":[float(w.min()),float(w.max())],
      "effort_minutes":{"min":min(times),"median":float(np.median(times)),
        "max":max(times),"fraction_14to16":durationgood/len(times)},
      "bees_by_guild":dict(tally),
      "guild_support":{g:{"positive_transects":len(pos[g]["events"]),
        "positive_fields":len(pos[g]["fields"])} for g in GROUPS},
      "permutable_site_daypart_groups":len(permutable),
      "permutable_transects":sum(map(len,permutable)),
      "permutation_groups":permutable,
      "scientific_status":"new retrospective 3-bee analysis after structural source audit; original 4-guild target HOLD"
    },data

def fit_poisson(X,y,off):
    def fn(b):
        z=X@b+off
        mu=np.exp(np.clip(z,-22,22))
        val=float(np.sum(mu-y*z))
        grad=X.T@(mu-y)
        return val,grad
    z=minimize(fn,np.zeros(X.shape[1]),jac=True,method="L-BFGS-B",
        options={"maxiter":1000,"ftol":5e-12,"gtol":1e-8})
    val,g=fn(z.x)
    return {"ok":bool(z.success and np.isfinite(val) and np.linalg.norm(g)<.02),
            "nll":val,"theta":z.x,"grad":float(np.linalg.norm(g)),
            "message":str(z.message)}
def analyse(gate,rows,permutations):
    if gate["status"]!="PASS":
        return {"status":gate["status"],"gate":gate,
            "result":"No ecological association estimated"}
    X0,X1=design(rows)
    if X0 is None:
        return {"status":"HOLD_RANK"}
    Y=np.array([[r["counts"][g] for g in GROUPS] for r in rows],float)
    y=Y.sum(axis=1)
    off=np.log(np.asarray([r["minutes"] for r in rows],float)/15.)
    cc0,cc1=fit_poisson(X0,y,off),fit_poisson(X1,y,off)
    mc0,mc1=fit_comp(X0,Y),fit_comp(X1,Y)
    if not all(z["ok"] for z in [cc0,cc1,mc0,mc1]):
        return {"status":"HOLD_FIT","fits":{"count0":cc0["message"],"count1":cc1["message"],
              "composition0":mc0["message"],"composition1":mc1["message"]}}
    obs_count=2*(cc0["nll"]-cc1["nll"])
    obs_comp=2*(mc0["nll"]-mc1["nll"])
    if min(obs_count,obs_comp)<-1e-6:return {"status":"HOLD_INVALID_MODEL_GAIN"}
    rng=np.random.default_rng(SEED)
    wind=np.asarray([r["wind"] for r in rows],float)
    p_count=[];p_comp=[];failed_count=0;failed_comp=0
    for step in range(permutations):
        shuffled=wind.copy()
        for group in gate["permutation_groups"]:
            idx=np.asarray(group,int)
            shuffled[idx]=wind[rng.permutation(idx)]
        _,Xperm=design(rows,wind=shuffled)
        if Xperm is None:return {"status":"HOLD_PERMUTATION_RANK"}
        cc=fit_poisson(Xperm,y,off)
        mc=fit_comp(Xperm,Y)
        if cc["ok"]:p_count.append(max(0.,2*(cc0["nll"]-cc["nll"])))
        else:failed_count+=1
        if mc["ok"]:p_comp.append(max(0.,2*(mc0["nll"]-mc["nll"])))
        else:failed_comp+=1
    null_ok=failed_count==0 and failed_comp==0 and len(p_count)==permutations and len(p_comp)==permutations
    def pvalue(stat,a):
        return (1+sum(v>=stat-1e-8 for v in a))/(permutations+1) if null_ok else None
    b=mc1["coefficients"].reshape(X1.shape[1],len(GROUPS)-1)
    active=np.where(Y.sum(axis=1)>0)[0]
    shift=np.zeros(X1.shape[1]);shift[-1]=.5
    def prob(z):
        a=np.column_stack([z,np.zeros(z.shape[0])])
        return np.exp(a - np.logaddexp.reduce(a,axis=1,keepdims=True))
    pa=prob((X1[active]-shift)@b)
    pb=prob((X1[active]+shift)@b)
    pred=dict(zip(GROUPS,(pb-pa).mean(axis=0).tolist()))
    caution=[]
    leave={}
    for field in gate["field_ids"]:
        rem=[r for r in rows if r["field"]!=field]
        x0,x1=design(rem)
        if x0 is None:
            leave[field]={"status":"HOLD_RANK"};continue
        y_rem=np.array([sum(r["counts"].values()) for r in rem],float)
        Y_rem=np.array([[r["counts"][g] for g in GROUPS] for r in rem],float)
        off_rem=np.log(np.array([r["minutes"] for r in rem])/15.)
        a=fit_poisson(x1,y_rem,off_rem)
        c=fit_comp(x1,Y_rem)
        leave[field]={"status":"PASS" if a["ok"] and c["ok"] else "HOLD_FIT",
                      "count_log_wind_coef":float(a["theta"][-1]) if a["ok"] else None,
                      "guild_log_wind_coefs_vs_solitary":c["coefficients"].reshape(x1.shape[1],2)[-1].tolist() if c["ok"] else None}
    sensitivity={}
    w0,w1=design(rows,weather=True)
    if w0 is None:
        sensitivity={"status":"HOLD_WEATHER_COVARIATE_DESIGN"}
    else:
        a0,a1=fit_poisson(w0,y,off),fit_poisson(w1,y,off)
        b0,b1=fit_comp(w0,Y),fit_comp(w1,Y)
        sensitivity={"status":"PASS" if all(f["ok"] for f in [a0,a1,b0,b1]) else "HOLD_OPTIMIZER",
                    "count_dev_gain":2*(a0["nll"]-a1["nll"]) if a0["ok"] and a1["ok"] else None,
                    "composition_dev_gain":2*(b0["nll"]-b1["nll"]) if b0["ok"] and b1["ok"] else None}
    result={
      "schema":"tnoa-natural-flower-3bee-wind-v1",
      "date":"2026-11-19","status":"EXPLORATORY_ESTIMATED" if null_ok else "HOLD_PERMUTATION_FIT",
      "scientific_role":"Retrospective reanalysis AFTER source QC; original 4-guild hypothesis remains HOLD",
      "source":{"raw_sha256":gate["source_sha256"],"zenodo_record":10869660,
        "original_paper_doi":"10.1016/j.baae.2023.06.001",
        "source_rows":496,"identical_fourfold_copies":True,
        "independent_source_transects_before_missing_weather":124},
      "coverage":{k:v for k,v in gate.items() if k!="permutation_groups"},
      "quantity":{"n_15min_eligible_transects":len(rows),
          "n_zero_bee_transects":int(sum(y==0)),
          "total_bee_visits":int(y.sum()),
          "count_baseline_nll":cc0["nll"],"count_full_nll":cc1["nll"],
          "dev_gain":obs_count,
          "log_rate_change_per_wind_iqr":float(cc1["theta"][-1]),
          "rate_ratio_per_wind_iqr":float(np.exp(cc1["theta"][-1])),
          "p_plus_one":pvalue(obs_count,p_count),
          "null_exceedances":sum(v>=obs_count-1e-8 for v in p_count)},
      "identity":{"categories":list(GROUPS),
          "conditional_composition_baseline_nll":mc0["nll"],
          "conditional_composition_full_nll":mc1["nll"],
          "dev_gain":obs_comp,"p_plus_one":pvalue(obs_comp,p_comp),
          "null_exceedances":sum(v>=obs_comp-1e-8 for v in p_comp),
          "model_based_share_change_wind_iqr":pred},
      "permutation":{"n":permutations,"seed":SEED,
        "exchangeable_unit":"source unique transect, shuffled within site×daypart",
        "valid_pvalues":null_ok,"failed_quantity":failed_count,"failed_identity":failed_comp},
      "leave_one_field_out":leave,
      "weather_sensitivity":sensitivity,
      "hard_limits":[
        "Fourfold identical raw replication removed strictly at FULL-row identity; original 496 do not represent 496 independent transects.",
        "Butterfly source field is not hoverfly; three bee guilds only, no four-guild rescue.",
        "Source weather was preferentially sampled in dry/still/warm conditions; no randomized wind.",
        "Three fields and temporally related visits limit external replication and permutation exchangeability.",
        "Observed visitation counts may differ by detection, transect context, floral quantity and observation effort.",
        "One weather station traveled between fields; no independent local weather station for each field.",
        "Original authors already identified time-of-day bee group differences, not a new discovery.",
        "No difference between two p values is a formal amount-vs-identity statistical interaction test.",
        "No pollination effectiveness, transfer efficiency, fitness, or TNOA-field classifier validation."]
    }
    return result

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--output",default="research/natural_flower_wind/THREE_BEE_GUILD_RESULT_2026-11-19.json")
    p.add_argument("--permutations",type=int,default=999)
    a=p.parse_args()
    gate,rows=build()
    result=analyse(gate,rows,a.permutations)
    path=Path(a.output);path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text(json.dumps(result,indent=2,ensure_ascii=False)+"\n")
    print("THREE_BEE_GUILD_WIND_RESULT",json.dumps({
      "status":result["status"],
      "unique_raw_transects":result.get("coverage",{}).get("unique_full_source_rows"),
      "n_used":result.get("coverage",{}).get("eligible_observations"),
      "bee_visits":result.get("quantity",{}).get("total_bee_visits"),
      "amount_ratio":result.get("quantity",{}).get("rate_ratio_per_wind_iqr"),
      "amount_p":result.get("quantity",{}).get("p_plus_one"),
      "identity_p":result.get("identity",{}).get("p_plus_one"),
      "gate":result.get("coverage",{}) if result["status"].startswith("HOLD_") else "complete"
      },ensure_ascii=False)[:18000])
    if result["status"].startswith("HOLD_"):
        raise SystemExit("ECOLOGICAL_HOLD_"+result["status"])
if __name__=="__main__":main()
