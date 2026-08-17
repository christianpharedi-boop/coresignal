# M0 Baseline LOD Modeling Protocol

M0 establishes CoreSignal's control condition before any inner-core predictor is introduced.

## Question

How well can LOD be predicted out of sample using only information available from the Earth-rotation record itself?

## Input

The exact EOP 20u24 C04 snapshot admitted for controlled analysis under the v0.3 rights-aware policy. The snapshot hash must match the experiment manifest.

IERS identifies EOP 20u24 C04 as a daily Earth-orientation series containing LOD in seconds. cite not allowed in repo files

## Leakage control

All fitting, feature construction, scaling, and model selection use training/validation data only. The final test interval is never used for model selection.

## Split

Chronological:
- 70% training
- 15% validation
- 15% test

No shuffling.

## Mandatory models

1. Persistence: next value equals the latest observed LOD.
2. Seasonal persistence: 365-day lag.
3. Autoregressive baseline using lagged LOD.

## Primary metric

Test RMSE in milliseconds.

Secondary metrics:
- MAE in milliseconds
- mean error in milliseconds
- correlation
- skill relative to persistence

Skill = `1 - RMSE_model / RMSE_persistence`.

## Reproducibility

Every run must record input hashes, exact split boundaries, model configuration, metrics, execution timestamp, software revision, and output hashes.

## Interpretation boundary

M0 is a control experiment. It provides no evidence for or against an inner-core mechanism.
