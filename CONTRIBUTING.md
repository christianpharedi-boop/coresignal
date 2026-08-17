# Contributing to CoreSignal

CoreSignal is a reproducibility-focused scientific research repository authored by Basie Pharedi. Contributions are welcome when they improve provenance, auditability, falsifiability, or reproducibility without weakening the fail-closed protocol.

## Scientific safeguards

Do not bypass an admission, reconstruction, archive-coverage, waveform-integrity, feature-freeze, or overlap-control gate. Do not introduce LOD access into seismic feature construction. Do not replace a blocked result with an inferred or simulated success. Changes that alter an experiment manifest, data schema, validation split, metric, or acceptance rule must explain the scientific consequence in the pull request.

## Language policy

The repository’s publication and machine-readable documentation pipeline currently enforces an English-only character policy for stable editorial processing. This is a project workflow decision, not a judgment about languages or contributors. Contributors should flag any legitimate author name, citation, or source title that conflicts with the check so the policy can be reviewed rather than bypassed silently.

## Data and rights

External data must retain source identity, acquisition metadata, byte size, SHA-256 hash, parsing status, quality status, and rights status. Analysis admission is tracked separately from redistribution permission. Do not commit raw external data unless redistribution rights are explicitly established.

## Validation before submission

Run the repository validators and the full test suite from the repository root:

```bash
python scripts/validate_provenance.py .
python scripts/check_english_only.py .
python -m unittest discover -s tests -v
```

If a dependency is missing, install the project with its test extra rather than relying on globally installed packages:

```bash
python -m pip install -e '.[test]'
```
