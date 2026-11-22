#!/usr/bin/env python3
"""Exploratory day-matched wind contrast of recorded bee RFID return identities.

This is a source-year-provenance-limited estimate of *recorded return events*
conditional on both RFID systems having any antenna reads in a 15-min bin.
It is NOT a relative abundance comparison, true foraging rate or wind causal
effect; the original files report 2020 while the paper methods report 2021.
No biological claim is unlocked if source/timing/coverage gates fail.
"""
from __future__ import annotations
from collections import defaultdict
from pathlib import Path
import argparse,json,math
import numpy as np
from scipy.optimize import minimize
from scipy.special import expit
SEED=20261122
NPERM=999

def fit(X,y,n):
    """Binomial likelihood on paired recorded arrivals; modest numerical tolerance."""
    def fn(b):
        z=X@b
        loss=np.sum(n*np.logaddexp(0,z)-y*z)
        grad=X.T@(n*expit(z)-y)
        return float(loss),grad
    r=minimize(fn,np.zeros(X.shape[1]),jac=True,method="L-BFGS-B",
       options={"maxiter":1400,"ftol":1e-12,"gtol":1e-7})
    val,g=fn(r.x)
    return {"ok":bool(np.isfinite(val) and np.isfinite(g).all() and
          np.linalg.norm(g)<.05),
       "nll":val,"coefficient":r.x,
       "gradient_norm":float(np.linalg.norm(g)),
       "niter":int(r.nit),"message":str(r.message),
       "max_coefficient":float(np.max(np.abs(r.x)))}

def admission(data):
    expected={
      "weather":"1f6b28b9be072ecf0160fb587e4c5f60dc16f4694252071106957ead2d29de5a",
      "bumblebee":"0d900614ff715944fb44304bdb6fd0a5d4c30275feb7db1292816dae3db247de",
      "honeybee":"28fae38017fe0fb4459cc0147420419d3ca87508e322ec99fb67dff5996d5431"}
    if data.get("source_sha256")!=expected:
        return {"status":"HOLD_SOURCE_DRIFT"}
    if data["status"]!="DERIVED_WINDOWS_ONLY_NO_WIND_EFFECT_FIT":
        return {"status":data["status"]}
    if data["literal_source_year"]!=2020 or data["manuscript_methods_year"]!=2021:
        return {"status":"HOLD_UNEXPLAINED_YEAR_REWRITE"}
    if data["days_accepted"]<12 or data["n_paired_15min_bins"]<200:
        return {"status":"HOLD_TOO_FEW_CLEAN_WINDOWS"}
    if any(r["meteorological_30s_readings"]<20 or
            r["honeybee_any_rf_read"]<1 or r["bumblebee_any_rf_read"]<1
           for r in data["rows"]):
        return {"status":"HOLD_UNQUALIFIED_PAIRED_SENSOR_EXPOSURE"}
    if data["n_paired_15min_bins"]!=len(data["rows"]):
        return {"status":"HOLD_INCONSISTENT_DERIVED_DENOMINATOR"}
    return {"status":"PASS"}

def prepare(rows,wind_override=None,weather=False):
    dates=sorted(set(r["date"] for r in rows))
    dayids=np.array([dates.index(r["date"]) for r in rows])
    n=len(rows)
    raw=np.array([r["wind"] for r in rows]) if wind_override is None else np.asarray(wind_override)
    if not np.isfinite(raw).all():
        return None
    # Re-centering within original source-day never uses biological outcomes.
    w=raw.astype(float).copy()
    for j in range(len(dates)):
        ix=dayids==j
        w[ix]-=w[ix].mean()
    basewind=np.array([r["wind"] for r in rows])
    wind_iqr=float(np.quantile(basewind,.75)-np.quantile(basewind,.25))
    if wind_iqr<.1:return None
    w/=wind_iqr
    clock=np.array([r["hour"] for r in rows])
    clock=(clock-14)/5
    base=[np.ones(n)]+[(dayids==j).astype(float) for j in range(1,len(dates))]+[clock,clock*clock]
    if weather:
        for k in ("temperature","solar"):
            z=np.array([r[k] for r in rows])
            if not np.isfinite(z).all() or z.std()<1e-7:return None
            base.append((z-z.mean())/z.std())
    X0=np.column_stack(base)
    X1=np.column_stack(base+[w])
    if np.linalg.matrix_rank(X0)!=X0.shape[1] or np.linalg.matrix_rank(X1)!=X1.shape[1]:
        return None
    return X0,X1,wind_iqr,dates

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--input",default="research/nest_activity_wind/DERIVED_SAFE_15MIN_2026-11-22.json")
    p.add_argument("--output",default="research/nest_activity_wind/EXPLORATORY_RFID_WIND_RESULT_2026-11-22.json")
    p.add_argument("--permutations",type=int,default=NPERM)
    a=p.parse_args()
    data=json.loads(Path(a.input).read_text(encoding="utf-8"))
    gate=admission(data)
    result={"schema":"tnoa-irish-allweather-nest-RFID-wind-retrospective-v1",
        "date":"2026-11-22",
        "source_identity":data.get("source_sha256"),
        "status":"HOLD",
        "scientific_target":"Within clean nominally concurrent 15-minute RFID antenna-active bins, is the ratio of recorded tagged honeybee vs bumblebee ARRIVING labels associated with wind within source-day?",
        "evidence_owner":"TNOA ecological sidecar, original source Karbassioon & Stanley; published patterns not claimed as new",
        "source_year_mismatch":True,
        "hard_limits":[
           "The original RFID/weather CSV timestamps read 2020, whereas the source publication methods say 2021; the discrepancy has not been resolved.",
           "Two partly overlapping HOBO weather streams had disagreeing duplicate exact times; any contaminated 15-minute bin is excluded, not averaged.",
           "Only bins with >=20 unambiguous weather measurements and raw antenna reads of BOTH guilds are analyzed. This is a source-conditioned sample.",
           "Observational event direction, RFID antenna errors and missed/unread tags may covary with weather; non-detection is not absence.",
           "Bee guilds observed are not comparable population samples (honeybee pollen foragers vs bumblebee tagged workers); a ratio is a detected-return ratio, not true relative abundance.",
           "The original study had only three honeybee and three bumblebee colonies with unequal RFID recovery; the date controls do not repair receiver failure.",
           "Within-day label permutations are not experimental wind randomization and can break serial/diurnal weather dependence.",
           "No linkage to crop flower visits/pollen transfer: field transects sampled different dates/places and selected favorable weather.",
           "This is one pre-published source with a separate measurement channel, not independent external ecological replication."]}
    if gate["status"]!="PASS":
        result["status"]=gate["status"]
    else:
        rows=data["rows"]
        Yh=np.array([r["honeybee_arriving"] for r in rows],float)
        Yb=np.array([r["bumblebee_arriving"] for r in rows],float)
        total=Yh+Yb
        active=np.where(total>0)[0]
        result["source_scope"]={
          "matched_days":data["days_accepted"],
          "clean_paired_antenna_bins":len(rows),
          "bins_with_recorded_return":len(active),
          "recorded_honey_returns":int(Yh.sum()),
          "recorded_bumble_returns":int(Yb.sum()),
          "source_original_honey_tag_read_n":data["rfid_source_qc"]["honeybee"]["unique_tag_ids_with_accepted_arrivals"],
          "source_original_bumble_tag_read_n":data["rfid_source_qc"]["bumblebee"]["unique_tag_ids_with_accepted_arrivals"]}
        if len(active)<150 or min(Yh.sum(),Yb.sum())<50:
            result["status"]="HOLD_RARE_TAGGED_ARRIVALS"
        else:
            # Drop zero-return bins from conditional identity likelihood but
            # retain them in source scope, without calling them biological absences.
            indexed=[rows[i] for i in active]
            y=Yh[active];n=total[active]
            prepared=prepare(indexed)
            if prepared is None:
                result["status"]="HOLD_DESIGN_RANK_OR_WIND"
            else:
                X0,X1,iqr,dates=prepared
                null=fit(X0,y,n);full=fit(X1,y,n)
                if not (null["ok"] and full["ok"]):
                    result["status"]="HOLD_MAIN_NUMERIC_FIT"
                    result["fit"]={"reduced_ok":null["ok"],"full_ok":full["ok"],
                       "reduced_grad":null["gradient_norm"],"full_grad":full["gradient_norm"]}
                else:
                    observed=float(2*(null["nll"]-full["nll"]))
                    if observed<-1e-6:
                        result["status"]="HOLD_INVALID_LIKELIHOOD_GAIN"
                    else:
                        # Permute original source exposures within literal day × daypart;
                        # weather label moves with no taxon or timestamp information.
                        strata=defaultdict(list)
                        for i,row in enumerate(indexed):
                            hr=row["hour"]
                            period="morning" if hr<11 else "afternoon" if hr<16 else "evening"
                            strata[(row["date"],period)].append(i)
                        groups=[g for g in strata.values() if len(g)>=2 and
                               len({indexed[i]["wind"] for i in g})>=2]
                        npermutable=sum(len(g) for g in groups)
                        result["permutation_support"]={
                            "distinct_date_daypart_strata":len(strata),
                            "permutable_strata":len(groups),
                            "permutable_positive_return_bins":npermutable}
                        if len(groups)<10 or npermutable<150:
                            result["status"]="HOLD_DAYPART_PERMUTATION_SUPPORT"
                        else:
                            rng=np.random.default_rng(SEED)
                            basewind=np.asarray([r["wind"] for r in indexed])
                            null_gains=[];fail=0
                            for rep in range(a.permutations):
                                shuffled=basewind.copy()
                                for g in groups:
                                    idx=np.array(g,dtype=int)
                                    shuffled[idx]=basewind[rng.permutation(idx)]
                                prep=prepare(indexed,wind_override=shuffled)
                                if prep is None:
                                    fail+=1;continue
                                pfull=fit(prep[1],y,n)
                                if pfull["ok"]:
                                    null_gains.append(max(0.,float(2*(null["nll"]-pfull["nll"]))))
                                else:fail+=1
                            valid=fail==0 and len(null_gains)==a.permutations
                            pvalue=(1+sum(z>=observed-1e-8 for z in null_gains))/(a.permutations+1) if valid else None
                            # Separate weather control is a sensitivity, not a new test.
                            sens=prepare(indexed,weather=True)
                            sens_res={"status":"HOLD_WEATHER_COVARIATES"}
                            if sens is not None:
                                f0=fit(sens[0],y,n);f1=fit(sens[1],y,n)
                                if f0["ok"] and f1["ok"]:
                                    sens_res={
                                        "status":"EXPLORATORY_ESTIMATED",
                                        "wind_odds_ratio":float(np.exp(f1["coefficient"][-1])),
                                        "deviance_gain":float(2*(f0["nll"]-f1["nll"]))}
                            # Leave-one-source-day-out is a fragility check,
                            # not a second search for significance.
                            leftout=[]
                            for held in dates:
                                keep_rows=[row for row in indexed if row["date"]!=held]
                                ty=np.array([r["honeybee_arriving"] for r in keep_rows],float)
                                tn=ty+np.array([r["bumblebee_arriving"] for r in keep_rows],float)
                                sub=prepare(keep_rows)
                                if sub is None:
                                    leftout.append({"excluded_day":held,"status":"HOLD_DESIGN"})
                                    continue
                                sf0=fit(sub[0],ty,tn);sf1=fit(sub[1],ty,tn)
                                if not (sf0["ok"] and sf1["ok"]):
                                    leftout.append({"excluded_day":held,"status":"HOLD_OPTIMIZER"})
                                else:
                                    leftout.append({"excluded_day":held,
                                        "status":"EXPLORATORY_ESTIMATED",
                                        "odds_ratio_per_local_wind_IQR":float(np.exp(sf1["coefficient"][-1])),
                                        "deviance_gain":float(2*(sf0["nll"]-sf1["nll"]))})
                            result.update({
                                "status":"EXPLORATORY_ESTIMATED" if valid else "HOLD_PERMUTATION_FIT",
                                "model":{"reference":"binomial honey arrivals among recorded honey+bumble arrivals in matched sensor-active bins",
                                  "reduced":"date fixed + quadratic clock time",
                                  "full":"reduced + within-date centered mean 15min wind / source wind IQR",
                                  "wind_IQR_mps":iqr,
                                  "deviance_gain":observed,
                                  "odds_ratio_detected_honey_vs_bumble_per_wind_IQR":float(np.exp(full["coefficient"][-1])),
                                  "honey_wind_coef":float(full["coefficient"][-1]),
                                  "reduced_grad":null["gradient_norm"],"full_grad":full["gradient_norm"],
                                  "max_coefficient":full["max_coefficient"]},
                                "permutation":{"n":a.permutations,"seed":SEED,
                                  "scheme":"shuffle same 15min-bin wind within literal date×daypart; no outcome moved",
                                  "failed_fits":fail,
                                  "n_at_or_above_observed":sum(z>=observed-1e-8 for z in null_gains),
                                  "plus_one_p":pvalue,
                                  "median_null_deviance":float(np.median(null_gains)) if null_gains else None,
                                  "q95_null_deviance":float(np.quantile(null_gains,.95)) if null_gains else None},
                                "weather_adjusted_sensitivity":sens_res,
                                "leave_one_source_day_out":leftout})
    path=Path(a.output);path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text(json.dumps(result,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
    print("TNOA_RFID_WIND_CONDITIONAL_RETURN_RESULT",json.dumps({
      "status":result["status"],"scope":result.get("source_scope"),
      "model":result.get("model"),"permutation":result.get("permutation"),
      "weather_adjusted_sensitivity":result.get("weather_adjusted_sensitivity"),
      "gates":result.get("permutation_support")},ensure_ascii=False)[:14000])
    if result["status"].startswith("HOLD"):
        print("TNOA_RFID_ECOLOGICAL_HOLD_RETAINED")
if __name__=="__main__":main()
