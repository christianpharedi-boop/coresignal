"""Validate the CoreSignal M1 Gate 2A acquisition ledger."""
from __future__ import annotations

import re
import sys
from pathlib import Path

import yaml

LEDGER_ID = re.compile(r"^gate2a_[a-z0-9_]+$")
RECORD_ID = re.compile(r"^gate2a_file_[0-9]{4}$")
SHA256 = re.compile(r"^[a-f0-9]{64}$")
ALLOWED_LEDGER_STATUS = {"BLOCKED", "READY_FOR_GATE2_RECONSTRUCTION", "INVALID"}
ALLOWED_FILE_STATUS = {"PLANNED", "ACQUIRED", "VERIFIED", "REJECTED", "SUPERSEDED"}
ALLOWED_VERIFICATION = {"PENDING", "VERIFIED", "FAILED"}
ALLOWED_LICENCE = {"PENDING", "VERIFIED", "RESTRICTED", "UNKNOWN", "NOT_APPLICABLE"}
REQUIRED_RECORD_FIELDS = {"record_id", "manifest_file_id", "file_state", "scientific_role", "source", "acquisition", "integrity", "licence", "verification", "execution"}


def validate_ledger(path: Path) -> list[str]:
    errors: list[str] = []
    try:
        document = yaml.safe_load(path.read_text(encoding="utf-8"))
    except Exception as exc:
        return [f"{path}: cannot parse YAML: {exc}"]
    if not isinstance(document, dict):
        return [f"{path}: ledger must be a mapping"]

    required = {"ledger", "files", "ledger_integrity"}
    errors.extend(f"{path}: missing top-level field '{key}'" for key in sorted(required - document.keys()))
    ledger = document.get("ledger", {})
    if not isinstance(ledger, dict):
        return [f"{path}: ledger section must be a mapping"]
    for key in ("ledger_id", "schema_version", "experiment_id", "gate", "frozen_manifest_id", "created_utc", "execution_policy"):
        if key not in ledger:
            errors.append(f"{path}: missing ledger field '{key}'")
    if ledger.get("ledger_id") and not LEDGER_ID.fullmatch(str(ledger["ledger_id"])):
        errors.append(f"{path}: invalid ledger_id")
    if ledger.get("schema_version") != "1.0.0":
        errors.append(f"{path}: schema_version must be 1.0.0")
    if ledger.get("experiment_id") != "m1_inner_core":
        errors.append(f"{path}: experiment_id must be m1_inner_core")
    if ledger.get("gate") != "M1-Gate-2A":
        errors.append(f"{path}: gate must be M1-Gate-2A")
    if ledger.get("execution_policy") != "fail_closed":
        errors.append(f"{path}: execution_policy must be fail_closed")

    files = document.get("files")
    if not isinstance(files, list) or not files:
        errors.append(f"{path}: files must be a non-empty list")
        files = []
    record_ids = []
    manifest_ids = []
    for index, record in enumerate(files, start=1):
        prefix = f"{path}: files[{index}]"
        if not isinstance(record, dict):
            errors.append(f"{prefix} must be a mapping")
            continue
        missing = REQUIRED_RECORD_FIELDS - record.keys()
        errors.extend(f"{prefix}: missing field '{key}'" for key in sorted(missing))
        record_id = record.get("record_id")
        manifest_id = record.get("manifest_file_id")
        if record_id:
            record_ids.append(record_id)
            if not RECORD_ID.fullmatch(str(record_id)):
                errors.append(f"{prefix}: invalid record_id")
        if manifest_id:
            manifest_ids.append(manifest_id)
        status = record.get("status", "PLANNED")
        if status not in ALLOWED_FILE_STATUS:
            errors.append(f"{prefix}: invalid status '{status}'")
        source = record.get("source", {})
        if not isinstance(source, dict) or not source.get("source_url") or not source.get("source_version"):
            errors.append(f"{prefix}: source_url and source_version are required")
        acquisition = record.get("acquisition", {})
        if not isinstance(acquisition, dict):
            errors.append(f"{prefix}: acquisition must be a mapping")
        elif status in {"VERIFIED", "REJECTED", "SUPERSEDED"} and (not acquisition.get("original_filename") or not acquisition.get("acquisition_timestamp_utc") or acquisition.get("byte_size") is None):
            errors.append(f"{prefix}: final records require acquisition timestamp, original filename, and byte size")
        integrity = record.get("integrity", {})
        digest = integrity.get("sha256") if isinstance(integrity, dict) else None
        if status in {"VERIFIED", "REJECTED", "SUPERSEDED"} and (not digest or not SHA256.fullmatch(str(digest))):
            errors.append(f"{prefix}: verified-or-final records require a lowercase SHA-256")
        licence = record.get("licence", {})
        if not isinstance(licence, dict) or licence.get("status") not in ALLOWED_LICENCE:
            errors.append(f"{prefix}: invalid licence status")
        verification = record.get("verification", {})
        if not isinstance(verification, dict) or verification.get("status") not in ALLOWED_VERIFICATION:
            errors.append(f"{prefix}: invalid verification status")
        execution = record.get("execution", {})
        if not isinstance(execution, dict) or execution.get("status") not in {"BLOCKED", "CLEARED"} or not isinstance(execution.get("blocking"), bool):
            errors.append(f"{prefix}: invalid execution status")

    if len(record_ids) != len(set(record_ids)):
        errors.append(f"{path}: duplicate record_id")
    if len(manifest_ids) != len(set(manifest_ids)):
        errors.append(f"{path}: duplicate manifest_file_id")

    integrity = document.get("ledger_integrity", {})
    if not isinstance(integrity, dict):
        errors.append(f"{path}: ledger_integrity must be a mapping")
    else:
        if integrity.get("record_count") != len(files):
            errors.append(f"{path}: record_count does not match files")
        if integrity.get("ledger_status") not in ALLOWED_LEDGER_STATUS:
            errors.append(f"{path}: invalid ledger_status")
        if integrity.get("ledger_status") == "READY_FOR_GATE2_RECONSTRUCTION":
            if not all(integrity.get(key) is True for key in ("unique_record_ids", "unique_manifest_file_ids", "all_required_files_present")):
                errors.append(f"{path}: READY status requires integrity booleans to be true")
    return errors


def main() -> int:
    path = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("data/m1_gate2/acquisition_ledger.yaml")
    errors = validate_ledger(path)
    if errors:
        print("Gate 2A ledger validation failed:")
        print("\n".join(errors))
        return 1
    print(f"Gate 2A ledger validation passed: {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
