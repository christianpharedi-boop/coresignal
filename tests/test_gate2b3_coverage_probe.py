import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REQUESTS = ROOT / "reports/m1_gate2b3/probe_requests.json"
RESULTS = ROOT / "reports/m1_gate2b3/probe_results.json"


class Gate2B3CoverageProbeTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.requests = json.loads(REQUESTS.read_text(encoding="utf-8"))
        cls.results = json.loads(RESULTS.read_text(encoding="utf-8"))

    def test_probe_selection_is_frozen_and_lod_independent(self):
        self.assertEqual(self.requests["source_pair_count"], 143)
        self.assertEqual(self.requests["request_count"], 14)
        self.assertTrue(self.requests["selection_frozen_before_response"])
        self.assertFalse(self.requests["lod_accessed"])
        self.assertEqual(self.requests["waveform_analysis"], "PROHIBITED")
        self.assertEqual(self.results["request_set_sha256"], "378a72e35379e3d33fc7b048ae378bb916e13563017b31d61487a3a2911e5f38")

    def test_empty_204_responses_remain_unknown(self):
        self.assertEqual(self.results["coverage_status"], "COVERAGE_UNKNOWN")
        self.assertEqual(len(self.results["waveform_requests"]), 14)
        self.assertTrue(all(item["http_status"] == 204 for item in self.results["waveform_requests"]))
        self.assertTrue(all(item["response_bytes"] == 0 for item in self.results["waveform_requests"]))

    def test_full_acquisition_and_analysis_remain_blocked(self):
        self.assertFalse(self.results["full_acquisition_authorized"])
        self.assertFalse(self.results["lod_accessed"])
        self.assertEqual(self.results["waveform_analysis"], "PROHIBITED")


if __name__ == "__main__":
    unittest.main()
