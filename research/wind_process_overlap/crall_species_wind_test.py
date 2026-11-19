#!/usr/bin/env python3
"""Crall (2020) male Euglossa species × wind: independent source-linked replay.

Exploratory SECONDARY model frozen after a primary genus-support HOLD.
Wind exposure unit is session, not bee. This never measures natural pollination.
Requires crall_derived_matrix.py (source ZIP hash-checked before producing input).
No original specimen-level CSV is re-hosted.
"""
from __future__ import annotations
import argparse
from collections import Counter, defaultdict
import json
from pathlib import Path

import numpy as np
from scipy.special import logsumexp

ZIP_SHA = "d5b217261e4695e2098bde90576238018ad978c581f4b7799c15e429be19384b"
PERM_SEED = 20261019
PRIMARY_NPERM = 999

def objective(b, X, Y):
    n, p = X.shape
    k = Y.shape[1]
    z = np.column_stack([X @ b.reshape(p, k-1), np.zeros(n)])
    logp = z - logsumexp(z, axis=1, keepdims=True)
    prob = np.exp(logp)
    val = -float(np.sum(Y*logp))
    grad = X.T @ (Y.sum(axis=1)[:,None]*prob[:,:-1]-Y[:,:-1])
    return val, grad.ravel()

def hessian(b, X, Y):
    n, p = X.shape
    k = Y.shape[1]
    z = np.column_stack([X @ b.reshape(p,k-1), np.zeros(n)])
    q = np.exp(z - logsumexp(z,axis=1,keepdims=True))[:,:-1]
    total = Y.sum(axis=1)
    weights = np.einsum("ik,kl->ikl", total[:,None]*q, np.eye(k-1)) - (
        total[:,None,None]*q[:,:,None]*q[:,None,:])
    return np.einsum("ia,ib,ikl->akbl", X,X,weights,optimize=True).reshape(p*(k-1),p*(k-1))

def fit(X, Y):
    """Unpenalized multinomial MLE; tiny Hessian damping is numerical, not a prior."""
    n,p=X.shape; k=Y.shape[1]
    b=np.zeros(p*(k-1))
    reason="maxiter"
    iterations=0
    for it in range(80):
        iterations=it+1
        val,g=objective(b,X,Y)
        if np.linalg.norm(g)<1e-6:
            reason="gradient_tolerance";break
        try:
            direction=np.linalg.solve(hessian(b,X,Y)+1e-8*np.eye(len(b)),g)
        except np.linalg.LinAlgError:
            reason="singular_hessian";break
        alpha=1.
        for trial in range(22):
            candidate=b-alpha*direction
            loss,_=objective(candidate,X,Y)
            if np.isfinite(loss) and loss<=val-1e-7*alpha*np.dot(g,direction):
                break
            alpha/=2.
        else:
            reason="backtracking_failed";break
        b=candidate
    val,g=objective(b,X,Y)
    norm=float(np.linalg.norm(g))
    return {"ok":bool(np.isfinite(val) and np.all(np.isfinite(b)) and norm<2e-5),
            "nll":float(val),"parameters":b,"iterations":iterations,"reason":reason,
            "gradient_norm":norm,"max_abs_coefficient":float(np.max(np.abs(b)))}

def probability(z):
    return np.exp(z-logsumexp(z,axis=1,keepdims=True))

def eligibility(data):
    assert data["source"]["sha256"]==ZIP_SHA, "Unexpected primary source hash"
    assert len(data["survey_sessions"])==70 and data["n_linked_bees"]==409
    rows=data["survey_sessions"]
    site_names=sorted({r["site"] for r in rows})
    sites=np.asarray([site_names.index(r["site"]) for r in rows],int)
    scent=np.asarray([r["scent"] for r in rows])
    wind=np.asarray([float(r["wind_mean"]) for r in rows])
    if np.any(~np.isfinite(wind)) or np.any(wind<=0):
        return {"status":"HOLD_NONPOSITIVE_WIND"}
    by_species=Counter()
    species_sessions=defaultdict(set)
    species_sites=defaultdict(set)
    for i,r in enumerate(rows):
        for species,c in r["bee_species_counts"].items():
            if species.startswith("euglossa "):
                by_species[species]+=c
                if c:
                    species_sessions[species].add(i)
                    species_sites[species].add(r["site"])
    if sum(by_species.values())!=399:
        raise ValueError("Euglossa source count drifted")
    selected=sorted(name for name,count in by_species.items()
        if count>=25 and len(species_sessions[name])>=8 and len(species_sites[name])>=3)
    if len(selected)<2:
        return {"status":"HOLD_SPECIES_SUPPORT","n_species":len(selected)}
    categories=selected+["other_euglossa"]
    Y=np.zeros((len(rows),len(categories)))
    for i,r in enumerate(rows):
        for species,c in r["bee_species_counts"].items():
            if species.startswith("euglossa "):
                Y[i,categories.index(species) if species in selected else -1]+=c
    if abs(Y.sum()-399)>1e-8:
        raise ValueError("Species count not exhaustive")
    site_support=sum(Y[sites==j].sum()>0 for j in range(len(site_names)))
    if site_support<6:
        return {"status":"HOLD_SITE_SUPPORT","n_sites":site_support}
    logw=np.log(wind)
    logw_iqr=float(np.quantile(logw,.75)-np.quantile(logw,.25))
    if logw_iqr<=0:
        return {"status":"HOLD_WIND_RANGE"}
    wc=logw.copy()
    for j in range(len(site_names)):
        wc[sites==j]-=np.mean(logw[sites==j])
    wc/=logw_iqr
    dates=np.asarray([float(r["day_since_first"]) for r in rows])
    dates=(dates-dates.mean())/max(1.,dates.std())
    X0=np.column_stack([
       np.ones(len(rows)),
       np.array([sites==j for j in range(1,len(site_names))]).T.astype(float),
       (scent=="meth").astype(float),dates
    ])
    X1=np.column_stack([X0,wc])
    if (np.linalg.matrix_rank(X0)!=X0.shape[1]
            or np.linalg.matrix_rank(X1)!=X1.shape[1]):
        return {"status":"HOLD_DESIGN_RANK"}
    strata=defaultdict(list)
    for i,r in enumerate(rows):
        strata[(r["site"],r["scent"])].append(i)
    perm_groups=[g for g in strata.values() if len(g)>=2]
    n_perm_sessions=sum(len(g) for g in perm_groups)
    if len(perm_groups)<6 or n_perm_sessions<30:
        return {"status":"HOLD_PERMUTATION_SUPPORT",
                "n_groups":len(perm_groups),"n_sessions":n_perm_sessions}
    return {"status":"ELIGIBLE","Y":Y,"X0":X0,"X1":X1,
            "wc":wc,"sites":sites,"site_names":site_names,
            "names":categories,"selected":selected,"counts":dict(by_species),
            "permutation_groups":perm_groups,"n_permutable":n_perm_sessions,
            "iqr":logw_iqr}

def execute(infile, nperm):
    source=json.loads(Path(infile).read_text(encoding="utf-8"))
    e=eligibility(source)
    if e["status"]!="ELIGIBLE":
        return {"schema":"tnoa-crall-species-wind-v1",
                "status":e["status"],
                "source_zip_sha256":ZIP_SHA,
                "scientific_interpretation":"HOLD; no species-wind association opened",
                "eligibility":e}
    Y,X0,X1=e["Y"],e["X0"],e["X1"]
    base=fit(X0,Y); full=fit(X1,Y)
    if not (base["ok"] and full["ok"]):
        return {"status":"HOLD_PRIMARY_OPTIMIZER",
                "base_ok":base["ok"],"full_ok":full["ok"]}
    gain=float(2*(base["nll"]-full["nll"]))
    if gain<-1e-5: return {"status":"HOLD_NEGATIVE_DEVIANCE","gain":gain}
    rng=np.random.default_rng(PERM_SEED)
    perm_stats=[]
    fail=0
    for rep in range(nperm):
        wp=e["wc"].copy()
        for group in e["permutation_groups"]:
            idx=np.asarray(group,int)
            wp[idx]=e["wc"][rng.permutation(idx)]
        alternative=fit(np.column_stack([X0,wp]),Y)
        if not alternative["ok"]:
            fail+=1
        else:
            perm_stats.append(max(0.,2*(base["nll"]-alternative["nll"])))
    valid=fail==0 and len(perm_stats)==nperm
    pvalue=((1+sum(t>=gain-1e-8 for t in perm_stats))/(nperm+1)) if valid else None
    k=len(e["names"])
    beta=full["parameters"].reshape(X1.shape[1],k-1)
    active=np.where(Y.sum(axis=1)>0)[0]
    direction=np.zeros(X1.shape[1]);direction[-1]=.5
    low=probability(np.column_stack([(X1[active]-direction)@beta,np.zeros(len(active))]))
    high=probability(np.column_stack([(X1[active]+direction)@beta,np.zeros(len(active))]))
    slopes=dict(zip(e["names"][:-1],beta[-1].tolist()))
    slopes[e["names"][-1]]=0.
    changes={name:float(np.mean(high[:,j]-low[:,j]))
             for j,name in enumerate(e["names"])}
    loo=[]
    for i,site in enumerate(e["site_names"]):
        keep=np.where(e["sites"]!=i)[0]
        mat=X1[keep]
        mat=np.delete(mat,i if i>0 else 1,axis=1)
        bmat=mat[:,:-1]
        if (np.linalg.matrix_rank(mat)!=mat.shape[1] or
                np.linalg.matrix_rank(bmat)!=bmat.shape[1]):
            loo.append({"site":site,"status":"HOLD_RANK"});continue
        reduced=fit(bmat,Y[keep]); extended=fit(mat,Y[keep])
        if not (reduced["ok"] and extended["ok"]):
            loo.append({"site":site,"status":"HOLD_OPTIMIZER"});continue
        cbeta=extended["parameters"].reshape(mat.shape[1],k-1)
        loo.append({"site":site,"status":"PASS",
                    "deviance_gain":float(2*(reduced["nll"]-extended["nll"])),
                    "species_slopes_vs_other":dict(zip(e["names"][:-1],cbeta[-1].tolist()))})
    totals={name:int(Y[:,j].sum()) for j,name in enumerate(e["names"])}
    return {
      "schema":"tnoa-crall-species-wind-v1","analysis_date":"2026-11-19",
      "status": "EXPLORATORY_ESTIMATED" if valid else "HOLD_FAILED_PERMUTATIONS",
      "scientific_interpretation":"Secondary retrospective species-composition association only; prior genus-level HOLD retained",
      "source":{"archive_sha256":ZIP_SHA,
                "derived_session_schema":source["schema"],
                "zenodo_doi":"10.5281/zenodo.3675327",
                "original_article_doi":"10.1098/rsbl.2020.0103"},
      "denominators":{"source_bees":450,"joined_bees":409,"excluded_bees":41,
         "sessions":70,"sessions_with_euglossa":int(np.sum(Y.sum(axis=1)>0)),
         "euglossa":int(Y.sum()),"eulaema":10,"sites":len(e["site_names"]),
         "named_species_eligible":len(e["selected"]),
         "categories":totals,
         "permutable_site_bait_groups":len(e["permutation_groups"]),
         "permutable_sessions":e["n_permutable"]},
      "model":{"response":"male Euglossa species identities among arrivals at artificial scent bait",
         "reduced":"site fixed + scent fixed + linear date",
         "full":"reduced + log(mean wind), within-site centred, divided by pooled IQR",
         "wind_log_iqr":e["iqr"],
         "reduced_nll":base["nll"],"full_nll":full["nll"],
         "deviance_gain":gain,
         "reduced_optimizer":{v:base[v] for v in
             ["ok","iterations","reason","gradient_norm","max_abs_coefficient"]},
         "full_optimizer":{v:full[v] for v in
             ["ok","iterations","reason","gradient_norm","max_abs_coefficient"]},
         "warning_near_separation":max(base["max_abs_coefficient"],
             full["max_abs_coefficient"])>10.,
         "wind_logit_slopes_vs_other":slopes,
         "one_wind_iqr_model_share_changes":changes,
         "effect_note":"Predicted conditional shares over Euglossa-positive sessions, not causal responses or absolute visitation."},
      "permutation":{"seed":PERM_SEED,"n":nperm,
         "scheme":"shuffle whole-session wind within site×bait group",
         "fit_failures":fail,"successful":len(perm_stats),
         "null_exceedances":sum(v>=gain-1e-8 for v in perm_stats),
         "p_plus_one":pvalue,
         "null_median":float(np.median(perm_stats)) if perm_stats else None,
         "null_p95":float(np.quantile(perm_stats,.95)) if perm_stats else None},
      "leave_one_site_out":loo,
      "hard_limits":[
        "Wind was not randomized; within-site×bait permutation assumes exchangeability despite date structure.",
        "399 individual Euglossa are NOT 399 independent session-level exposures.",
        "Only male scent-bait arrivals, not flower visits, pollen transport, or reproductive fitness.",
        "Near-separation and small bait/specific-species cells limit model stability.",
        "Original work had already reported wind-total-abundance association; this is not new source data.",
        "One system, no independent ecological transfer across datasets; absence of significance is not a zero effect.",
        "Secondary test was adopted after the genus-level support gate failed; not preregistered independent confirmation."]
    }

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--input",default="research/wind_process_overlap/crall_derived_session_matrix.json")
    ap.add_argument("--output",default="research/wind_process_overlap/crall_species_wind_result.json")
    ap.add_argument("--permutations",type=int,default=PRIMARY_NPERM)
    a=ap.parse_args()
    ans=execute(a.input,a.permutations)
    path=Path(a.output)
    path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text(json.dumps(ans,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
    print("CRALL_WIND_SPECIES_RESULT",json.dumps({
      "status":ans["status"],"sample":ans.get("denominators"),
      "deviance_gain":ans.get("model",{}).get("deviance_gain"),
      "nperm":ans.get("permutation",{}).get("n"),
      "p":ans.get("permutation",{}).get("p_plus_one"),
      "failed_perm":ans.get("permutation",{}).get("fit_failures")
    }))
    if ans["status"].startswith("HOLD_"):
        raise SystemExit("HOLD: " + ans["status"])

if __name__=="__main__":main()
