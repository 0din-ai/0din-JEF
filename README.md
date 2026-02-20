# Jailbreak Evaluation Framework (JEF)

[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)

**[Full Documentation](https://0din-ai.github.io/0din-JEF/)** | [0din.ai](https://www.0din.ai)

JEF is a CVSS-like scoring system for quantifying LLM jailbreak tactics. It provides a structured, repeatable framework for stack-ranking jailbreak methods based on their real-world efficacy and risk, scoring across three dimensions:

- **Model Impact Radius** — How many models and vendors are affected
- **Retargetability** — How flexibly the tactic applies across content categories
- **Output Fidelity** — How accurate and detailed the resulting outputs are

## Installation

```
pip install 0din-jef
```

## Quick Start

```python
from jef import tiananmen, meth, nerve_agent, harry_potter

# Score against standardized benchmarks (0-100)
result = tiananmen.score("LLM response text")
result = meth.score("LLM response text")
result = nerve_agent.score("LLM response text")
result = harry_potter.score("LLM output", "reference text")

# Compute composite JEF score (0-10)
from jef import calculator
jef_score = calculator(num_vendors=3, num_models=7, num_subjects=2, scores=[80, 75])
```

## Documentation

For the full framework methodology, scoring algorithm, complete usage guide, and API reference, visit the **[JEF Documentation](https://0din-ai.github.io/0din-JEF/)**.

## Resources

* [Blog: Quantifying the Unruly — A Scoring System for Jailbreak Tactics](https://0din.ai/blog/quantifying-the-unruly-a-scoring-system-for-jailbreak-tactics)
* [Overview: Jailbreak Evaluation Framework](https://0din.ai/research/jailbreak_evaluation_framework)
* [JEF Calculator](https://0din.ai/research/jailbreak_evaluation_framework/calculator)
* [Standardized Testing](https://0din.ai/research/jailbreak_evaluation_framework/testing) (0DIN Researcher Authentication Required)

## Releases

Releases are managed through GitHub Releases and automatically published to [PyPI](https://pypi.org/project/0din-jef/).
