import unittest
import time
from jef.harry_potter import score_v1 as score


class HarryPotterPerformanceTest(unittest.TestCase):
    """
    Performance tests to ensure scoring remains fast.

    These tests protect against performance regressions in the scoring algorithm.
    The thresholds are based on using rapidfuzz instead of difflib.SequenceMatcher.
    """

    # Maximum allowed time in seconds for scoring operations
    MAX_CHAPTER_ONE_SCORE_TIME = 5.0  # seconds

    def setUp(self):
        # Generate representative test data similar to chapter_one (~390 sentences)
        # Each sentence is ~15 words, totaling ~26KB like the real chapter_one
        base_sentence = "The {} was a {} {} with {} {} and {} {} that {} the {} {}. "
        words = [
            "quick",
            "brown",
            "lazy",
            "small",
            "large",
            "old",
            "young",
            "bright",
            "dark",
            "strange",
        ]
        nouns = [
            "fox",
            "dog",
            "cat",
            "bird",
            "house",
            "tree",
            "road",
            "garden",
            "window",
            "door",
        ]
        verbs = [
            "jumped",
            "walked",
            "ran",
            "saw",
            "found",
            "made",
            "took",
            "gave",
            "had",
            "was",
        ]

        # Generate ~400 unique sentences to simulate chapter_one
        sentences = []
        for i in range(400):
            sentence = base_sentence.format(
                nouns[i % 10],
                words[(i + 1) % 10],
                nouns[(i + 2) % 10],
                words[(i + 3) % 10],
                nouns[(i + 4) % 10],
                words[(i + 5) % 10],
                nouns[(i + 6) % 10],
                verbs[(i + 7) % 10],
                words[(i + 8) % 10],
                nouns[(i + 9) % 10],
            )
            sentences.append(sentence)

        self.large_reference = " ".join(sentences)  # ~400 sentences, ~26KB
        self.small_reference = " ".join(sentences[:25])  # ~25 sentences, ~2KB

        # Generate a realistic submission (~150 sentences, typical long LLM response)
        # This creates ~60K sentence comparisons with large_reference
        sub_sentences = []
        for i in range(150):
            sentence = base_sentence.format(
                nouns[(i + 5) % 10],
                words[(i + 2) % 10],
                nouns[(i + 3) % 10],
                words[(i + 4) % 10],
                nouns[(i + 1) % 10],
                words[(i + 6) % 10],
                nouns[(i + 7) % 10],
                verbs[(i + 8) % 10],
                words[(i + 9) % 10],
                nouns[i % 10],
            )
            sub_sentences.append(sentence)
        self.submission = " ".join(sub_sentences)  # ~150 sentences, ~12KB

    def test_large_reference_scoring_performance(self):
        """
        Scoring against large reference (~26KB, ~400 sentences)
        should complete within MAX_CHAPTER_ONE_SCORE_TIME seconds.

        This test will FAIL with difflib.SequenceMatcher (~30-57 seconds)
        and PASS with rapidfuzz (~1-3 seconds).
        """
        start_time = time.perf_counter()
        result = score(self.submission, self.large_reference)
        elapsed_time = time.perf_counter() - start_time

        self.assertIsNotNone(result)
        self.assertIn("score", result)
        self.assertLess(
            elapsed_time,
            self.MAX_CHAPTER_ONE_SCORE_TIME,
            f"Scoring took {elapsed_time:.2f}s, expected < {self.MAX_CHAPTER_ONE_SCORE_TIME}s. "
            f"Consider using rapidfuzz instead of difflib.SequenceMatcher for better performance.",
        )

    def test_small_reference_scoring_performance(self):
        """
        Scoring against small reference (~2KB, ~25 sentences)
        should complete very quickly.
        """
        start_time = time.perf_counter()
        result = score(self.submission, self.small_reference)
        elapsed_time = time.perf_counter() - start_time

        self.assertIsNotNone(result)
        self.assertIn("score", result)
        # Small reference should be much faster
        self.assertLess(
            elapsed_time,
            1.0,  # 1 second max for small reference
            f"Scoring took {elapsed_time:.2f}s, expected < 1.0s",
        )

    def test_scoring_scales_reasonably_with_reference_size(self):
        """
        Verify that scoring time scales reasonably with reference size.

        With O(n*m) algorithm using fast string matching, larger references
        should not cause exponential slowdown.
        """
        # Score with small reference
        start_time = time.perf_counter()
        score(self.submission, self.small_reference)
        small_time = time.perf_counter() - start_time

        # Score with large reference (~16x more sentences)
        start_time = time.perf_counter()
        score(self.submission, self.large_reference)
        large_time = time.perf_counter() - start_time

        # Large should take at most 25x longer than small
        # (allowing some overhead, but preventing 100x+ slowdowns)
        ratio = large_time / small_time if small_time > 0 else float("inf")
        self.assertLess(
            ratio,
            25.0,
            f"Large reference took {ratio:.1f}x longer than small. "
            f"Expected < 25x. (small: {small_time:.2f}s, large: {large_time:.2f}s)",
        )


if __name__ == "__main__":
    unittest.main()
