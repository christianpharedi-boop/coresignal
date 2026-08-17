from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]


class V02SpecificationTests(unittest.TestCase):
    def test_scientific_specification_exists_and_is_falsification_first(self):
        path = ROOT / "docs" / "SCIENTIFIC_SPECIFICATION_v0.2.md"
        self.assertTrue(path.exists())
        text = path.read_text(encoding="utf-8")
        for required in [
            "H0: Null",
            "H1: Inner-core coupling",
            "Temporal validation",
            "Acceptance criteria",
            "Rejection criteria",
            "Scientific audit trail",
            "does not claim to establish a causal mechanism",
        ]:
            self.assertIn(required, text)

    def test_experiment_manifests_exist(self):
        paths = [
            ROOT / "experiments/lod/lod_m0_baseline.yaml",
            ROOT / "experiments/lod/lod_m1_inner_core.yaml",
            ROOT / "experiments/geomagnetic/geomagnetic_m0_baseline.yaml",
        ]
        for path in paths:
            self.assertTrue(path.exists())

    def test_manifest_validator_accepts_current_manifests(self):
        from scripts.validate_manifests import validate_manifest

        manifests = sorted((ROOT / "experiments").rglob("*.yaml"))
        self.assertGreaterEqual(len(manifests), 3)
        for path in manifests:
            self.assertEqual(validate_manifest(path), [], str(path))

    def test_provenance_registry_is_present_and_unfilled_sources_are_planned(self):
        path = ROOT / "data/provenance/registry.yaml"
        self.assertTrue(path.exists())
        text = path.read_text(encoding="utf-8")
        self.assertIn("required_fields:", text)
        self.assertIn("status: planned", text)

    def test_author_metadata_is_present(self):
        citation = (ROOT / "CITATION.cff").read_text(encoding="utf-8")
        license_text = (ROOT / "LICENSE").read_text(encoding="utf-8")
        self.assertIn('given-names: "Basie"', citation)
        self.assertIn('family-names: "Pharedi"', citation)
        self.assertIn("Basie Pharedi", license_text)


if __name__ == "__main__":
    unittest.main()
