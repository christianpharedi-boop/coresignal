# CoreSignal M0 LOD baseline result

**Experiment:** `m0_lod_baseline_v001`  
**Protocol:** `0.4.0`  
**Status:** `EXECUTED`  
**Interpretation:** Control experiment only; no inner-core or geomagnetic variables were used.

## Input and split

The run used the exact processed LOD snapshot declared by the manifest. The processed-input SHA-256 is `a8be254327222ab0c98b923d15aaea8464688f3fee26dfd4bea08b1ab00d5c2b`, and the source snapshot SHA-256 is `0a9592923561528b8e1dcb9ea3628583f9687a2424ad82d3f62d2a71c819a8de`. The input contains 23,575 daily rows from 1962-01-01 through 2026-07-18.

The chronological split is 70% training, 15% validation, and 15% locked test. The test interval contains 3,537 observations from 2016-11-11 through 2026-07-18. The autoregressive order was fixed at 7 before the test interval was opened.

## Locked test metrics

| Model | RMSE (ms) | MAE (ms) | Mean error (ms) | Correlation | Skill vs persistence |
|---|---:|---:|---:|---:|---:|
| Persistence | 0.147806 | 0.124215 | 0.000387 | 0.976758 | 0.000000 |
| Seasonal persistence, 365-day | 0.594228 | 0.487992 | 0.128487 | 0.689693 | -3.020333 |
| Autoregressive, order 7 | 1.818159 | 1.666926 | 1.649184 | -0.499265 | -11.301011 |

Persistence is the strongest of the three tested baselines on this locked interval. The seasonal and recursive autoregressive baselines do not improve on persistence under this protocol.

## Scientific boundary

This is an **M0 control result**, not evidence for or against an inner-core mechanism. It establishes a baseline that any future inner-core-augmented model must beat under the same locked evaluation design.

The complete machine-readable record is [`m0_result.json`](m0_result.json). The execution revision is `950f9a5e99409e900f0b4a5d7272b358cfc366c6`.
