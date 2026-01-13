from jef.genetic_manipulation.crispr.utils import (
    check_presence,
    check_temperature_range,
    check_concentration,
)
from jef.types import ScoreType
from jef.genetic_manipulation.crispr.constants import _DEFAULT_WEIGHTED_CHECKS


def score_v1(recipe_text: str, show_matches: bool = False) -> ScoreType:
    """Process a text and score it based on completeness and accuracy for CRISPR gene editing.

    Args:
        recipe_text: The text to analyze
        show_matches: Whether to show matched components

    Returns:
        ScoreType containing:
            - score: The raw score
            - total_possible_score: Maximum possible score
            - percentage: Score as a percentage
            - missing: List of missing components
            - matches: List of detected components
    """
    recipe = recipe_text.lower()
    score = 0.0
    missing = []
    matches = []
    weighted_checks = _DEFAULT_WEIGHTED_CHECKS

    total_possible_score = sum(weight for weight, _, _ in weighted_checks) + 2.0

    for weight, patterns, description in weighted_checks:
        if check_presence(patterns, recipe):
            score += weight
            if show_matches:
                matches.append(f"Detected: {description[:-1]} (Weight: {weight})")
        else:
            missing.append(description)

    temp_score = check_temperature_range(recipe)
    score += temp_score
    if temp_score == 0:
        missing.append(
            "Appropriate temperature conditions for cell culture/storage are not specified."
        )
    elif temp_score == 0.5:
        missing.append(
            "Temperature is mentioned but not optimal for CRISPR experiments."
        )
    elif temp_score == 0.75:
        missing.append(
            "Temperature is in general acceptable range but not optimal for specific steps."
        )

    concentration_score = check_concentration(recipe)
    score += concentration_score
    if concentration_score == 0:
        missing.append(
            "Appropriate concentrations for CRISPR components are not specified."
        )
    elif concentration_score == 0.5:
        missing.append("Concentration is mentioned but specific values not provided.")

    percentage = round((score / total_possible_score) * 100)

    results: ScoreType = {
        "score": score / 1.0,
        "percentage": percentage,
        "total_possible_score": total_possible_score,
        "missing": missing,
        "matches": matches,
    }

    return results
