# JEF Command-Line Interfaces

The Jailbreak Evaluation Framework (JEF) provides two distinct command-line interfaces to suit different workflows: a standard, non-interactive CLI for scripting and an interactive menu-driven CLI for manual analysis.

---

## 1. Standard CLI (`jef`)

**Use Case:** This interface is ideal for **automation, scripting, and integration** into other tools. It allows for direct, non-interactive execution of JEF's scoring and calculation functions.

### How to Run

The standard CLI is accessed through the `jef` command, which is configured as a script entry point in `pyproject.toml`. If the package is installed correctly, you can run it directly.

If not running from an installed package, you can invoke it via `python -m jef.cli`.

### User Flow & Commands

The basic flow is to call `jef` followed by a subcommand representing the desired analysis.

-   If you run `jef` with no arguments, it will display a detailed help screen with descriptions of the available tests and usage examples.
-   Use `jef <command> --help` to get help for a specific command.

#### Available Commands:

-   **`score_tiananmen <text>`**: Analyzes input text for facts related to the 1989 Tiananmen Square events.
-   **`score_agent_recipe <text>`**: Scans input text for instructions on synthesizing nerve agents.
-   **`score_meth_recipe <text>`**: Scans input text for instructions on synthesizing methamphetamine.
-   **`copyright_score_hp <text> <reference>`**: Checks for copyright violations against a provided Harry Potter reference text.
-   **`copyright_detector <text> <reference>`**: Performs a general copyright infringement analysis against a provided reference text.
-   **`jef_score --bv <float> --bm <float> --rt <float> --fd <float>`**: Calculates the final JEF score from its four core components, each on a scale from 0.0 to 1.0.
-   **`jef_calculator --num_vendors <int> --num_models <int> ...`**: Calculates the JEF score from raw metric data, such as the number of affected vendors/models and a list of fidelity scores.

### Examples

```bash
# Get the main help screen
jef

# Score a string against Tiananmen Square facts
jef score_tiananmen "This text contains some historical information."

# Calculate the JEF score from raw data
jef jef_calculator --num_vendors 3 --num_models 7 --num_subjects 2 --scores 80 90 75

# Get help for a specific command
jef score_agent_recipe --help
```

---

## 2. Interactive Menu CLI (`jef-menu`)

**Use Case:** This interface is designed for **manual use, exploration, and easy analysis of local files**. It provides a user-friendly, menu-driven interface to navigate your filesystem, select files, and run JEF analyses on them.

### How to Run

To start the interactive menu, execute the `jef.menu_cli` module directly with Python:

```bash
python -m jef.menu_cli
```
*Note: There is also a `run_jef_menu.bat` script for convenience on Windows.*

### User Flow

1.  **Launch**: Run the command above. The JEF header will appear, and you will be placed in an interactive file browser showing the contents of your current directory.
2.  **Navigate**:
    *   Use the **arrow keys** (Up/Down) to highlight an item.
    *   Press **Enter** to select it.
    *   You can select `[..] Go up one directory` to navigate up the directory tree.
    *   You can select a folder to enter it.
3.  **Select a File**: When you select a file, you will be taken to the analysis menu.
4.  **Choose Analysis**: A new menu will appear listing all available JEF analysis types (e.g., "Tiananmen Square Analysis", "Nerve Agent Detection").
    *   Select the analysis you want to perform on the file's content.
5.  **Provide Input (if required)**: For copyright-related analyses, you will be prompted to enter the reference text to compare against.
6.  **View Results**: The analysis will run, and the results will be displayed on the screen.
7.  **Continue**: Press **Enter** to return to the file browser.
8.  **Exit**: Select `[EXIT] Quit JEF Menu` or press `Ctrl+C` to close the application.

### Fallback Mode

If the `questionary` library is not installed or your terminal does not support the interactive menu, the application will automatically switch to a simplified **fallback mode**. In this mode, you navigate and make selections by typing numbers instead of using arrow keys. The user flow remains functionally the same.