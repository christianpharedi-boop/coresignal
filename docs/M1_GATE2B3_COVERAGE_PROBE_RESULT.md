# M1 Gate 2B.3 — Predeclared archive coverage probe

**Probe:** `WAVEFORM_COVERAGE_PROBE_v001`  
**Coverage status:** `COVERAGE_UNKNOWN`  
**Full acquisition:** Not authorized  
**Waveform analysis:** Prohibited  
**LOD accessed:** No

Gate 2B.3 tested a deterministic infrastructure-validation subset of the already established 143 event pairs. It did not select observations using LOD, waveform quality, or scientific outcome; it did not add stations, channels, events, or date windows; and it did not analyze the returned bytes.

## Frozen probe design

The request set was generated before archive responses were inspected. It contains 7 deterministic event-pair selections—earliest, latest, middle, and the first eligible pair in each of four temporal blocks—evaluated at both ILAR and YKA, for **14 requests** total. The request-set SHA-256 is:

```text
378a72e35379e3d33fc7b048ae378bb916e13563017b31d61487a3a2911e5f38
```

Each request used the frozen `IM.FB.SHZ` channel and a predeclared window from 120 seconds before the event origin to 1,800 seconds after it.

## Probe response

All 14 EarthScope FDSN dataselect requests returned HTTP **204 No Content** with zero response bytes. The runner recorded each request URL, response status, content type, response byte count, empty-response SHA-256, and retrieval timestamp. No response was promoted to a scientific observation.

A 204 response establishes that this particular request returned no body; it does not establish that the underlying waveform population is absent. Accordingly, the result is `COVERAGE_UNKNOWN`, not `COVERAGE_FAILED` and not `COVERAGE_ESTABLISHED`.

## Decision boundary

```text
COVERAGE_UNKNOWN
    ↓
WAVEFORM_REQUEST_SET_v001: NOT_FROZEN
    ↓
full waveform acquisition: NOT_AUTHORIZED
    ↓
waveform analysis: PROHIBITED
```

The result is a successful infrastructure audit of the request pathway only in the limited sense that the authoritative service responded to all 14 requests. It is **not** evidence that the requested waveform data were delivered, and it does not authorize full acquisition.

The next permissible action is to resolve why the frozen requests receive empty responses—such as request semantics, archive availability, or service requirements—using an authoritative, auditable method. No substitute station, channel, event, or date window may be introduced.

## References

[1]: https://www.earthscope.org/news/earthscope-fdsnws-dataselect-service-has-moved-as-part-of-cloud-transition/ "EarthScope fdsnws-dataselect service migration notice"

[2]: https://service.earthscope.org/fdsnws/dataselect/1/ "EarthScope FDSN dataselect service documentation"
