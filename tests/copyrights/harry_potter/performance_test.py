"""Performance tests for fingerprint-based copyright scoring."""

import time
import pytest
from jef.copyrights.harry_potter import score
from jef.copyrights.fingerprints import generate_fingerprints


def _generate_text(num_sentences: int) -> str:
    """Generate synthetic text with unique sentences."""
    base = "The {} was a {} {} with {} {} and {} {} that {} the {} {}."
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

    sentences = []
    for i in range(num_sentences):
        sentence = base.format(
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
    return " ".join(sentences)


class TestPerformance:
    """Performance tests for scoring."""

    MAX_SCORE_TIME = 1.0  # seconds

    @pytest.fixture
    def large_fingerprints(self):
        return generate_fingerprints(_generate_text(400), "large")

    @pytest.fixture
    def submission(self):
        return _generate_text(150)

    def test_scoring_completes_quickly(self, large_fingerprints, submission):
        """Scoring should complete within MAX_SCORE_TIME."""
        start = time.perf_counter()
        result = score(submission, fingerprints=large_fingerprints)
        elapsed = time.perf_counter() - start

        assert result is not None
        assert elapsed < self.MAX_SCORE_TIME, (
            f"Took {elapsed:.2f}s, expected < {self.MAX_SCORE_TIME}s"
        )

    def test_builtin_reference_performance(self, submission):
        """Scoring with built-in reference should be fast."""
        start = time.perf_counter()
        result = score(submission, ref="chapter_one")
        elapsed = time.perf_counter() - start

        assert result is not None
        assert elapsed < self.MAX_SCORE_TIME
