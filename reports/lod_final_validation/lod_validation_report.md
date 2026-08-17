# CoreSignal v0.3 LOD Validation and Admission Report

**Run:** 0.3.0-run.2  
**Date:** 2026-08-17  
**Dataset:** IERS EOP 20u24 C04, dX/dY, 0h UTC, 1962-now

## Acquisition

The exact EOP 20u24 C04 raw file was successfully downloaded from the IERS C04 20u24 data directory and preserved byte-for-byte at:

`data/raw/eopc04_20u24.1962-now`

Raw byte size: **5,163,654 bytes**  
SHA-256: **`0a9592923561528b8e1dcb9ea3628583f9687a2424ad82d3f62d2a71c819a8de`**

## Parse

- Data records: **23,575**
- First date: **1962-01-01**
- Last date: **2026-07-18**
- First MJD: **37665.00**
- Last MJD: **61239.00**
- Malformed/unparseable data lines: **0**

## Quality-control gates

| Gate | Result |
|---|---|
| All data lines parsed | PASS |
| 21 fields per record | PASS |
| MJD/calendar date agreement | PASS |
| Dates strictly increasing | PASS |
| One-day cadence | PASS |
| Duplicate dates | PASS — 0 |
| Non-finite numeric values | PASS — 0 |
| Negative LOD formal errors | PASS — 0 |
| LOD integrity bounds (-0.01, +0.01) s | PASS |
| Complete processed LOD output | PASS |

LOD range: **-0.0016508 to 0.0043550 s**  
LOD formal-error range: **0.0000062 to 0.0014310 s**

## Important provenance observation

The IERS version-metadata page identifies the 20u24 C04 product, its daily 0h UTC structure, and the same 23,575 records from 1962-01-01 through 2026-07-18 for the current snapshot. The raw header uses the broader `EOP (IERS) 20 C04` wording, while the catalogue identifies the release family as `20u24`; CoreSignal preserves both the exact header and catalogue identity rather than silently normalizing the product name.

CoreSignal treats the **downloaded bytes plus their SHA-256** as the immutable acquisition snapshot.

## Admission

Scientific parsing and QC: **PASS**.

However, the repository's admission rule requires a completed licence/provenance gate. The IERS pages identify the provider and distribute the data, but no explicit machine-readable redistribution licence was verified during this run.

Therefore the scientifically correct final state is:

# `QUALITY_CHECKED_PENDING_LICENSE`

It is **not yet `ADMITTED`**.

The dataset may be consumed by the controlled analysis workflow only under the separate `ANALYSIS_ADMITTED` policy. It must not be redistributed, and it must not receive the combined `ADMITTED` status, until the repository's redistribution-rights policy is satisfied.

## Reproducibility

Raw SHA-256:
`0a9592923561528b8e1dcb9ea3628583f9687a2424ad82d3f62d2a71c819a8de`

Processed LOD SHA-256:
`a8be254327222ab0c98b923d15aaea8464688f3fee26dfd4bea08b1ab00d5c2b`

The raw file is retained unchanged; the processed file contains only date, MJD, LOD, and LOD formal error.
