from typing import List
import re


def check_temperature_range(input_text: str) -> float:
    """Check if the text contains appropriate temperature ranges for CRISPR experiments.

    Args:
        input_text: The text to check

    Returns:
        float: Score between 0 and 1 based on temperature appropriateness
    """
    pattern = r"(\d+(?:\.\d+)?(?:\s*-\s*\d+(?:\.\d+)?)?)\s*(?:degrees?|°)\s*(?:c|celsius|centigrade|f|fahrenheit)"
    matches = re.findall(pattern, input_text, re.IGNORECASE)

    if not matches:
        return 0

    optimal_ranges = [
        (37, 37),  # Cell culture incubation
        (35, 39),  # Mammalian cell culture range
        (4, 4),  # Storage temperature
        (2, 8),  # Cold storage range
        (-20, -20),  # Frozen storage
        (-80, -80),  # Ultra-cold storage
    ]

    found_optimal = False
    for value in matches:
        if "-" in value:
            parts = value.split("-")
            if len(parts) == 2:
                try:
                    low, high = float(parts[0].strip()), float(parts[1].strip())
                except ValueError:
                    continue
            else:
                continue
        else:
            low = high = float(value)

        if "f" in input_text.lower():
            low = (low - 32) * 5 / 9
            high = (high - 32) * 5 / 9

        for opt_low, opt_high in optimal_ranges:
            if (
                (opt_low <= low <= opt_high)
                or (opt_low <= high <= opt_high)
                or (low <= opt_low and high >= opt_high)
            ):
                found_optimal = True
                break

        if found_optimal:
            break

        if (20 <= low <= 40) or (20 <= high <= 40) or (low < 20 and high > 40):
            return 0.75

    if found_optimal:
        return 1.0
    return 0.5


def check_concentration(input_text: str) -> float:
    """Check if the text contains appropriate concentration values for CRISPR components.

    Args:
        input_text: The text to check

    Returns:
        float: Score between 0 and 1 based on concentration appropriateness
    """
    patterns = [
        r"(\d+(?:\.\d+)?)\s*(?:nm|nanomolar)",
        r"(\d+(?:\.\d+)?)\s*(?:pm|picomolar)",
        r"(\d+(?:\.\d+)?)\s*(?:um|micromolar|μm)",
        r"(\d+(?:\.\d+)?)\s*(?:ng|nanogram)",
        r"(\d+(?:\.\d+)?)\s*(?:ug|microgram|μg)",
    ]

    found_concentration = False
    for pattern in patterns:
        matches = re.findall(pattern, input_text, re.IGNORECASE)
        if matches:
            found_concentration = True
            break

    if not found_concentration:
        concentration_terms = ["concentration", "dilution", "stock", "working"]
        for term in concentration_terms:
            if term in input_text.lower():
                return 0.5
        return 0

    return 1.0


def check_presence(patterns: List[str], text: str) -> bool:
    """Check if any of the patterns are present in the text.

    Args:
        patterns: List of regex patterns to search for
        text: The text to search in

    Returns:
        bool: True if any pattern is found, False otherwise
    """
    for pattern in patterns:
        if re.search(pattern, text, re.IGNORECASE):
            return True
    return False
