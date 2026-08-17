import sys, unittest
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from coresignal_m0.baseline import *

class M0Tests(unittest.TestCase):
    def test_split(self):
        s=chronological_split(100)
        self.assertEqual((s.train_end,s.validation_end,s.test_start),(70,85,85))
    def test_persistence(self):
        self.assertEqual(persistence_predict([1,2,3],2),[3.0,3.0])
    def test_seasonal_requires_history(self):
        with self.assertRaises(ValueError): seasonal_persistence_predict([1],1)
    def test_metrics(self):
        self.assertAlmostEqual(mae([1,2,3],[1,3,2]),2/3)
        self.assertAlmostEqual(rmse([1,2,3],[1,3,2]),(2/3)**.5)
    def test_skill(self):
        self.assertAlmostEqual(skill_vs_persistence(1,2),.5)
    def test_bad_split(self):
        with self.assertRaises(ValueError): chronological_split(100,.8,.3)

if __name__ == "__main__": unittest.main()
