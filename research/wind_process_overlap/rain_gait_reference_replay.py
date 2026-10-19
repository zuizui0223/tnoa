#!/usr/bin/env python3
"""Exploratory mammal movement × source-RAIN label replay on independent CCTV pass truth.

Not a pre-registered rainfall-ecology test. Reuses the published Findlay camera/CCTV
data but DOES NOT condition outcome discovery on camera trigger; record-gate
selection is evaluated as a separate secondary measurement contrast.

No raw external data are redistributed. No individual-level or day-level IDs
exist in this source. Positions are observation strata, not biological replicas.
"""
from __future__ import annotations
import argparse
import csv
import hashlib
import io
import json
from pathlib import Path
from urllib.request import Request, urlopen

SOURCE_COMMIT = "abc72f535bb59ebed202fb7acca852fc1647e97a"
SOURCE_BLOB = "d2dc9852ca1f2a1380b991acba425d16e12327d5"
FILENAME = "REGISTRATION_FOX_BADGER.csv"
SOURCE_URL = "https://raw.githubusercontent.com/melaniefindlay/CT-Detection/" + SOURCE_COMMIT + "/" + FILENAME
POSITIONS = ["SNIG", "AP", "SF", "FF"]
SPECIES = ["FOX", "BADGER"]
WEATHER = ["YES", "NO"]

def load():
    req=Request(SOURCE_URL,headers={"User-Agent":"TNOA-exploratory-ecology-audit/1.0"})
    with urlopen(req,timeout=60) as r: raw=r.read()
    git_blob = b"blob " + str(len(raw)).encode() + b"\0" + raw
    actual = hashlib.sha1(git_blob).hexdigest()
    if actual != SOURCE_BLOB:
        raise ValueError("Source Git blob identity mismatch; abort rather than reinterpret changed upstream")
    rows=list(csv.DictReader(io.StringIO(raw.decode("utf-8-sig"))))
    if len(rows)!=881: raise ValueError("Expected original 881 CCTV pass records")
    return rows,hashlib.sha256(raw).hexdigest()

def fraction(records, field, expected="W"):
    return sum(x[field]==expected for x in records)/len(records) if records else None

def cell_summary(records, stage="reference"):
    grouped={}
    for species in SPECIES:
        grouped[species]={}
        for weather in WEATHER:
            valid=[x for x in records if x["SPECIES"]==species and x["RAIN"]==weather]
            if stage=="trigger":valid=[x for x in valid if x["TRIGGER"]=="1"]
            if stage=="capture":valid=[x for x in valid if x["CAPTURE"]=="1"]
            grouped[species][weather]={
              "n":len(valid),
              "walk_count":sum(x["GAIT"]=="W" for x in valid),
              "walk_fraction":fraction(valid,"GAIT","W")}
        if all(grouped[species][w]["n"]>0 for w in WEATHER):
            grouped[species]["rain_minus_no_walk"]=(
              grouped[species]["YES"]["walk_fraction"]-grouped[species]["NO"]["walk_fraction"])
        else:
            grouped[species]["rain_minus_no_walk"]=None
    fox=grouped["FOX"]["rain_minus_no_walk"]
    badger=grouped["BADGER"]["rain_minus_no_walk"]
    return {"by_species":grouped,
            "fox_minus_badger_rain_contrast":fox-badger if fox is not None and badger is not None else None}

def position_summary(records):
    sites={}
    for pos in POSITIONS:
        subset=[x for x in records if x["CT.POS"]==pos]
        block=cell_summary(subset)
        sites[pos]={"n":len(subset),
                    "by_species":block["by_species"],
                    "contrast":block["fox_minus_badger_rain_contrast"]}
    valid=[x["contrast"] for x in sites.values() if x["contrast"] is not None]
    return {"by_position":sites,
            "equal_position_fox_minus_badger_difference":sum(valid)/len(valid) if len(valid)==len(POSITIONS) else None,
            "fox_positive_positions":sum(sites[p]["by_species"]["FOX"]["rain_minus_no_walk"]>0 for p in POSITIONS),
            "badger_negative_positions":sum(sites[p]["by_species"]["BADGER"]["rain_minus_no_walk"]<0 for p in POSITIONS)}

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument("--output",default="research/wind_process_overlap/rain_gait_reference_result.json")
    args=parser.parse_args()
    original,source_sha=load()
    rejected={str(k):sum(x["RAIN"]==k for x in original) for k in sorted({x["RAIN"] for x in original}) if k not in WEATHER}
    admitted=[x for x in original if x["RAIN"] in WEATHER]
    if len(admitted)!=870 or rejected!={"N0":4,"NA":7}:
        raise ValueError("Unexpected RAIN code denominator; do not impute N0 as NO")
    result={
      "schema":"tnoa-rain-gait-observed-pass-exploration-v1",
      "date":"2026-10-19",
      "science_status":"retrospective-exploratory-not-confirmed-abiotic-causal-effect",
      "original_source":{
         "paper":"Findlay MA, Briers RA, White PJC (2020). Mammal Research 65:167-180",
         "paper_doi":"10.1007/s13364-020-00478-y",
         "repository":"melaniefindlay/CT-Detection",
         "commit":SOURCE_COMMIT,"path":FILENAME,"git_blob_sha1":SOURCE_BLOB,
         "raw_source_sha256":source_sha},
      "denominators":{"original_CCTV_pass_rows":len(original),"RAIN_YES_NO_admitted":len(admitted),
                      "excluded_uninterpretable_RAIN_values":rejected},
      "biological_endpoint":"CCTV-observed gait: walk=W vs trot=T or run=R among TRUE passes, conditional on observed passes",
      "exposure":"Literal RAIN=YES versus RAIN=NO CSV label; the original article does not specify a full rain-measurement protocol. Neither intensity nor temporal assignment has been verified.",
      "reference":cell_summary(admitted),
      "by_position":position_summary(admitted),
      "stage_comparison":{
         "camera_triggered":cell_summary(admitted,stage="trigger"),
         "final_camera_capture":cell_summary(admitted,stage="capture")},
      "sensitivity":{
         "only_lateral_orientation":cell_summary([x for x in admitted if x["ORIENT"]=="L"]),
         "exclude_loitering":cell_summary([x for x in admitted if x["LOIT"]=="0"]),
         "perpendicular_distance_1to7m":cell_summary([x for x in admitted if 1<=int(x["DIST"])<=7])},
      "rejected_inferences":[
        "RAIN label confirmed as an independently calibrated rain intensity/exposure",
        "same-animal independence of CCTV passes",
        "independent population replication of four CT positions",
        "weather effects on total mammal activity rate without rain-time exposure denominator",
        "causal rainfall effects on gait or species choice",
        "a validated TNOA-field performance result",
        "prospective evidence of natural process-superposition universality"],
      "note":"Source article examines detection outcomes, not a weather-by-species causal gait hypothesis. This ecological reanalysis is new and post hoc; role as hypothesis generation, not a publishable causal result."
    }
    observed=result["by_position"]
    def near(actual,expected):
        if abs(actual-expected)>0.0000005:
            raise AssertionError(f"Frozen exploratory replay changed: {actual} != {expected}")
    near(result["reference"]["by_species"]["FOX"]["rain_minus_no_walk"],0.24262391097444913)
    near(result["reference"]["by_species"]["BADGER"]["rain_minus_no_walk"],-0.15401621223286663)
    near(observed["equal_position_fox_minus_badger_difference"],0.3886201026649085)
    if observed["fox_positive_positions"]!=4 or observed["badger_negative_positions"]!=4:
        raise AssertionError("Position-level directional sensitivity changed")
    near(result["sensitivity"]["only_lateral_orientation"]["fox_minus_badger_rain_contrast"],0.4134871632174931)
    near(result["sensitivity"]["exclude_loitering"]["fox_minus_badger_rain_contrast"],0.45723124545342797)
    output=Path(args.output)
    output.parent.mkdir(parents=True,exist_ok=True)
    output.write_text(json.dumps(result,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
    print("RAIN_GAIT_REFERENCE_REPLAY_PASS",
       "n",len(admitted),
       "fox_rain_minus_no",result["reference"]["by_species"]["FOX"]["rain_minus_no_walk"],
       "badger_rain_minus_no",result["reference"]["by_species"]["BADGER"]["rain_minus_no_walk"],
       "equal_pos_interaction",observed["equal_position_fox_minus_badger_difference"],
       "lateral_interaction",result["sensitivity"]["only_lateral_orientation"]["fox_minus_badger_rain_contrast"])
if __name__=="__main__":
    main()
