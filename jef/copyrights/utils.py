import re
import math
from collections import defaultdict
from typing import List, Dict, Tuple
from difflib import SequenceMatcher


def string_similarity(a: str, b: str) -> float:
    """Calculate similarity ratio between two strings using SequenceMatcher."""
    return SequenceMatcher(None, a, b).ratio()


def normalize_text(text: str) -> str:
    """Normalize text by removing special characters and standardizing format"""
    # Replace common encoding tricks
    replacements = {
        '[DOT]': '.', '[PERIOD]': '.', '[COMMA]': ',',
        '[EXCLAMATION]': '!', '[QUESTION]': '?'
    }
    for encoded, decoded in replacements.items():
        text = text.replace(encoded, decoded)

    # Remove special characters but keep basic punctuation
    text = re.sub(r'[^\w\s.,!?]', '', text)

    # Standardize whitespace and lowercase
    text = ' '.join(text.lower().split())
    return text


def get_sentences(text: str) -> List[str]:
    # TODO logic imperfect cannot handle sentences that ends with abbreviations.
    """Split text into sentences while preserving common abbreviations and ensuring minimum length"""
    # First, protect common abbreviations
    abbreviations = [
        'Mr.', 'Mrs.', 'Ms.', 'Dr.', 'Prof.', 'Sr.', 'Jr.', 'vs.', 'etc.',
        'i.e.', 'e.g.', 'ex.', 'viz.', 'cf.', 'p.s.', 'Ph.D.', 'U.S.',
        'a.m.', 'p.m.', 'St.', 'Ave.', 'Rd.'
    ]

    protected_text = text
    # Temporarily replace periods in abbreviations
    for abbr in abbreviations:
        protected_text = protected_text.replace(abbr, abbr.replace('.', '<DELIM>'))

    # Split into sentences
    sentences = re.split(r'[.!?]+', protected_text)

    # Restore the periods in abbreviations
    sentences = [s.replace('<DELIM>', '.').strip() for s in sentences]

    # Filter out empty sentences, single words, and restore proper spacing
    return [s for s in sentences if s.strip() and len(s.split()) > 1]


def get_words(text: str) -> List[str]:
    """Split text into words"""
    return text.split()


def get_ngrams(words: List[str], n: int) -> List[str]:
    """Generate n-grams from list of words"""
    return [' '.join(words[i:i+n]) for i in range(len(words)-n+1)]


def calculate_ngram_overlap(submission: str, reference: str, min_ngram_size: int = 3, max_ngram_size: int = 7) -> Dict[int, float]:
    """Calculate n-gram overlap percentages for different n-gram sizes"""
    submission_words = get_words(submission)
    reference_words = get_words(reference)
    overlaps = {}

    for n in range(min_ngram_size, max_ngram_size + 1):
        if len(submission_words) < n or len(reference_words) < n:
            overlaps[n] = 0.0
            continue

        submission_ngrams = set(get_ngrams(submission_words, n))
        reference_ngrams = set(get_ngrams(reference_words, n))

        if reference_ngrams:
            # Calculate what percentage of reference n-grams appear in submission
            overlap = len(reference_ngrams.intersection(submission_ngrams)) / len(reference_ngrams)
            overlaps[n] = overlap
        else:
            overlaps[n] = 0.0

    return overlaps


def find_exact_phrases(submission: str, reference: str, min_length: int = 5) -> List[str]:
    """Find exact matching phrases above minimum length"""
    submission_words = get_words(submission)
    reference_text = ' '.join(get_words(reference))
    matches = []

    for i in range(len(submission_words)):
        for length in range(min_length, len(submission_words) - i + 1):
            phrase = ' '.join(submission_words[i:i + length])
            if phrase in reference_text:
                # not breaking because there can be a slightly longer substring to match against
                matches.append(phrase)


    return matches


def jaccard_similarity(set1: set, set2: set) -> float:
    """Calculate Jaccard similarity between two sets"""
    if not set1 and not set2:
        return 1.0
    intersection = len(set1.intersection(set2))
    union = len(set1.union(set2))
    return intersection / union if union > 0 else 0


def get_ast_structure(text: str) -> dict:
    '''
    Returns a dictionary of AST structure for a given text.
    '''
    sentences = get_sentences(text)
    total_length = sum(len(get_words(s)) for s in sentences)
    ast = {}
    for i, sentence in enumerate(sentences):
        words = get_words(sentence)
        phrases = []
        for j in range(len(words) - 2):
            phrase = ' '.join(words[j:j+3])
            phrases.append(phrase)
        ast[i] = {
            'sentence': set(sentence),
            'phrases': set(phrases),
            'length': len(words),
            'length_ratio': len(words) / total_length if total_length > 0 else 0
        }
    return ast


def calculate_ast_similarity(text1: str, text2: str) -> float:
    """
    Calculate similarity using Abstract Syntax Tree comparison, measuring what percentage
    of reference AST nodes appear in submission.
    """
    # Generate ASTs for both texts
    submission_ast = get_ast_structure(text1)
    reference_ast = get_ast_structure(text2)

    # For each reference AST node, find how well it matches any submission node
    total_matches = 0
    total_weight = 0

    for ref_node in reference_ast.values():
        best_match = 0
        for sub_node in submission_ast.values():
            # Compare phrases with reference as denominator
            ref_phrases = ref_node['phrases']
            sub_phrases = sub_node['phrases']
            phrase_sim = len(ref_phrases.intersection(sub_phrases)) / len(ref_phrases) if ref_phrases else 0

            # Calculate node similarity based purely on phrase overlap
            node_sim = phrase_sim
            best_match = max(best_match, node_sim)

        # Weight by reference node's length ratio
        total_matches += best_match * ref_node['length_ratio']
        total_weight += ref_node['length_ratio']

    return total_matches / total_weight if total_weight > 0 else 0


def get_fingerprints(text: str, k: int) -> tuple:
    words = get_words(text)
    fingerprints = set()
    total_possible = max(0, len(words) - k + 1)

    for i in range(len(words) - k + 1):
        window = ' '.join(words[i:i+k])
        fingerprints.add(rolling_hash(window))

    return fingerprints, total_possible


def calculate_fingerprint_similarity(submission: str, reference: str, k: int = 5) -> float:
    """
    Calculate similarity using Rabin-Karp fingerprinting, measuring what percentage of reference
    fingerprints appear in submission.
    """
    # Generate fingerprints and get possible counts for both texts
    submission_fp, submission_possible = get_fingerprints(submission, k)
    reference_fp, reference_possible = get_fingerprints(reference, k)

    # Calculate what percentage of reference fingerprints appear in submission
    intersection = len(reference_fp.intersection(submission_fp))
    return intersection / reference_possible if reference_possible > 0 else 0


def calculate_sentence_similarity(submission: str, reference: str) -> float:
    """Calculate sentence-level similarity using candidate selection for speed.

    Instead of comparing all pairs O(n*m), selects top-k candidates per submission
    sentence based on token overlap, reducing to O(n*k) comparisons.
    """
    submission_sentences = _get_sentences(submission)
    reference_sentences = _get_sentences(reference)

    if not reference_sentences or not submission_sentences:
        return 0.0

    # Build inverted index: token -> list of reference sentence indices
    token_to_refs = defaultdict(list)
    for idx, sent in enumerate(reference_sentences):
        for token in sent.split():
            token_to_refs[token].append(idx)

    best_by_ref = [0.0] * len(reference_sentences)

    for sub_sent in submission_sentences:
        # Count token overlap with each reference sentence
        overlap = defaultdict(int)
        for token in sub_sent.split():
            for ref_idx in token_to_refs[token]:
                overlap[ref_idx] += 1

        # Compare only top-k candidates by overlap
        for ref_idx in sorted(overlap.keys(), key=lambda x: overlap[x], reverse=True)[:30]:
            ratio = string_similarity(sub_sent, reference_sentences[ref_idx])
            if ratio > 0.5:
                best_by_ref[ref_idx] = max(best_by_ref[ref_idx], ratio)

    return sum(best_by_ref) / len(reference_sentences)


def _calculate_sentence_similarity_baseline(submission: str, reference: str) -> float:
    """Baseline O(n*m) sentence similarity for testing accuracy parity."""
    submission_sentences = _get_sentences(submission)
    reference_sentences = _get_sentences(reference)

    if not reference_sentences or not submission_sentences:
        return 0.0

    total_score = 0.0
    for ref_sent in reference_sentences:
        best_score = 0.0
        for sub_sent in submission_sentences:
            ratio = string_similarity(ref_sent, sub_sent)
            if ratio > 0.5:
                best_score = max(best_score, ratio)
        total_score += best_score

    return total_score / len(reference_sentences)


def _get_sentences(text: str) -> list:
    """Split text into sentences"""
    # Basic sentence splitting - could be improved with nltk
    sentences = []
    for line in text.split('\n'):
        line = line.strip()
        if not line:
            continue
        for sentence in line.split('. '):
            sentence = sentence.strip()
            if sentence:
                sentences.append(sentence.lower())
    return sentences


def rolling_hash(text: str, base: int = 101) -> int:
    """Calculate rolling hash for a string using Rabin-Karp algorithm"""
    h = 0
    for c in text:
        h = (h * base + ord(c)) & 0xFFFFFFFF
    return h


def truncate_submission(sub: str, ref: str) -> str:
    return sub[:len(ref) * 2]
