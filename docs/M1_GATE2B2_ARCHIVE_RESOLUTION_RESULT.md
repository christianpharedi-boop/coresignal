# M1 Gate 2B.2 — Authoritative archive resolution

**Decision:** `DEFER_RECONSTRUCTION`  
**Waveform request set:** `NOT_FROZEN`  
**Waveform retrieval:** `NOT_AUTHORIZED`  
**LOD accessed:** No  
**Waveform bytes accessed:** No

Gate 2B.2 tested only authoritative archive mechanisms associated with the frozen Gate 2 source contract. It did not change the 121-event or 143-pair population, substitute stations, broaden date windows, inspect LOD, or retrieve waveform bytes.

## Resolution results

| Provider/mechanism | Authority | Request semantics | Response | Coverage | Decision |
|---|---|---|---|---|---|
| EarthScope FDSN dataselect | Verified | Verified from current EarthScope documentation | HTTP 200; version `1.1.73` | Unknown because no data request was executed | Defer |
| Legacy IRIS FDSN availability | Verified as documented legacy mechanism | Verified by FDSN/IRIS documentation | HTTP 410 | Endpoint failure; does not prove absent data | Defer |
| CNSN archive page | Provider authority verified | Unknown | HTTP 200 | Unknown; no reproducible date-specific waveform request semantics established | Defer |

The EarthScope migration notice states that `service.earthscope.org/fdsnws/dataselect/1` is the current primary miniSEED service and that the former IRIS location redirects to it.[1] The NSF SAGE documentation identifies the archive as a waveform-data repository.[2] The FDSN documentation defines dataselect and availability as separate services, while the historical IRIS notice documents the availability service and its deprecation of the old `irisws-availability` endpoint.[3] [4]

The HTTP 410 from the legacy availability endpoint is retained as immutable failure evidence. It is not treated as evidence that ILAR or YKA waveforms are absent.

## Request-set boundary

The frozen PKIKP query specification has SHA-256:

```text
c54412417b4a4fb424038022f7122e33ebd09b9e76cd588c0a7a74b981ef98a6
```

`WAVEFORM_REQUEST_SET_v001` has **not** been created or hashed. It cannot be frozen until an archive mechanism establishes authority, request semantics, and date-specific coverage for the unchanged event × station × channel population.

The current chain is therefore:

```text
121 events
  ↓
143 pairs
  ↓
station metadata
  ↓
station/date feasibility
  ↓
archive authority: partial
  ↓
archive coverage: unknown
  ↓
waveform request set: not frozen
  ↓
waveform retrieval: blocked
```

## Gate decision

The result is `DEFER_RECONSTRUCTION`, not `REJECT_CANDIDATE`. The archive mechanisms tested here did not establish coverage, but their failures do not establish that the underlying observations cannot be reconstructed. A future archive-resolution attempt may proceed only by resolving the current service semantics or documenting an authoritative alternative without changing the scientific population.

## References

[1]: https://www.earthscope.org/news/earthscope-fdsnws-dataselect-service-has-moved-as-part-of-cloud-transition/ "EarthScope fdsnws-dataselect service migration notice"

[2]: https://ds.iris.edu/ds/nodes/dmc/data/types/waveform-data/ "NSF SAGE waveform data documentation"

[3]: https://ds.iris.edu/ds/newsletter/vol21/no3/513/fdsn-availability-web-service/ "IRIS FDSN availability web-service notice"

[4]: https://www.fdsn.org/webservices/ "FDSN Web Services specifications"
