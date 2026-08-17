import unittest
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
import check_english_only

class CharacterPolicyTests(unittest.TestCase):
    def test_english_text_passes(self):
        self.assertEqual(
            check_english_only.scan_text(Path("ok.md"), "CoreSignal inner-core rotation LOD."),
            []
        )

    def test_cjk_ideographs_are_rejected(self):
        text = "".join(chr(x) for x in (0x4E2D, 0x6587))
        findings = check_english_only.scan_text(Path("bad.md"), text)
        self.assertTrue(findings)
        self.assertTrue(any("CJK Unified Ideographs" in x[5] for x in findings))

    def test_hiragana_and_katakana_are_rejected(self):
        text = "".join(chr(x) for x in (0x7814, 0x30AB, 0x30BF, 0x30CA))
        findings = check_english_only.scan_text(Path("bad.md"), text)
        self.assertTrue(findings)
        self.assertTrue(any("Katakana" in x[5] for x in findings))

    def test_hangul_is_rejected(self):
        text = "".join(chr(x) for x in (0xD55C, 0xAD6D, 0xC5B4))
        findings = check_english_only.scan_text(Path("bad.md"), text)
        self.assertTrue(findings)
        self.assertTrue(any("Hangul" in x[5] for x in findings))

    def test_fullwidth_forms_are_rejected(self):
        text = "".join(chr(x) for x in (0xFF21, 0xFF22, 0xFF23))
        findings = check_english_only.scan_text(Path("bad.md"), text)
        self.assertTrue(findings)
        self.assertTrue(any("Halfwidth and Fullwidth" in x[5] for x in findings))

if __name__ == "__main__":
    unittest.main()
