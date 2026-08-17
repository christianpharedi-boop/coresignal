# Gate 2B.4 external source notes

The Gate 2B.4 semantic-resolution decision uses the following authoritative sources.

| Source | Relevant finding |
|---|---|
| https://www.earthscope.org/news/earthscope-fdsnws-dataselect-service-has-moved-as-part-of-cloud-transition/ | EarthScope states that its fdsnws-dataselect service moved from `service.iris.edu` to `service.earthscope.org` during the cloud transition and identifies the new endpoint as the primary miniSEED service. |
| https://service.earthscope.org/fdsnws/dataselect/1/ | The current EarthScope dataselect documentation endpoint responded HTTP 200 during the Gate 2B.4 diagnostic. |
| https://service.earthscope.org/fdsnws/dataselect/1/version | The current service version endpoint responded HTTP 200 with version `1.1.73`. |
| https://ds.iris.edu/ds/nodes/dmc/data/types/waveform-data/ | NSF SAGE documentation describes the EarthScope archive as a repository of waveform time-series data and identifies standard waveform formats. |
| https://ds.iris.edu/ds/newsletter/vol21/no3/513/fdsn-availability-web-service/ | IRIS documents the FDSN availability service and explains that the legacy `irisws-availability` service was taken offline in favor of the FDSN implementation. |
| https://www.fdsn.org/webservices/ | FDSN defines separate station, dataselect, event, and availability web-service specifications. |

Gate 2B.4 did not retrieve waveform bytes. It checked only the frozen `IM.FB.SHZ` identity, UTC request-window formatting, station-response identity, and service documentation/version responses. Historical coverage remains unknown.
