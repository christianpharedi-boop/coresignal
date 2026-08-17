#!/usr/bin/env python3
"""Validate CoreSignal's machine-readable provenance registry."""

from __future__ import annotations

import argparse
import hashlib
import re
import sys
from pathlib import Path

REQUIRED = [
    "source_id", "domain", "provider", "dataset_name", "status",
    "source_reference", "access_date", "license", "time_coverage",
    "sampling_interval", "units", "reference_frame",
]

ALLOWED_STATUS = {
    "planned", "discovered", "metadata_verified", "acquired",
    "hashed", "parsed", "quality_checked", "quality_checked_pending_license", "admitted", "rejected",
}

def simple_yaml_blocks(text: str):
    blocks = []
    current = None
    for line in text.splitlines():
        if line.startswith("  - source_id:"):
            if current:
                blocks.append(current)
            current = {}
            key, value = line.strip()[2:].split(":", 1)
            current[key.strip()] = value.strip()
        elif current and re.match(r"    [A-Za-z0-9_]+:", line):
            key, value = line.strip().split(":", 1)
            current[key.strip()] = value.strip()
    if current:
        blocks.append(current)
    return blocks

def validate_root(root: Path):
    registry = root / "data" / "registry.yaml"

    if not registry.exists():
        return 1

    blocks = simple_yaml_blocks(registry.read_text(encoding="utf-8"))
    if not blocks:
        return 1

    errors = []
    ids = set()

    for index, record in enumerate(blocks, 1):
        prefix = f"record {index}"
        for key in REQUIRED:
            if key not in record or not record[key]:
                errors.append(f"{prefix}: missing {key}")

        source_id = record.get("source_id")
        if source_id in ids:
            errors.append(f"{prefix}: duplicate source_id {source_id}")
        ids.add(source_id)

        status = record.get("status")
        if status not in ALLOWED_STATUS:
            errors.append(f"{prefix}: invalid status {status}")

        if status in {"quality_checked", "quality_checked_pending_license", "admitted"}:
            for key in ("sha256", "byte_size"):
                if not record.get(key) or record[key] in {"null", "to_be_recorded"}:
                    errors.append(f"{prefix}: {status} source missing {key}")
        if status == "quality_checked_pending_license":
            if record.get("analysis_status") != "analysis_admitted":
                errors.append(f"{prefix}: pending-license source must declare analysis_status=analysis_admitted")
            if record.get("redistribution_status") != "redistribution_pending":
                errors.append(f"{prefix}: pending-license source must declare redistribution_status=redistribution_pending")

    return 1 if errors else 0

def main_for_test(root: Path):
    return validate_root(root)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("root", nargs="?", default=".")
    root = Path(parser.parse_args().root).resolve()
    code = validate_root(root)
    if code:
        print("ERROR: provenance validation failed.")
    else:
        registry = root / "data" / "registry.yaml"
        blocks = simple_yaml_blocks(registry.read_text(encoding="utf-8"))
        print(f"Provenance validation passed for {len(blocks)} registered sources.")
    return code

if __name__ == "__main__":
    sys.exit(main())
