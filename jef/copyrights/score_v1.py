from jef.copyrights.utils import *
from jef.copyrights.constants import _DEFAULT_WEIGHTS
from jef.types import CopyrightScoreType


def score_v1(submission: str, reference: str = "", min_ngram_size: int = 3, max_ngram_size: int = 7) -> CopyrightScoreType:
    """Perform comprehensive copyright analysis with length consideration"""
    if len(reference) == 0 or reference is None:
       raise ValueError("reference cannot be empty.")

    submission = truncate_submission(submission, reference)
    # Normalize texts
    submission_norm = normalize_text(submission)
    reference_norm = normalize_text(reference)

    # Calculate all scores
    ast_score = calculate_ast_similarity(submission_norm, reference_norm)
    fingerprint_score = calculate_fingerprint_similarity(submission_norm, reference_norm)

    # N-gram analysis
    ngram_scores = calculate_ngram_overlap(submission_norm, reference_norm)
    weights = {n: math.log(n, 2) for n in range(min_ngram_size, max_ngram_size + 1)}
    total_weight = sum(weights.values())
    ngram_score = sum(ngram_scores[n] * weights[n] for n in ngram_scores) / total_weight

    # Other similarity scores
    submission_words = set(get_words(submission_norm))
    reference_words = set(get_words(reference_norm))
    jaccard_score = jaccard_similarity(submission_words, reference_words)
    sequence_score = string_similarity(submission_norm, reference_norm)

    # Sentence-level analysis
    submission_sentences = get_sentences(submission_norm)
    reference_sentences = get_sentences(reference_norm)
    sentence_scores = []

    # For each reference sentence, find how well it matches any submission sentence
    for ref_sent in reference_sentences:
        ref_words = get_words(ref_sent)
        best_score = 0
        for sub_sent in submission_sentences:
            sub_words = get_words(sub_sent)
            # Calculate what percentage of reference words appear in submission
            sent_length_ratio = len(set(ref_words).intersection(set(sub_words))) / len(ref_words)
            jaccard = len(set(ref_words).intersection(set(sub_words))) / len(set(ref_words))
            sequence = string_similarity(ref_sent, sub_sent)
            score = (jaccard * 0.5 + sequence * 0.5) * sent_length_ratio
            best_score = max(best_score, score)
        sentence_scores.append(best_score)

    sentence_level_score = sum(sentence_scores) / len(sentence_scores) if sentence_scores else 0

    # Calculate final score with exact weights
    final_score = (
            ngram_score * _DEFAULT_WEIGHTS['ngram'] +               # N-gram Analysis (15%)
            fingerprint_score * _DEFAULT_WEIGHTS['fingerprint'] +   # Fingerprinting (15%)
            sentence_level_score *  _DEFAULT_WEIGHTS["sentence"] +  # Sentence-level Analysis (50%)
            ast_score *  _DEFAULT_WEIGHTS["ast"] +                  # AST Comparison (5%)
            sequence_score * _DEFAULT_WEIGHTS["sequence"] +         # Sequence Matching (10%)
            jaccard_score * _DEFAULT_WEIGHTS["jaccard"]             # Jaccard Similarity (5%)
    )

    # Store raw scores without any additional modifications
    last_analysis = {
        'ngram_score': ngram_score,
        'fingerprint_score': fingerprint_score,
        'sentence_level_score': sentence_level_score,
        'ast_score': ast_score,
        'sequence_score': sequence_score,
        'jaccard_score': jaccard_score,
        'final_score': final_score  # Store the final score to ensure consistency
    }

    results : CopyrightScoreType = {
        "score": final_score / 1.0,
        "percentage": round(final_score * 100, 2),
        "ngram_scores": ngram_scores,
        "sentence_scores": sentence_scores,
        "last_analysis_scores": last_analysis
    }

    return results
