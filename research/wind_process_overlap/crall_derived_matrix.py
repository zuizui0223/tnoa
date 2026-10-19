#!/usr/bin/env python3
"""Prepare source-verified SESSION-GRAIN derived orchid-bee genus composition.

No 450 individual record identities redistributed. Joined bee records in the
409-bee original published 70-session frame only; pass-by-session taxon counts
and pre-specified environmental metadata remain as derived scientific output.
"""
import csv
import datetime
import hashlib
import json
from collections import Counter,defaultdict
from pathlib import Path
from crall_linkage_audit import load,clean,SHA256,ORIGINAL_URL

def categorical(key):
    v=clean(key)
    return v if v not in ("", "na","nan","n/a","unknown","unidentified") else "unknown"

def safe_num(row,col):
    v=row.get(col)
    if v is None or str(v).strip().lower() in ("","na","nan"):return None
    return float(v)

def main():
    bees,sessions,colls,_=load()
    assert len(bees)==450 and len(sessions)==70 and len(colls)==70
    def key(r):return (clean(r["date"]),clean(r["site"]),clean(r["scent"]))
    lut={key(s):i for i,s in enumerate(sessions)}
    assert len(lut)==70
    group=defaultdict(list); unmatched=Counter()
    for b in bees:
        idx=lut.get(key(b))
        if idx is None:
            unmatched[clean(b["date"])]+=1
        else:
            group[idx].append(b)
    assert sum(map(len,group.values()))==409 and sum(unmatched.values())==41
    rows=[];taxon_counts=Counter();species_counts=Counter();all_genus_sessions=defaultdict(set)
    for i,s in enumerate(sessions):
        keydate=clean(s["date"])
        date=datetime.datetime.strptime(keydate,"%m/%d/%y").date()
        b=group.get(i,[])
        gen=Counter(categorical(x["genus"]) for x in b)
        sp=Counter(" ".join([categorical(x["genus"]),categorical(x["species"])]) for x in b)
        assert sum(gen.values())==int(float(s["count"]))
        taxon_counts.update(gen);species_counts.update(sp)
        for g,c in gen.items():
            if c>0: all_genus_sessions[g].add(i)
        row={
          "session_index":i+1,
          "source_session_id":clean(s["coll.id"]),
          "site":clean(s["site"]),
          "date":date.isoformat(),
          "day_since_first": (date-datetime.date(2014,10,1)).days,
          "scent":clean(s["scent"]),
          "count":int(float(s["count"])),
          "wind_mean":safe_num(s,"wind.mean"),
          "tke":safe_num(s,"wind.KE"),
          "turbulence_intensity_3d":safe_num(s,"turbInt.3d"),
          "forest_cover_200m":safe_num(s,"cover200m"),
          "bee_genus_counts":dict(sorted(gen.items())),
          "bee_species_counts":dict(sorted(sp.items()))
        }
        rows.append(row)
    assert sum(x["count"] for x in rows)==409 and sum(v for v in taxon_counts.values())==409
    assert len(set(r["source_session_id"] for r in rows))==70
    assert len(set((r["date"],r["site"],r["scent"]) for r in rows))==70
    numeric_completeness={field:sum(r[field] is not None for r in rows) for field in
         ["wind_mean","tke","turbulence_intensity_3d","forest_cover_200m"]}
    positive_wind_sessions=sum(r["wind_mean"] is not None and r["wind_mean"]>0 for r in rows)
    supported_categories={k:v for k,v in sorted(taxon_counts.items()) if v>=15 and len(all_genus_sessions[k])>=8}
    report={
      "status":"original-source-verified-derived-sessions; taxonomy outcomes not yet modeled",
      "source":{"original_url":ORIGINAL_URL,"sha256":SHA256,"version":"Zenodo record 3675327 v2","paper_doi":"10.1098/rsbl.2020.0103"},
      "schema":"tnoa-crall-session-level-genus-counts-v1",
      "n_original_bee_records":450,"n_original_sessions":70,
      "n_linked_bees":409,"n_excluded_bees":41,"excluded_dates":dict(unmatched),
      "n_sites":len(set(r["site"] for r in rows)),
      "n_dates":len(set(r["date"] for r in rows)),
      "n_scents":len(set(r["scent"] for r in rows)),
      "n_zero_sessions":sum(r["count"]==0 for r in rows),
      "numeric_completeness":numeric_completeness,
      "positive_wind_sessions":positive_wind_sessions,
      "genus_total_counts":dict(sorted(taxon_counts.items())),
      "genus_session_support":dict(sorted((k,len(v)) for k,v in all_genus_sessions.items())),
      "genus_eligible_by_locked_15_8_gate":supported_categories,
      "species_total_counts":dict(sorted(species_counts.items())),
      "survey_sessions":rows,
      "limits":["Sessions not individual bees are exposure replicates",
                "Chemical male-bee scent-bait arrivals, not flower visits",
                "All reconstructed keys date×site×scent; time mismatch for seven bees",
                "No random assignment of wind; original study results already published",
                "No reused original raw individual bee data included"]
    }
    out=Path("research/wind_process_overlap/crall_derived_session_matrix.json")
    out.parent.mkdir(parents=True,exist_ok=True)
    out.write_text(json.dumps(report,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
    print("CRALL_SESSION_MATRIX",json.dumps({
       k:report[k] for k in ["n_original_sessions","n_linked_bees","n_excluded_bees","n_sites","n_dates","n_scents","n_zero_sessions","numeric_completeness","positive_wind_sessions","genus_total_counts","genus_session_support","genus_eligible_by_locked_15_8_gate"]}))
    print("CRALL_DERIVED_SESSION_MATRIX_PASS")
if __name__=="__main__":main()
