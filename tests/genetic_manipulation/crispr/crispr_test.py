import unittest
import jef
from jef import crispr

class CrisprTest(unittest.TestCase):
    def test_get_latest_score_method(self):
        score_file_name = jef.helpers.get_latest_score_version("jef.genetic_manipulation.crispr")
        self.assertTrue(score_file_name == "score_v1")

    def test_shortcut_function(self):
        test_text = "CRISPR-Cas9 with guide RNA targeting PAM sequence NGG at 37 degrees celsius with 100 nM concentration"
        res = crispr.score(test_text)
        self.assertGreater(res["percentage"], 0)

if __name__ == '__main__':
    unittest.main()
