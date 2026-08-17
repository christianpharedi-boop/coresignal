"""Generate the predeclared Gate 2B.3 archive-coverage probe request set."""
from __future__ import annotations

import hashlib
import json
from datetime import datetime, timedelta, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INPUT = ROOT / "reports/m1_gate2b1/gate2b1_station_feasibility.json"
OUTPUT = ROOT / "reports/m1_gate2b3/probe_requests.json"
SERVICE = "https://service.earthscope.org/fdsnws/dataselect/1/query"


def parse_time(value: str) -> datetime:
    return datetime.fromisoformat(value.replace("Z", "+00:00")).replace(tzinfo=timezone.utc)


def unique_pairs(report: dict) -> list[dict]:
    pairs = {}
    for row in report["pair_feasibility"]:
        pairs.setdefault(row["pair_id"], {
            "pair_id": row["pair_id"],
            "event_a": row["event_a"],
            "event_b": row["event_b"],
            "event_a_origin_utc": row["event_a_origin_utc"],
            "event_b_origin_utc": row["event_b_origin_utc"],
        })
    return list(pairs.values())


def choose_pairs(pairs: list[dict]) -> list[tuple[str, dict]]:
    ordered = sorted(pairs, key=lambda p: (parse_time(p["event_a_origin_utc"]), parse_time(p["event_b_origin_utc"]), p["pair_id"]))
    chosen: list[tuple[str, dict]] = []
    chosen.append(("earliest_eligible", ordered[0]))
    chosen.append(("latest_eligible", max(pairs, key=lambda p: (parse_time(p["event_b_origin_utc"]), p["pair_id"]))))
    chosen.append(("middle_period", ordered[(len(ordered) - 1) // 2]))
    blocks = [
        ("block_1991_1999", datetime(1991, 1, 1, tzinfo=timezone.utc), datetime(1999, 12, 31, 23, 59, 59, tzinfo=timezone.utc)),
        ("block_2000_2009", datetime(2000, 1, 1, tzinfo=timezone.utc), datetime(2009, 12, 31, 23, 59, 59, tzinfo=timezone.utc)),
        ("block_2010_2019", datetime(2010, 1, 1, tzinfo=timezone.utc), datetime(2019, 12, 31, 23, 59, 59, tzinfo=timezone.utc)),
        ("block_2020_2023", datetime(2020, 1, 1, tzinfo=timezone.utc), datetime(2023, 12, 31, 23, 59, 59, tzinfo=timezone.utc)),
    ]
    for label, start, end in blocks:
        eligible = [p for p in ordered if start <= parse_time(p["event_a_origin_utc"]) <= end and start <= parse_time(p["event_b_origin_utc"]) <= end]
        if eligible:
            chosen.append((label, eligible[0]))
    result = []
    seen = set()
    for reason, pair in chosen:
        if pair["pair_id"] not in seen:
            result.append((reason, pair))
            seen.add(pair["pair_id"])
    return result


def request_record(reason: str, pair: dict, station: str) -> dict:
    event_time = parse_time(pair["event_a_origin_utc"])
    start = event_time - timedelta(seconds=120)
    end = event_time + timedelta(seconds=1800)
    params = {
        "network": "IM",
        "station": station,
        "location": "FB",
        "channel": "SHZ",
        "starttime": start.isoformat().replace("+00:00", "Z"),
        "endtime": end.isoformat().replace("+00:00", "Z"),
    }
    query = "&".join(f"{key}={value}" for key, value in params.items())
    return {
        "probe_reason": reason,
        "pair_id": pair["pair_id"],
        "event_id": pair["event_a"],
        "origin_time_utc": pair["event_a_origin_utc"],
        "station": station,
        "network": "IM",
        "location": "FB",
        "channel": "SHZ",
        "start_time_utc": params["starttime"],
        "end_time_utc": params["endtime"],
        "service": SERVICE,
        "request_parameters": params,
        "request_url": f"{SERVICE}?{query}",
        "waveform_analysis": "PROHIBITED",
    }


def main() -> int:
    report = json.loads(INPUT.read_text(encoding="utf-8"))
    pairs = unique_pairs(report)
    selected = choose_pairs(pairs)
    requests = [request_record(reason, pair, station) for reason, pair in selected for station in ("ILAR", "YKA")]
    output = {
        "probe_id": "WAVEFORM_COVERAGE_PROBE_v001",
        "contract": "data/m1_gate2/gate2b3_coverage_probe_contract.yaml",
        "source_pair_count": len(pairs),
        "selected_pair_count": len(selected),
        "request_count": len(requests),
        "selection_frozen_before_response": True,
        "lod_accessed": False,
        "waveform_analysis": "PROHIBITED",
        "generated_utc": datetime.now(timezone.utc).isoformat(timespec="seconds").replace("+00:00", "Z"),
        "requests": requests,
    }
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(json.dumps(output, indent=2) + "\n", encoding="utf-8")
    digest = hashlib.sha256(OUTPUT.read_bytes()).hexdigest()
    print(json.dumps({"request_count": len(requests), "selected_pair_ids": [p[1]["pair_id"] for p in selected], "request_set_sha256": digest}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
