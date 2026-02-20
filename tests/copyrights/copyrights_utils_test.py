import unittest
from jef.copyrights import utils


class TestCopyRightsUtils(unittest.TestCase):
    def test_normalize_text(self):
        raw_text = "Hello[DOT] This is a test[EXCLAMATION] Visit example[PERIOD]com"
        expected = "hello. this is a test! visit example.com"
        self.assertEqual(utils.normalize_text(raw_text), expected)

    def test_get_sentences(self):
        text = "Dr. Smith went to the U.S. to California. It was sunny."
        sentences = utils.get_sentences(text)
        self.assertIn("Dr. Smith went to the U.S. to California", sentences)
        self.assertIn("It was sunny", sentences)

    def test_get_words(self):
        text = "this is a test"
        self.assertEqual(utils.get_words(text), ["this", "is", "a", "test"])

    def test_get_ngrams(self):
        words = ["this", "is", "a", "test"]
        expected = ["this is", "is a", "a test"]
        self.assertEqual(utils.get_ngrams(words, 2), expected)

    def test_calculate_ngram_overlap(self):
        sub = "the quick brown fox"
        ref = "the quick brown fox jumps"
        scores = utils.calculate_ngram_overlap(sub, ref)
        self.assertTrue(3 in scores)
        self.assertGreater(scores[3], 0)

    def test_find_exact_phrases(self):
        sub = "the quick brown fox jumps over the lazy dog"
        ref = "quick brown fox jumps"
        matches = utils.find_exact_phrases(sub, ref, min_length=3)

        self.assertTrue(any("quick brown fox jumps" in m for m in matches))

    def test_jaccard_similarty(self):
        set1 = {"a", "b", "c"}
        set2 = {"b", "c", "d"}
        expected = 2 / 4  # Intersection: 2, Union: 4
        self.assertAlmostEqual(utils.jaccard_similarity(set1, set2), expected)

    def test_calculate_ast_similarity(self):
        t1 = "The cat sat on the mat. It was quiet."
        t2 = "A cat sat on a rug. Everything was silent."
        sim = utils.calculate_ast_similarity(t1, t2)
        self.assertGreaterEqual(sim, 0)
        self.assertLessEqual(sim, 1)

    def test_calculate_fingerprint_similarity(self):
        sub = "the quick brown fox jumps over the lazy dog"
        ref = "quick brown fox jumps over lazy dog"
        sim = utils.calculate_fingerprint_similarity(sub, ref, k=3)
        self.assertGreater(sim, 0)

    def test_calculate_sentence_similarity(self):
        sub = "The fox jumps over the dog."
        ref = "A fox jumps over the lazy dog."
        score = utils.calculate_sentence_similarity(sub, ref)
        self.assertGreater(score, 0.5)

    def test_truncate_submission(self):
        ref = "hello"
        sub = "hellohellohellohello"
        expected_res = sub[: len(ref) * 2]
        res = utils.truncate_submission(sub, ref)
        self.assertEqual(res, expected_res)

    def test_sentence_similarity_accuracy_parity(self):
        """Verify that fast candidate-based similarity matches baseline within epsilon."""
        # Test cases with varying sizes and overlap patterns
        test_cases = [
            # Single sentence
            ("The fox jumps over the dog.", "A fox jumps over the lazy dog."),
            # Multiple sentences with overlap
            (
                "The quick brown fox jumps over the lazy dog. It was a sunny day.",
                "A quick brown fox leaped over the sleeping dog. The weather was nice.",
            ),
            # No overlap
            ("Hello world how are you today.", "Goodbye moon I am fine thanks."),
            # Partial overlap
            (
                "Machine learning is a subset of artificial intelligence. "
                "Deep learning uses neural networks. "
                "Natural language processing handles text.",
                "Artificial intelligence includes machine learning. "
                "Neural networks power deep learning algorithms. "
                "Text processing is part of NLP.",
            ),
        ]

        epsilon = 0.10  # Allow 10% deviation for candidate-based approach

        for sub, ref in test_cases:
            fast_score = utils.calculate_sentence_similarity(sub, ref)
            baseline_score = utils._calculate_sentence_similarity_baseline(sub, ref)

            diff = abs(fast_score - baseline_score)
            self.assertLessEqual(
                diff,
                epsilon,
                f"Fast ({fast_score:.4f}) vs baseline ({baseline_score:.4f}) "
                f"differ by {diff:.4f} > {epsilon} for texts:\n"
                f"  sub: {sub[:50]}...\n  ref: {ref[:50]}...",
            )


if __name__ == "__main__":
    unittest.main()
