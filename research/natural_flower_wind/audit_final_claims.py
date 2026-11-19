#!/usr/bin/env python3
"""Fail-closed publication boundary audit of two source-verified ecological datasets.

The locked comparison has an initial cross-day wind association, adverse
within-day tests, an unestimable within-date guild composition model, and a
negative same-visit behavioral co-occurrence null. NEVER silently promote a
source-corrected post hoc finding into the frozen TNOA methods manuscript.
"""
from __future__ import annotations
from pathlib import Path
import json,math

ROOT=Path("research/natural_flower_wind")
def read(name):
    return json.loads((ROOT/name).read_text(encoding="utf-8"))
def near(x,y,tol=1e-6):
    assert x is not None and math.isfinite(x) and abs(x-y)<=tol, f"anchor drift: {x} != {y}"

def main():
    source=read("source_intake_receipt.json")
    taxonomy=read("SEMANTIC_AUDIT_2026-11-19.json")
    primary=read("THREE_BEE_GUILD_RESULT_2026-11-19.json")
    same_day=read("THREE_BEE_DATE_BLOCK_SENSITIVITY_2026-11-19.json")
    fixed=read("THREE_BEE_SITE_DATE_FIXED_EFFECT_2026-11-19.json")
    wyoming=read("WESCHLER_BEHAVIOR_COOCCURRENCE_2026-11-19.json")
    west_source=read("WESCHLER_SOURCE_INTAKE_2026-11-19.json")
    west_key=read("WESCHLER_SESSION_KEY_AUDIT_2026-11-19.json")

    assert source["status"]=="HOLD_UNVERIFIED_HOVERFLY_COLUMN"
    assert source["hoverfly_candidate_columns"]==[]
    assert source["butterfly_is_a_different_taxon"] is True
    assert source["source"]["sha256"]=="07c902217da47953966f93319ef8db4ef1a83d7911f41c86cbe735368e7820b5"
    assert taxonomy["source_rows"]==496 and taxonomy["unique_all_columns_rows"]==124
    assert taxonomy["site_time_transect_group_size_distribution"]=={"4":124}
    assert primary["source"]["identical_fourfold_copies"] is True
    assert primary["source"]["independent_source_transects_before_missing_weather"]==124
    assert primary["coverage"]["eligible_observations"]==120
    assert primary["quantity"]["total_bee_visits"]==3282
    assert primary["identity"]["categories"]==["honeybee","bumblebee","solitary"]
    assert "hoverfly" not in primary["identity"]["categories"]
    assert primary["permutation"]["n"]==999 and primary["permutation"]["failed_quantity"]==0
    assert primary["permutation"]["failed_identity"]==0
    near(primary["quantity"]["rate_ratio_per_wind_iqr"],0.7989421127418261)
    near(primary["quantity"]["p_plus_one"],0.016,1e-9)
    near(primary["identity"]["p_plus_one"],0.001,1e-9)

    assert same_day["status"]=="EXPLORATORY_ESTIMATED"
    assert same_day["source_rows"]==496 and same_day["exact_unique_transects"]==124
    assert same_day["n_permutations"]==999 and same_day["source_support"]["permutable_transects"]==101
    near(same_day["field_date_permutation_count_p"],0.982,1e-9)
    near(same_day["field_date_permutation_guild_p"],0.641,1e-9)
    assert same_day["count_fit_failures"]==same_day["guild_fit_failures"]==0
    assert same_day["temp_solar_adjusted_fit"]["status"]=="PASS"
    near(same_day["temp_solar_adjusted_fit"]["count_rate_ratio_per_wind_iqr"],0.9094986412707176)

    assert fixed["status"]=="PARTIAL_COUNT_ESTIMATED_GUILD_HOLD"
    assert fixed["count_status"]=="ESTIMABLE"
    assert fixed["guild_status"]=="HOLD_DATE_FIXED_EFFECT_GUILD_OPTIMIZER"
    assert fixed["site_date_group_count"]==17
    assert fixed["n_permutable_rows"]==101 and fixed["permutations"]==999
    assert fixed["null_count_fit_failures"]==0
    assert fixed["within_day_guild_permutation_p"] is None
    near(fixed["within_day_count_rate_ratio_per_source_wind_IQR"],1.3999943237719237)
    near(fixed["within_day_count_permutation_p"],0.101,1e-9)
    # Sign reversal from across-day slope to within-day slope must remain explicit.
    assert primary["quantity"]["rate_ratio_per_wind_iqr"]<1.0
    assert fixed["within_day_count_rate_ratio_per_source_wind_IQR"]>1.0

    assert west_source["csv"]["sha256"]=="55f514b6dfae277fcbae43e105e796667af77a897a1da558407f5c15929647e0"
    assert west_key["rows"]==472 and west_key["unique_id_groups"]==15
    assert west_key["multi_plant_unique_id_group_n"]==2
    assert wyoming["status"]=="EXPLORATORY_ESTIMATED"
    assert wyoming["units"]["valid_interactions"]==472
    assert wyoming["units"]["video_sessions"]==15
    assert wyoming["units"]["pollen_positive_visits"]==198
    assert wyoming["units"]["nectar_positive_visits"]==39
    assert wyoming["primary"]["observed_joint_visits"]==20
    near(wyoming["primary"]["expected_under_within_video_session_independence"],20.221611017121855)
    near(wyoming["primary"]["two_sided_p_plus_one"],1.,1e-9)
    assert wyoming["primary"]["n_permutations"]==999
    for scenario in ["source_visit_session_by_plant","source_visit_session_by_filename",
                     "source_visit_session_by_plant_filename"]:
        x=wyoming["plant_and_video_file_null_sensitivity"][scenario]
        assert x["status"]=="EXPLORATORY_ESTIMATED"
        near(x["two_sided_p_plus_one"],1.,1e-9)
    assert wyoming["wind_exploration"]["status"]=="DESCRIPTIVE_ONLY"

    receipt={
      "schema":"tnoa-natural-flower-ecological-claim-gate-v1",
      "date":"2026-11-19",
      "status":"SOURCE_VERIFIED_RESULTS_AND_HOLDS_FROZEN",
      "original_four_guild_ireland":"HOLD_UNVERIFIED_HOVERFLY_COLUMN",
      "corrected_three_bee_ireland":{
          "n_independent_transects":120,
          "baseline_amount_rate_ratio":primary["quantity"]["rate_ratio_per_wind_iqr"],
          "baseline_amount_p":primary["quantity"]["p_plus_one"],
          "baseline_guild_composition_p":primary["identity"]["p_plus_one"],
          "same_day_block_permutation_amount_p":same_day["field_date_permutation_count_p"],
          "same_day_block_permutation_guild_p":same_day["field_date_permutation_guild_p"],
          "fixed_site_date_amount_rate_ratio":fixed["within_day_count_rate_ratio_per_source_wind_IQR"],
          "fixed_site_date_amount_p":fixed["within_day_count_permutation_p"],
          "fixed_site_date_guild":"HOLD_DATE_FIXED_EFFECT_GUILD_OPTIMIZER",
          "interpretation":"NO ROBUST POSITIVE SAME-DAY WIND ASSOCIATION; first-pass wind sign is reversed by source date fixed effects."
      },
      "wyoming_video_behavior_overlap":{
        "n_video_interactions":472,
        "n_source_uid_wind_contexts":15,
        "observed_pollen_and_nectar":20,
        "within_uid_null_expected":20.221611017121855,
        "within_uid_p":1.,
        "stricter_plant_file_p":1.,
        "interpretation":"NO SUPPORT FOR BEYOND-SESSION-INDEPENDENCE EXCESS OF POLLEN×NECTAR BEHAVIOR."
      },
      "prohibited_generalizations":[
        "A causal wind effect on any bee guild or count",
        "Universal ecological wind–interaction amount or identity rule",
        "A biological difference proven by comparing independent p values",
        "Absence of natural pollen transfer or pollination effectiveness",
        "TNOA classifier ecological field validation or C2 intervention prediction confirmation",
        "Converting butterfly to hoverfly or 496 rows to independent transects"
      ]
    }
    path=ROOT/"FINAL_REPRODUCED_DISPOSITION_2026-11-19.json"
    path.write_text(json.dumps(receipt,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
    print("TNOA_NATURAL_FLOWER_FINAL_CLAIM_GATE_PASS")
    print(json.dumps(receipt,ensure_ascii=False))
if __name__=="__main__":
    main()
