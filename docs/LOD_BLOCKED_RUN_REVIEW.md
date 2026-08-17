# Review of the blocked LOD v0.3 run

## Assessment

The blocked result is scientifically correct. Metadata verification is not raw-data acquisition, and the run appropriately avoids claiming a hash, parsed record count, quality-control result, processed dataset, or `ADMITTED` status without the raw file.

The artifact nevertheless has several implementation shortcomings that should be corrected before the next execution.

| Area | Shortcoming | Required safeguard |
|---|---|---|
| Input contract | The artifact expects `data/raw/eopc04.1962-now`, while the repository’s v0.3 layout uses a source-specific directory. | Use one canonical path from the manifest and resolve it relative to the repository root. |
| Parser strictness | Malformed or short data lines are silently skipped. A partially parsed file could therefore appear valid. | Count and report every malformed data line, and fail closed if any occur. |
| Completeness | The runner does not compare parsed rows with the IERS-reported count, declared date range, or expected source version. | Require expected record count, first date, last date, and product identity from the locked manifest. |
| Temporal integrity | Duplicate dates are checked, but MJD/date agreement, ordering, one-day cadence, and explicit missing dates are not fully enforced. | Validate calendar date, MJD consistency, monotonic ordering, and exact one-day cadence. |
| Numeric integrity | The parser checks only LOD range and negative formal error. It does not reject non-finite values, sentinels, missing fields, or invalid date/MJD values. | Reject all non-finite, sentinel, missing, and physically invalid required fields. |
| Admission logic | `admitted` is assigned when local parser errors are absent, without checking the complete provenance record, source hash against the manifest, licensing state, or expected metadata. | Make admission a separate final gate requiring all provenance and completeness checks. |
| Failure artifacts | The runner returns blocked status when the raw file is absent but does not always emit a machine-readable blocked report. | Emit a deterministic report for every run, including blocked and rejected states. |
| Output safety | The runner writes processed output before the final status is known. | Write processed data only after all gates pass; otherwise retain only a rejection/blocked report. |
| Test coverage | The artifact has no negative fixtures for malformed lines, wrong headers, MJD mismatch, gaps, count mismatch, or missing raw data. | Add small local fixtures and tests for each fail-closed gate. |

## Version distinction

The artifact identifies **EOP 20u24 C04**, whereas the earlier repository inventory used an older **EOP 20 C04** file. These must not be merged under one provenance identity. The exact product version, source URL, header, release metadata, hash, and coverage must remain distinct records.

## Recommended next state

Keep the current run as `metadata_verified_acquisition_blocked`. Do not mark the source `ACQUIRED`, `QUALITY_CHECKED`, or `ADMITTED` until the exact EOP 20u24 raw file is placed at the manifest-defined path and the strict parser/QC runner passes all locked expectations.
