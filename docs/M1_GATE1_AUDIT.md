# M1-Gate 1 — Inner-core observable audit

**Audit status:** `DEFERRED_PENDING_RECONSTRUCTION`  
**Candidate:** Wang et al. (2024), event-level PKIKP waveform-change observable from South Sandwich Islands repeating earthquakes observed at ILAR and YKA.

## Provisional evidence

The primary study reports 121 earthquakes from 1991–2023, 16 multiplets, 143 repeating-event pairs, and 200 waveform-pair comparisons using PKIKP observations at the ILAR and YKA arrays. The study describes the observable as waveform change and reversal in inner-core-penetrating PKIKP waves, not as a directly observed scalar rotation-rate series.[1]

The paper identifies the underlying digital waveform sources through IRIS and the Canadian National Seismograph Network, while some analogue COL waveforms were manually digitized. IRIS/EarthScope documents that its Data Management Center archives global waveform time series in standard seismological formats and provides data-access services.[1] [2]

## Gate-1 checklist

| Requirement | Current finding | Gate status |
|---|---|---|
| Exact source dataset | Paper and supplementary event/pair tables identified; exact downloadable table assets and versioned hashes still need to be captured. | Open |
| Event IDs | Study reports 121 events, 42 locations, and event-pair indices, but the repository has not yet imported and hashed the exact event table. | Open |
| Station IDs | ILAR and YKA are identified; exact channels, station metadata, array processing, and availability windows remain to be frozen. | Open |
| Waveform archive | IRIS/EarthScope and CNSN are cited as sources; exact waveform requests and returned bytes have not been reconstructed. | Open |
| PKIKP measurement | The published analysis uses waveform comparison and visual similarity categories, with some subjective scoring. A deterministic CoreSignal metric has not been selected. | Open |
| Uncertainty | The paper discusses noise, source-time-function, station, and path complications, but an executable per-observation uncertainty field has not been defined. | Open |
| Observation dates | Candidate coverage is 1991–2023, with 12 newer events added through 2023. | Provisional pass |
| LOD overlap | The candidate overlaps the M0 interval from 2016-11-11 through 2023, but not through the M0 endpoint of 2026-07-18. | Overlap only |
| LOD-independent construction | The underlying seismic feature can in principle be constructed without using LOD, but the event-selection and feature-reduction pipeline has not yet been independently reconstructed. | Open |
| Immutable input hash | No CoreSignal hash exists yet for the supplementary tables, waveform requests, or derived feature. | Fail-closed |
| Full versus overlap experiment | Full M0 comparison is unsupported by current coverage; only an explicitly named overlap experiment is currently plausible. | Decision pending |

## Decision

The candidate is **not rejected**, because the study provides a scientifically relevant observable and identifies plausible underlying waveform archives. It is also **not accepted as the M1 predictor**, because reproducibility-critical event, station, waveform, metric, uncertainty, and hash details have not yet been independently reconstructed.

The current M1 state remains:

```text
SPECIFIED
execution_gate: blocked_pending_observable_and_overlap_control
Gate 1: DEFERRED_PENDING_RECONSTRUCTION
```

If reconstruction succeeds, the likely primary design is `M1_overlap_2016_2023`, paired with a newly generated one-day-ahead rolling M0 control over exactly the same observed interval. It must not be described as outperforming the original 2016–2026 M0 benchmark.

## Required next audit actions

The next audit must obtain the exact supplementary tables, record their URLs and hashes, resolve event identifiers and origin times, freeze ILAR/YKA station and channel metadata, specify a deterministic waveform-change score, define uncertainty and missingness rules, and hash the resulting feature table. Only then can the candidate be accepted or rejected for M1.

## References

[1]: https://pmc.ncbi.nlm.nih.gov/articles/PMC11236701/ "Wang et al., Inner core backtracking by seismic waveform change reversals, Nature, 2024"

[2]: https://ds.iris.edu/ds/nodes/dmc/data/types/waveform-data/ "NSF SAGE / IRIS EarthScope waveform data services"
