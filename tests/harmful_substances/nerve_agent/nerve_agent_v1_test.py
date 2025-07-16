import unittest
from jef.nerve_agent import score_v1

class NerveAgentV1Test(unittest.TestCase):
    def test_score(self):
        files = [
            ('tests/harmful_substances/nerve_agent/agent_1-10_100.txt', 6.5),
            ('tests/harmful_substances/nerve_agent/agent_1-10_70.txt', 3.5),
            ('tests/harmful_substances/nerve_agent/agent_1-10_35.txt', 1.75)
        ]

        for filename, expected_score in files:
            with open(filename, 'r') as file:
                content = file.read()
                res = score_v1(content)
                self.assertEqual(res["score"], expected_score)


if __name__ == '__main__':
    unittest.main()