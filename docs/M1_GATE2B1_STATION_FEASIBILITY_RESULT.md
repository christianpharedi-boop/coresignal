# M1 Gate 2B.1 — Station metadata resolution and path feasibility

**Decision:** `DEFER_RECONSTRUCTION`  
**Waveform retrieval:** `NOT_AUTHORIZED`  
**LOD accessed:** No  
**Waveform bytes accessed:** No

Gate 2B.1 executed only the frozen IRIS station metadata query and evaluated date-specific station/channel operational coverage against the 143 reconstructed event pairs. It did not request waveform bytes or inspect LOD.

## Resolved station inventory

| Network | Station | Location | Channel | Latitude | Longitude | Elevation | Operational start | Response hash |
|---|---|---|---|---:|---:|---:|---|---|
| IM | ILAR | FB | SHZ | 64.771400 | -146.886597 | 419.0 m | 1980-01-01 | `ac343629c718474e321a52360e0c9881da257dfb8bce46a05d878ee2f3dd0397` |
| IM | YKA | FB | SHZ | 62.493198 | -114.605301 | 197.0 m | 1989-01-25 | `6c7ee6743fb8a708816b63fcae16f88f59ebdd352711d0c4f9cbf9539e9b30f6` |

Both responses were obtained from the authoritative [IRIS FDSN station service](https://service.iris.edu/fdsnws/station/1/query?station=ILAR&level=channel&format=text) with the corresponding station parameter. The responses include instrument descriptions, scale, sample rate, and channel metadata. Their original text bytes are preserved under `data/m1_gate2/station_inventory`.

## Per-pair feasibility

The resolver evaluated both ILAR and YKA for every one of the 143 event pairs, producing **286 station-pair feasibility records**. For both stations, the metadata start date precedes every event origin date in the reconstructed 1991–2023 population. Therefore:

| Check | Result |
|---|---:|
| Event pairs evaluated | 143 |
| Station-array paths evaluated | 286 |
| Operational at event A | 286 / 286 |
| Operational at event B | 286 / 286 |
| Channel available by station metadata | 286 / 286 |
| Archive-level waveform coverage | Unknown |
| PKIKP request feasibility | Deferred |

This establishes **station metadata coverage**, not archive waveform availability. The IRIS availability endpoint attempted for date-specific archive coverage returned HTTP 410 Gone. No alternative endpoint was substituted, and no claim was made that the waveform archive contains every requested record.

## Authorization decision

```text
EVENT_RECONSTRUCTION: PASS
PAIR_RECONSTRUCTION: PASS
STATION_METADATA: PASS
ARCHIVE_COVERAGE: UNKNOWN
WAVEFORM_REQUEST_SET: NOT_FROZEN
WAVEFORM_RETRIEVAL: NOT_AUTHORIZED
DECISION: DEFER_RECONSTRUCTION
```

The next action is not waveform retrieval. The archive-coverage method must first be resolved, after which an exact event × station × channel request set can be constructed, hashed, and reviewed. Until then, the Gate 2B.1 decision remains deferred.

## References

[1]: https://service.iris.edu/fdsnws/station/1/query?station=ILAR&level=channel&format=text "IRIS FDSN station metadata query for ILAR"

[2]: https://service.iris.edu/fdsnws/station/1/query?station=YKA&level=channel&format=text "IRIS FDSN station metadata query for YKA"

[3]: https://ds.iris.edu/ds/nodes/dmc/data/types/waveform-data/ "NSF SAGE / IRIS waveform data services"
