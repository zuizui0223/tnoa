#!/usr/bin/env python3
"""Explicit site×date fixed-effect check for wind effects among actual flower visits.

This check was defined AFTER the exploratory result and is NOT confirmatory.
It isolates within-site-day wind variation rather than treating repeated weather
periods as independent field days. A rank/fit failure is a scientific HOLD.
"""
from collections import defaultdict
from pathlib import Path
import json
import numpy as np
from test_three_bee_guilds import build,fit_poisson,GROUPS
from test_amount_vs_guild import fit_comp

SEED=20261119+515
N=999

def prepare(rows,wind=None):
    n=len(rows)
    keys=sorted(set((r["field"],r["date"]) for r in rows))
    idx=np.asarray([keys.index((r["field"],r["date"])) for r in rows])
    groups=[np.where(idx==i)[0] for i in range(len(keys))]
    w=np.array([r["wind"] for r in rows]) if wind is None else np.array(wind)
    iqr=float(np.quantile([r["wind"] for r in rows],.75)-
              np.quantile([r["wind"] for r in rows],.25))
    w=w.copy()
    for g in groups:w[g]-=w[g].mean()
    w/=iqr
    locs=sorted(set(r["location"] for r in rows))
    clock=np.array([r["clock"]/3600 for r in rows],float)
    clock=(clock-14)/5
    # Fixed observed survey-day effects; never interpret as independent site replication
    X0=np.column_stack([np.ones(n)]+[
        (idx==i).astype(float) for i in range(1,len(keys))]+[
        np.asarray([r["location"]==loc for r in rows],float)
        for loc in locs[1:]]+[clock,clock*clock])
    X1=np.column_stack([X0,w])
    return (X0,X1,groups,keys,{"rank_reduced":int(np.linalg.matrix_rank(X0)),
        "rank_full":int(np.linalg.matrix_rank(X1)),
        "columns_reduced":X0.shape[1],"columns_full":X1.shape[1],
        "within_day_wind_scale_IQR":iqr,
        "groups_with_2plus_distinct_wind":sum(len(set(float(v) for v in w[g]))>=2 for g in groups),
        "group_n":len(groups)})

def main():
    gate,rows=build()
    if gate["status"]!="PASS":raise SystemExit("RAW_SOURCE_GATE_HOLD_"+gate["status"])
    X0,X1,groups,keys,diag=prepare(rows)
    good=[np.asarray(g,dtype=int) for g in groups
          if len(g)>1 and len(set(rows[int(i)]["wind"] for i in g))>1]
    output={"schema":"tnoa-irish-3bee-within-field-date-fixed-effect-sensitivity-v1",
     "scientific_status":"post-result adversarial sensitivity only, not prospective ecological confirmation",
     "source_sha256":gate["source_sha256"],
     "unique_raw_transects":124,"eligible_transects":len(rows),
     "site_date_group_count":len(groups),
     "source_support":diag,
     "n_permutable_groups":len(good),
     "n_permutable_rows":sum(len(g) for g in good),
     "permutations":N,
     "null_description":"Shuffle wind within each observed site×date block, retaining all response vectors. Reduced and full fits include fixed site×date effects.",
     "limitations":["Only 3 fields and 10 observation dates; 17 site×date clusters, not 120 independent weather histories.",
       "No randomized wind treatment; dependence within the day cannot be fully eliminated.",
       "Post hoc sensitivity; no protected new ecological study.",
       "Original four-guild target remains HOLD; only the three observed bee guilds are valid."]}
    if X0.shape[1]!=diag["rank_reduced"] or X1.shape[1]!=diag["rank_full"]:
        output["status"]="HOLD_FIXED_EFFECT_RANK"
    elif len(good)<6 or sum(map(len,good))<30:
        output["status"]="HOLD_WITHIN_DAY_WIND_SUPPORT"
    else:
        Y=np.array([[r["counts"][g] for g in GROUPS] for r in rows],float)
        y=Y.sum(axis=1)
        off=np.log(np.asarray([r["minutes"] for r in rows],float)/15)
        base=fit_poisson(X0,y,off);full=fit_poisson(X1,y,off)
        bcomp=fit_comp(X0,Y);fcomp=fit_comp(X1,Y)
        output["source_fit_status"]={k:{"ok":v["ok"],"gradient_norm":v["grad"] if "grad" in v else v["gradient_norm"],
              "message":v["message"]} for k,v in
              [("quantity_reduced",base),("quantity_full",full),
               ("guild_reduced",bcomp),("guild_full",fcomp)]}
        count_estimable=base["ok"] and full["ok"]
        guild_estimable=bcomp["ok"] and fcomp["ok"]
        output["guild_status"]="ESTIMABLE" if guild_estimable else "HOLD_DATE_FIXED_EFFECT_GUILD_OPTIMIZER"
        output["count_status"]="ESTIMABLE" if count_estimable else "HOLD_DATE_FIXED_EFFECT_COUNT_OPTIMIZER"
        if not count_estimable and not guild_estimable:
            output["status"]="HOLD_DATE_FIXED_EFFECT_OPTIMIZER"
        else:
            obs_count=2*(base["nll"]-full["nll"]) if count_estimable else None
            obs_comp=2*(bcomp["nll"]-fcomp["nll"]) if guild_estimable else None
            rate=float(np.exp(full["theta"][-1])) if count_estimable else None
            rng=np.random.default_rng(SEED)
            winds=np.array([r["wind"] for r in rows],float)
            nullcount=[];nullcomp=[];badcount=0;badcomp=0
            for _ in range(N):
                w=winds.copy()
                for g in good:
                    w[g]=winds[rng.permutation(g)]
                _,Xp,_,_,_=prepare(rows,w)
                if np.linalg.matrix_rank(Xp)!=Xp.shape[1]:
                    raise ValueError("Permutation design rank changed")
                if count_estimable:
                    c=fit_poisson(Xp,y,off)
                    if c["ok"]:nullcount.append(max(0,2*(base["nll"]-c["nll"])))
                    else:badcount+=1
                if guild_estimable:
                    v=fit_comp(Xp,Y)
                    if v["ok"]:nullcomp.append(max(0,2*(bcomp["nll"]-v["nll"])))
                    else:badcomp+=1
            count_valid=count_estimable and badcount==0 and len(nullcount)==N
            guild_valid=guild_estimable and badcomp==0 and len(nullcomp)==N
            output.update({
              "status":("EXPLORATORY_ESTIMATED" if count_valid and guild_valid else
                        "PARTIAL_COUNT_ESTIMATED_GUILD_HOLD" if count_valid and not guild_valid else
                        "PARTIAL_GUILD_ESTIMATED_COUNT_HOLD" if guild_valid and not count_valid else
                        "HOLD_NULL_OPTIMIZER"),
              "count_deviance_gain":obs_count,"guild_deviance_gain":obs_comp,
              "within_day_count_rate_ratio_per_source_wind_IQR":rate,
              "null_count_exceedances":sum(v>=obs_count-1e-8 for v in nullcount)
                   if obs_count is not None else None,
              "null_guild_exceedances":sum(v>=obs_comp-1e-8 for v in nullcomp)
                   if obs_comp is not None else None,
              "null_count_fit_failures":badcount,"null_guild_fit_failures":badcomp,
              "within_day_count_permutation_p":(
                (1+sum(v>=obs_count-1e-8 for v in nullcount))/(N+1) if count_valid else None),
              "within_day_guild_permutation_p":(
                (1+sum(v>=obs_comp-1e-8 for v in nullcomp))/(N+1) if guild_valid else None)})
    out=Path("research/natural_flower_wind/THREE_BEE_SITE_DATE_FIXED_EFFECT_2026-11-19.json")
    out.write_text(json.dumps(output,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
    print("IRISH_DATE_FIXED_EFFECT",json.dumps(output,ensure_ascii=False)[:14000])
    if output["status"] not in ("EXPLORATORY_ESTIMATED","HOLD_FIXED_EFFECT_RANK",
      "HOLD_WITHIN_DAY_WIND_SUPPORT","HOLD_DATE_FIXED_EFFECT_OPTIMIZER","HOLD_NULL_OPTIMIZER",
       "PARTIAL_COUNT_ESTIMATED_GUILD_HOLD","PARTIAL_GUILD_ESTIMATED_COUNT_HOLD"):
        raise SystemExit("Unknown result state")
if __name__=="__main__":main()
