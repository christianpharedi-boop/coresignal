# CoreSignal

CoreSignal is a reproducible computational research framework for testing whether independently inferred inner-core dynamics have predictive power for Earth-rotation and geomagnetic observations.

## Current release

**v0.3.0 - Data Acquisition & Scientific Provenance**

v0.2 defined the scientific protocol. v0.3 establishes the controlled data boundary required before modelling.

## Falsification-first principle

CoreSignal is designed to falsify its motivating hypothesis, not merely demonstrate it.

No scientific experiment may execute against a dataset whose provenance is incomplete or whose admission checks have failed.

## Dataset lifecycle

```text
PLANNED
  -> DISCOVERED
  -> METADATA_VERIFIED
  -> ACQUIRED
  -> HASHED
  -> PARSED
  -> QUALITY_CHECKED
  -> ADMITTED
```

Only `ADMITTED` datasets may be used by scientific experiments.

## v0.3 first target

The first operational target is Earth rotation, specifically length-of-day (LOD), because it provides a clean first benchmark before adding inner-core predictors and geomagnetic targets.

The underlying research question remains whether time-varying inner-core differential rotation and deformation can be quantitatively connected to measurable variations in LOD and geomagnetic secular variation. The complete v0.2 protocol is in [`docs/SCIENTIFIC_SPECIFICATION_v0.2.md`](docs/SCIENTIFIC_SPECIFICATION_v0.2.md), with supporting [experiment](docs/EXPERIMENT_PROTOCOL.md), [provenance](docs/DATA_PROVENANCE.md), and [scientific-status](docs/SCIENTIFIC_STATUS.md) documentation.

## Local validation

```bash
python scripts/validate_provenance.py .
python scripts/check_english_only.py .
python -m unittest discover -s tests -v
```

## Data policy

Raw external data are never silently edited. Derived datasets must retain a provenance link to their raw source and transformation version.

Do not commit externally licensed raw datasets unless their terms explicitly permit redistribution.

## Author and citation

CoreSignal is authored by **Basie Pharedi**. Citation metadata are maintained in [`CITATION.cff`](CITATION.cff).
