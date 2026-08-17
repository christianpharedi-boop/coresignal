# M1 Gate 2B.4 — Request semantics resolution

**Decision:** `REQUEST_SEMANTICS_VERIFIED`  
**Historical coverage:** `UNKNOWN`  
**Waveform request set:** `WAVEFORM_COVERAGE_PROBE_v001` remains immutable  
**Full acquisition:** Not authorized  
**Waveform analysis:** Prohibited  
**LOD accessed:** No

Gate 2B.4 resolved the semantics of the already-frozen request without changing the scientific population, stations, channels, or date windows.

## Verified semantics

| Check | Result |
|---|---|
| Network/station/location/channel | `IM.FB.SHZ` matches the authoritative ILAR/YKA station responses. |
| Temporal format | All 14 frozen requests use UTC ISO-8601 timestamps with `Z` suffix. |
| Temporal window | Each request begins 120 seconds before the event-origin time and ends 1,800 seconds after it. |
| EarthScope service | Current FDSN dataselect documentation endpoint responded HTTP 200. |
| Service version | `1.1.73`, HTTP 200. |
| Historical archive coverage | Still unknown. |
| Alternative search | None performed. |
| Waveform bytes | None retrieved during the semantic checks. |

The original request-set hash remains unchanged:

```text
WAVEFORM_COVERAGE_PROBE_v001
378a72e35379e3d33fc7b048ae378bb916e13563017b31d61487a3a2911e5f38
```

## Coverage rerun

Because request semantics were verified, the immutable v001 probe was rerun under a separate result path. The rerun produced the same outcome as the initial probe: all 14 requests returned HTTP 204 with zero response bytes. The versioned result is recorded in `reports/m1_gate2b3/probe_results_v001_semantics_verified.json`.

This leaves coverage `UNKNOWN`. The 204 response establishes only that the service returned no body for these exact requests; it does not establish that the historical observations are absent.

## Decision boundary

```text
REQUEST_SEMANTICS_VERIFIED
        ↓
immutable v001 coverage probe rerun
        ↓
COVERAGE_UNKNOWN
        ↓
WAVEFORM_REQUEST_SET_v001: NOT_FROZEN
        ↓
full acquisition: NOT_AUTHORIZED
        ↓
waveform analysis: PROHIBITED
```

No alternative channel, location, station, network, event, or date window was tested. `WAVEFORM_REQUEST_SET_v002` was not created because no semantic correction was required.

The next decision is therefore historical archive resolution, not scientific modeling. If an authoritative mechanism can establish coverage, the complete request set may be frozen. If not, the candidate remains deferred rather than being silently replaced.

## References

[1]: https://www.earthscope.org/news/earthscope-fdsnws-dataselect-service-has-moved-as-part-of-cloud-transition/ "EarthScope fdsnws-dataselect service migration notice"

[2]: https://service.earthscope.org/fdsnws/dataselect/1/ "EarthScope FDSN dataselect documentation"

[3]: https://service.earthscope.org/fdsnws/dataselect/1/version "EarthScope FDSN dataselect service version endpoint"
