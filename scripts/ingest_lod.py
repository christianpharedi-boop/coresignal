#!/usr/bin/env python3
"""Parse the IERS EOP 20 C04 ASCII file and write a reproducible LOD QC report."""
from __future__ import annotations

import argparse
import hashlib
import json
import math
from datetime import date, timedelta
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from rotation.lod import LODRecord, validate_lod  # noqa: E402


def file_sha256(path: Path) -> tuple[str, int]:
    digest = hashlib.sha256()
    size = 0
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
            size += len(chunk)
    return digest.hexdigest(), size


def parse_records(path: Path) -> tuple[str, list[LODRecord], list[str]]:
    header_lines: list[str] = []
    records: list[LODRecord] = []
    errors: list[str] = []
    for line_number, raw_line in enumerate(path.read_text(encoding="ascii").splitlines(), 1):
        line = raw_line.strip()
        if not line:
            continue
        if line.startswith("#"):
            header_lines.append(line)
            continue
        fields = line.split()
        if len(fields) < 20:
            errors.append(f"line {line_number}: expected at least 20 fields, found {len(fields)}")
            continue
        try:
            epoch = date(int(fields[0]), int(fields[1]), int(fields[2]))
            lod_seconds = float(fields[12])
            lod_error_seconds = float(fields[19])
        except (TypeError, ValueError) as exc:
            errors.append(f"line {line_number}: parse error: {exc}")
            continue
        if not math.isfinite(lod_seconds) or not math.isfinite(lod_error_seconds):
            errors.append(f"line {line_number}: non-finite LOD or LOD error")
            continue
        records.append(LODRecord(epoch, lod_seconds * 1000.0, f"formal_error={lod_error_seconds:g}"))
    return "\n".join(header_lines), records, errors


def build_report(path: Path) -> dict:
    digest, byte_size = file_sha256(path)
    header, records, parse_errors = parse_records(path)
    validation_errors = validate_lod(records)
    dates = [record.epoch for record in records]
    gaps = [
        {"after": str(previous), "before": str(current), "missing_days": (current - previous).days - 1}
        for previous, current in zip(dates, dates[1:])
        if current - previous != timedelta(days=1)
    ]
    lod_values = [record.lod_ms for record in records]
    return {
        "source_file": str(path.relative_to(ROOT)),
        "sha256": digest,
        "byte_size": byte_size,
        "header": header,
        "record_count": len(records),
        "date_start": str(min(dates)) if dates else None,
        "date_end": str(max(dates)) if dates else None,
        "lod_unit": "ms",
        "lod_min_ms": min(lod_values) if lod_values else None,
        "lod_max_ms": max(lod_values) if lod_values else None,
        "date_gap_count": len(gaps),
        "date_gaps": gaps[:25],
        "parse_error_count": len(parse_errors),
        "parse_errors": parse_errors[:25],
        "validation_error_count": len(validation_errors),
        "validation_errors": validation_errors[:25],
        "status": "quality_checked" if not parse_errors and not validation_errors else "rejected",
    }


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
    print(json.dumps({key: report[key] for key in ("source_file", "sha256", "record_count", "date_start", "date_end", "date_gap_count", "status")}, indent=2))
    return 0 if report["status"] == "quality_checked" else 1


if __name__ == "__main__":
    raise SystemExit(main())
