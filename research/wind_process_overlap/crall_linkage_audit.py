#!/usr/bin/env python3
"""Pre-outcome Crall 2020 Zenodo raw source identity and specimen↔session linkage audit.

This script intentionally reads only identity and metadata fields, not ecological
responses. Only prints aggregates needed to define the sampling/analysis unit.
"""
import csv,io,hashlib,json,zipfile
from pathlib import Path
from urllib.request import Request,urlopen

ORIGINAL_URL="https://zenodo.org/records/3675327/files/CrallEtAl_OrchidBeeWindEcology.zip?download=1"
SHA256="d5b217261e4695e2098bde90576238018ad978c581f4b7799c15e429be19384b"

def load():
    with urlopen(Request(ORIGINAL_URL, headers={"User-Agent":"scientific-source-replay/1.0"}),timeout=60) as resp:
        src=resp.read()
    assert hashlib.sha256(src).hexdigest()==SHA256,"Original Zenodo ZIP identity drift"
    z=zipfile.ZipFile(io.BytesIO(src))
    def csvfile(name):
        raw=z.read("Zenodo/"+name)
        try:
            decoded=raw.decode("utf-8-sig")
            encoding="utf-8-sig"
        except UnicodeDecodeError:
            decoded=raw.decode("latin-1")
            encoding="latin-1"
        print("LINKAGE_SOURCE_ENCODING",name,encoding)
        return list(csv.DictReader(io.StringIO(decoded)))
    return csvfile("beedata.csv"),csvfile("integratedSpatialWindData.csv"),csvfile("collectionMetadata.csv"),z

def clean(s):
    return str(s if s is not None else "").strip().lower()
def main():
    bees,sessions,collections,z=load()
    assert len(bees)==450 and len(sessions)==70 and len(collections)==70
    bj=["number","date","site","time","scent"]
    sj=["coll.id","date","site","start.time","scent"]
    bjkey={x:[] for x in bj}
    sjkey={x:[] for x in sj}
    for row in bees:
        for col in bj: bjkey[col].append(clean(row[col]))
    for row in sessions:
        for col in sj: sjkey[col].append(clean(row[col]))
    idsession={clean(x["coll.id"]):i for i,x in enumerate(sessions)}
    missing_number=[x for x in bjkey["number"] if x not in idsession]
    duplicated_ids=len(idsession)!=len(sessions)
    beadates=[(clean(x["date"]),clean(x["site"]),clean(x["scent"])) for x in bees]
    sessionsdates=[(clean(x["date"]),clean(x["site"]),clean(x["scent"])) for x in sessions]
    observedstrata=set(sessionsdates)
    missing_meta=[x for x in beadates if x not in observedstrata]
    mult_meta=sum(sessionsdates.count(k)>1 for k in set(sessionsdates))
    # number+site/date/scent collision audit, excluding actual biology outcomes
    num_to_meta_error=sum(
      bool(clean(x["number"]) in idsession) and
      any(clean(x[c])!=clean(sessions[idsession[clean(x["number"])]][cs]) for c,cs in [
          ("date","date"),("site","site"),("scent","scent")])
      for x in bees)
    totals={"original_Zenodo_sha256":SHA256,"bees":len(bees),"sessions":len(sessions),
        "metadata_rows":len(collections),"n_sites":len(set(sjkey["site"])),
        "n_dates":len(set(sjkey["date"])),
        "n_scents":len(set(sjkey["scent"])),
        "n_session_ids":len(idsession),"non_session_bee_number":len(missing_number),
        "duplicate_session_ids":duplicated_ids,
        "bee_date_site_scent_missing":len(missing_meta),
        "date_site_scent_nonunique_session_keys":mult_meta,
        "number_metadata_contradictions":num_to_meta_error,
        "sample_bee_keys":[{k:r[k] for k in bj} for r in bees[:3]],
        "sample_session_keys":[{k:r[k] for k in sj} for r in sessions[:3]],
        "R_source_lines":[line.strip() for line in
             z.read("Zenodo/GenerateFiguresAndAnalyses_CrallEtAl_OrchidBeeWindEcology.R")
              .decode("utf-8-sig",errors="replace").splitlines()
             if ("coll.id" in line or "beedata" in line.lower() or "keep" in line.lower() or
                 "count" in line.lower() or "scent" in line.lower())][:60],
        "status":"LINKAGE_SCHEMA_ONLY; no biological wind×taxon response scores opened"}
    out=Path("research/wind_process_overlap/crall_linkage_audit_receipt.json")
    out.parent.mkdir(parents=True,exist_ok=True)
    out.write_text(json.dumps(totals,indent=2)+"\n")
    print("CRALL_LINKAGE",json.dumps({k:v for k,v in totals.items() if k not in
            ["R_source_lines","sample_bee_keys","sample_session_keys"]}))
    print("BEEDATA_KEY_EXAMPLES",json.dumps(totals["sample_bee_keys"]))
    print("SESSION_KEY_EXAMPLES",json.dumps(totals["sample_session_keys"]))
    print("SOURCE_ANALYSIS_R_REFERENCES",json.dumps(totals["R_source_lines"]))
    print("CRALL_LINKAGE_SCHEMA_ONLY_PASS")
if __name__=="__main__":main()
