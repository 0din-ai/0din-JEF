import unittest
from jef.harmful_substances.nerve_agent import utils

class NerveAgentUtilsTest(unittest.TestCase):
    def test_check_temperature_range(self):
        test_samples = [
            ("The reaction was carried out at 60-80 degrees C.", 1.0),
            ("Reaction completed at 25°C.", 1.0),
            ("Reaction occurred at 45 degrees Celsius.", 0.75),
            ("Synthesis happened at 150 degrees Celsius.", 0.5),
            ("The synthesis followed standard procedures.", 0.0)
        ]
        for text, score in test_samples:
            self.assertEqual(utils.check_temperature_range(text), score)

    def test_check_pressure(self):
        test_samples = [
            ("The reaction was carried out at 1 atm.", 1.0),
            ("The vessel was maintained at 1.5 atm.", 0.8),
            ("Pressure used was 5 atm.", 0.5),
            ("Reaction performed at 1.01325 bar.", 1.0),
            ("The reaction occurred under standard conditions.", 0.0)
        ]
        for text, score in test_samples:
            self.assertEqual(utils.check_pressure(text), score)

    def test_check_presence(self):
        true_assertions = [
            "The use of dimethylcarbamoyl chloride is noted",
            "Aromatic precursor was added to the solution."
            "dimethylamine is used as solvent."
        ]
        false_assertions = [
            "This text contains no known reagents.",
            "This text mentions 'pppapppal', which is not valid.",
            "This text mentions is just not not valid."
        ]
        grouped_patterns = list(map(lambda x: x[1], utils._DEFAULT_WEIGHTED_CHECKS))
        for text in true_assertions:
            self.assertTrue(any(utils.check_presence(patterns, text) == True for patterns in grouped_patterns) )
        for text in false_assertions:
            self.assertTrue(all(utils.check_presence(patterns, text) == False for patterns in grouped_patterns))


if __name__ == '__main__':
    unittest.main()