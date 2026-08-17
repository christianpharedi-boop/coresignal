import tempfile
import unittest
from pathlib import Path

import yaml

from scripts.validate_gate2a_ledger import validate_ledger

ROOT = Path(__file__).resolve().parents[1]
LEDGER = ROOT / "data/m1_gate2/acquisition_ledger.yaml"


class Gate2ALedgerTests(unittest.TestCase):
    def test_initial_ledger_is_valid_and_blocked(self):
        self.assertEqual(validate_ledger(LEDGER), [])
        document = yaml.safe_load(LEDGER.read_text(encoding="utf-8"))
        self.assertEqual(document["ledger_integrity"]["ledger_status"], "READY_FOR_GATE2_RECONSTRUCTION")
        self.assertTrue(all(record["execution"]["blocking"] for record in document["files"]))

    def test_duplicate_record_id_is_rejected(self):
        document = yaml.safe_load(LEDGER.read_text(encoding="utf-8"))
        document["files"][1]["record_id"] = document["files"][0]["record_id"]
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "ledger.yaml"
            path.write_text(yaml.safe_dump(document), encoding="utf-8")
            errors = validate_ledger(path)
        self.assertTrue(any("duplicate record_id" in error for error in errors))

    def test_verified_record_requires_sha256(self):
        document = yaml.safe_load(LEDGER.read_text(encoding="utf-8"))
        document["files"][0]["status"] = "VERIFIED"
        document["files"][0]["acquisition"]["acquisition_timestamp_utc"] = "2026-08-17T18:11:11Z"
        document["files"][0]["acquisition"]["original_filename"] = "source.bin"
        document["files"][0]["acquisition"]["byte_size"] = 1
        document["files"][0]["integrity"]["sha256"] = None
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "ledger.yaml"
            path.write_text(yaml.safe_dump(document), encoding="utf-8")
            errors = validate_ledger(path)
        self.assertTrue(any("verified-or-final records require a lowercase SHA-256" in error for error in errors))


if __name__ == "__main__":
    unittest.main()
