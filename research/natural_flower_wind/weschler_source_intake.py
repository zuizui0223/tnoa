#!/usr/bin/env python3
"""Metadata-only audit of archived Wyoming natural flower interaction videos.

No biological behavior-outcome counts, wind effects, or co-occurrence examined.
"""
import csv,hashlib,io,json,re
from pathlib import Path
from urllib.request import Request,urlopen

RECORD=15447016
SOURCES={
 "csv":("WindPollinatorData110823.csv","9bcab4765c4fe5a9edaaf096867caf5b"),
 "r":("Bee_Behavior_CLEAN.R","5789f8f51791ae6b549abb20a2cde5c9")
}
def fetch(k):
    name,expected=SOURCES[k]
    u=f"https://zenodo.org/records/{RECORD}/files/{name}?download=1"
    with urlopen(Request(u,headers={"User-Agent":"scientific-source-authentication/1.0"}),timeout=60) as r:
        data=r.read()
    if hashlib.md5(data).hexdigest()!=expected:
        raise ValueError(f"Source MD5 drift for {name}")
    return data,u
def readcsv(data):
    text=data.decode("utf-8-sig",errors="replace")
    delimiter=csv.Sniffer().sniff(text[:4096],delimiters=",;\t").delimiter
    rows=list(csv.DictReader(io.StringIO(text),delimiter=delimiter))
    if not rows or not rows[0]:raise ValueError("CSV without header/data")
    return rows,list(rows[0])
def main():
    data,url=fetch("csv")
    code,rcodeurl=fetch("r")
    rows,headers=readcsv(data)
    auth=code.decode("utf-8-sig",errors="replace")
    keys=["site","camera","session","video","plot","date","time","wind","temp",
          "flower","plant","order","pollinator","pollen","nectar","crawl",
          "rest","touch","behavior","duration","length","id"]
    candidates={k:[s for s in headers if k in s.lower()] for k in keys}
    # Only identity candidate metadata support; no biological answer distributions opened.
    idkeys=[s for s in headers if any(x in s.lower() for x in ["site","session","record","video","camera","date","plant"])]
    diversity={}
    for col in idkeys:
        vals=[str(row.get(col,"")).strip() for row in rows]
        diversity[col]={"distinct_values":len(set(vals)),
           "missing":sum(not v or v.lower() in ("na","nan") for v in vals),
           "examples":list(dict.fromkeys(vals))[:8]}
    relevant_code=[s.strip() for s in auth.splitlines()
      if any(x in s.lower() for x in ["read.csv","read_csv","read.table",
         "wind", "pollen","nectar","crawl","duration","session","video",
         "bee_behavior", "id="])][:65]
    o={
      "schema":"tnoa-weschler-natural-flower-source-intake-v1",
      "scientific_status":"ORIGINAL_SOURCE_INTEGRITY_ONLY_NO_BEHAVIORAL_EFFECTS_OPENED",
      "original_record":RECORD,
      "article_doi":"10.1002/njb.04996",
      "csv":{"url":url,"md5":SOURCES["csv"][1],
        "sha256":hashlib.sha256(data).hexdigest(),"bytes":len(data),
        "n_rows":len(rows),"n_columns":len(headers),"headers":headers,
        "column_role_candidates":candidates,"source_identity_support":diversity},
      "original_r_script":{"url":rcodeurl,"md5":SOURCES["r"][1],
        "sha256":hashlib.sha256(code).hexdigest(),"bytes":len(code),
        "relevant_original_author_code_lines":relevant_code},
      "notes":["Data source is outside TNOA observation-record validation",
        "Source contains actual video-coded natural-flower insect visits but study sampled one wind facility system",
        "Individual insect interaction rows are not independent wind exposure units",
        "No ecological result is unlocked without validated video session identity and behavior codebook"]
    }
    p=Path("research/natural_flower_wind/WESCHLER_SOURCE_INTAKE_2026-11-19.json")
    p.parent.mkdir(parents=True,exist_ok=True)
    p.write_text(json.dumps(o,indent=2,ensure_ascii=False)+"\n")
    print("WESCHLER_SOURCE_INTAKE",json.dumps(o,ensure_ascii=False)[:18000])
    print("WESCHLER_SOURCE_IDENTITY_PASS",len(rows),len(headers))
if __name__=="__main__":main()
