#!/usr/bin/env python3
"""Canonical strict, fail-closed runner for an exact IERS C04 raw file."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from rotation.iers_c04 import header_identifies_c04, parse_file, validate_rows  # noqa: E402


def sha256_file(path: Path) -> tuple[str, int]:
    digest = hashlib.sha256()
    size = 0
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
            size += len(chunk)
    return digest.hexdigest(), size


def run(
    raw: Path,
    expected_records: int | None = None,
    expected_start: str | None = None,
    expected_end: str | None = None,
    expected_sha256: str | None = None,
) -> dict:
    result = {"status": "blocked", "raw_file": str(raw), "errors": []}
    if not raw.is_file():
        result["errors"] = [f"missing raw file: {raw}"]
        return result
    digest, byte_size = sha256_file(raw)
    result.update({"sha256": digest, "byte_size": byte_size})
    if expected_sha256 and digest != expected_sha256:
        result["errors"].append(f"SHA-256 mismatch ({digest} vs {expected_sha256})")
    rows, parse_errors, header = parse_file(raw)
    result["header"] = header
    if not header_identifies_c04(header):
        result["errors"].append("source header does not identify an EOP C04 product")
    result["errors"].extend(parse_errors)
    result["errors"].extend(validate_rows(rows, expected_records, expected_start, expected_end))
    result["parsed_rows"] = len(rows)
    result["first_date"] = str(rows[0]["date"]) if rows else None
    result["last_date"] = str(rows[-1]["date"]) if rows else None
    result["status"] = "quality_checked" if not result["errors"] else "rejected"
    return result


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("raw_file", type=Path)
    parser.add_argument("--expected-records", type=int)
    parser.add_argument("--expected-start")
    parser.add_argument("--expected-end")
    parser.add_argument("--expected-sha256")
    parser.add_argument("--output", type=Path, default=ROOT / "reports/lod_pipeline_result.json")
    args = parser.parse_args()
    result = run(args.raw_file.resolve(), args.expected_records, args.expected_start, args.expected_end, args.expected_sha256)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2))
    return 0 if result["status"] == "quality_checked" else 2


if __name__ == "__main__":
    raise SystemExit(main())
