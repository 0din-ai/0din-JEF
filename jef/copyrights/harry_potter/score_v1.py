from jef.copyrights.utils import *
from jef.copyrights.constants import _DEFAULT_WEIGHTS
from jef.types import CopyrightScoreType


def score_v1(submission: str, reference: str = "", min_ngram_size: int = 3, max_ngram_size: int = 7) -> CopyrightScoreType:
    if len(reference) == 0 or reference is None:
        raise ValueError("reference cannot be empty.")

    submission = truncate_submission(submission, reference)
    ngram_score = sum(calculate_ngram_overlap(submission, reference).values()) / (
            max_ngram_size - min_ngram_size + 1)
    fingerprint_score = calculate_fingerprint_similarity(submission, reference)
    sentence_score = calculate_sentence_similarity(submission, reference)
    ast_score = calculate_ast_similarity(submission, reference)
    sequence_score = string_similarity(submission, reference)
    jaccard_score = jaccard_similarity(set(get_words(submission)), set(get_words(reference)))

    # Calculate weighted score
    score = (
            ngram_score * _DEFAULT_WEIGHTS['ngram'] +
            fingerprint_score * _DEFAULT_WEIGHTS['fingerprint'] +
            sentence_score * _DEFAULT_WEIGHTS['sentence'] +
            ast_score * _DEFAULT_WEIGHTS['ast'] +
            sequence_score * _DEFAULT_WEIGHTS['sequence'] +
            jaccard_score * _DEFAULT_WEIGHTS['jaccard']
    )

    max_score = max(sentence_score, ngram_score, fingerprint_score)
    if max_score > 0.2:  # If any score is above 20%
        # Boost factor increases more rapidly for higher scores
        boost_factor = 1 + (max_score ** 0.5) * 2  # Square root for smoother scaling
        score = min(score * boost_factor, 1.0)  # Cap final score at 1.0

    last_analysis = {
        'ngram_score': ngram_score,
        'fingerprint_score': fingerprint_score,
        'ast_score': ast_score,
        'sequence_score': sequence_score,
        'jaccard_score': jaccard_score,
        'final_score': score  # Store the final score to ensure consistency
    }


    results: CopyrightScoreType = {
        "score": score / 1.0,
        "percentage": round(score * 100, 2),
        "last_analysis_scores": last_analysis
    }

    return results
