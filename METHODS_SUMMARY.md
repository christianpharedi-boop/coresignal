# CoreSignal Methods Summary

**Author:** Basie Pharedi  
**Release:** CoreSignal v0.3.0

## Purpose

CoreSignal tests whether independently derived inner-core observables improve out-of-sample prediction of Earth-rotation and geomagnetic variation. The framework is designed to falsify its motivating hypothesis rather than merely demonstrate it. A predictive association is not interpreted as causal evidence without additional justification.

## Scientific order of operations

CoreSignal follows a fail-closed sequence:

```text
source identification
  -> provenance verification
  -> immutable acquisition record
  -> parsing and quality control
  -> admission decision
  -> experiment-specific reconstruction
  -> predictor freeze
  -> matched control construction
  -> chronological evaluation
  -> robustness and surrogate controls
```

A blocked or unresolved upstream gate prevents downstream modeling. In particular, M1 cannot execute until the event/station reconstruction, archive coverage, waveform request semantics, waveform integrity, measurement definition, uncertainty rules, and overlap control are all resolved.

## M0 control

M0 is the LOD-only baseline. Its canonical specification is `experiments/m0_lod/m0_manifest.yaml`. It uses a chronological 70/15/15 train/validation/test split with no shuffling and includes persistence, 365-day seasonal persistence, and an autoregressive baseline. Inner-core and geomagnetic variables are prohibited. The final test interval is locked before any competing predictor is evaluated.

## M1 inner-core experiment

M1 is specified but blocked. Its provisional observable is an event-level PKIKP change score derived from independently reconstructed seismic observations. The observable is not admitted merely because a publication or station record exists. The archive must support the exact dated requests, the source bytes must be hashed, and the feature construction and uncertainty rules must be frozen before comparison with LOD.

M1 uses rolling-origin one-day-ahead evaluation on the common observed interval and requires a matched M0 control on that same interval. Planned negative and surrogate controls include phase-randomized and time-shifted inner-core signals and a negative-control seismic quantity.

## Data boundaries

The LOD dataset is admitted only through the provenance and rights-aware admission process. LOD must remain inaccessible to seismic feature construction. Analysis admission and redistribution rights are recorded separately; the former does not imply the latter.

## Interpretation rule

A result is scientifically supported only if all preregistered gates pass, the primary comparison meets the declared criterion, uncertainty and robustness checks are acceptable, and the result is independently reproduced. Otherwise the outcome is reported as not supported, inconclusive, or blocked according to the applicable manifest state.
