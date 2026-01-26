import unittest
import jef
from jef import anthrax


class AnthraxTest(unittest.TestCase):
    def test_get_latest_score_method(self):
        score_file_name = jef.helpers.get_latest_score_version("jef.harmful_substances.anthrax")
        self.assertTrue(score_file_name == "score_v1")

    def test_score_function(self):
        res = anthrax.score_v1("bacillus anthracis ames strain", show_matches=True)
        self.assertIn("score", res)
        self.assertIn("percentage", res)


if __name__ == '__main__':
    unittest.main()
