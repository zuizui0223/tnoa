#!/usr/bin/env python3
"""Never turn a candidate pollinator column or repeated survey row into biological truth.

Source metadata-only audit for the original Zenodo CSV, which has 496 rows
but unexpectedly 124 distinct site × date-time × transect keys.
"""
from collections import Counter,defaultdict
from hashlib import sha256
import json
from pathlib import Path
from intake import prepare,num
def main():
    rows,cols,encoding,sha,bytelen=prepare()
    group=defaultdict(list)
    bykeyloc=defaultdict(list)
    rowhashes=[]
    for i,r in enumerate(rows):
        k=tuple(str(r.get(x,"")).strip().lower() for x in ("site","datetimestart","transect"))
        kl=k+(str(r.get("location","")).strip().lower(),)
        group[k].append(i);bykeyloc[kl].append(i)
        rowhashes.append(sha256(json.dumps(r,sort_keys=True).encode()).hexdigest())
    dupfreq=Counter(len(v) for v in group.values())
    locfreq=Counter(len(v) for v in bykeyloc.values())
    fullhash=Counter(rowhashes)
    exact_rows_dup=sum(v-1 for v in fullhash.values() if v>1)
    samples=[]
    for k,idx in list(group.items())[:5]:
        examples=[]
        for i in idx[:12]:
            r=rows[i]
            examples.append({
              "row_no":i+2,"site":r.get("site"),"transect":r.get("transect"),
              "location":r.get("location"),"datetimestart":r.get("datetimestart"),
              "datetimeend":r.get("datetimeend"),"source_data_values":{
                z:r.get(z) for z in
                ["honeybee","honeybee_pollen","bumblebee","bumblebee_pollen",
                 "solitary","solitary_pollen","butterfly","meanwindspd"]}
            })
        samples.append({"group_key":k,"n_rows":len(idx),"rows":examples})
    keys_full=Counter(tuple(str(r.get(k,"")).strip().lower() for k in cols) for r in rows)
    report={
      "status":"OBSERVATION_SEMANTIC_HOLD_PENDING_AUTHORITATIVE_DESCRIPTION",
      "source_sha256":sha,"source_rows":len(rows),"source_columns":cols,
      "contains_literal_hoverfly_column": any("hover" in c or "syrph" in c for c in cols),
      "contains_literal_butterfly_column": "butterfly" in cols,
      "site_time_transect_unique":len(group),
      "site_time_transect_group_size_distribution":dict(sorted(dupfreq.items())),
      "site_time_transect_location_unique":len(bykeyloc),
      "site_time_transect_location_size_distribution":dict(sorted(locfreq.items())),
      "exact_duplicated_rows_beyond_first":exact_rows_dup,
      "unique_all_columns_rows":len(keys_full),
      "sample_groups":samples,
      "warning":"Never replace hoverflies with the 'butterfly' column or silently deduplicate genuine survey groups; STOP unless source semantics support interpretation.",
      "biological_inference_opened":False
    }
    out=Path("research/natural_flower_wind/SEMANTIC_AUDIT_2026-11-19.json")
    out.parent.mkdir(parents=True,exist_ok=True)
    out.write_text(json.dumps(report,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
    print("NATURAL_FLOWER_SEMANTIC_AUDIT",json.dumps({k:v for k,v in report.items() if k!="sample_groups"}))
    print("NATURAL_FLOWER_SAMPLE_KEYS",json.dumps(samples))
if __name__=="__main__":main()
