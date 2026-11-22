#!/usr/bin/env python3
"""Mandatory source+negative ecological result claim ceiling for RFID sidecar."""
import json,math
from pathlib import Path
ROOT=Path("research/nest_activity_wind")
def source(name):
    return json.loads((ROOT/name).read_text(encoding="utf-8"))
def near(x,y,tol=1e-6):
    assert x is not None and math.isfinite(x) and abs(x-y)<tol,(x,y)
def main():
    orig=source("INTAKE_RECEIPT_2026-11-22.json")
    audit=source("TEMPORAL_SUPPORT_2026-11-22.json")
    windows=source("CLEAN_WINDOW_ELIGIBILITY_2026-11-22.json")
    times=source("RFID_ARRIVAL_TIME_CONSISTENCY_2026-11-22.json")
    derived=source("DERIVED_SAFE_15MIN_2026-11-22.json")
    result=source("EXPLORATORY_RFID_WIND_RESULT_2026-11-22.json")
    assert orig["files"]["weather"]["rows"]==102392
    assert orig["files"]["honeybee"]["rows"]==20774
    assert orig["files"]["bumblebee"]["rows"]==25158
    assert audit["unreconciled_year_mismatch"]
    assert audit["overlap"]["n_dates_with_arrivals_both_taxa_and_weather"]==27
    assert audit["weather"]["distinct_value_conflicting_duplicate_timestamps"]==19410
    assert windows["weather_bins_min_20_stable_and_zero_conflicts"]==1974
    assert windows["both_guilds_raw_antenna_reads_in_safe_weather_bins"]==504
    assert times["by_taxon"]["honeybee"]["arriving_abs_difference_gt1"]==0
    assert times["by_taxon"]["bumblebee"]["arriving_abs_difference_gt1"]==0
    assert derived["literal_source_year"]==2020 and derived["manuscript_methods_year"]==2021
    assert derived["days_accepted"]==12 and derived["n_paired_15min_bins"]==459
    assert derived["total_honey_arriving"]==463
    assert derived["total_bumble_arriving"]==602
    assert len(derived["rows"])==459
    assert result["source_year_mismatch"] is True
    assert len(result["hard_limits"])>=8
    assert result["status"]=="EXPLORATORY_ESTIMATED"
    assert result["source_scope"]["bins_with_recorded_return"]==391
    near(result["model"]["deviance_gain"],0.6045097875671672)
    near(result["model"]["wind_IQR_mps"],2.8798333333333335)
    near(result["model"]["odds_ratio_detected_honey_vs_bumble_per_wind_IQR"],0.7683605309555762)
    assert result["permutation"]["n"]==999
    assert result["permutation"]["n_at_or_above_observed"]==370
    near(result["permutation"]["plus_one_p"],0.371)
    assert result["permutation"]["failed_fits"]==0
    assert result["permutation_support"]["permutable_positive_return_bins"]==390
    near(result["weather_adjusted_sensitivity"]["wind_odds_ratio"],0.9228471995435826)
    assert len(result["leave_one_source_day_out"])==12
    # Source-year disagreement and weather duplication are NEVER silently repaired.
    safe={
      "schema":"tnoa-rfid-wind-ecological-claim-gate-v1",
      "date":"2026-11-22",
      "status":"SOURCE_VERIFIED_NEGATIVE_ECOLOGICAL_RESULT",
      "domain":"recorded RFID return share only, not true bee foraging or natural flower visitation",
      "literal_source_year":2020,
      "published_methods_year":2021,
      "source_year_discrepancy":"UNRESOLVED",
      "meteorological_conflict_timestamps":19410,
      "source_original_files_authenticated":3,
      "n_paired_15minute_bins":459,
      "n_days":12,
      "recorded_returns":{"honeybee":463,"bumblebee":602},
      "binomial_recorded_return_ratio_wind_iqr_odds_ratio":0.7683605309555762,
      "n_permutations":999,
      "wind_species_recording_share_p":0.371,
      "temperature_solar_wind_odds_ratio":0.9228471995435826,
      "scientific_conclusion":"NOT SUPPORTED: no detectable within-day wind-associated difference in recorded honeybee versus bumblebee return identity under the declared source-safe design.",
      "owner":"tnoa exploratory ecological sidecar ONLY",
      "prohibited_inference":[
         "Causal wind effect on bee activity or species sorting",
         "This is a study of 2021 in data files (literal year is 2020)",
         "Conflicting weather readings may be arbitrarily merged",
         "RFID absence is biological absence",
         "Source samples provide unbiased comparable total colony worker counts",
         "Original positive field-flower visit comparison was independently confirmed",
         "General ecological TNOA process-superposition law established"
      ]}
    p=ROOT/"FINAL_RFID_CLAIM_DISPOSITION_2026-11-22.json"
    p.write_text(json.dumps(safe,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
    print("TNOA_RFID_NEGATIVE_SOURCE_CLAIM_AUDIT_PASS")
    print(json.dumps(safe,ensure_ascii=False))
if __name__=="__main__":main()
