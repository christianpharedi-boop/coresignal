import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / "reports/m1_gate2b/gate2b_reconstruction.json"


class Gate2BReconstructionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.report = json.loads(REPORT.read_text(encoding="utf-8"))

    def test_event_population_reconstructs(self):
        events = self.report["event_reconstruction"]
        self.assertTrue(events["pass"])
        self.assertEqual(events["expected_count"], 121)
        self.assertEqual(events["observed_count"], 121)
        self.assertEqual(events["duplicate_event_ids"], [])

    def test_pair_population_reconstructs_and_preserves_label_discrepancy(self):
        pairs = self.report["pair_reconstruction"]
        self.assertTrue(pairs["pass"])
        self.assertEqual(pairs["table_label_count"], 142)
        self.assertEqual(pairs["observed_count"], 143)
        self.assertEqual(pairs["unique_pair_id_count"], 143)
        self.assertEqual(pairs["dangling_event_references"], [])
        self.assertFalse(pairs["count_discrepancy_requires_resolution"])

    def test_waveform_retrieval_remains_blocked(self):
        self.assertEqual(self.report["decision"], "DEFER_RECONSTRUCTION")
        self.assertFalse(self.report["waveform_retrieval"]["authorized"])
        self.assertFalse(self.report["station_reconstruction"]["pass"])
        self.assertFalse(self.report["lod_accessed"])
        self.assertFalse(self.report["waveform_accessed"])


if __name__ == "__main__":
    unittest.main()
