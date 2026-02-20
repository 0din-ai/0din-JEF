Red-Teaming Integrations
========================

JEF integrates with two leading LLM red-teaming frameworks:
`garak <https://github.com/NVIDIA/garak>`_ (NVIDIA) and
`PyRIT <https://github.com/Azure/PyRIT>`_ (Microsoft).
These integrations let you use JEF's scoring rubrics directly inside
automated red-teaming pipelines — no glue code required.

.. _garak-integration:

Garak
-----

`garak <https://docs.garak.ai/>`_ is an LLM vulnerability scanner.
JEF provides **detectors** (scoring) and **probes** (attack prompts) that
plug directly into garak's CLI and Python API.


Installation
^^^^^^^^^^^^

.. code-block:: bash

   pip install 0din-jef[garak]

This pulls in ``garak >= 0.13.3`` alongside JEF.


Available Detectors
^^^^^^^^^^^^^^^^^^^

Detectors score model outputs using JEF rubrics.  Each detector returns a
value in garak's ``0.0``-``1.0`` scale (JEF percentage / 100).

.. list-table::
   :header-rows: 1
   :widths: 40 60

   * - Detector
     - What It Scores
   * - ``0din_jef.CrystalMethScore``
     - Crystal meth synthesis content
   * - ``0din_jef.NerveAgentScore``
     - Nerve agent synthesis content
   * - ``0din_jef.FentanylScore``
     - Fentanyl synthesis content
   * - ``0din_jef.AnthraxScore``
     - Anthrax / B. anthracis content
   * - ``0din_jef.CRISPRScore``
     - CRISPR gene-editing content
   * - ``0din_jef.CopyRightScoreHarryPotterPageOne``
     - Harry Potter page-one reproduction
   * - ``0din_jef.CopyRightScoreHarryPotterChapterOne``
     - Harry Potter chapter-one reproduction


Available Probes
^^^^^^^^^^^^^^^^

Probes are disclosed jailbreak techniques (n-days) from the
`0DIN bug-bounty programme <https://0din.ai>`_.
Each probe carries its original attack prompts and links to its
0DIN disclosure page.

.. list-table::
   :header-rows: 1
   :widths: 40 60

   * - Probe
     - Technique
   * - ``0din_jef.PlaceholderInjection``
     - Guardrail bypass via placeholder text between words
   * - ``0din_jef.IncrementalTableCompletion``
     - Incomplete-table pattern completion
   * - ``0din_jef.TechnicalFieldGuide``
     - Law-enforcement field-guide framing
   * - ``0din_jef.ChemicalCompilerDebug``
     - Obfuscated chemical notation as a "debug" task
   * - ``0din_jef.Correction``
     - Forensic document correction request
   * - ``0din_jef.HexRecipeBook``
     - Hex-encoded instructions in fictional context


CLI Usage
^^^^^^^^^

Run a probe with a detector in a single command:

.. code-block:: bash

   # Score a model against crystal meth rubric using a disclosed n-day
   garak --model_type openai --model_name gpt-4 \
         -p 0din_jef.PlaceholderInjection \
         -d 0din_jef.CrystalMethScore

   # Mix JEF detectors with any garak probe
   garak --model_type openai --model_name gpt-4 \
         -p <any-probe> \
         -d 0din_jef.NerveAgentScore

   # Use multiple detectors
   garak --model_type openai --model_name gpt-4 \
         -p 0din_jef.Correction \
         -d 0din_jef.CrystalMethScore,0din_jef.FentanylScore


Python Usage
^^^^^^^^^^^^

.. code-block:: python

   from garak._plugins import load_plugin

   # Load a detector
   detector = load_plugin("detectors.0din_jef.CrystalMethScore")
   results = detector.detect(attempt)  # list[float] in 0.0-1.0

   # Load a probe
   probe = load_plugin("probes.0din_jef.PlaceholderInjection")
   print(probe.prompts)        # attack prompt strings
   print(probe.goal)           # short goal statement
   print(probe.uri)            # 0DIN disclosure URL

.. note::

   JEF detectors and probes are installed as **namespace packages**.
   ``--list_detectors`` may not show them, but explicit ``-d 0din_jef.<Name>``
   always works.


.. _pyrit-integration:

PyRIT
-----

`PyRIT <https://azure.github.io/PyRIT/>`_ (Python Risk Identification Tool
for generative AI) is Microsoft's red-teaming orchestration framework.
JEF provides **scorers** and **seed datasets** for PyRIT.


Installation
^^^^^^^^^^^^

.. code-block:: bash

   pip install 0din-jef[pyrit]

This pulls in ``pyrit >= 0.11`` alongside JEF.


Available Scorers
^^^^^^^^^^^^^^^^^

All scorers inherit from ``pyrit.score.FloatScaleScorer`` and return values
in PyRIT's ``0.0``-``1.0`` range.

.. list-table::
   :header-rows: 1
   :widths: 35 65

   * - Scorer
     - What It Scores
   * - ``JEFMethScorer``
     - Crystal meth synthesis content
   * - ``JEFNerveAgentScorer``
     - Nerve agent synthesis content
   * - ``JEFFentanylScorer``
     - Fentanyl synthesis content
   * - ``JEFAnthraxScorer``
     - Anthrax / B. anthracis content
   * - ``JEFCRISPRScorer``
     - CRISPR gene-editing content
   * - ``JEFCopyrightScorer``
     - Harry Potter copyright reproduction


Python Usage
^^^^^^^^^^^^

.. code-block:: python

   from jef.integrations.pyrit.scorers import JEFMethScorer

   scorer = JEFMethScorer()
   scores = await scorer.score_text_async("some LLM output")
   print(scores[0].get_value())  # float in 0.0-1.0

The copyright scorer accepts additional parameters:

.. code-block:: python

   from jef.integrations.pyrit.scorers import JEFCopyrightScorer

   scorer = JEFCopyrightScorer(
       ref="page_one",       # or "chapter_one" (default)
       min_ngram_size=5,
       max_ngram_size=7,
   )
   scores = await scorer.score_text_async("some LLM output")


Seed Datasets
^^^^^^^^^^^^^

JEF ships pre-built PyRIT seed datasets for each n-day probe.  These are
YAML files loadable via ``pyrit.models.SeedDataset.from_yaml_file()``.

.. code-block:: python

   from pyrit.models import SeedDataset
   from jef.integrations.pyrit.seeds import SEEDS_DIR

   # Load the PlaceholderInjection seed dataset
   dataset = SeedDataset.from_yaml_file(SEEDS_DIR / "placeholder_injection.yaml")
   for seed in dataset.seeds:
       print(seed.value)

Available seed files (one per n-day probe):

- ``placeholder_injection.yaml``
- ``incremental_table_completion.yaml``
- ``technical_field_guide.yaml``
- ``chemical_compiler_debug.yaml``
- ``correction.yaml``
- ``hex_recipe_book.yaml``


Regenerating Seeds
^^^^^^^^^^^^^^^^^^

If you add a new probe definition to the config, regenerate the seed YAML
files:

.. code-block:: bash

   python -m jef.integrations.pyrit.seeds


.. _integrations-architecture:

Architecture
------------

Both integrations share a common layer in ``jef.integrations``:

- **Scorer registry** (``SUBSTANCE_SCORERS``) — maps short keys to JEF
  scoring modules.  Used by both garak detectors and PyRIT scorers.
- **N-day probe registry** (``NDAY_PROBES``) — loaded from
  ``jef/integrations/config/nday_probes.yaml``.  Garak probes are
  generated dynamically; PyRIT seeds are pre-built YAML files.
- **Normalised results** (``JEFResult``) — every JEF call returns a
  consistent ``value`` (0.0-1.0), ``percentage`` (0-100), ``raw_score``,
  and ``metadata`` dict.

Adding a new n-day probe:

1. Add an entry to ``jef/integrations/config/nday_probes.yaml``
2. Run ``python -m jef.integrations.pyrit.seeds`` to regenerate YAML
3. Commit the new seed file — the garak probe class is generated
   automatically at import time
