#!/usr/bin/env python3
"""Strict, fail-closed runner for an exact IERS C04 raw file."""
from __future__ import annotations

import argparse
import hashlib
import json
import math
from datetime import date, timedelta
from pathlib import Path

MJD_ORIGIN = date(1858, 11, 17)
ROOT = Path(__file__).resolve().parents[1]


def sha256_file(path: Path) -> tuple[str, int]:
    digest = hashlib.sha256()
    size = 0
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
            size += len(chunk)
    return digest.hexdigest(), size


def parse_file(path: Path) -> tuple[list[dict], list[str], str]:
    rows: list[dict] = []
    errors: list[str] = []
    headers: list[str] = []
    for line_number, raw in enumerate(path.read_text(encoding="ascii", errors="strict").splitlines(), 1):
        line = raw.rstrip("\n")
        if not line.strip():
            continue
        if line.startswith("#"):
            headers.append(line)
            continue
        fields = line.split()
        if len(fields) < 20:
            errors.append(f"line {line_number}: expected 20 fields, found {len(fields)}")
            continue
        try:
            epoch = date(int(fields[0]), int(fields[1]), int(fields[2]))
            mjd = float(fields[4])
            lod_s = float(fields[12])
            lod_error_s = float(fields[19])
        except (ValueError, IndexError) as exc:
            errors.append(f"line {line_number}: invalid required field: {exc}")
            continue
        if not all(math.isfinite(value) for value in (mjd, lod_s, lod_error_s)):
            errors.append(f"line {line_number}: non-finite MJD, LOD, or LOD error")
            continue
        expected_mjd = (epoch - MJD_ORIGIN).days
        if abs(mjd - expected_mjd) > 0.01:
            errors.append(f"line {line_number}: MJD/date mismatch ({mjd} vs {expected_mjd})")
        if lod_error_s < 0:
            errors.append(f"line {line_number}: negative LOD formal error")
        rows.append({"date": epoch, "mjd": mjd, "lod_s": lod_s, "lod_error_s": lod_error_s})
    return rows, errors, "\n".join(headers)


def validate_rows(rows: list[dict], expected_records: int | None, expected_start: str | None, expected_end: str | None) -> list[str]:
    errors: list[str] = []
    dates = [row["date"] for row in rows]
    if not rows:
        return ["no parseable data rows found"]
    if expected_records is not None and len(rows) != expected_records:
        errors.append(f"record-count mismatch ({len(rows)} parsed vs {expected_records} expected)")
    if expected_start and str(dates[0]) != expected_start:
        errors.append(f"first-date mismatch ({dates[0]} vs {expected_start})")
    if expected_end and str(dates[-1]) != expected_end:
        errors.append(f"last-date mismatch ({dates[-1]} vs {expected_end})")
    if dates != sorted(dates):
        errors.append("dates are not monotonically increasing")
    if len(dates) != len(set(dates)):
        errors.append("duplicate dates detected")
    gaps = [(a, b) for a, b in zip(dates, dates[1:]) if b - a != timedelta(days=1)]
    if gaps:
        errors.append(f"cadence gaps or irregular intervals detected ({len(gaps)} intervals)")
    return errors


def run(raw: Path, expected_records: int | None = None, expected_start: str | None = None, expected_end: str | None = None, expected_sha256: str | None = None) -> dict:
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
    if "EOP" not in header or "C04" not in header:
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
