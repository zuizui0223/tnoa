#!/usr/bin/env python3
"""Independent source-verified ecological behavior coexistence test.

Weschler et al. natural wildflower videos: repeated pollen and nectar actions
within the same insect–flower visit. Not a TNOA field observer validation or
a turbine/wind causal experiment. Original MD5 from Zenodo v3 is mandatory.
"""
from collections import Counter,defaultdict
from pathlib import Path
from random import Random
from urllib.request import Request,urlopen
import csv,hashlib,io,json,math,statistics

URL="https://zenodo.org/records/15447016/files/WindPollinatorData110823.csv?download=1"
MD5="9bcab4765c4fe5a9edaaf096867caf5b"
SEED=20261119
N_PERM=999

def boolfield(x):
    s=str(x if x is not None else "").strip().lower()
    if s in ("0","0.0","false","f"):return 0
    if s in ("1","1.0","true","t"):return 1
    return None

def numfield(x):
    try:
        z=float(str(x).strip())
        return z if math.isfinite(z) else None
    except (TypeError,ValueError):return None

def read():
    with urlopen(Request(URL,headers={"User-Agent":"ecology-public-archive-integrity-check/1.0"}),timeout=60) as response:
        raw=response.read()
    assert hashlib.md5(raw).hexdigest()==MD5,"Upstream Weschler source MD5 mismatch"
    rows=list(csv.DictReader(io.StringIO(raw.decode("utf-8-sig",errors="replace"))))
    return rows,hashlib.sha256(raw).hexdigest()

def analyze(rows,sha):
    must={"Unique_ID","Site","Date","Plant","CollectingPollen","DrinkNectar","WindSpeed"}
    if not rows or not must.issubset(rows[0]):
        return {"status":"HOLD_MISSING_FIELDS","fields":list(rows[0]) if rows else []}
    if len(rows)<300:return {"status":"HOLD_TOO_FEW_INTERACTIONS","n":len(rows)}
    bysession=defaultdict(list);rejected=Counter()
    for r in rows:
        id=str(r["Unique_ID"]).strip()
        p=boolfield(r["CollectingPollen"]);n=boolfield(r["DrinkNectar"])
        if not id or p is None or n is None:
            rejected["missing_id_or_binary_behavior"]+=1;continue
        bysession[id].append({
          "p":p,"n":n,"wind":numfield(r["WindSpeed"]),
          "site":str(r["Site"]).strip(),"date":str(r["Date"]).strip(),
          "plant":str(r["Plant"]).strip(),"file":str(r["FileName"]).strip()})
    total=sum(map(len,bysession.values()))
    if total<300 or len(bysession)<12:
        return {"status":"HOLD_BEHAVIOR_OR_SESSION_COUNT",
          "original_rows":len(rows),"valid_rows":total,"session_n":len(bysession),"excluded":dict(rejected)}
    contexts={}
    for sid,rr in bysession.items():
        for col in ("site","date","wind"):
            if len(set(r[col] for r in rr))!=1:
                return {"status":"HOLD_SESSION_NONUNIQUE_CONTEXT",
                  "field":col,"unique_session_id":sid,"n_values":len(set(r[col] for r in rr))}
        contexts[sid]={"site":rr[0]["site"],"date":rr[0]["date"],
                       "n_plants":len({r["plant"] for r in rr}),"n_source_files":len({r["file"] for r in rr}),"wind":rr[0]["wind"],"n":len(rr)}
    pollen=sum(r["p"] for rr in bysession.values() for r in rr)
    nectar=sum(r["n"] for rr in bysession.values() for r in rr)
    both=sum(r["p"]*r["n"] for rr in bysession.values() for r in rr)
    sessions_p=sum(any(r["p"] for r in rr) for rr in bysession.values())
    sessions_n=sum(any(r["n"] for r in rr) for rr in bysession.values())
    if min(pollen,nectar)<15 or min(sessions_p,sessions_n)<5:
        return {"status":"HOLD_ACTION_SUPPORT","pollen":pollen,"nectar":nectar,
             "pollen_sessions":sessions_p,"nectar_sessions":sessions_n}
    expect=sum(sum(r["p"] for r in rr)*sum(r["n"] for r in rr)/len(rr)
               for rr in bysession.values())
    if max(expect,both)<10:return {"status":"HOLD_PAIR_SUPPORT","both":both,"expected":expect}
    rng=Random(SEED);null=[]
    for _ in range(N_PERM):
        score=0
        for rr in bysession.values():
            p=[r["p"] for r in rr]
            n=[r["n"] for r in rr]
            rng.shuffle(n)
            score+=sum(x*y for x,y in zip(p,n))
        null.append(score)
    if statistics.pstdev(null)==0:return {"status":"HOLD_DEGENERATE_PAIR_NULL"}
    # Plant and file-level controls are more restrictive than original
    # same-session shuffle; all are calculated on the same source rows.
    subgroup_controls={}
    for mode,fields in (
        ("source_visit_session_by_plant",("plant",)),
        ("source_visit_session_by_filename",("file",)),
        ("source_visit_session_by_plant_filename",("plant","file"))):
        subsegs=[]
        for sid,rr in bysession.items():
            clusters=defaultdict(list)
            for item in rr:
                clusters[tuple(item[f] for f in fields)].append(item)
            subsegs.extend(clusters.values())
        o=sum(z["p"]*z["n"] for seg in subsegs for z in seg)
        expected_seg=sum(sum(z["p"] for z in seg)*sum(z["n"] for z in seg)/len(seg)
                         for seg in subsegs)
        rng_robust=Random(SEED+len(subsegs)*11)
        nnull=[]
        for _ in range(N_PERM):
            val=0
            for seg in subsegs:
                ps=[z["p"] for z in seg];ns=[z["n"] for z in seg]
                rng_robust.shuffle(ns)
                val+=sum(x*y for x,y in zip(ps,ns))
            nnull.append(val)
        sd_robust=statistics.pstdev(nnull)
        p_robust=(1+sum(abs(v-expected_seg)>=abs(o-expected_seg)-1e-9
                    for v in nnull))/(N_PERM+1) if sd_robust>0 else None
        subgroup_controls[mode] = {
           "status":"EXPLORATORY_ESTIMATED" if sd_robust>0 else "HOLD_DEGENERATE_NULL",
           "subgroups":len(subsegs),"subgroups_with_2plus_interactions":
              sum(len(seg)>=2 for seg in subsegs),
           "observed_pair":o,"expected_pair":expected_seg,
           "excess_pair":o-expected_seg,
           "two_sided_p_plus_one":p_robust,
           "null_sd":sd_robust,
           "note":"Stricter same source control for plant or physical filename within Unique_ID; not independent confirmation."
        }
    n_extreme=sum(abs(a-expect)>=abs(both-expect)-1e-9 for a in null)
    pvalue=(1+n_extreme)/(1+N_PERM)
    sortednull=sorted(null)
    sites=sorted({x["site"] for x in contexts.values()})
    site_out=[]
    for site in sites:
        rr=[v for k,v in bysession.items() if contexts[k]["site"]!=site]
        observed=sum(z["p"]*z["n"] for segment in rr for z in segment)
        ex=sum(sum(z["p"] for z in segment)*sum(z["n"] for z in segment)/len(segment)
               for segment in rr)
        site_out.append({"excluded_site":site,
               "remaining_sessions":len(rr),"excess_pair_count":observed-ex})
    ws=[x["wind"] for x in contexts.values() if x["wind"] is not None]
    windout={"status":"HOLD_WIND_CONTEXT_SUPPORT"}
    if len(ws)>=12:
        med=statistics.median(ws)
        low=[x for x in contexts.values() if x["wind"] is not None and x["wind"]<=med]
        high=[x for x in contexts.values() if x["wind"] is not None and x["wind"]>med]
        if len(low)>=4 and len(high)>=4 and len({x["site"] for x in low})>=3 and len({x["site"] for x in high})>=3:
            samples=[]
            for k,rr in bysession.items():
                wind=contexts[k]["wind"]
                if wind is None:continue
                observed=sum(z["p"]*z["n"] for z in rr)
                exp=sum(z["p"] for z in rr)*sum(z["n"] for z in rr)/len(rr)
                samples.append((wind,(observed-exp)/len(rr)))
            mx=statistics.mean(x for x,y in samples)
            my=statistics.mean(y for x,y in samples)
            denom=sum((x-mx)**2 for x,y in samples)
            slope=sum((x-mx)*(y-my) for x,y in samples)/denom if denom else None
            windout={"status":"DESCRIPTIVE_ONLY","n_sessions":len(samples),
                "low_wind_sessions":len(low),"high_wind_sessions":len(high),
                "slope_excess_pair_fraction_per_mps":slope,
                "no_causal_inference":True}
    return {
      "schema":"tnoa-weschler-wildflower-visit-behavior-overlap-v1",
      "status":"EXPLORATORY_ESTIMATED",
      "analysis_date":"2026-11-19",
      "source":{"zenodo_record":15447016,"doi":"10.5281/zenodo.15447016",
        "source_md5":MD5,"source_sha256":sha,"original_article_doi":"10.1002/njb.04996"},
      "biological_target":"Pollen-collection and nectar-drinking activities co-occurring in same recorded natural flower visit beyond session-marginal independence",
      "units":{"raw_interaction_rows":len(rows),"valid_interactions":total,
        "excluded":dict(rejected),"video_sessions":len(bysession),
        "physical_sites":len(sites),"observation_days":len({x["date"] for x in contexts.values()}),
        "source_unique_id_group_units":len(contexts),
        "uid_groups_with_multiple_plant_taxa":sum(x["n_plants"]>1 for x in contexts.values()),
        "source_filenames_across_groups":len({(sid,r["file"]) for sid,rr in bysession.items() for r in rr}),
        "pollen_positive_visits":pollen,"nectar_positive_visits":nectar,
        "sessions_with_pollen":sessions_p,"sessions_with_nectar":sessions_n},
      "primary":{"pair":"CollectingPollen AND DrinkNectar",
        "observed_joint_visits":both,
        "expected_under_within_video_session_independence":expect,
        "excess_joint_visits":both-expect,
        "observed_to_expected_ratio":both/expect if expect else None,
        "null_median":statistics.median(null),"null_sd":statistics.pstdev(null),
        "null_q025":sortednull[int(.025*(N_PERM-1))],
        "null_q975":sortednull[int(.975*(N_PERM-1))],
        "permutation_extremes":n_extreme,
        "two_sided_p_plus_one":pvalue,"n_permutations":N_PERM,
        "seed":SEED,
        "scheme":"Shuffle DrinkNectar binary labels among interactions within the same original Unique_ID, preserving both per-session margins"},
      "plant_and_video_file_null_sensitivity":subgroup_controls,
      "leave_one_site_out":site_out,
      "wind_exploration":windout,
      "claim_limits":[
        "Behavior cooccurrence within a visit can be sequential actions, not instant simultaneity.",
        "Source authors already reported multi-behavior visits and single-behavior wind/turbine associations.",
        "No direct pollen-transfer, stigma-contact, seed set or species-level adaptation claim.",
        "One wind-turbine facility system, not independent wind-farm replications.",
        "Wind measured at session scale, confounded by distance, site, plant composition and time.",
        "Repeated insects/plants and uncertain observation quality may affect behavior coding.",
        "This is ecological field-video data, not validation of a calibrated TNOA field observer.",
        "No natural pollinator response is inferred from video rows without grouping by recording session."]
    }

def main():
    rows,sha=read()
    output=analyze(rows,sha)
    f=Path("research/natural_flower_wind/WESCHLER_BEHAVIOR_COOCCURRENCE_2026-11-19.json")
    f.parent.mkdir(parents=True,exist_ok=True)
    f.write_text(json.dumps(output,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
    print("WESCHLER_BEHAVIOR_COOCCURRENCE",json.dumps({
      "status":output["status"],"units":output.get("units"),
      "primary":output.get("primary"),"wind":output.get("wind_exploration")},
      ensure_ascii=False)[:20000])
    if output["status"].startswith("HOLD_"):
        raise SystemExit("WESCHLER_BEHAVIOR_SCIENCE_HOLD_"+output["status"])
if __name__=="__main__":main()
