#!/usr/bin/env python3
"""Check source event timing semantics for RFID arrival rows; no ecological model."""
import collections as cc
import json
from pathlib import Path
from intake import obtain
from audit_temporal_support import parse_time
def main():
    result={"schema":"tnoa-rfid-arrival-time-source-consistency-v1",
      "date":"2026-11-22","status":"SOURCE_TIMING_QA_ONLY","by_taxon":{}}
    for kind in ("bumblebee","honeybee"):
        rows,_=obtain(kind)
        name="firstimefound" if kind=="bumblebee" else "firsttimefound"
        allm=cc.Counter();arrivals=cc.Counter()
        time_groups=cc.defaultdict(lambda:cc.Counter())
        for row in rows:
            t=parse_time(row["timestamp"])
            mm=int(row[name].split(":")[0])
            d=((mm-t.minute+30)%60)-30
            allm[d]+=1
            if row["direction"].strip().lower()=="arriving":
                arrivals[d]+=1
                time_groups[t.date().isoformat()][d]+=1
        result["by_taxon"][kind]={
         "all_rows_minute_difference":dict(sorted(allm.items())),
         "arriving_minute_difference":dict(sorted(arrivals.items())),
         "arriving_total":sum(arrivals.values()),
         "arriving_minute_mismatch":sum(n for k,n in arrivals.items() if k!=0),
         "arriving_abs_difference_gt1":sum(n for k,n in arrivals.items() if abs(k)>1),
         "arriving_by_day_minute_mismatch":{day:sum(n for k,n in x.items() if k!=0)
                                            for day,x in sorted(time_groups.items())}}
    p=Path("research/nest_activity_wind/RFID_ARRIVAL_TIME_CONSISTENCY_2026-11-22.json")
    p.write_text(json.dumps(result,indent=2)+"\n")
    print("RFID_ARRIVAL_TIMING_QA",json.dumps({k:{
      kk:v for kk,v in a.items() if kk!="arriving_by_day_minute_mismatch"
      } for k,a in result["by_taxon"].items()}))
if __name__=="__main__":main()
