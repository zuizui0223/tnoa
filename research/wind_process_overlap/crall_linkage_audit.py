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
    # beedata.number is a bee specimen row ordinal, NOT a session ID.
    # The paper's sessions have a unique date × site × bait compound key.
    def makekey(row):
        return (clean(row["date"]),clean(row["site"]),clean(row["scent"]))
    session_by_key={makekey(row): i for i,row in enumerate(sessions)}
    session_keys=[makekey(row) for row in sessions]
    if len(session_by_key)!=len(sessions):
        raise ValueError("Sampling sessions are not unique by date/site/scent; cannot join")
    matched=[(bee,session_by_key[makekey(bee)]) for bee in bees if makekey(bee) in session_by_key]
    unmatched=[bee for bee in bees if makekey(bee) not in session_by_key]
    from collections import Counter
    actual_by_session=Counter(i for bee,i in matched)
    summary_counts=[]
    time_equal=0
    for bee,i in matched:
        time_equal+=clean(bee["time"])==clean(sessions[i]["start.time"])
    for i,row in enumerate(sessions):
        raw=row.get("count", "")
        try: source_count=int(float(raw))
        except (ValueError, TypeError):source_count=None
        summary_counts.append({"session_key":"|".join(makekey(row)),
          "source_count":source_count,
          "linked_bees":actual_by_session.get(i,0),
          "keep":clean(row.get("keep","")),
          "valid_wind":bool(row.get("wind.mean","") not in ("","NA","NaN","nan")),
          "site":clean(row["site"]),"date":clean(row["date"])})
    mismatched=[item for item in summary_counts if item["source_count"]!=item["linked_bees"]]
    wind_valid=sum(int(item["valid_wind"]) for item in summary_counts)
    totals={"original_Zenodo_sha256":SHA256,"bee_record_rows":len(bees),
        "session_rows":len(sessions),
        "collection_metadata_rows":len(collections),
        "unique_sessions_date_site_scent":len(session_by_key),
        "matched_specimen_rows":len(matched),
        "unmatched_specimen_rows":len(unmatched),
        "matched_bees_time_equal_session_start_time":time_equal,
        "sessions_with_at_least_one_bee":len(actual_by_session),
        "session_count_total":sum(item["source_count"] for item in summary_counts if item["source_count"] is not None),
        "session_matched_bee_total":sum(actual_by_session.values()),
        "sessions_source_count_mismatch":len(mismatched),
        "sessions_valid_mean_wind":wind_valid,
        "session_keep_distribution":dict(Counter(item["keep"] for item in summary_counts)),
        "unmatched_bee_dates":dict(Counter(clean(bee["date"]) for bee in unmatched)),
        "matched_sites":len({clean(sessions[i]["site"]) for bee,i in matched}),
        "dates_of_sessions":len(set(clean(x["date"]) for x in sessions)),
        "scent_types":sorted(set(clean(x["scent"]) for x in sessions)),
        "first_six_count_mismatches":mismatched[:6],
        "source_fields":{"beedata":list(bees[0]),"sessions":list(sessions[0])},
        "status":"SOURCE_LINKAGE_ONLY; no wind×taxon ecological effect computed"}
    if len(matched)<0.85*len(bees):
        raise ValueError("Insufficient original bee-session metadata linkage")
    print("CRALL_LINKAGE",json.dumps(totals))
    print("CRALL_LINKAGE_SCHEMA_ONLY_PASS")
    out=Path("research/wind_process_overlap/crall_linkage_audit_receipt.json")
    out.parent.mkdir(parents=True,exist_ok=True)
    out.write_text(json.dumps(totals,indent=2)+"\n")
    print("CRALL_LINKAGE",json.dumps({k:v for k,v in totals.items() if k not in
            ["R_source_lines","sample_bee_keys","sample_session_keys"]}))
if __name__=="__main__":main()
