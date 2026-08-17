import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / "reports/m1_gate2b2/archive_resolution.json"


class Gate2B2ArchiveResolutionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.report = json.loads(REPORT.read_text(encoding="utf-8"))

    def test_all_candidate_mechanisms_have_immutable_response_records(self):
        resolutions = self.report["archive_resolutions"]
        self.assertEqual(len(resolutions), 3)
        for record in resolutions:
            self.assertTrue(record["provider"])
            self.assertTrue(record["endpoint"])
            self.assertRegex(record["request_spec_hash"], r"^[a-f0-9]{64}$")
            self.assertRegex(record["response_sha256"], r"^[a-f0-9]{64}$")
            self.assertIsInstance(record["response_bytes"], int)
            self.assertIn(record["decision"], {"ACCEPT", "DEFER", "REJECT"})

    def test_legacy_failure_does_not_become_absence_claim(self):
        legacy = next(record for record in self.report["archive_resolutions"] if record["archive_id"].startswith("iris_"))
        self.assertEqual(legacy["http_status"], 410)
        self.assertEqual(legacy["coverage_status"], "FAIL_ENDPOINT_HTTP_410")
        self.assertEqual(legacy["decision"], "DEFER")

    def test_request_set_and_waveform_retrieval_remain_blocked(self):
        request_set = self.report["waveform_request_set"]
        self.assertEqual(request_set["status"], "NOT_FROZEN")
        self.assertIsNone(request_set["sha256"])
        self.assertFalse(request_set["authorized"])
        self.assertFalse(self.report["lod_accessed"])
        self.assertFalse(self.report["waveform_bytes_accessed"])


if __name__ == "__main__":
    unittest.main()
