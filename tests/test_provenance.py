import unittest
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import validate_provenance


class ProvenanceTests(unittest.TestCase):
    def test_registry_validates(self):
        self.assertEqual(validate_provenance.main_for_test(ROOT), 0)


if __name__ == "__main__":
    unittest.main()
