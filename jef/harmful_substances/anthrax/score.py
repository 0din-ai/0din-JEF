from jef.helpers import get_latest_score_version
from jef.types import ScoreType
from jef.harmful_substances import anthrax


def score(recipe_text: str, show_matches: bool = False) -> ScoreType:
    """
    method to call the latest version of score_v1 in the Harmful Substances Anthrax submodule
    """
    recent_score_version = get_latest_score_version(
        dirname="jef.harmful_substances.anthrax"
    )
    print(f"executing anthrax {recent_score_version}")
    func = getattr(anthrax, recent_score_version)

    return func(
        recipe_text=recipe_text,
        show_matches=show_matches,
    )
