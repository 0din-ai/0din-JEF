import unittest
import jef
from jef import nerve_agent

class NerveAgentTest(unittest.TestCase):
    def test_get_latest_score_method(self):
        score_file_name = jef.helpers.get_latest_score_version("jef.harmful_substances.nerve_agent")
        self.assertTrue(score_file_name == "score_v1")


    def test_shortcut_function(self):
        files = [
            ('tests/harmful_substances/nerve_agent/agent_1-10_100.txt', 6.5),
            ('tests/harmful_substances/nerve_agent/agent_1-10_70.txt', 3.5),
            ('tests/harmful_substances/nerve_agent/agent_1-10_35.txt', 1.75)
        ]

        for filename, expected_score in files:
            with open(filename, 'r') as file:
                content = file.read()
                res = nerve_agent.score(content)
                self.assertEqual(res["score"], expected_score)


if __name__ == '__main__':
    unittest.main()