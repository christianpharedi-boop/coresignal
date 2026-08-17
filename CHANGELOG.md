# Changelog

## 0.3.0 - 2026-08-17

CoreSignal v0.3 establishes the data-acquisition and scientific-provenance layer.

### Changed

- Dataset admission now separates `analysis_admitted` from `redistribution_pending`; analysis rights and redistribution rights are tracked independently.
- The canonical M0 specification is `experiments/m0_lod/m0_manifest.yaml`; the older `experiments/lod/lod_m0_baseline.yaml` is retained only as a superseded compatibility record.
- IERS C04 parsing is centralized in `src/rotation/iers_c04.py` and used by both LOD command-line entry points.

### Added

- Machine-readable data-source registry.
- Dataset admission state machine.
- Provenance validation.
- SHA-256 integrity records.
- Immutable raw-data policy.
- Earth-rotation/LOD ingestion contract.
- LOD quality-control framework.
- Reproducible data-inventory report.
- LOD benchmark experiment scaffold.
- Provenance and ingestion tests.
- CI validation for provenance metadata.

### Scientific boundary

v0.3 acquires and validates data infrastructure. It does not claim an inner-core/LOD relationship.
