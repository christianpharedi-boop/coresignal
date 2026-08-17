import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / "reports/m1_gate2b4/request_semantics.json"
RERUN = ROOT / "reports/m1_gate2b3/probe_results_v001_semantics_verified.json"


class Gate2B4RequestSemanticsTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.report = json.loads(REPORT.read_text(encoding="utf-8"))
        cls.rerun = json.loads(RERUN.read_text(encoding="utf-8"))

    def test_frozen_request_semantics_are_verified(self):
        self.assertEqual(self.report["decision"], "REQUEST_SEMANTICS_VERIFIED")
        self.assertEqual(self.report["request_set_sha256"], "378a72e35379e3d33fc7b048ae378bb916e13563017b31d61487a3a2911e5f38")
        self.assertTrue(all(item["identity_pass"] for item in self.report["identity_checks"]))
        self.assertTrue(all(item["temporal_pass"] for item in self.report["identity_checks"]))
        self.assertTrue(all(item["identity_pass"] for item in self.report["station_checks"]))
        self.assertFalse(self.report["alternative_search_performed"])

    def test_semantics_rerun_preserves_unknown_coverage(self):
        self.assertEqual(self.rerun["request_set_sha256"], self.report["request_set_sha256"])
        self.assertEqual(self.rerun["coverage_status"], "COVERAGE_UNKNOWN")
        self.assertEqual(len(self.rerun["waveform_requests"]), 14)
        self.assertTrue(all(item["http_status"] == 204 for item in self.rerun["waveform_requests"]))

    def test_waveform_and_lod_remain_blocked(self):
        self.assertFalse(self.report["lod_accessed"])
        self.assertFalse(self.report["waveform_bytes_accessed"])
        self.assertEqual(self.report["waveform_analysis"], "PROHIBITED")
        self.assertFalse(self.rerun["full_acquisition_authorized"])


if __name__ == "__main__":
    unittest.main()
