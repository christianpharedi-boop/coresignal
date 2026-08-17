import unittest
from datetime import date
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from rotation.lod import LODRecord, validate_lod


class LODValidationTests(unittest.TestCase):
    def test_valid_record(self):
        records = [LODRecord(date(2020, 1, 1), 0.25, "good")]
        self.assertEqual(validate_lod(records), [])

    def test_duplicate_epoch_fails(self):
        d = date(2020, 1, 1)
        records = [LODRecord(d, 0.25, "good"), LODRecord(d, 0.30, "good")]
        self.assertTrue(validate_lod(records))

    def test_missing_quality_flag_fails(self):
        records = [LODRecord(date(2020, 1, 1), 0.25, "")]
        self.assertTrue(validate_lod(records))

    def test_committed_inventory_artifact_is_quality_checked(self):
        import json

        report = ROOT / "reports/lod_inventory/eop20_c04_qc.json"
        self.assertTrue(report.exists())
        document = json.loads(report.read_text(encoding="utf-8"))
        self.assertEqual(document["status"], "quality_checked")
        self.assertGreater(document["record_count"], 0)
        self.assertEqual(document["date_gap_count"], 0)
        self.assertEqual(document["validation_error_count"], 0)


if __name__ == "__main__":
    unittest.main()
