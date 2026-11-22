#!/usr/bin/env python3
"""Public Zenodo all-weather nest RFID + meteorology metadata gate.

NO bee×weather effects opened; only field lists, categories, temporal support,
identifier and row-count QA. Never redistribute original records.
"""
from __future__ import annotations
import argparse
from collections import Counter
import csv
import hashlib
import io
import json
from pathlib import Path
from urllib.request import Request,urlopen

ROOT="https://zenodo.org/records/10869660/files/"
SOURCES={
 "bumblebee":("2_bumblebee_rfid_data.csv","ad215b52b6ae3d0e9be400e88b033547"),
 "honeybee":("3_honeybee_rfid_data.csv","13740f28b901ab1b440409e13ff31feb"),
 "weather":("4_rfid_weather_data.csv","8de93d02dc1df37e6c9ac31e37a0ab09")
}
def obtain(kind):
    name,known_md5=SOURCES[kind]
    url=ROOT+name+"?download=1"
    with urlopen(Request(url,headers={"User-Agent":"tnoa-public-scientific-source-audit/1.0"}),timeout=80) as res:
        content=res.read()
    actual_md5=hashlib.md5(content).hexdigest()
    if actual_md5!=known_md5:raise ValueError(f"Original Zenodo source changed for {kind}: {actual_md5} != {known_md5}")
    enc=None
    for code in ("utf-8-sig","cp1252","latin1"):
        try:
            txt=content.decode(code)
            enc=code;break
        except UnicodeDecodeError:continue
    if enc is None:raise ValueError(f"unknown source encoding {kind}")
    sep=","
    try:sep=csv.Sniffer().sniff(txt[:8000],delimiters=",;\t").delimiter
    except csv.Error:pass
    rows=list(csv.DictReader(io.StringIO(txt),delimiter=sep))
    if len(rows)<10 or any(None in r for r in rows):
        raise ValueError(f"CSV incomplete {kind}, or invalid header")
    return rows,{
      "original_name":name,"url":url,"published_md5":known_md5,
      "observed_md5":actual_md5,"source_sha256":hashlib.sha256(content).hexdigest(),
      "bytes":len(content),"encoding":enc,"delimiter":sep,
      "rows":len(rows),"columns":list(rows[0])
    }

def simple(s):
    return str(s if s is not None else "").strip()
def temporal_support(rows,columns):
    candidate=[c for c in columns if ("time" in c.lower() or "date" in c.lower())]
    out={}
    for c in candidate[:8]:
        val=[simple(x[c]) for x in rows]
        seen=set(v for v in val if v)
        out[c]={"n_nonempty":len(val)-sum(not v for v in val),
          "n_distinct":len(seen),
          "first_examples":list(dict.fromkeys(v for v in val if v))[:7]}
    return out
def identifier_support(rows,columns):
    candidate=[c for c in columns if any(k in c.lower() for k in
                ("uid","collection","colony","tag","direction","ant","firsttime","lasttime","numfound"))]
    out={}
    for c in candidate[:12]:
        val=[simple(x[c]) for x in rows]
        freq=Counter(val)
        ordered=freq.most_common(16)
        out[c]={"n_distinct":len(freq),"n_empty":freq.get("",0),
                "top_examples":ordered if len(freq)<=16 else ordered[:8]}
    return out

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--output",default="research/nest_activity_wind/INTAKE_RECEIPT_2026-11-22.json")
    args=p.parse_args()
    audit={"schema":"tnoa-irish-nest-rfid-intake-v1",
      "date":"2026-11-22",
      "scientific_status":"source_schema_and_join_feasibility_only; NO bee-wind contrasts examined",
      "owner":"TNOA ecological sidecar, not TNOA MEE paper",
      "source_doi":"10.5061/dryad.jq2bvq8dw",
      "files":{},
      "observation_boundaries":[
          "RFID antenna reads are not independent bees or independent meteorological samples",
          "Weather data are expected to be 30-second records during July 2021",
          "Arrival direction must be observed, not inferred from all reads",
          "Must not call nest returns natural flower visits or crop pollination",
          "No row-level original data redistributed"
      ]}
    for kind in SOURCES:
        rows,rec=obtain(kind)
        rec["time_candidates"]=temporal_support(rows,rec["columns"])
        rec["identity_candidates"]=identifier_support(rows,rec["columns"])
        audit["files"][kind]=rec
        print("RFID_SOURCE_FILE",kind,"n",rec["rows"],"sha256",rec["source_sha256"],
              "columns",rec["columns"])
        print("RFID_SOURCE_TIME",kind,json.dumps(rec["time_candidates"]))
        print("RFID_SOURCE_ID",kind,json.dumps(rec["identity_candidates"]))
    path=Path(args.output);path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text(json.dumps(audit,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
    assert len(audit["files"])==3
    print("RFID_ALL_WEATHER_INTAKE_SOURCE_PASS")
if __name__=="__main__":main()
