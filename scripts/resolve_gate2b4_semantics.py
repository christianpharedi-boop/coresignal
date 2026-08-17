"""Resolve Gate 2B.4 request semantics without waveform retrieval or analysis."""
from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parents[1]
REQUESTS = ROOT / "reports/m1_gate2b3/probe_requests.json"
STATION_DIR = ROOT / "data/m1_gate2/station_inventory"
OUTPUT = ROOT / "reports/m1_gate2b4/request_semantics.json"

SERVICE_DOCS = "https://service.earthscope.org/fdsnws/dataselect/1/"
SERVICE_VERSION = "https://service.earthscope.org/fdsnws/dataselect/1/version"
STATION_URL = "https://service.iris.edu/fdsnws/station/1/query?station={station}&level=channel&format=text"


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def fetch(url: str) -> dict:
    try:
        request = Request(url, headers={"User-Agent": "CoreSignal-Gate2B4/1.0"})
        with urlopen(request, timeout=60) as response:
            body = response.read()
            return {"url": url, "http_status": response.status, "response_bytes": len(body), "response_sha256": sha256(body), "content_type": response.headers.get("Content-Type")}
    except Exception as exc:
        return {"url": url, "http_status": getattr(exc, "code", None), "response_bytes": 0, "response_sha256": sha256(b""), "content_type": None, "error": str(exc)}


def main() -> int:
    request_doc = json.loads(REQUESTS.read_text(encoding="utf-8"))
    request_hash = sha256(REQUESTS.read_bytes())
    request_checks = []
    for request in request_doc["requests"]:
        params = request["request_parameters"]
        start = datetime.fromisoformat(params["starttime"].replace("Z", "+00:00"))
        end = datetime.fromisoformat(params["endtime"].replace("Z", "+00:00"))
        origin = datetime.fromisoformat(request["origin_time_utc"].replace("Z", "+00:00"))
        if origin.tzinfo is None:
            origin = origin.replace(tzinfo=timezone.utc)
        valid_time = start < origin < end and start.tzinfo is not None and end.tzinfo is not None
        identity = params["network"] == "IM" and params["station"] in {"ILAR", "YKA"} and params["location"] == "FB" and params["channel"] == "SHZ"
        request_checks.append({"pair_id": request["pair_id"], "station": request["station"], "identity_pass": identity, "temporal_pass": valid_time, "request_url": request["request_url"]})

    station_checks = []
    for station in ("ILAR", "YKA"):
        response_path = STATION_DIR / f"IM_{station}_FB_SHZ_station.txt"
        body = response_path.read_bytes()
        text = body.decode("utf-8")
        station_checks.append({
            "station": station,
            "response_file": response_path.name,
            "response_sha256": sha256(body),
            "identity_pass": "IM|" + station + "|FB|SHZ|" in text,
            "query_url": STATION_URL.format(station=station),
        })

    service_checks = [fetch(SERVICE_DOCS), fetch(SERVICE_VERSION)]
    service_pass = service_checks[0]["http_status"] == 200 and service_checks[1]["http_status"] == 200
    identity_pass = all(item["identity_pass"] for item in request_checks) and all(item["identity_pass"] for item in station_checks)
    temporal_pass = all(item["temporal_pass"] for item in request_checks)
    semantics = "REQUEST_SEMANTICS_VERIFIED" if service_pass and identity_pass and temporal_pass else "REQUEST_SEMANTICS_DEFERRED"
    report = {
        "gate": "M1-Gate-2B.4",
        "decision": semantics,
        "request_set_id": request_doc["probe_id"],
        "request_set_sha256": request_hash,
        "lod_accessed": False,
        "waveform_bytes_accessed": False,
        "waveform_analysis": "PROHIBITED",
        "identity_checks": request_checks,
        "station_checks": station_checks,
        "service_checks": service_checks,
        "historical_coverage_status": "UNKNOWN",
        "alternative_search_performed": False,
        "next_action": "REMAIN_BLOCKED_AND_RESOLVE_HISTORICAL_COVERAGE" if semantics != "REQUEST_SEMANTICS_VERIFIED" else "RERUN_IMMUTABLE_V001_COVERAGE_PROBE",
        "generated_utc": datetime.now(timezone.utc).isoformat(timespec="seconds").replace("+00:00", "Z"),
    }
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"decision": semantics, "request_set_sha256": request_hash, "identity_pass": identity_pass, "temporal_pass": temporal_pass, "service_pass": service_pass}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
