# G2A_SOURCE_PACKAGE_VERIFIED

**Verification event:** 2026-08-17T18:11:11Z  
**Publication:** Wang et al. (2024), DOI `10.1038/s41586-024-07536-4`  
**Next gate:** Gate 2B — Event/Station Reconstruction

Gate 2A-1 acquired and identity-verified two static supplementary source files and two immutable query-specification objects. No waveform bytes were retrieved, no table was normalized, no event was discarded, no LOD observation was inspected, and no PKIKP metric was calculated.

## Source-package records

| Record | Object boundary | Original filename or identity | Bytes | SHA-256 | Status |
|---|---|---|---:|---|---|
| `gate2a_file_0001` | Wang supplementary workbook; Extended Data Table 1 event table | `41586_2024_7536_MOESM1_ESM.xlsx` | 31,048 | `89468776ba9a85af29537c37665552582d454e85e3c898312b79b7776843f47e` | `VERIFIED` |
| `gate2a_file_0002` | Same workbook; Extended Data Table 2 event-pair table | `41586_2024_7536_MOESM1_ESM.xlsx` | 31,048 | `89468776ba9a85af29537c37665552582d454e85e3c898312b79b7776843f47e` | `VERIFIED` |
| `gate2a_file_0003` | Immutable station metadata query definition for ILAR/YKA | `ilar_yka_station_metadata_query.yaml` | 538 | `42248b5f75021943d9dae130494a02aaeee347f42e14ea64f01a30b86c5bcf3d` | `VERIFIED` |
| `gate2a_file_0004` | Immutable future PKIKP waveform query definition | `pkikp_waveform_query_spec.yaml` | 874 | `c54412417b4a4fb424038022f7122e33ebd09b9e76cd588c0a7a74b981ef98a6` | `VERIFIED` |

The supplementary PDF was also preserved locally as a source-package companion object: `41586_2024_7536_MOESM2_ESM.pdf`, 3,642,087 bytes, SHA-256 `c33ca6dc3402d1b485267451935fa9c12df83dba206869d67ba8c75aa264f899`. It is not a separate declared required object because it is supplementary narrative material rather than the event/pair/station/waveform-reference object boundary. Its source URL is the corresponding Springer static-content endpoint.

## Rights boundary

The article is published under CC BY 4.0, subject to any third-party-material qualifications and attribution requirements. The ledger records analysis and redistribution rights separately. The source files remain outside the public repository; the repository contains provenance metadata and query specifications, not the acquired supplementary bytes.

The query specifications are CoreSignal-authored immutable records. They establish future archive-request identity; they do **not** represent retrieved waveform data and do not grant rights to archive-returned bytes.

## Gate status

```text
G2A_SOURCE_PACKAGE_VERIFIED
    ↓
Gate 2B — Event/Station Reconstruction
```

M1 modeling remains blocked. Gate 2B must reconstruct the published event/pair population and resolve the station/query boundary before any waveform retrieval or measurement construction begins.

## References

[1]: https://static-content.springer.com/esm/art%3A10.1038%2Fs41586-024-07536-4/MediaObjects/41586_2024_7536_MOESM1_ESM.xlsx "Wang et al. supplementary workbook"

[2]: https://static-content.springer.com/esm/art%3A10.1038%2Fs41586-024-07536-4/MediaObjects/41586_2024_7536_MOESM2_ESM.pdf "Wang et al. supplementary PDF"

[3]: https://creativecommons.org/licenses/by/4.0/ "Creative Commons Attribution 4.0 International License"
