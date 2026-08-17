#!/usr/bin/env python3
"""Validate CoreSignal experiment manifests against the v0.2 minimum contract."""
from __future__ import annotations

import sys
from pathlib import Path

try:
    import yaml
except ImportError as exc:  # pragma: no cover - exercised in clean environments
    raise SystemExit("PyYAML is required: install it with 'python -m pip install pyyaml'.") from exc

REQUIRED_TOP_LEVEL = {
    "experiment_id",
    "target",
    "predictors",
    "model",
    "validation",
    "primary_metric",
    "acceptance",
}
REQUIRED_TARGET = {"variable", "unit"}
REQUIRED_VALIDATION = {"method", "final_test_locked"}
REQUIRED_METRIC = {"name", "direction"}
REQUIRED_ACCEPTANCE = {"threshold_declared_before_final_test"}
ALLOWED_VALIDATION = {"rolling_origin", "blocked_temporal", "fixed_temporal_holdout"}


def validate_manifest(path: Path) -> list[str]:
    errors: list[str] = []
    try:
        document = yaml.safe_load(path.read_text(encoding="utf-8"))
    except Exception as exc:
        return [f"{path}: cannot parse YAML: {exc}"]

    if not isinstance(document, dict):
        return [f"{path}: manifest must contain a mapping"]

    missing = REQUIRED_TOP_LEVEL - document.keys()
    errors.extend(f"{path}: missing top-level field '{field}'" for field in sorted(missing))

    for section, required in (
        ("target", REQUIRED_TARGET),
        ("validation", REQUIRED_VALIDATION),
        ("primary_metric", REQUIRED_METRIC),
        ("acceptance", REQUIRED_ACCEPTANCE),
    ):
        value = document.get(section)
        if not isinstance(value, dict):
            errors.append(f"{path}: '{section}' must be a mapping")
            continue
        errors.extend(
            f"{path}: missing {section} field '{field}'"
            for field in sorted(required - value.keys())
        )

    validation = document.get("validation", {})
    if isinstance(validation, dict) and validation.get("method") not in ALLOWED_VALIDATION:
        errors.append(f"{path}: unsupported validation method '{validation.get('method')}'")

    if document.get("predictors") == []:
        errors.append(f"{path}: predictors must not be empty")

    return errors


def main(root: Path) -> int:
    manifests = sorted((root / "experiments").rglob("*.yaml"))
    if not manifests:
        print("No experiment manifests found.")
        return 1

    errors = [error for manifest in manifests for error in validate_manifest(manifest)]
    if errors:
        print("Manifest validation failed:")
        print("\n".join(errors))
        return 1

    print(f"Manifest validation passed for {len(manifests)} experiment manifest(s).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(Path(sys.argv[1]) if len(sys.argv) > 1 else Path(".")))
