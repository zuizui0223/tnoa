#!/usr/bin/env python3
"""Timestamp, overlapping-day, duplicate-weather audit before RFID ecological inference.

No wind-return association, model coefficient or species difference calculated.
This script deliberately retains literal source years, never shifts 2020 to 2021.
"""
from __future__ import annotations
import collections
import datetime as dt
import json
from pathlib import Path
from intake import obtain

def parse_time(v,seconds=False):
    t=str(v).strip()
    forms=("%m-%d-%y %H:%M:%S","%m-%d-%y %H:%M")
    for fmt in forms:
        try:return dt.datetime.strptime(t,fmt)
        except ValueError:pass
    raise ValueError("source unparseable date: "+repr(t))
def normalize_weather(row):
    return tuple(str(row[c]).strip() for c in ["temp","rh","solar","rain","windpsd","secssincemidnight"])
def do_rfid(kind):
    data,meta=obtain(kind)
    t=[parse_time(x["timestamp"]) for x in data]
    bydate=collections.Counter(x.date().isoformat() for x in t)
    first=min(t);last=max(t)
    arrivals=[(t[i],x) for i,x in enumerate(data)
               if x["direction"].strip().lower()=="arriving"]
    valid_uid=len(set(x["uid"] for t,x in arrivals))
    uidday=collections.defaultdict(set)
    arrivals_byday=collections.Counter()
    arrival_collection_day=collections.defaultdict(collections.Counter)
    duplicate_uid_clock=collections.Counter()
    for timestamp,row in arrivals:
        day=timestamp.date().isoformat()
        arrivals_byday[day]+=1
        uidday[day].add(row["uid"])
        arrival_collection_day[day][row["collection"]]+=1
        duplicate_uid_clock[(timestamp,row["uid"])]+=1
    per_uid_multiples=sum(c-1 for c in duplicate_uid_clock.values() if c>1)
    return {
      "original_rows":len(data),
      "raw_years":dict(collections.Counter(x.year for x in t)),
      "first_literal_time":first.isoformat(),"last_literal_time":last.isoformat(),
      "all_event_days":len(bydate),"all_event_by_day":dict(sorted(bydate.items())),
      "arrival_records":len(arrivals),"arriving_unique_tag_ids":valid_uid,
      "arrival_by_day":dict(sorted(arrivals_byday.items())),
      "arrival_unique_tags_by_day":dict(sorted((k,len(v)) for k,v in uidday.items())),
      "arrival_per_colony_per_day":{
         d:dict(sorted(counter.items())) for d,counter in sorted(arrival_collection_day.items())},
      "duplicate_arriving_tag_at_minute":per_uid_multiples,
      "raw_timestamp_uniques":len(set(t)),
      "firstimefound_column":("firstimefound" if kind=="bumblebee" else "firsttimefound"),
      "caution":"Datetime source years literal; no 2021 offset applied, no 5-minute de-duplication yet. Arrival time has minute precision until source firsttimefound parsing checked."}

def do_weather():
    rows,meta=obtain("weather")
    parsed=[parse_time(row["datetime"]) for row in rows]
    byday=collections.Counter(d.date().isoformat() for d in parsed)
    time_records=collections.defaultdict(list)
    for d,row in zip(parsed,rows):
        time_records[d].append(normalize_weather(row))
    duplicates=sum(len(v)-1 for v in time_records.values())
    conflict_keys=[k for k,v in time_records.items() if len(set(v))>1]
    multiplicity=collections.Counter(len(v) for v in time_records.values())
    missing=collections.Counter()
    for row in rows:
        for c in ("temp","solar","rh","rain","windpsd"):
            x=str(row.get(c,"")).strip().lower()
            if x in ("","na","nan","null"):missing[c]+=1
    return {
     "rows":len(rows),
     "raw_years":dict(collections.Counter(t.year for t in parsed)),
     "first_literal_time":min(parsed).isoformat(),
     "last_literal_time":max(parsed).isoformat(),
     "n_unique_datetime":len(time_records),
     "duplicate_weather_datetime_rows":duplicates,
     "duplicate_multiplicity":dict(sorted(multiplicity.items())),
     "distinct_value_conflicting_duplicate_timestamps":len(conflict_keys),
     "first_conflicting_duplicate_times":[d.isoformat() for d in conflict_keys[:10]],
     "missing_counts":dict(missing),
     "by_day":dict(sorted(byday.items())),
     "warning":"Duplication is removable only if timestamp duplicates agree on all measured weather and time fields. If values disagree, HOLD or obtain station provenance."}

def main():
    tax={k:do_rfid(k) for k in ("bumblebee","honeybee")}
    weather=do_weather()
    bee_days=[set(tax[k]["arrival_by_day"]) for k in ("bumblebee","honeybee")]
    met_days=set(weather["by_day"])
    triple=sorted(bee_days[0]&bee_days[1]&met_days)
    overlap={"n_dates_with_arrivals_both_taxa_and_weather":len(triple),
             "dates":triple,
             "bumblebee_arrival_days_with_weather":len(bee_days[0]&met_days),
             "honeybee_arrival_days_with_weather":len(bee_days[1]&met_days)}
    out={
      "schema":"tnoa-rfid-weather-temporal-support-only-v1",
      "date":"2026-11-22",
      "scientific_status":"TIME_AND_JOIN_AUDIT_ONLY_NO_BIOLOGICAL_ASSOCIATION",
      "source_original_reported_field_year":2021,
      "unreconciled_year_mismatch":2020 in weather["raw_years"],
      "taxa":tax,"weather":weather,"overlap":overlap,
      "inference_hold_conditions":[
       "Less than 12 overlap days",
       "Conflicting meteorological values at duplicated exact timestamps",
       "RFID timestamp minute and fractional firsttimefound are inconsistent",
       "No independently supported RFID receiver logging uptime",
       "Observation source lists 2021 methods but actual CSV reports 2020; never silently shift years"] }
    path=Path("research/nest_activity_wind/TEMPORAL_SUPPORT_2026-11-22.json")
    path.write_text(json.dumps(out,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
    print("RFID_TEMPORAL_SUPPORT",json.dumps({
      "year_mismatch":out["unreconciled_year_mismatch"],
      "overlap":overlap,
      "bumble_n_days":tax["bumblebee"]["all_event_days"],
      "honey_n_days":tax["honeybee"]["all_event_days"],
      "bumble_arrivals":tax["bumblebee"]["arrival_records"],
      "honey_arrivals":tax["honeybee"]["arrival_records"],
      "weather_days":len(weather["by_day"]),
      "weather_duplicate_rows":weather["duplicate_weather_datetime_rows"],
      "weather_duplicate_conflicting_times":weather["distinct_value_conflicting_duplicate_timestamps"],
      "weather_missing_counts":weather["missing_counts"]}))
    print("TNOA_RFID_TEMPORAL_AUDIT_PASS")
if __name__=="__main__":main()
