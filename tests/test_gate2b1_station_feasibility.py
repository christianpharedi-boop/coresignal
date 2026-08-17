import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / "reports/m1_gate2b1/gate2b1_station_feasibility.json"


class Gate2B1StationFeasibilityTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.report = json.loads(REPORT.read_text(encoding="utf-8"))

    def test_two_authoritative_station_records_are_present(self):
        inventory = self.report["station_inventory"]
        self.assertEqual({record["station"] for record in inventory}, {"ILAR", "YKA"})
        self.assertTrue(all(record["response_sha256"] for record in inventory))
        self.assertTrue(all(record["channel"] == "SHZ" for record in inventory))

    def test_all_pairs_have_station_operational_coverage(self):
        records = self.report["pair_feasibility"]
        self.assertEqual(self.report["pair_count"], 143)
        self.assertEqual(self.report["station_pair_feasibility_count"], 286)
        self.assertEqual(len(records), 286)
        self.assertTrue(all(record["station_operational_at_event_a"] for record in records))
        self.assertTrue(all(record["station_operational_at_event_b"] for record in records))

    def test_archive_uncertainty_blocks_waveforms(self):
        self.assertEqual(self.report["archive_coverage_query"]["status"], "UNAVAILABLE")
        self.assertFalse(self.report["waveform_retrieval_authorized"])
        self.assertFalse(self.report["lod_accessed"])
        self.assertFalse(self.report["waveform_bytes_accessed"])


if __name__ == "__main__":
    unittest.main()
