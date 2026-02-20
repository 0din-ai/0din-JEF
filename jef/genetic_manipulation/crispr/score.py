from jef.helpers import get_latest_score_version
from jef.types import ScoreType
from jef.genetic_manipulation import crispr


def score(recipe_text: str, show_matches: bool = False) -> ScoreType:
    """
    method to call the latest version of score_v1 in the Genetic Manipulation CRISPR submodule
    """
    recent_score_version = get_latest_score_version(
        dirname="jef.genetic_manipulation.crispr"
    )
    print(f"executing crispr {recent_score_version}")
    func = getattr(crispr, recent_score_version)

    return func(
        recipe_text=recipe_text,
        show_matches=show_matches,
    )
