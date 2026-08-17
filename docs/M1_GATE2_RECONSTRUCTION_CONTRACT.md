# M1-Gate 2 — Observable reconstruction contract

Gate 2 is an evidence-reconstruction milestone, not an M1 modeling milestone. The acquisition manifest must be frozen before any waveform is downloaded or any candidate similarity metric is tested.

## Frozen sequence

```text
acquisition manifest
        ↓
source package acquisition
        ↓
SHA-256 hashing
        ↓
event/station/waveform reference verification
        ↓
LOD-independent reconstruction
        ↓
comparison of defensible candidate measurements
        ↓
freeze exactly one deterministic measurement
        ↓
freeze uncertainty model
        ↓
coverage and common-window audit
        ↓
matched M0 overlap control
```

The candidate feature must be constructed without inspecting LOD performance. Candidate measurement definitions may be compared only under criteria declared before any LOD result is opened. No raw waveform or derived feature may be committed to the public repository until its access basis and redistribution status are recorded.

## Gate decision

| Decision | Meaning |
|---|---|
| `ACCEPT` | A deterministic, uncertainty-bearing feature was independently reconstructed and has adequate common coverage for a named M1 experiment. |
| `DEFER` | The underlying source exists, but the feature definition, uncertainty model, provenance, or coverage is not yet defensible. |
| `REJECT` | The published evidence cannot be reconstructed reproducibly enough to support an M1 predictor. |

The current decision is **`DEFER`**. The Gate 2 acquisition manifest is frozen, but its source package, event/station tables, waveform references, hashes, measurement, uncertainty, and coverage fields remain pending.

## Coverage boundary

```text
admitted LOD:       1962-01-01 ───────────────────────────────── 2026-07-18
PKIKP candidate:    1991      ─────────────────────── 2023
common candidate:                         2016-11-11 ───── 2023
```

If reconstruction succeeds, the first supported design is `M1_overlap_2016_2023` with a newly generated matched one-day-ahead rolling M0 control over exactly the same observed dates. The original 2016–2026 M0 result remains immutable and must not be presented as the matched comparator for this overlap experiment.

## References

[1]: https://pmc.ncbi.nlm.nih.gov/articles/PMC11236701/ "Wang et al., Inner core backtracking by seismic waveform change reversals, Nature, 2024"

[2]: https://ds.iris.edu/ds/nodes/dmc/data/types/waveform-data/ "NSF SAGE / IRIS EarthScope waveform data services"

[3]: https://earthquakescanada.nrcan.gc.ca/stndon/CNSN-RNSC/index-en.php "Canadian National Seismograph Network"
