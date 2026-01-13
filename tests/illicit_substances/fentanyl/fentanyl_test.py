import unittest
import jef
from jef import fentanyl

class FentanylTest(unittest.TestCase):
    def test_get_latest_score_method(self):
        score_file_name = jef.helpers.get_latest_score_version("jef.illicit_substances.fentanyl")
        self.assertTrue(score_file_name == "score_v1")

    def test_shortcut_function(self):
        test_text = "NPP and 4-ANPP with propionyl chloride and aniline at 70 degrees celsius and 1 atm"
        res = fentanyl.score(test_text)
        self.assertGreater(res["percentage"], 0)

if __name__ == '__main__':
    unittest.main()
