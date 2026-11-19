#!/usr/bin/env python3
"""Outcome-blind session-key audit of Weschler's recorded field-flower video rows."""
from collections import defaultdict,Counter
import json
from pathlib import Path
from weschler_behavior_pair_test import read

def main():
    rows, sha=read()
    keys=["Site","Date","JulianDate","FileName","Plant","WindSpeed","Total_Site_Time","Video_Time","Temp","BudCount"]
    for key in ["Unique_ID"]+keys:
        assert key in rows[0],f"Source column {key} missing"
    groups=defaultdict(list)
    for row in rows:
        groups[str(row["Unique_ID"]).strip()].append(row)
    support={}
    for col in keys:
        support[col]=dict(Counter(len(set(str(r[col]).strip() for r in rr)) for rr in groups.values()))
    composite={
        "uid":len(groups),
        "uid_filename":len(set((r["Unique_ID"],r["FileName"]) for r in rows)),
        "uid_plant":len(set((r["Unique_ID"],r["Plant"]) for r in rows)),
        "uid_filename_plant":len(set((r["Unique_ID"],r["FileName"],r["Plant"]) for r in rows)),
        "site_date_filename":len(set((r["Site"],r["Date"],r["FileName"]) for r in rows)),
        "site_date_plant":len(set((r["Site"],r["Date"],r["Plant"]) for r in rows)),
        "site_date_filename_plant":len(set((r["Site"],r["Date"],r["FileName"],r["Plant"]) for r in rows))
    }
    combos=["Unique_ID","FileName","Plant"]
    bad_uid={uid:{key:len(set(str(r[key]).strip() for r in rr)) for key in keys}
       for uid,rr in groups.items() if len(set(str(r["Plant"]).strip() for r in rr))>1}
    num_by_uid=Counter(len(rr) for rr in groups.values())
    byuid_examples=[{
        "uid":uid,"n":len(groups[uid]),"sites":sorted({r["Site"] for r in groups[uid]}),
        "dates":sorted({r["Date"] for r in groups[uid]}),
        "plants":sorted({r["Plant"] for r in groups[uid]}),
        "filenames":sorted({r["FileName"] for r in groups[uid]})[:8],
        "winds":sorted({r["WindSpeed"] for r in groups[uid]})
      } for uid in list(groups)[:12]]
    result={"schema":"weschler-source-session-identity-audit-v1",
      "status":"SOURCE_METADATA_ONLY_NO_BEHAVIOR_COUNTS",
      "raw_source_sha256":sha,"rows":len(rows),
      "unique_id_groups":len(groups),
      "unique_id_group_size_distribution":dict(num_by_uid),
      "distinct_values_within_unique_id":support,
      "candidate_composite_keys":composite,
      "multi_plant_unique_id_group_n":len(bad_uid),
      "examples":byuid_examples,
      "inference_warning":"A grouping key with variable site, date or wind cannot license independent wind exposure. A grouping that combines plant taxa may be too coarse for behavior co-occurrence null and needs biology-aware subgroup analysis."}
    p=Path("research/natural_flower_wind/WESCHLER_SESSION_KEY_AUDIT_2026-11-19.json")
    p.write_text(json.dumps(result,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
    print("WESCHLER_SESSION_KEY_AUDIT",json.dumps({k:v for k,v in result.items() if k!="examples"},ensure_ascii=False))
    print("WESCHLER_SESSION_EXAMPLES",json.dumps(byuid_examples,ensure_ascii=False))
if __name__=="__main__":main()
