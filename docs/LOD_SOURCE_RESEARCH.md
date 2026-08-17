# First LOD source research record

## Candidate source

The first candidate for CoreSignal LOD ingestion is the **IERS EOP 14 C04 series**, published by the IERS Earth Orientation Centre. The official IERS product metadata identify it as a daily ASCII Earth-orientation series containing date, MJD, pole coordinates, UT1-UTC, LOD, celestial-pole offsets, and associated uncertainties.

The metadata page states that the series is sampled at a **1-day interval**, is consistent with ITRF2014, and includes LOD in seconds with an LOD uncertainty field. It also identifies the official source directory and the C04 guide/update documentation.

## References

1. [IERS Earth orientation data](https://www.iers.org/iers/en/dataproducts/earthorientationdata/eop)
2. [IERS EOP 14 C04 product metadata](https://datacenter.iers.org/productMetadata.php?id=222)
3. [IERS EOP 14 C04 available versions](https://datacenter.iers.org/availableVersions.php?id=222)
4. [IERS C04 source directory](https://hpiers.obspm.fr/iers/eop/eopc04/)

## Acquisition decision

Acquire the official ASCII C04 file only after recording the exact filename/version, access date, license/distribution terms, source URL, and SHA-256 hash in `data/registry.yaml`. Raw data must remain outside version control unless redistribution terms explicitly permit committing it.

## Acquired file verification

The downloaded file `eopc04.1962-now` identifies itself in its header as **EOP (IERS) 20 C04**, consistent with ITRF 2020, sampled at 0h UTC. Its header declares daily fields for date, MJD, x/y, UT1-UTC, dX/dY, pole-coordinate rates, LOD, and formal errors including LOD error.

The current directory listing exposes `eopc04.1962-now` and reports a same-day update timestamp. The IERS version-metadata endpoint confirms that the EOP 20 C04 format is ASCII, daily, includes LOD in seconds and LOD formal error, and is published by the IERS Earth Orientation Centre. The acquired file itself is treated as the authoritative artifact for exact byte-level provenance; metadata are recorded against the actual header and URL rather than the older EOP 14 C04 product page.

5. [IERS EOP 20 C04 version metadata](https://datacenter.iers.org/versionMetadata.php?filename=latestVersionMeta/234_EOP_C04_20.62-NOW234.txt)
6. [Current IERS C04 directory listing](https://hpiers.obspm.fr/eoppc/eop/eopc04/)
