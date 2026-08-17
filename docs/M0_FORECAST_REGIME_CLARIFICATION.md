# M0 forecast-regime clarification

The published M0 result is valid as a **fixed-origin recursive AR(7) comparison**, but it is not a symmetric one-step-ahead comparison across all models.

| Model | Published M0 regime |
|---|---|
| Persistence | One-step prediction using the immediately preceding observed LOD value. |
| Seasonal persistence | One-step prediction using the observed value 365 days earlier. |
| AR(7) | Fit on the training segment once, then recursively forecast the full validation/test horizon without updating from observed values. |

The AR(7) result must therefore be interpreted narrowly: this specified recursive configuration did not generalize on the locked test interval. It is not evidence that autoregression as a model family is intrinsically ineffective.

For M1, CoreSignal adopts a **one-day-ahead rolling forecast contract** as the primary comparison regime. Every model must use only information available before the prediction day, and all candidate models must be evaluated under the same rolling-origin procedure. The original M0 result remains archived and must not be relabeled; a matched rolling M0 control must be generated before M1 is executed.

The original locked interval remains fixed. Changing the forecast regime creates a new explicitly named control run; it does not overwrite the published M0 result.
