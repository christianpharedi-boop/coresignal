# CoreSignal

CoreSignal is a reproducible computational research framework for testing whether independently inferred inner-core dynamics have predictive power for Earth-rotation and geomagnetic observations.

> **CoreSignal is designed to falsify its motivating hypothesis, not merely demonstrate it.**

A predictive association must not automatically be interpreted as causation. A causal claim requires additional geophysical modeling and independent evidence.

## Research question

Can time-varying inner-core differential rotation and deformation be quantitatively connected to measurable variations in Earth's length of day (LOD) and geomagnetic secular variation?

## Scientific protocol

The current protocol is **v0.2.0**. It defines falsifiable hypotheses H0–H4, explicit positive-result gates, formal variables and units, data-provenance requirements, an ingestion contract, LOD and geomagnetic experiment families, chronological and rolling-origin validation, anti-leakage requirements, uncertainty and robustness frameworks, preregistered acceptance and rejection criteria, machine-readable experiment manifests, and reproducibility gates.

The protocol is documented in [`docs/SCIENTIFIC_SPECIFICATION_v0.2.md`](docs/SCIENTIFIC_SPECIFICATION_v0.2.md). Supporting documents define the [data-provenance standard](docs/DATA_PROVENANCE.md), [experiment protocol](docs/EXPERIMENT_PROTOCOL.md), and [scientific status labels](docs/SCIENTIFIC_STATUS.md).

## Repository status

The repository currently contains a **specified protocol and manifest scaffolding**. It does not claim a scientific result. The next milestone is **v0.3: Data Acquisition & Provenance**, which will admit authoritative Earth-rotation, seismic/inner-core, and geomagnetic data only after provenance, licensing, units, quality flags, and source hashes have been recorded.

## Character policy

All repository-controlled source code, documentation, notebooks, manuscript source, configuration, metadata, and text-bearing figure assets must use English and standard scientific notation.

CI rejects Chinese, Japanese, Korean, CJK punctuation, fullwidth CJK forms, and the CJK Unicode blocks defined in `scripts/check_english_only.py`.

The scanner covers source code, documentation, notebooks, manuscript files, vector figures, and decodable figure metadata. Raster pixels are not OCR-scanned by CI; authoritative figure labels must also exist in text or vector source.

## Local checks

```bash
python scripts/check_english_only.py .
python scripts/validate_manifests.py .
python -m unittest discover -s tests -v
```

## Author and citation

CoreSignal is authored by **Basie Pharedi**. Please see [`CITATION.cff`](CITATION.cff) for citation metadata.
