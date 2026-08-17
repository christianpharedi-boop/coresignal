"""Execute the frozen Gate 2B.3 archive-coverage probe without waveform analysis."""
from __future__ import annotations

import argparse
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parents[1]
REQUESTS_PATH = ROOT / "reports/m1_gate2b3/probe_requests.json"
DEFAULT_RAW_DIR = Path("/home/ubuntu/coresignal_work/gate2b3_probe/raw")
DEFAULT_RESULT_PATH = ROOT / "reports/m1_gate2b3/probe_results.json"


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=DEFAULT_RESULT_PATH)
    parser.add_argument("--raw-dir", type=Path, default=DEFAULT_RAW_DIR)
    args = parser.parse_args()
    request_doc = json.loads(REQUESTS_PATH.read_text(encoding="utf-8"))
    request_set_hash = sha256_bytes(REQUESTS_PATH.read_bytes())
    args.raw_dir.mkdir(parents=True, exist_ok=True)
    results = []
    for index, request in enumerate(request_doc["requests"], start=1):
        filename = f"probe_{index:03d}_{request['pair_id']}_{request['station']}.mseed"
        output_path = args.raw_dir / filename
        record = {
            "probe_index": index,
            "pair_id": request["pair_id"],
            "event_id": request["event_id"],
            "station": request["station"],
            "request_url": request["request_url"],
            "request_set_sha256": request_set_hash,
            "retrieval_timestamp_utc": datetime.now(timezone.utc).isoformat(timespec="seconds").replace("+00:00", "Z"),
            "waveform_analysis": "PROHIBITED",
            "raw_path": str(output_path),
        }
        try:
            req = Request(request["request_url"], headers={"User-Agent": "CoreSignal-Gate2B3/1.0"})
            with urlopen(req, timeout=60) as response:
                data = response.read()
                record.update({
                    "http_status": response.status,
                    "content_type": response.headers.get("Content-Type"),
                    "response_bytes": len(data),
                    "response_sha256": sha256_bytes(data),
                })
                output_path.write_bytes(data)
        except Exception as exc:
            record.update({
                "http_status": getattr(exc, "code", None),
                "content_type": None,
                "response_bytes": 0,
                "response_sha256": sha256_bytes(b""),
                "error_type": type(exc).__name__,
                "error": str(exc),
            })
            output_path.write_bytes(b"")
        results.append(record)

    successful = [record for record in results if record.get("http_status") == 200 and record.get("response_bytes", 0) > 0]
    responses_without_bytes = [record for record in results if record.get("http_status") is not None and record.get("response_bytes", 0) == 0]
    if len(successful) == len(results):
        coverage = "COVERAGE_ESTABLISHED"
    elif successful:
        coverage = "COVERAGE_PARTIAL"
    elif responses_without_bytes:
        coverage = "COVERAGE_UNKNOWN"
    else:
        coverage = "COVERAGE_FAILED"

    output = {
        "probe_id": "WAVEFORM_COVERAGE_PROBE_v001",
        "request_set_sha256": request_set_hash,
        "retrieval_timestamp_utc": datetime.now(timezone.utc).isoformat(timespec="seconds").replace("+00:00", "Z"),
        "coverage_status": coverage,
        "waveform_analysis": "PROHIBITED",
        "lod_accessed": False,
        "waveform_requests": results,
        "full_acquisition_authorized": coverage == "COVERAGE_ESTABLISHED",
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(output, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({
        "coverage_status": coverage,
        "request_set_sha256": request_set_hash,
        "successful": len(successful),
        "total": len(results),
        "full_acquisition_authorized": output["full_acquisition_authorized"],
    }, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
