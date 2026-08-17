from __future__ import annotations
import math
from dataclasses import dataclass
from typing import Sequence

@dataclass(frozen=True)
class Split:
    train_end: int
    validation_end: int
    test_start: int

def chronological_split(n: int, train_fraction=.70, validation_fraction=.15) -> Split:
    if n < 10 or not (0 < train_fraction < 1) or not (0 < validation_fraction < 1):
        raise ValueError("Invalid split parameters")
    if train_fraction + validation_fraction >= 1:
        raise ValueError("Train plus validation must be below one")
    train_end = math.floor(n * train_fraction)
    validation_end = math.floor(n * (train_fraction + validation_fraction))
    return Split(train_end, validation_end, validation_end)

def persistence_predict(history: Sequence[float], horizon: int) -> list[float]:
    if not history:
        raise ValueError("History cannot be empty")
    return [float(history[-1])] * horizon

def seasonal_persistence_predict(history: Sequence[float], horizon: int, period=365) -> list[float]:
    if len(history) < period:
        raise ValueError("Insufficient history")
    return [float(history[-period + i]) for i in range(horizon)]

def rmse(observed: Sequence[float], predicted: Sequence[float]) -> float:
    if len(observed) != len(predicted) or not observed:
        raise ValueError("Equal non-empty arrays required")
    return math.sqrt(sum((a-b)**2 for a,b in zip(observed,predicted))/len(observed))

def mae(observed: Sequence[float], predicted: Sequence[float]) -> float:
    if len(observed) != len(predicted) or not observed:
        raise ValueError("Equal non-empty arrays required")
    return sum(abs(a-b) for a,b in zip(observed,predicted))/len(observed)

def skill_vs_persistence(model_rmse: float, persistence_rmse: float) -> float:
    if persistence_rmse <= 0:
        raise ValueError("Persistence RMSE must be positive")
    return 1.0 - model_rmse / persistence_rmse
