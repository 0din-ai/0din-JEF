# jef/__init__.py
from importlib.metadata import version, PackageNotFoundError

from . import chinese_censorship
from . import copyrights
from . import harmful_substances
from . import illicit_substances
from . import genetic_manipulation
from . import registry
from . import score_algos


calculator = score_algos.calculator
score = score_algos.score
__call__ = score

try:
    __version__ = version("0din-jef")
except PackageNotFoundError:
    # Package not installed (e.g., running from source checkout)
    __version__ = "0.0.0.dev0"
