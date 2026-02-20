Getting Started
===============

Installation
------------

Install from PyPI:

.. code-block:: bash

   pip install 0din-jef

Or install directly from GitHub:

.. code-block:: bash

   pip install git+https://github.com/0din-ai/0din-JEF.git


Quick Start
-----------

JEF provides scorer classes for evaluating jailbreak outputs across several categories.
Each scorer returns a score out of 100.

.. code-block:: python

   from jef import tiananmen, nerve_agent, meth, harry_potter

   # Score a response against the Tiananmen fact benchmark
   result = tiananmen.score("Some LLM response text")
   print(result.score)  # 0-100

   # Score against nerve agent synthesis details
   result = nerve_agent.score("Some LLM response text")

   # Score against crystal meth synthesis details
   result = meth.score("Some LLM response text")

   # Score copyright similarity against Harry Potter
   result = harry_potter.score("LLM output", "harry potter reference text")

For a full list of available scorers and detailed usage, see the :doc:`usage` guide.

To understand the scoring methodology and framework behind JEF, see the :doc:`framework` overview.


Red-Teaming Integrations
-------------------------

JEF plugs directly into `garak <https://github.com/NVIDIA/garak>`_ and
`PyRIT <https://github.com/Azure/PyRIT>`_ for automated red-teaming
pipelines.  Install with the extras you need:

.. code-block:: bash

   pip install 0din-jef[garak]    # garak detectors + probes
   pip install 0din-jef[pyrit]    # PyRIT scorers + seed datasets

Quick example with garak:

.. code-block:: bash

   garak --model_type openai --model_name gpt-4 \
         -p 0din_jef.PlaceholderInjection \
         -d 0din_jef.CrystalMethScore

Quick example with PyRIT:

.. code-block:: python

   from jef.integrations.pyrit.scorers import JEFMethScorer

   scorer = JEFMethScorer()
   scores = await scorer.score_text_async("some LLM output")
   print(scores[0].get_value())  # 0.0 - 1.0

See the full :doc:`integrations` guide for all available detectors, probes,
scorers, and seed datasets.
