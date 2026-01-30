# jef/__init__.py
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
__version__ = "0.1.12"  # TODO-Update: this before each release
