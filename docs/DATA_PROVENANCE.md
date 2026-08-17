# Data Provenance Standard

Every dataset admitted to CoreSignal must have a provenance record.

Required fields:

- provider
- dataset
- version
- persistent identifier
- source reference
- access date
- license
- time coverage
- sampling interval
- units
- coordinate/reference frame
- quality flags
- preprocessing
- source-file hash

Raw data must remain immutable once admitted.

Derived datasets must contain a machine-readable pointer to the raw-data provenance record and the transformation code version.
