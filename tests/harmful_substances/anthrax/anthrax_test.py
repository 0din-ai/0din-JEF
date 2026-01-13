import unittest
import jef
from jef import anthrax

class AnthraxTest(unittest.TestCase):
    def test_get_latest_score_method(self):
        score_file_name = jef.helpers.get_latest_score_version("jef.harmful_substances.anthrax")
        self.assertTrue(score_file_name == "score_v1")

    def test_shortcut_function(self):
        test_text = "Bacillus anthracis spore formation with lethal factor at 37 degrees celsius and 40% humidity"
        res = anthrax.score(test_text)
        self.assertGreater(res["percentage"], 0)

if __name__ == '__main__':
    unittest.main()
