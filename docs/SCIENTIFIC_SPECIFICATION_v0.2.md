# CoreSignal Scientific Specification v0.2

**Status:** Research protocol  
**Version:** 0.2.0  
**Date:** 2026-08-17  
**Author:** Basie Pharedi

## 1. Purpose

CoreSignal is a computational research program testing whether independently inferred inner-core dynamics contain reproducible predictive information about Earth's rotation and geomagnetic variation.

The project is explicitly hypothesis-falsifying. The implementation must not assume that inner-core dynamics explain the observed signals.

## 2. Primary research question

Can time-varying inner-core differential rotation and deformation be quantitatively connected to measurable variations in Earth's length of day (LOD) and geomagnetic secular variation?

## 3. Hypotheses

### H0: Null

After accounting for appropriate baseline and control variables, the inferred inner-core state provides no reproducible out-of-sample predictive improvement for LOD.

### H1: Inner-core coupling

The inferred inner-core state provides statistically significant and physically interpretable out-of-sample predictive information for LOD.

### H2: Lagged coupling

The predictive relationship between inner-core state and LOD is improved when a physically plausible temporal lag is allowed.

### H3: Geomagnetic extension

The inner-core state provides reproducible predictive information for selected geomagnetic secular-variation observables beyond an appropriate baseline model.

### H4: Coupled model

A model containing inner-core and other independently justified core/mantle state variables performs better out of sample than models using the inner-core state alone.

## 4. Falsifiable predictions

A positive result must satisfy all relevant gates:

1. The inner-core predictor is derived without using the target-period LOD observations.
2. The relationship survives temporal out-of-sample testing.
3. Predictive improvement exceeds the pre-registered threshold against the baseline.
4. The effect is robust to reasonable preprocessing choices.
5. The sign, magnitude, and lag are physically interpretable.
6. The result survives appropriate uncertainty and dependence controls.
7. A competing model cannot explain the result equally well or better without the inner-core predictor.

Failure of any required gate prevents a positive coupling claim.

## 5. Core variables

| Variable | Symbol | Unit | Description |
|---|---|---|---|
| Earth angular velocity | Omega_E | rad/s | Earth rotation rate |
| Length of day anomaly | dLOD | ms | Deviation from reference LOD |
| Inner-core angular velocity perturbation | dOmega_IC | rad/s | Perturbation relative to reference inner-core rotation |
| Inner-core differential rotation | DeltaOmega_IC | rad/s | Inner-core rotation relative to mantle/reference frame |
| Inner-core deformation amplitude | D_IC | dimensionless | Normalized deformation parameter |
| Lag | tau | days or years | Candidate response delay |
| Geomagnetic observable | B_j | dataset-defined | Selected field component or secular-variation metric |

All transformations must be recorded in experiment manifests.

## 6. Data provenance

Every external dataset must have:

- Provider.
- Dataset name and version.
- Persistent identifier where available.
- Original URL or repository reference.
- Access date.
- License/terms.
- Time coverage.
- Sampling interval.
- Coordinate/reference frame.
- Units.
- Quality flags.
- Preprocessing operations.
- Hash of the acquired source file where legally and technically possible.

Raw external data must not be silently modified.

## 7. Data-source registry

The initial registry shall contain candidates for:

### Earth rotation

- IERS Earth-orientation products.
- LOD/UT1 series with documented reference conventions.

### Inner-core observations

- Published seismic observations of inner-core differential rotation.
- Published estimates of inner-core deformation or related observables where quantitatively usable.

### Geomagnetism

- Authoritative geomagnetic observatory or global-field products.
- Secular-variation observables with documented uncertainty.

A source is not admitted to an experiment until provenance and licensing metadata are recorded.

## 8. Data-ingestion contract

Each ingestion pipeline must implement:

```text
acquire
  -> validate
  -> parse
  -> normalize
  -> quality_control
  -> provenance_record
  -> analysis_dataset
```

The pipeline must fail closed when:

- Required columns are missing.
- Units are ambiguous.
- Time coordinates cannot be interpreted.
- Duplicate records violate the source specification.
- Quality flags indicate unusable observations.
- Provenance metadata are incomplete.

## 9. Inner-core state construction

The inner-core state must be constructed independently of the LOD target variable.

The preferred representation is a time-indexed state vector:

X_IC(t) = [
    DeltaOmega_IC(t),
    D_IC(t),
    optional_state_components(t)
]

Where optional components are only admitted if their observational basis and physical interpretation are documented.

No target leakage is permitted.

## 10. LOD experiments

### M0: Baseline

Use only independently justified baseline predictors and the historical target structure required by the forecasting task.

### M1: Inner-core

M0 + X_IC(t).

### M2: Lagged inner-core

M0 + X_IC(t - tau), with tau estimated only inside the training data.

### M3: Competing core model

M0 + independently justified outer-core or other control variables.

### M4: Coupled

M0 + inner-core + independently justified competing core variables.

## 11. Geomagnetic experiments

The same model-comparison logic applies.

The target must be defined before model fitting, including:

- observable,
- location or global basis,
- temporal resolution,
- forecast horizon,
- uncertainty representation.

No geomagnetic target may be used to construct the inner-core predictor.

## 12. Temporal validation

Random train/test splitting is prohibited for the primary experiments.

Use chronological evaluation.

Minimum protocol:

```text
training period
        |
        v
validation period
        |
        v
held-out test period
```

Hyperparameters and lag selection must be determined without access to the final test period.

A rolling-origin evaluation is preferred when sufficient observations exist.

## 13. Primary metrics

For continuous prediction, report at minimum:

- RMSE.
- MAE.
- Correlation.
- Skill relative to baseline.
- Explained variance where appropriate.
- Calibration/coverage for probabilistic predictions.

The primary decision metric must be declared before the final test is opened.

## 14. Statistical controls

The analysis must address:

- Autocorrelation.
- Non-stationarity.
- Common trends.
- Spectral leakage.
- Multiple comparisons.
- Parameter uncertainty.
- Measurement uncertainty.
- Sensitivity to filtering and smoothing.
- Potential time alignment errors.

Permutation or surrogate-data tests must preserve relevant temporal structure where necessary.

## 15. Robustness analysis

A positive result must be tested against reasonable alternatives for:

- Reference period.
- Filtering bandwidth.
- Smoothing method.
- Sampling interval.
- Lag range.
- Model specification.
- Missing-data treatment.

The analysis must report whether the conclusion changes.

## 16. Acceptance criteria

A positive LOD coupling claim requires:

1. Predefined baseline.
2. Statistically defensible out-of-sample improvement.
3. Improvement exceeding the registered practical threshold.
4. Robustness across predefined sensitivity tests.
5. No evidence that target leakage produced the result.
6. A physically plausible temporal relationship.
7. Better performance than or clear incremental value over the strongest competing model.

Exact numerical thresholds must be registered in the experiment manifest before final evaluation.

## 17. Rejection criteria

The hypothesis is rejected for the tested formulation if:

- No out-of-sample improvement is observed.
- Apparent skill disappears under temporal validation.
- The signal is explained by baseline/control variables.
- The effect is highly sensitive to arbitrary preprocessing.
- The inferred lag is unstable or physically implausible.
- The result cannot be reproduced from the locked experiment manifest.

Rejection applies to the tested formulation and dataset, not automatically to every possible inner-core coupling mechanism.

## 18. Uncertainty

Every reported effect must include uncertainty.

Where analytical uncertainty propagation is insufficient, use an appropriate resampling or probabilistic method.

Confidence or credible intervals must be reported with the exact method used.

## 19. Scientific audit trail

Every experiment must record:

```text
experiment_id
code_version
configuration_hash
dataset_identifiers
dataset_hashes
preprocessing_version
random_seed
model_specification
training_period
validation_period
test_period
metrics
uncertainty_method
result_artifacts
```

A result without this audit trail is not publication-grade.

## 20. Experiment manifest

Example:

```yaml
experiment_id: lod_m1_v001
target:
  variable: dLOD
  unit: ms

predictors:
  - DeltaOmega_IC

model:
  family: declared_in_code
  lag: fixed_or_training_selected

validation:
  method: rolling_origin
  final_test_locked: true

primary_metric:
  name: RMSE
  direction: lower_is_better

random_seed: 20260817

acceptance:
  threshold_declared_before_final_test: true
```

## 21. Planned publication outputs

The initial publication pipeline should produce:

1. Data provenance table.
2. Inner-core state reconstruction.
3. LOD observed-versus-predicted figure.
4. Temporal phase/lag analysis.
5. Model comparison table.
6. Robustness matrix.
7. Uncertainty summary.
8. Geomagnetic extension results.
9. Reproducibility manifest.

## 22. Reproducibility gates

Before a scientific result is labeled reproducible:

- Clean environment installation succeeds.
- All required data sources are resolvable.
- Provenance checks pass.
- Unit tests pass.
- Character-policy CI passes.
- Experiment executes from a clean checkout.
- Results match registered tolerances.
- Figures regenerate without manual intervention.

## 23. Scientific status labels

CoreSignal shall use these labels:

- `SPECIFIED`: protocol exists, no analysis yet.
- `INGESTED`: data acquired and validated.
- `EXECUTED`: experiment completed.
- `REPRODUCED`: independent clean execution matches registered outputs.
- `SUPPORTED`: predefined acceptance criteria passed.
- `NOT_SUPPORTED`: predefined acceptance criteria failed.
- `INVALIDATED`: methodological or data-quality failure prevents interpretation.

No `SUPPORTED` label may be assigned manually without an experiment artifact.

## 24. Scope boundary

CoreSignal does not claim to establish a causal mechanism merely from predictive association.

A predictive result is evidence for a testable relationship. Physical causation requires additional geophysical modeling and independent evidence.
