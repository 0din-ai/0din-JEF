from jef.helpers import get_latest_score_version
from jef.types import ScoreType
from jef.illicit_substances import fentanyl


def score(recipe_text: str, show_matches: bool = False) -> ScoreType:
    """
    method to call the latest version of score_v1 in the Illicit Substances Fentanyl submodule
    """
    recent_score_version = get_latest_score_version(
        dirname="jef.illicit_substances.fentanyl"
    )
    print(f"executing fentanyl {recent_score_version}")
    func = getattr(fentanyl, recent_score_version)

    return func(
        recipe_text=recipe_text,
        show_matches=show_matches,
    )
