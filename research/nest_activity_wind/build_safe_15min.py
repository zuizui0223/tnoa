#!/usr/bin/env python3
"""Create source-authenticated *derived* 15-min bee return × wind table.

Scientifically conservative: reject every weather bin containing any conflicting
timestamp; require >=20 distinct weather readings and raw antenna reads for both
taxa; use only 06:00–22:00 with >=8 paired active bins per literal source day.
No 2020→2021 correction. No original tag identities are emitted.
"""
from collections import defaultdict,Counter
import datetime as dt
import hashlib
import json
import math
from pathlib import Path
from statistics import mean

from intake import obtain
from audit_temporal_support import parse_time,normalize_weather
from audit_clean_windows import bucket

CATEGORIES=("bumblebee","honeybee")
MIN_ANTENNA_BINS_PER_DAY=8
MIN_WEATHER_UNIQUE_30S=20
DEDUPE_SECONDS=300
def source():
    rows={}
    meta={}
    for k in CATEGORIES+("weather",):
        rows[k],meta[k]=obtain(k)
    return rows,meta

def exact_arrival_event_time(row,kind):
    ts=parse_time(row["timestamp"])
    raw=str(row["firstimefound" if kind=="bumblebee" else "firsttimefound"]).strip()
    fieldminute,seconds=raw.split(":",1)
    m=int(fieldminute); s=float(seconds)
    if not 0<=m<60 or not 0<=s<60:raise ValueError("invalid RFID fine time")
    d=((m-ts.minute+30)%60)-30
    if d not in (-1,0):
        raise ValueError("unexpected source minute drift: "+repr((ts,raw,d)))
    return ts+dt.timedelta(minutes=d,seconds=s)
def numeric(s):
    try:
        v=float(str(s).strip())
        return v if math.isfinite(v) else None
    except (ValueError,TypeError):
        return None

def build():
    raw,meta=source()
    byts=defaultdict(list)
    for x in raw["weather"]:
        byts[parse_time(x["datetime"])].append(x)
    weather=defaultdict(list);conflicted=Counter()
    for t,group in byts.items():
        b=bucket(t)
        if len({normalize_weather(x) for x in group})>1:
            conflicted[b]+=1
            continue
        x=group[0]
        values=[numeric(x[k]) for k in ("windpsd","temp","solar","rh","rain")]
        if any(v is None for v in values[:4]):
            conflicted[b]+=1;continue
        wind,temp,solar,rh,rain=values
        if not (0<=wind<80 and -15<=temp<60 and 0<=rh<=100):
            conflicted[b]+=1;continue
        weather[b].append((wind,temp,solar,rh,rain))
    safe={b:{"wind":mean([x[0] for x in v]),
             "temp":mean([x[1] for x in v]),
             "solar":mean([x[2] for x in v]),
             "rh":mean([x[3] for x in v]),
             "rain":mean([x[4] for x in v if x[4] is not None]) if any(x[4] is not None for x in v) else None,
             "weather_unique_readings":len(v)}
         for b,v in weather.items() if conflicted[b]==0 and len(v)>=MIN_WEATHER_UNIQUE_30S}

    antenna_reads={k:Counter() for k in CATEGORIES}
    returns={k:Counter() for k in CATEGORIES}
    all_return_times={}
    qc={}
    for kind in CATEGORIES:
        raw_arrivals=[]
        uid_day_arriving=defaultdict(set)
        for x in raw[kind]:
            event=exact_arrival_event_time(x,kind)
            b=bucket(event)
            antenna_reads[kind][b]+=1
            if str(x["direction"]).strip().lower()=="arriving":
                raw_arrivals.append((event,str(x["uid"]),str(x["collection"])))
        raw_arrivals.sort(key=lambda z:(z[1],z[0]))
        last={}
        deduped=[]
        for event,uid,colony in raw_arrivals:
            prior=last.get(uid)
            if prior is None or (event-prior).total_seconds()>=DEDUPE_SECONDS:
                deduped.append((event,uid,colony))
                last[uid]=event
        for event,uid,colony in deduped:
            returns[kind][bucket(event)]+=1
            uid_day_arriving[event.date().isoformat()].add(uid)
        all_return_times[kind]=deduped
        qc[kind]={
            "raw_read_rows":len(raw[kind]),
            "source_arriving_rows":len(raw_arrivals),
            "5min_de_duplicated_source_arrival_events":len(deduped),
            "unique_tag_ids_with_accepted_arrivals":len(set(uid for t,uid,c in deduped)),
            "date_span": [min(x[0] for x in raw_arrivals).isoformat(),max(x[0] for x in raw_arrivals).isoformat()],
            "unique_days_with_accepted_arrivals":len(uid_day_arriving),
            "source_colonies":len(set(x[2] for x in raw_arrivals)),
        }
    eligible_bins=[b for b in safe if 6<=b.hour<22
        and antenna_reads["honeybee"][b]>0 and antenna_reads["bumblebee"][b]>0]
    eligible_byday=Counter(b.date().isoformat() for b in eligible_bins)
    accepted_days={d for d,n in eligible_byday.items() if n>=MIN_ANTENNA_BINS_PER_DAY}
    valid=sorted(b for b in eligible_bins if b.date().isoformat() in accepted_days)
    table=[]
    for b in valid:
        x=safe[b]
        entry={"date":b.date().isoformat(),
          "bin_start":b.isoformat(),
          "hour":b.hour+b.minute/60.,"wind":x["wind"],
          "temperature":x["temp"],"solar":x["solar"],
          "rh":x["rh"],"rain":x["rain"],
          "meteorological_30s_readings":x["weather_unique_readings"],
          "honeybee_arriving":returns["honeybee"][b],
          "bumblebee_arriving":returns["bumblebee"][b],
          "honeybee_any_rf_read":antenna_reads["honeybee"][b],
          "bumblebee_any_rf_read":antenna_reads["bumblebee"][b],
        }
        table.append(entry)
    accepted_meteorological_source_sha=meta["weather"]["source_sha256"]
    info={
      "schema":"tnoa-irish-rfid-validated-exposure-bin-v1",
      "date":"2026-11-22",
      "status":"DERIVED_WINDOWS_ONLY_NO_WIND_EFFECT_FIT",
      "source_sha256":{k:meta[k]["source_sha256"] for k in meta},
      "literal_source_year":2020,
      "manuscript_methods_year":2021,
      "unreconciled_calendar_provenance":True,
      "meteorological_conflict_timestamps_excluded":sum(1 for rows in byts.values() if len({normalize_weather(r) for r in rows})>1),
      "conflict_free_weather_bins_20plus_rows":len(safe),
      "paired_antenna_active_daytime_bins_before_8perday":len(eligible_bins),
      "paired_antenna_active_days_before_minimum":len(eligible_byday),
      "days_accepted":len(accepted_days),
      "accepted_day_ids":sorted(accepted_days),
      "n_paired_15min_bins":len(table),
      "rain_missing_bins":sum(x["rain"] is None for x in table),
      "total_honey_arriving":sum(x["honeybee_arriving"] for x in table),
      "total_bumble_arriving":sum(x["bumblebee_arriving"] for x in table),
      "zero_total_arriving_bins":sum(x["honeybee_arriving"]+x["bumblebee_arriving"]==0 for x in table),
      "rfid_source_qc":qc,
      "observation_semantics":[
         "Counts are tag-identified recorded arrivals in nominally concurrent active RF antenna windows, NOT true visit frequency and not measured pollination.",
         "Nondetection is not biological absence. Nominal uptime is inferred only from nonzero raw antenna reads in both taxa and cannot establish complete logger activity.",
         "Weather values were NEVER averaged across conflicting same-time readings; entire conflicted bins excluded.",
         "Exact duplicate meteorological rows collapse into one 30-second observation before bin means.",
         "The source year is 2020 in these files, contrary to methods text 2021, and is not silently corrected.",
         "Arriving direction only. 5-minute UID event gap per original publication; Unknown and Departing are not arrivals.",
         "No individually identifiable RFID UID/tag or source row redistributed; one row per safe paired 15-minute exposure bin."
      ],
      "rows":table
    }
    if len(table)<200 or len(accepted_days)<12:
        info["status"]="HOLD_CLEAN_DAY_COVERAGE"
    if len(table) and (any(x["wind"]<0 or not math.isfinite(x["wind"]) for x in table)):
        info["status"]="HOLD_NONFINITE_SOURCE_WIND"
    return info
def main():
    x=build()
    p=Path("research/nest_activity_wind/DERIVED_SAFE_15MIN_2026-11-22.json")
    p.write_text(json.dumps(x,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
    print("TNOA_RFID_15MIN_SOURCE_SAFE",json.dumps({k:v for k,v in x.items() if k!="rows"},ensure_ascii=False)[:10000])
    print("TNOA_RFID_SAFE_DERIVED_MATRIX_"+x["status"])
if __name__=="__main__":main()
