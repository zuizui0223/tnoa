#!/usr/bin/env python3
"""Source-only probe for unambiguous within-day RFID/wind support.

Strictly discard weather 15-minute bins with ANY conflicting same-time weather
entries. Keep exact consistent copies as one independent time observation.
Do not use unlabeled station record mixtures as a biological wind exposure.
Never shift literal 2020 dates to the 2021 field year of paper methods.
"""
from __future__ import annotations
import collections as cc
import datetime as dt
import json
from pathlib import Path
from intake import obtain
from audit_temporal_support import parse_time,normalize_weather

def bucket(t):
    return t.replace(minute=(t.minute//15)*15,second=0,microsecond=0)

def main():
    raw={x:obtain(x)[0] for x in ("bumblebee","honeybee","weather")}
    weather=cc.defaultdict(list)
    for row in raw["weather"]:
        t=parse_time(row["datetime"])
        weather[t].append(row)
    stable=cc.defaultdict(list); conflicts=cc.Counter(); totals=cc.Counter()
    conflicts_by_bin=cc.Counter()
    for ts,records in weather.items():
        b=bucket(ts);totals[b]+=1
        vals={normalize_weather(row) for row in records}
        if len(vals)>1:
            conflicts[b]+=1
            conflicts_by_bin[b]+=len(records)
        else:
            try:
                v=float(records[0]["windpsd"])
                if not (-0.01<=v<80):raise ValueError("nonphysical wind")
                temp=float(records[0]["temp"]);solar=float(records[0]["solar"])
                if not all(map(lambda x:x==x,(v,temp,solar))):raise ValueError("non-finite weather")
                stable[b].append((ts,v,temp,solar))
            except (ValueError,TypeError,KeyError):
                conflicts[b]+=1
    # A safe weather-bin has 20+ independent 30-second timestamps and 0 conflict
    safe={b:rows for b,rows in stable.items() if len(rows)>=20 and conflicts[b]==0}
    all_bee_bins={};arrival_per_bin={}
    minute_issues={}
    for kind in ("bumblebee","honeybee"):
        reads=cc.Counter();arrivals=cc.Counter()
        wrong_minute=0;parse_fails=0
        # More than one antenna read in a minute is NOT the same as multiple independent returns.
        for row in raw[kind]:
            ts=parse_time(row["timestamp"]);b=bucket(ts)
            reads[b]+=1
            tcol="firstimefound" if kind=="bumblebee" else "firsttimefound"
            tval=str(row[tcol]).strip().split(":")
            try:
                m=int(tval[0]);s=float(tval[1])
                if ts.minute!=m or not (0<=s<60):wrong_minute+=1
            except (ValueError,IndexError):
                parse_fails+=1
            if str(row["direction"]).strip().lower()=="arriving":arrivals[b]+=1
        all_bee_bins[kind]=reads
        arrival_per_bin[kind]=arrivals
        minute_issues[kind]={"wrong_clock_minute":wrong_minute,
                            "unparseable_firsttimefound":parse_fails}
    dates={}
    for b in totals:
        d=b.date().isoformat()
        rec=dates.setdefault(d,{"unique_weather_15min":0,"clean_weather_15min":0,
            "conflicting_weather_15min":0,"safe_weather_15min":0,"safe_with_both_antennas":0,
            "safe_with_both_known_arrivals":0,"safe_bumble_arrival_reads":0,
            "safe_honey_arrival_reads":0})
        rec["unique_weather_15min"]+=1
        if conflicts[b]:rec["conflicting_weather_15min"]+=1
        else:rec["clean_weather_15min"]+=1
        if b in safe:
            rec["safe_weather_15min"]+=1
            a=all_bee_bins["bumblebee"][b];c=all_bee_bins["honeybee"][b]
            if a>0 and c>0:
                rec["safe_with_both_antennas"]+=1
            if arrival_per_bin["bumblebee"][b]>0 and arrival_per_bin["honeybee"][b]>0:
                rec["safe_with_both_known_arrivals"]+=1
            rec["safe_bumble_arrival_reads"]+=arrival_per_bin["bumblebee"][b]
            rec["safe_honey_arrival_reads"]+=arrival_per_bin["honeybee"][b]
    safe_active=[b for b in safe if all_bee_bins["bumblebee"][b] and all_bee_bins["honeybee"][b]]
    days_active=len({b.date() for b in safe_active})
    out={
      "schema":"tnoa-rfid-unambiguous-weather-support-v1",
      "date":"2026-11-22",
      "scientific_status":"source_eligibility_only; no wind×bee association fitted",
      "source_time_year":2020,
      "paper_methods_reported_year":2021,
      "weather_unique_timestamps":len(weather),
      "weather_conflicting_unique_timestamps":sum(1 for rows in weather.values() if len({normalize_weather(r) for r in rows})>1),
      "weather_unique_15min_bins":len(totals),
      "weather_bins_any_conflict":sum(bool(n) for n in conflicts.values()),
      "weather_bins_min_20_stable_and_zero_conflicts":len(safe),
      "both_guilds_raw_antenna_reads_in_safe_weather_bins":len(safe_active),
      "distinct_days_with_both_antenna_reads_and_safe_weather":days_active,
      "unique_days_with_sufficient_safe_active_bins_at_least_8":sum(d["safe_with_both_antennas"]>=8 for d in dates.values()),
      "source_firsttimefound_precision_checks":minute_issues,
      "by_literal_day":dict(sorted(dates.items())),
      "strict_admission":"Only unambiguous weather 15-min bins with >=20 timestamp rows and no conflicting duplicates. Equal-time weather records never arbitrarily averaged. Both-tag antenna read required to call a bin nominally online.",
      "prohibited_claims":[
        "No proof of RFID console uptime from nonzero read events alone",
        "No 2020→2021 timestamp correction or hard-coded 1-year shift",
        "Cannot treat Unknown direction as departure/arrival",
        "This is not yet a valid sample of total nest arrival effort or a biological weather effect",
        "Do not treat 100,000 weather rows as independent bee behavioral observations",
        "Source field and nest observations are not same population/time/plant domain."
      ]}
    p=Path("research/nest_activity_wind/CLEAN_WINDOW_ELIGIBILITY_2026-11-22.json")
    p.write_text(json.dumps(out,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
    print("TNOA_RFID_CLEAN_WEATHER_WINDOWS",json.dumps({
      k:v for k,v in out.items() if k not in ("by_literal_day","prohibited_claims")},
      ensure_ascii=False))
    print("TNOA_RFID_CLEAN_BY_DAY",json.dumps(out["by_literal_day"],ensure_ascii=False)[:22000])
    print("TNOA_RFID_CLEAN_WINDOW_QA_PASS")
if __name__=="__main__":main()
