#!/usr/bin/env python3
"""Execute the CoreSignal M0 LOD baseline experiment."""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import math
import subprocess
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def sha256_file(path: Path) -> tuple[str, int]:
    digest = hashlib.sha256()
    size = 0
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
            size += len(chunk)
    return digest.hexdigest(), size


def load_lod(path: Path) -> tuple[list[str], list[float]]:
    dates: list[str] = []
    values: list[float] = []
    with path.open(newline="", encoding="utf-8") as handle:
        for row in csv.DictReader(handle):
            dates.append(row["date"])
            values.append(float(row["lod_s"]))
    if not values or len(values) != len(set(dates)):
        raise ValueError("Input must contain non-empty unique-date LOD records")
    if any(not math.isfinite(value) for value in values):
        raise ValueError("Input contains non-finite LOD values")
    return dates, values


def split_indices(n: int) -> tuple[int, int, int]:
    train_end = math.floor(n * 0.70)
    validation_end = math.floor(n * 0.85)
    return train_end, validation_end, n


def persistence(values: list[float], start: int, end: int) -> list[float]:
    return [values[index - 1] for index in range(start, end)]


def seasonal_persistence(values: list[float], start: int, end: int, period: int = 365) -> list[float]:
    if start < period:
        raise ValueError("Seasonal baseline lacks the required 365-day history")
    return [values[index - period] for index in range(start, end)]


def solve_linear_system(matrix: list[list[float]], vector: list[float]) -> list[float]:
    n = len(vector)
    augmented = [matrix[row][:] + [vector[row]] for row in range(n)]
    for column in range(n):
        pivot = max(range(column, n), key=lambda row: abs(augmented[row][column]))
        if abs(augmented[pivot][column]) < 1e-12:
            raise ValueError("Singular autoregressive design matrix")
        augmented[column], augmented[pivot] = augmented[pivot], augmented[column]
        divisor = augmented[column][column]
        augmented[column] = [value / divisor for value in augmented[column]]
        for row in range(n):
            if row == column:
                continue
            factor = augmented[row][column]
            augmented[row] = [a - factor * b for a, b in zip(augmented[row], augmented[column])]
    return [augmented[row][-1] for row in range(n)]


def autoregressive_predict(train_values: list[float], horizon: int, order: int = 7) -> list[float]:
    if len(train_values) <= order:
        raise ValueError("Insufficient training history for autoregression")
    rows = []
    targets = []
    for index in range(order, len(train_values)):
        rows.append([1.0] + [train_values[index - lag] for lag in range(1, order + 1)])
        targets.append(train_values[index])
    width = order + 1
    gram = [[0.0] * width for _ in range(width)]
    rhs = [0.0] * width
    for row, target in zip(rows, targets):
        for left in range(width):
            rhs[left] += row[left] * target
            for right in range(width):
                gram[left][right] += row[left] * row[right]
    ridge = 1e-10
    for index in range(1, width):
        gram[index][index] += ridge
    coefficients = solve_linear_system(gram, rhs)
    history = train_values[:]
    predictions = []
    for _ in range(horizon):
        features = [1.0] + [history[-lag] for lag in range(1, order + 1)]
        prediction = sum(coefficient * feature for coefficient, feature in zip(coefficients, features))
        predictions.append(prediction)
        history.append(prediction)
    return predictions


def metrics(observed: list[float], predicted: list[float]) -> dict[str, float | None]:
    errors = [prediction - actual for actual, prediction in zip(observed, predicted)]
    rmse = math.sqrt(sum(error * error for error in errors) / len(errors))
    mae = sum(abs(error) for error in errors) / len(errors)
    mean_error = sum(errors) / len(errors)
    mean_observed = sum(observed) / len(observed)
    mean_predicted = sum(predicted) / len(predicted)
    numerator = sum((actual - mean_observed) * (prediction - mean_predicted) for actual, prediction in zip(observed, predicted))
    denominator = math.sqrt(sum((actual - mean_observed) ** 2 for actual in observed) * sum((prediction - mean_predicted) ** 2 for prediction in predicted))
    return {"rmse_s": rmse, "rmse_ms": rmse * 1000.0, "mae_ms": mae * 1000.0, "mean_error_ms": mean_error * 1000.0, "correlation": numerator / denominator if denominator else None}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("processed_input", type=Path)
    parser.add_argument("--source-sha256", required=True)
    parser.add_argument("--processed-sha256", required=True)
    parser.add_argument("--output", type=Path, default=ROOT / "reports/m0_lod/m0_result.json")
    args = parser.parse_args()
    source_digest, source_bytes = sha256_file(args.processed_input)
    processed_digest = args.processed_sha256
    if source_digest != processed_digest:
        raise SystemExit(f"ERROR: processed input hash mismatch: observed {source_digest}, manifest {processed_digest}")
    dates, values = load_lod(args.processed_input)
    train_end, validation_end, test_end = split_indices(len(values))
    observed = values[validation_end:test_end]
    persistence_predictions = persistence(values, validation_end, test_end)
    seasonal_predictions = seasonal_persistence(values, validation_end, test_end)
    ar_predictions = autoregressive_predict(values[:train_end], test_end - validation_end, order=7)
    persistence_metrics = metrics(observed, persistence_predictions)
    model_results = {
        "persistence": persistence_metrics,
        "seasonal_persistence_365": metrics(observed, seasonal_predictions),
        "autoregressive_order_7": metrics(observed, ar_predictions),
    }
    baseline_rmse = persistence_metrics["rmse_ms"]
    for result in model_results.values():
        result["skill_vs_persistence"] = 1.0 - result["rmse_ms"] / baseline_rmse
    report = {
        "experiment_id": "m0_lod_baseline_v001",
        "protocol_version": "0.4.0",
        "status": "executed",
        "scientific_interpretation": "control experiment only; no inner-core or geomagnetic variables used",
        "input": {"path": str(args.processed_input), "processed_sha256_observed": source_digest, "processed_sha256_manifest": processed_digest, "source_snapshot_sha256": args.source_sha256, "byte_size": source_bytes, "rows": len(values), "first_date": dates[0], "last_date": dates[-1]},
        "split": {"method": "chronological", "train_end_exclusive": train_end, "validation_end_exclusive": validation_end, "test_start": validation_end, "test_end_exclusive": test_end, "fractions": {"train": 0.70, "validation": 0.15, "test": 0.15}, "test_dates": {"first": dates[validation_end], "last": dates[-1]}},
        "model_selection": {"autoregressive_order": 7, "selected_without_test": True, "test_locked": True},
        "metrics": model_results,
        "execution": {"timestamp_utc": datetime.now(timezone.utc).isoformat(), "git_revision": subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()},
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
