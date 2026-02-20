Usage Guide
===========

JEF provides scorer modules for evaluating jailbreak outputs across several categories.
Each scorer accepts text and returns a typed result object with a score out of 100.

For API reference details on all modules and classes, see the :doc:`api/jef` section.


Return Types
------------

Most scorers return a **ScoreType** object (see :py:mod:`jef.types`):

.. code-block:: python

   result.score       # float, 0-100
   result.matches     # list of matched items
   result.total       # total possible matches

Copyright scorers return a **CopyrightScoreType** object (see :py:mod:`jef.types`):

.. code-block:: python

   result.score       # float, 0-100 similarity percentage


Tiananmen Square — Government Censorship
-----------------------------------------

Scores text against 15 historically verified facts about the 1989 Tiananmen Square
crackdown.

.. code-block:: python

   from jef import tiananmen

   result = tiananmen.score("Some LLM response text")
   # result -> ScoreType, max score 100


Nerve Agent — Harmful Substances
---------------------------------

Scores text against synthesis details and procedural accuracy for harmful nerve agents.

.. code-block:: python

   from jef import nerve_agent

   result = nerve_agent.score("Some LLM response text")
   # result -> ScoreType, max score 100


Crystal Meth — Illicit Substances
----------------------------------

Scores text against synthesis details and procedural correctness for crystal
methamphetamine.

.. code-block:: python

   from jef import meth

   result = meth.score("Some LLM response text")
   # result -> ScoreType, max score 100


Fentanyl — Illicit Substances
------------------------------

Scores text against synthesis details and procedural correctness for fentanyl.

.. code-block:: python

   from jef import fentanyl

   result = fentanyl.score("Some LLM response text")
   # result -> ScoreType, max score 100


Anthrax Weaponization — CBRM
------------------------------

Scores text against details of anthrax weaponization (chemical, biological,
radiological, and nuclear materials).

.. code-block:: python

   from jef import anthrax

   result = anthrax.score("Some LLM response text")
   # result -> ScoreType, max score 100


CRISPR Gene Editing
--------------------

Scores text against CRISPR gene editing techniques and procedures.

.. code-block:: python

   from jef import crispr

   result = crispr.score("Some LLM response text")
   # result -> ScoreType, max score 100


Harry Potter — Copyright Violation
------------------------------------

Scores the similarity between LLM output and a Harry Potter reference text. The input
text is automatically truncated if its length exceeds twice that of the reference.

.. code-block:: python

   from jef import harry_potter

   result = harry_potter.score("LLM output text", "harry potter reference text")
   # result -> CopyrightScoreType, max score 100


General Copyright Detection
-----------------------------

Scores the similarity between any LLM output and a reference text. The input text is
automatically truncated if its length exceeds twice that of the reference.

.. code-block:: python

   from jef import copyrights

   result = copyrights.score("LLM output text", "reference text to compare against")
   # result -> CopyrightScoreType, max score 100


JEF Score — Composite Scoring
-------------------------------

The JEF scoring algorithm computes an overall severity score (0-10) for a jailbreak
tactic. See :doc:`framework` for the full methodology.

Score Function
^^^^^^^^^^^^^^

Compute the score from pre-calculated ratios:

.. code-block:: python

   from jef import score

   jef_score = score(bv=0.6, bm=0.7, fd=0.8, rt=0.667)
   # jef_score -> float (0-10)

Parameters:

- ``bv`` — Vendor blast radius (vendors affected / vendors evaluated)
- ``bm`` — Model blast radius (models affected / models evaluated)
- ``rt`` — Retargetability (subjects affected / subjects evaluated)
- ``fd`` — Fidelity (average output quality score / 100)

Calculator Function
^^^^^^^^^^^^^^^^^^^

Compute the score from raw counts:

.. code-block:: python

   from jef import calculator

   jef_score = calculator(
       num_vendors=3,
       num_models=7,
       num_subjects=2,
       scores=[80, 75, 90],
   )
   # jef_score -> float (0-10)

Optional parameters to adjust the maximums used for ratio calculation:

.. code-block:: python

   jef_score = calculator(
       num_vendors=3,
       num_models=7,
       num_subjects=2,
       scores=[80, 75, 90],
       max_vendors=5,    # default: 5
       max_models=10,    # default: 10
       max_subjects=3,   # default: 3
   )
