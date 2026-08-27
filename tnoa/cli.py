from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path

from .core import classify_rows, summarize


def main() -> None:
    ap = argparse.ArgumentParser(
        prog="tnoa",
        description="Map calibrated positive-support evidence to B/T/N/U without converting non-detection to absence.",
    )
    ap.add_argument("input", type=Path, help="CSV containing calibrated support flags")
    ap.add_argument("output", type=Path, help="Annotated CSV with decision/reason columns")
    ap.add_argument("--summary", type=Path, help="Optional JSON summary of state and U-reason rates")
    ap.add_argument("--group-by", default="", help="Comma-separated covariate columns for the summary")
    ap.add_argument("--deviation", default="deviation_observed")
    ap.add_argument("--target", default="target_supported")
    ap.add_argument("--nuisance", default="nuisance_supported")
    ap.add_argument("--observable", default="observable")
    ap.add_argument("--coupled", default="coupled_response_supported")
    ap.add_argument("--attribution", default="attribution_supported")
    args = ap.parse_args()

    with args.input.open(newline="", encoding="utf-8") as fh:
        rows = list(csv.DictReader(fh))
    if not rows:
        raise SystemExit("input CSV contains no data rows")

    annotated = classify_rows(
        rows,
        deviation=args.deviation,
        target=args.target,
        nuisance=args.nuisance,
        observable=args.observable,
        coupled=args.coupled,
        attribution=args.attribution,
    )

    args.output.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = list(annotated[0].keys())
    with args.output.open("w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(annotated)

    if args.summary:
        group_by = [x.strip() for x in args.group_by.split(",") if x.strip()]
        payload = {
            "schema": "tnoa-summary-v1",
            "input_rows": len(annotated),
            "group_by": group_by,
            "summary": summarize(annotated, group_by=group_by),
            "boundary": "inputs are already-calibrated positive support flags; this CLI does not calibrate raw sensor scores or certify biological absence",
        }
        args.summary.parent.mkdir(parents=True, exist_ok=True)
        args.summary.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
