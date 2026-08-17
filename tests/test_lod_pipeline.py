import tempfile
import unittest
from datetime import date
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from run_lod_pipeline import run  # noqa: E402


def row(day: int, mjd: int, lod: str = "0.0010000") -> str:
    fields = ["2020", "01", f"{day:02d}", "0", f"{mjd:.2f}"]
    fields += ["0"] * 8
    fields[12] = lod
    fields += ["0"] * 7
    fields[19] = "0.0000100"
    return " ".join(fields)


class StrictLODPipelineTests(unittest.TestCase):
    def write_fixture(self, text: str) -> Path:
        directory = Path(tempfile.mkdtemp())
        path = directory / "eopc04.1962-now"
        path.write_text("# EOP 20 C04 fixture\n" + text, encoding="ascii")
        return path

    def test_missing_file_is_blocked(self):
        result = run(Path("/tmp/coresignal-file-that-does-not-exist"))
        self.assertEqual(result["status"], "blocked")

    def test_valid_fixture_is_quality_checked(self):
        path = self.write_fixture(row(1, 58849) + "\n" + row(2, 58850) + "\n")
        result = run(path, expected_records=2, expected_start="2020-01-01", expected_end="2020-01-02")
        self.assertEqual(result["status"], "quality_checked", result)

    def test_mjd_mismatch_is_rejected(self):
        path = self.write_fixture(row(1, 58850))
        result = run(path)
        self.assertEqual(result["status"], "rejected")
        self.assertTrue(any("MJD/date mismatch" in error for error in result["errors"]))

    def test_gap_and_count_mismatch_are_rejected(self):
        path = self.write_fixture(row(1, 58849) + "\n" + row(3, 58851) + "\n")
        result = run(path, expected_records=3)
        self.assertEqual(result["status"], "rejected")
        self.assertTrue(any("record-count mismatch" in error for error in result["errors"]))
        self.assertTrue(any("cadence gaps" in error for error in result["errors"]))

    def test_malformed_line_is_rejected(self):
        path = self.write_fixture("2020 01 01 malformed\n")
        result = run(path)
        self.assertEqual(result["status"], "rejected")
        self.assertTrue(any("expected 20 fields" in error for error in result["errors"]))


if __name__ == "__main__":
    unittest.main()
