#!/usr/bin/env python3
"""Compatibility entry point for the canonical strict IERS C04 LOD pipeline.

The historical ``ingest_lod.py`` command remains available, but parsing and
validation are delegated to ``run_lod_pipeline.py`` so the repository has one
source-specific parser and one set of acceptance rules.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from run_lod_pipeline import run  # noqa: E402


def build_report(path: Path) -> dict:
    """Return the canonical strict report under the legacy function name."""
    return run(path)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("raw_file", type=Path)
    parser.add_argument("--output", type=Path, default=ROOT / "reports/lod_inventory/eop20_c04_qc.json")
    args = parser.parse_args()
    raw_file = args.raw_file.resolve()
    if not raw_file.is_file():
        raise SystemExit(f"ERROR: raw file not found: {raw_file}")
    report = build_report(raw_file)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({key: report.get(key) for key in ("raw_file", "sha256", "parsed_rows", "first_date", "last_date", "status")}, indent=2))
    return 0 if report["status"] == "quality_checked" else 1


if __name__ == "__main__":
    raise SystemExit(main())
