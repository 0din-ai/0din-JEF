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
