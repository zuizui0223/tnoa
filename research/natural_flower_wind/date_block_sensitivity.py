#!/usr/bin/env python3
"""Adversarial *post-result* date-block wind sensitivity; does not revise main 999 test.

Source MD5 and exact fourfold source repetition are rechecked by imported build().
Whole-transect wind permutations are restricted within field×calendar date,
preserving all biological outcomes and each date's wind distribution.
Results are exploratory sensitivity, not a new preregistered confirmation.
"""
from collections import defaultdict
from pathlib import Path
import json
import numpy as np
from test_three_bee_guilds import build,fit_poisson,GROUPS
from test_amount_vs_guild import design,fit_comp,SEED

N=999
def main():
    gate, rows = build()
    if gate["status"]!="PASS":
        raise SystemExit("DATA_GATE_HOLD_"+gate["status"])
    groups=defaultdict(list)
    for i,r in enumerate(rows):
        groups[(r["field"],r["date"])].append(i)
    eligible=[g for g in groups.values() if len(g)>=2 and
              len({rows[i]["wind"] for i in g})>=2]
    eligible.sort(key=lambda g:g[0])
    n_permutable=sum(map(len,eligible))
    support={
      "site_date_groups":len(groups),
      "permutable_groups":len(eligible),
      "permutable_transects":n_permutable,
      "nonpermutable_transects":len(rows)-n_permutable,
      "group_sizes":[len(g) for g in eligible],
      "original_eligible":len(rows),
      "minimum_support_rule":"At least 6 field×date groups and 30 permutable transects"}
    output={
      "schema":"tnoa-natural-flower-3bee-site-date-adversarial-sensitivity-v1",
      "date":"2026-11-19",
      "scientific_role":"strictly post-result, non-confirmatory test of within-day versus across-day weather confounding",
      "original_source_sha256":gate["source_sha256"],
      "source_rows":496,"exact_unique_transects":124,"eligible_records":len(rows),
      "source_support":support,
      "n_permutations":N,"seed":SEED,
      "limitation":"Wind not randomized. Field-date-constrained shuffling preserves observed date means; within-day temporal/weather autocorrelation may remain and exchangeability is not guaranteed. Multiple sensitivity tests are not independent confirmations."}
    if len(eligible)<6 or n_permutable<30:
      output["status"]="HOLD_FIELD_DATE_PERMUTATION_SUPPORT"
    else:
      X0,X1=design(rows)
      if X0 is None:
        output["status"]="HOLD_DESIGN_RANK"
      else:
        y=np.array([sum(r["counts"].values()) for r in rows],float)
        Y=np.array([[r["counts"][g] for g in GROUPS] for r in rows],float)
        offset=np.log(np.array([r["minutes"] for r in rows])/15.)
        base_count=fit_poisson(X0,y,offset)
        full_count=fit_poisson(X1,y,offset)
        base_comp=fit_comp(X0,Y)
        full_comp=fit_comp(X1,Y)
        if not all(z["ok"] for z in (base_count,full_count,base_comp,full_comp)):
          output["status"]="HOLD_OPTIMIZER"
        else:
          delta_count=2*(base_count["nll"]-full_count["nll"])
          delta_comp=2*(base_comp["nll"]-full_comp["nll"])
          rng=np.random.default_rng(SEED+101)
          wind=np.array([r["wind"] for r in rows])
          null_count=[];null_comp=[];failed_count=0;failed_comp=0
          for rep in range(N):
            shuffled=wind.copy()
            for group in eligible:
              ix=np.asarray(group,int)
              shuffled[ix]=wind[rng.permutation(ix)]
            _,X1p=design(rows,wind=shuffled)
            if X1p is None:raise ValueError("Permutation changed model rank")
            c=fit_poisson(X1p,y,offset)
            m=fit_comp(X1p,Y)
            if c["ok"]:null_count.append(max(0,2*(base_count["nll"]-c["nll"])))
            else:failed_count+=1
            if m["ok"]:null_comp.append(max(0,2*(base_comp["nll"]-m["nll"])))
            else:failed_comp+=1
          valid=failed_count==0 and failed_comp==0
          pcount=(1+sum(v>=delta_count-1e-8 for v in null_count))/(N+1) if valid else None
          pcomp=(1+sum(v>=delta_comp-1e-8 for v in null_comp))/(N+1) if valid else None
          output.update({
            "status":"EXPLORATORY_ESTIMATED" if valid else "HOLD_PERMUTATION_OPTIMIZER",
            "replay_base_continuous_wind_model_unchanged":True,
            "observed_count_deviance":delta_count,
            "observed_guild_deviance":delta_comp,
            "count_wind_rate_ratio":float(np.exp(full_count["theta"][-1])),
            "field_date_permutation_count_p":pcount,
            "field_date_permutation_guild_p":pcomp,
            "null_count_exceedances":sum(v>=delta_count-1e-8 for v in null_count),
            "null_guild_exceedances":sum(v>=delta_comp-1e-8 for v in null_comp),
            "count_fit_failures":failed_count,"guild_fit_failures":failed_comp})
          # Covariate-conditioned fit only; no valid independent p or causal inference
          W0,W1=design(rows,weather=True)
          if W0 is None:
            output["temp_solar_adjusted_fit"]={"status":"HOLD_RANK_OR_MISSING"}
          else:
            v0,v1=fit_poisson(W0,y,offset),fit_poisson(W1,y,offset)
            m0,m1=fit_comp(W0,Y),fit_comp(W1,Y)
            output["temp_solar_adjusted_fit"]={
              "status":"PASS" if all(a["ok"] for a in (v0,v1,m0,m1)) else "HOLD_OPTIMIZER",
              "count_rate_ratio_per_wind_iqr":float(np.exp(v1["theta"][-1])) if v1["ok"] else None,
              "count_deviance_gain":2*(v0["nll"]-v1["nll"]) if v0["ok"] and v1["ok"] else None,
              "guild_deviance_gain":2*(m0["nll"]-m1["nll"]) if m0["ok"] and m1["ok"] else None}
    dest=Path("research/natural_flower_wind/THREE_BEE_DATE_BLOCK_SENSITIVITY_2026-11-19.json")
    dest.parent.mkdir(parents=True,exist_ok=True)
    dest.write_text(json.dumps(output,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
    print("IRISH_THREE_BEE_DATE_BLOCK",json.dumps({k:v for k,v in output.items()
      if k not in ("limitation",)},ensure_ascii=False)[:12000])
    # Scientifically valid HOLD is a completed sensitivity gate.
    if output["status"] not in ("EXPLORATORY_ESTIMATED",
        "HOLD_FIELD_DATE_PERMUTATION_SUPPORT","HOLD_DESIGN_RANK","HOLD_OPTIMIZER",
        "HOLD_PERMUTATION_OPTIMIZER"):
      raise SystemExit("Unexpected status: "+output["status"])
if __name__=="__main__":main()
