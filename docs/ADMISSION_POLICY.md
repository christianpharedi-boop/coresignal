# CoreSignal data admission policy

CoreSignal separates **scientific usability** from **redistribution rights**. A dataset may be downloaded, hashed, parsed, and quality-checked for a controlled research workflow without being cleared for redistribution in the public repository.

## Status model

```text
QUALITY_CHECKED
      |
      +--> ANALYSIS_ADMITTED
      |       The exact snapshot may be used by the controlled analysis workflow.
      |
      +--> REDISTRIBUTION_CLEARED
              The rights holder, licence, or authoritative terms permit redistribution.
```

A source may be `ANALYSIS_ADMITTED / REDISTRIBUTION_PENDING`. This means the scientific pipeline may consume the exact locally retained snapshot under project policy, while the raw and derived bytes must remain outside the public repository until rights are verified.

`ADMITTED` is reserved for a complete provenance record whose intended use, integrity, quality, and rights gates are all satisfied. The legacy single-state label must not be used to imply redistribution permission when only analysis use has been established.

## EOP 20u24 C04 snapshot

The final v0.3 validation artifact records the IERS EOP 20u24 C04 snapshot as `QUALITY_CHECKED_PENDING_LICENSE`, with `ANALYSIS_ADMITTED` and `REDISTRIBUTION_PENDING`. The raw file and processed output are therefore not committed to the public repository. Their SHA-256 values and validation results are retained in the final metadata reports.

No licence is inferred from the fact that IERS publishes a download endpoint. A redistribution clearance requires an explicit rights statement, licence, or authoritative terms from IERS or the relevant rights holder.
