#!/usr/bin/env python3
"""Crall 2020 published total-arrival result: post-result matched-model comparison.

This is NOT a new biological discovery. A secondary comparison of male orchid-
bee numbers to the species-composition endpoint, using the identical original
70 scent-bait sessions and the same site/bait/date and permutation strata.
"""
from __future__ import annotations
import argparse
import json
from pathlib import Path

import numpy as np
from crall_species_wind_test import eligibility,PERM_SEED

def objective(b,X,y):
    linear=X@b
    expected=np.exp(np.clip(linear,-20,20))
    f=float(np.sum(expected-y*linear))
    g=X.T@(expected-y)
    return f,g,expected

def fit(X,y):
    theta=np.zeros(X.shape[1]);reason="maxiter"
    for iteration in range(100):
        val,gradient,mu=objective(theta,X,y)
        if np.linalg.norm(gradient)<1e-7:
            reason="gradient_tolerance";break
        H=X.T@(mu[:,None]*X)
        try:
            delta=np.linalg.solve(H + np.eye(len(theta))*1e-9,gradient)
        except np.linalg.LinAlgError:
            reason="singular";break
        alpha=1.
        for j in range(25):
            beta=theta-alpha*delta
            new,_,_=objective(beta,X,y)
            if np.isfinite(new) and new<=val-1e-8*alpha*np.dot(gradient,delta):break
            alpha/=2.
        else:
            reason="backtracking_failed";break
        theta=beta
    val,gradient,mu=objective(theta,X,y)
    return {"ok":bool(np.linalg.norm(gradient)<1e-5),
            "nll_ignoring_logfactorials":float(val),
            "theta":theta,"iterations":iteration+1,"reason":reason,
            "gradient_norm":float(np.linalg.norm(gradient)),
            "pearson_overdispersion":float(np.sum((y-mu)**2/np.maximum(mu,1e-9))/(len(y)-X.shape[1]))}

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--input",default="research/wind_process_overlap/crall_derived_session_matrix.json")
    ap.add_argument("--output",default="research/wind_process_overlap/crall_total_count_reference_result.json")
    ap.add_argument("--permutations",type=int,default=999)
    args=ap.parse_args()
    source=json.loads(Path(args.input).read_text())
    e=eligibility(source)
    if e["status"]!="ELIGIBLE":raise ValueError("Locked cohort does not satisfy source validity")
    X0,X1=e["X0"],e["X1"]
    y=np.asarray([float(r["count"]) for r in source["survey_sessions"]])
    assert len(y)==70 and sum(y)==409 and sum(y==0)==3
    base=fit(X0,y);full=fit(X1,y)
    assert base["ok"] and full["ok"],"Unable to fit stated auxiliary count model"
    gain=float(2*(base["nll_ignoring_logfactorials"]-full["nll_ignoring_logfactorials"]))
    rng=np.random.default_rng(PERM_SEED)
    perms=[]
    for rep in range(args.permutations):
        wp=e["wc"].copy()
        for group in e["permutation_groups"]:
            ix=np.array(group,int);wp[ix]=e["wc"][rng.permutation(ix)]
        fitted=fit(np.column_stack([X0,wp]),y)
        if not fitted["ok"]:raise RuntimeError("Auxiliary count permutation failed")
        perms.append(max(0.,2*(base["nll_ignoring_logfactorials"]-fitted["nll_ignoring_logfactorials"])))
    p=(1+sum(v>=gain-1e-8 for v in perms))/(1+args.permutations)
    site_leaveout=[]
    sites=e["sites"]
    for i,s in enumerate(e["site_names"]):
        ix=np.where(sites!=i)[0]
        m=np.delete(X1[ix],i if i>0 else 1,axis=1)
        f=fit(m,y[ix])
        site_leaveout.append({"site":s,"ok":f["ok"],"log_rate_ratio":float(f["theta"][-1]),
                              "relative_rate":float(np.exp(f["theta"][-1]))})
    result={
      "schema":"tnoa-crall-published-count-comparator-v1",
      "analysis_date":"2026-11-19",
      "status":"EXPLORATORY_REPLAY_OF_PUBLISHED_WIND_ABUNDANCE_ASSOCIATION",
      "scientific_role":"auxiliary source-author result, NOT novel ecological confirmation and NOT primary composition outcome",
      "source_zip_sha256":source["source"]["sha256"],
      "n_sessions":70,"n_sites":len(e["site_names"]),"n_total_bees":409,"n_zero_sessions":3,
      "model":"Poisson session counts; site + bait + linear day vs same + within-site-centered log(mean wind)/pooled log IQR",
      "deviance_gain":gain,
      "log_count_ratio_per_log_wind_iqr":float(full["theta"][-1]),
      "count_ratio_per_log_wind_iqr":float(np.exp(full["theta"][-1])),
      "poisson_pearson_overdispersion":full["pearson_overdispersion"],
      "permutation":{"n":args.permutations,"seed":PERM_SEED,"strata":"site×bait session-level",
                     "null_exceedances":sum(v>=gain-1e-8 for v in perms),
                     "plus_one_p":p,"median":float(np.median(perms)),
                     "q95":float(np.quantile(perms,.95))},
      "leave_one_site_out":site_leaveout,
      "limitations":[
        "Source authors already identified positive wind/total-bee association; this is a post hoc matched-specification comparison.",
        "Poisson mean model shows overdispersion; the permutation p assumes exchangeable wind within site/bait across dates.",
        "Scent-bait attraction of male bees is not natural flower visitation or pollen transfer.",
        "No weather intervention, independent studies, or observational detection correction.",
        "Source publication and frozen genus-level HOLD remain unchanged."
      ]}
    out=Path(args.output);out.parent.mkdir(parents=True,exist_ok=True)
    out.write_text(json.dumps(result,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
    print("CRALL_COUNT_REFERENCE",json.dumps({
       "n":len(y),"wind_count_ratio":result["count_ratio_per_log_wind_iqr"],
       "deviance":gain,"p":p,
       "overdispersion":result["poisson_pearson_overdispersion"]}))

if __name__=="__main__": main()
