#!/usr/bin/env python3
"""Original-source admission; no wind-vs-biological outcome associations opened.

Public Zenodo record 10869660, independent Ireland Brassica flower visitors.
Never redistribute the original CSV in the repository or action artifact.
"""
from __future__ import annotations
import csv,datetime,hashlib,io,json
from pathlib import Path
from collections import Counter,defaultdict
from urllib.request import Request,urlopen

URL="https://zenodo.org/records/10869660/files/1_osr_abundance_and_weather_data.csv?download=1"
EXPECTED_MD5="85cc235a323d45c0fa52efcc27db9f82"
REQUIRED=["transect","site","location","bumblebee","honeybee","solitary",
          "bumblebee_pollen","honeybee_pollen","solitary_pollen","datetimestart",
          "datetimeend","meantemp","meanwindspd","secssincemidnight"]
GUILDS=("honeybee","bumblebee","solitary","hoverfly")
def num(v):
    if v is None or str(v).strip().lower() in {"","na","nan","null","n/a"}:return None
    return float(str(v).strip().replace(",",""))
def decode(raw):
    for encoding in ("utf-8-sig","cp1252","latin-1"):
        try:return raw.decode(encoding),encoding
        except UnicodeDecodeError:pass
    raise ValueError("Unexpected source encoding")
def prepare():
    with urlopen(Request(URL,headers={"User-Agent":"Ecology-source-integrity-audit/1.0"}), timeout=45) as resp:
        raw=resp.read()
    md5=hashlib.md5(raw).hexdigest()
    if md5 != EXPECTED_MD5:raise ValueError("Zenodo file checksum mismatch: "+md5)
    text,enc=decode(raw)
    table=list(csv.DictReader(io.StringIO(text)))
    if not table:raise ValueError("Empty original CSV")
    columns=[x.strip().lower() for x in table[0].keys()]
    if len(columns)!=len(set(columns)):raise ValueError("Ambiguous case-folded duplicate source columns")
    normalized=[{k.strip().lower():v for k,v in r.items()} for r in table]
    return normalized, columns, enc,hashlib.sha256(raw).hexdigest(),len(raw)

def main():
    data,columns,enc,sha,nbytes=prepare()
    present = [k for k in REQUIRED if k in columns]
    missing = [k for k in REQUIRED if k not in columns]
    hovered=[x for x in columns if "hover" in x or "syrph" in x]
    count_columns = {k: [k] for k in ["honeybee","bumblebee","solitary"]}
    for k in ["honeybee","bumblebee","solitary"]:count_columns[k].append(k+"_pollen")
    if "hoverfly" in columns: count_columns["hoverfly"]=["hoverfly"]
    else:count_columns["hoverfly"]=hovered
    status = "SOURCE_SCHEMA_PASS"
    if missing or len(count_columns["hoverfly"])!=1:status="HOLD_UNVERIFIED_HOVERFLY_COLUMN"
    sites=Counter(str(r.get("site","")).strip() for r in data)
    locs=Counter(str(r.get("location","")).strip() for r in data)
    wind=[num(r.get("meanwindspd")) for r in data]
    finite=[v for v in wind if v is not None]
    tally=Counter();occurrences=defaultdict(lambda:{"transects":set(),"sites":set()})
    uncertain_counts=[]
    if status=="SOURCE_SCHEMA_PASS":
        for i,r in enumerate(data):
            for guild, cols in count_columns.items():
                values=[num(r.get(k)) for k in cols]
                if any(v is None or v<0 or abs(v-round(v))>1e-8 for v in values):
                    uncertain_counts.append({"row":i,"guild":guild})
                    continue
                total=int(sum(values))
                tally[guild]+=total
                if total>0:
                    occurrences[guild]["transects"].add(i)
                    occurrences[guild]["sites"].add(str(r["site"]).strip())
    from statistics import median
    wsort=sorted(finite)
    quant=lambda q: wsort[min(len(wsort)-1,round((len(wsort)-1)*q))] if wsort else None
    raw_dates=[str(x.get("datetimestart","")).strip() for x in data]
    recordids=[(str(x.get("site","")).strip(),str(x.get("datetimestart","")).strip(),
                str(x.get("transect","")).strip()) for x in data]
    receipt={
      "schema":"tnoa-natural-flower-wind-source-intake-v1",
      "source":{"zenodo_record":10869660,"zenodo_doi":"10.5061/dryad.jq2bvq8dw",
         "url":URL,"published_md5":EXPECTED_MD5,"sha256":sha,"source_bytes":nbytes,
         "encoding":enc},
      "status":status,
      "n_rows":len(data),
      "columns":columns,
      "required_columns_missing":missing,
      "hoverfly_candidate_columns":hovered,
      "butterfly_is_a_different_taxon":("butterfly" in columns),
      "source_site_distribution":dict(sites),
      "source_location_distribution":dict(locs),
      "unique_site_datetime_transect_keys":len(set(recordids)),
      "nonempty_start_timestamps":sum(bool(x) for x in raw_dates),
      "wind":{"n_finite":len(finite),"min":min(finite) if finite else None,
          "q25":quant(.25),"median":median(finite) if finite else None,
          "q75":quant(.75),"max":max(finite) if finite else None},
      "count_columns":count_columns,
      "per_guild_support":{k:{"total_visits":tally.get(k,0),
        "positive_transects":len(occurrences[k]["transects"]),
        "positive_fields":len(occurrences[k]["sites"])} for k in GUILDS},
      "uncertain_count_cell_examples":uncertain_counts[:12],
      "uncertain_count_cell_count":len(uncertain_counts),
      "status_reason":"Source MD5 verified. Butterfly is not hoverfly; the published README calls the literal butterfly field butterflies. Biological four-guild test is HOLD unless exact hoverfly source exists.",
      "hard_limits":["Natural flower visitors observed in relatively favourable weather; not a full wind-gradient experiment",
        "One weather station shifted among three sites; site/day/time confounding possible",
        "Field x date, not insect or transect rows, is uncertainty-clustering unit",
        "Published time-of-day/guild pattern remains original authors' result"]
    }
    output=Path("research/natural_flower_wind/source_intake_receipt.json")
    output.parent.mkdir(parents=True,exist_ok=True)
    output.write_text(json.dumps(receipt,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
    print("NATURAL_FLOWER_SOURCE_AUDIT",json.dumps(receipt,ensure_ascii=False))
    if status!="SOURCE_SCHEMA_PASS":
        print("SOURCE_AUDIT_COMPLETED_WITH_SCIENCE_HOLD",status)
if __name__=="__main__":main()
