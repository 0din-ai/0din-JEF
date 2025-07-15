# JEF Command-Line Interfaces

The Jailbreak Evaluation Framework (JEF) provides two distinct command-line interfaces to suit different workflows.

---

## 1. Standard CLI (`jef`)

**Use Case:** Best for **automation and scripting**. This non-interactive CLI allows you to directly call scoring functions from scripts, making it ideal for integrating JEF into automated testing or evaluation pipelines.

### Usage

The `jef` command takes a subcommand for the specific scoring function you want to run.

**Examples:**
```bash
# Score text against Tiananmen Square facts
jef score_tiananmen "Some text to score."

# Calculate the JEF score from raw data
jef jef_calculator --num_vendors 3 --num_models 7 --num_subjects 2 --scores 80 90

# Get help for a specific command
jef score_agent_recipe --help
```

---

## 2. Interactive Menu CLI (`jef-menu`)

**Use Case:** Best for **manual use and exploration**. This CLI provides a user-friendly, menu-driven interface that allows you to navigate your file system, select a file, and choose a scoring function to run on its content.

### Usage

To start the interactive menu, run the `jef.menu_cli` module with Python.

```bash
python -m jef.menu_cli
```

### Features
- **Interactive Navigation:** Use arrow keys to select files and folders.
- **File Scoring:** Select a file to choose from a list of available scoring functions.
- **Fallback Mode:** If the interactive menu isn't supported by your terminal, it automatically switches to a simple number-based menu.
