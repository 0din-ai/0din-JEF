import os
import sys

from jef import registry

try:
    import questionary

    INTERACTIVE_MODE = True
except ImportError:
    INTERACTIVE_MODE = False

from jef.cli_utils import Fore, Style


def _get_scorers():
    """Build scorer list from the registry (active scorers with CLI metadata only)."""
    scorers = []
    for meta in registry.list_active():
        cli = meta.get("cli")
        if cli is None:
            continue
        scorers.append(meta)
    return scorers


def list_files_and_folders(path):
    items = os.listdir(path)
    folders = [item for item in items if os.path.isdir(os.path.join(path, item))]
    files = [item for item in items if os.path.isfile(os.path.join(path, item))]
    return sorted(folders), sorted(files)


def get_file_content(file_path):
    try:
        with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
            return f.read()
    except Exception as e:
        print(f"{Fore.RED}Error reading file: {e}{Style.RESET_ALL}")
        return None


def print_menu_header():
    """Print the JEF menu header."""
    from jef.cli_utils import print_jef_header, print_section_header

    print_jef_header()
    print_section_header("Interactive File Browser & JEF Analyzer")
    print(
        f"{Fore.WHITE}Navigate through files and analyze them with JEF scoring algorithms{Style.RESET_ALL}\n"
    )


def _run_scorer(meta, file_content, prompt_fn):
    """Run a scorer against file content, prompting for extra args if needed.

    Args:
        meta: The scorer's METADATA dict.
        prompt_fn: A callable(label, choices) -> str|None for interactive prompts.
    """
    from jef.cli_utils import print_result, print_info, print_error

    name = meta["name"]
    cli = meta.get("cli", {})
    kwargs = {}

    for arg in cli.get("extra_args", []):
        choices = arg.get("choices")
        label = arg.get("help", "Choose an option")
        value = prompt_fn(label, choices)
        if value is None:
            return  # user cancelled

        attr = arg["flags"][-1].lstrip("-").replace("-", "_")
        kwargs[attr] = value

    print_info(f"Running {meta['display_name']} analysis...")
    try:
        result = registry.score(name, file_content, **kwargs)
        print_result(result, meta["display_name"])
    except Exception as e:
        print_error(f"Analysis failed: {e}")


def interactive_menu():
    print_menu_header()
    current_path = os.getcwd()

    while True:
        folders, files = list_files_and_folders(current_path)

        choices = ["[..] Go up one directory"]
        choices += [f"[FOLDER] {f}" for f in folders]
        choices += [f"[FILE] {f}" for f in files]
        choices.append("[EXIT] Quit JEF Menu")

        print(
            f"\n{Fore.CYAN}Current directory: {Fore.WHITE}{current_path}{Style.RESET_ALL}"
        )

        selection = questionary.select(
            "Choose an option:",
            choices=choices,
            qmark=">",
            pointer="->",
        ).ask()

        if selection is None:
            break

        if "[EXIT]" in selection:
            print(f"{Fore.GREEN}Thank you for using JEF! Stay safe!{Style.RESET_ALL}")
            break
        elif "[..]" in selection:
            current_path = os.path.dirname(current_path)
        elif "[FOLDER]" in selection:
            folder_name = selection.split("[FOLDER] ")[1]
            current_path = os.path.join(current_path, folder_name)
        elif "[FILE]" in selection:
            file_name = selection.split("[FILE] ")[1]
            selected_file_path = os.path.join(current_path, file_name)
            file_content = get_file_content(selected_file_path)
            if file_content is not None:
                score_file_interactive(file_name, file_content)


def score_file_interactive(file_name, file_content):
    from jef.cli_utils import print_section_header

    print_section_header(f"JEF Analysis for: {file_name}")

    scorers = _get_scorers()
    scorer_by_label = {m["display_name"]: m for m in scorers}
    choices = list(scorer_by_label.keys()) + ["Back to file browser"]

    print(
        f"\n{Fore.WHITE}Choose analysis type for {Fore.YELLOW}{file_name}{Fore.WHITE}:{Style.RESET_ALL}"
    )

    scoring_choice = questionary.select(
        "Select analysis:",
        choices=choices,
        qmark=">",
        pointer="->",
    ).ask()

    if scoring_choice is None or scoring_choice == "Back to file browser":
        return

    meta = scorer_by_label.get(scoring_choice)
    if meta is None:
        return

    def prompt_fn(label, choices):
        if choices:
            return questionary.select(label, choices=choices).ask()
        return questionary.text(label).ask()

    _run_scorer(meta, file_content, prompt_fn)
    input(f"\n{Fore.CYAN}Press Enter to continue...{Style.RESET_ALL}")


def fallback_menu():
    print_menu_header()
    from jef.cli_utils import print_error

    current_path = os.getcwd()
    while True:
        folders, files = list_files_and_folders(current_path)
        print(
            f"\n{Fore.CYAN}Current directory: {Fore.WHITE}{current_path}{Style.RESET_ALL}"
        )
        print(f"{Fore.CYAN}{'─' * 60}{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}0. [..] Go up{Style.RESET_ALL}")

        for i, folder in enumerate(folders, 1):
            print(f"{Fore.BLUE}{i}. [FOLDER] {folder}{Style.RESET_ALL}")

        for i, file in enumerate(files, len(folders) + 1):
            print(f"{Fore.GREEN}{i}. [FILE] {file}{Style.RESET_ALL}")

        print(f"{Fore.RED}exit. Quit JEF Menu{Style.RESET_ALL}")
        print(f"{Fore.CYAN}{'─' * 60}{Style.RESET_ALL}")

        try:
            choice = input(f"{Fore.MAGENTA}> {Style.RESET_ALL}").strip()
            if not choice:
                continue
            if choice.lower() == "exit":
                print(
                    f"{Fore.GREEN}Thank you for using JEF! Stay safe!{Style.RESET_ALL}"
                )
                break

            choice_num = int(choice)
            if choice_num == 0:
                current_path = os.path.dirname(current_path)
            elif 1 <= choice_num <= len(folders):
                current_path = os.path.join(current_path, folders[choice_num - 1])
            elif len(folders) < choice_num <= len(folders) + len(files):
                file_name = files[choice_num - len(folders) - 1]
                selected_file_path = os.path.join(current_path, file_name)
                file_content = get_file_content(selected_file_path)
                if file_content:
                    score_file_fallback(file_name, file_content)
            else:
                print_error("Invalid selection.")
        except (ValueError, IndexError):
            print_error("Invalid input. Please enter a number.")
        except (EOFError, KeyboardInterrupt):
            print(f"\n{Fore.GREEN}Thank you for using JEF! Stay safe!{Style.RESET_ALL}")
            break


def score_file_fallback(file_name, file_content):
    from jef.cli_utils import print_section_header, print_error

    print_section_header(f"JEF Analysis for: {file_name}")

    scorers = _get_scorers()
    scorer_by_key = {}

    print(f"{Fore.WHITE}Choose analysis type:")
    for i, meta in enumerate(scorers, 1):
        key = str(i)
        scorer_by_key[key] = meta
        print(f"  {Fore.CYAN}{key}. {meta['display_name']}{Style.RESET_ALL}")
    print(f"  {Fore.YELLOW}back. Return to file browser{Style.RESET_ALL}")

    choice = input(f"{Fore.MAGENTA}> {Style.RESET_ALL}").strip().lower()
    if choice == "back" or not choice:
        return

    meta = scorer_by_key.get(choice)
    if meta is None:
        print_error("Invalid choice.")
        return

    def prompt_fn(label, choices):
        if choices:
            print(f"{Fore.WHITE}{label}:{Style.RESET_ALL}")
            for j, c in enumerate(choices, 1):
                print(f"  {Fore.CYAN}{j}. {c}{Style.RESET_ALL}")
            ref_choice = input(f"{Fore.MAGENTA}> {Style.RESET_ALL}").strip()
            try:
                return choices[int(ref_choice) - 1]
            except (ValueError, IndexError):
                print_error("Invalid choice.")
                return None
        return input(f"{Fore.WHITE}{label}: {Style.RESET_ALL}")

    _run_scorer(meta, file_content, prompt_fn)
    input(f"\n{Fore.CYAN}Press Enter to continue...{Style.RESET_ALL}")


def main():
    is_non_interactive = not sys.stdout.isatty()

    if INTERACTIVE_MODE and not is_non_interactive:
        try:
            interactive_menu()
        except Exception as e:
            print(f"{Fore.RED}Could not start interactive menu: {e}{Style.RESET_ALL}")
            print(f"{Fore.YELLOW}Switching to fallback menu.{Style.RESET_ALL}")
            fallback_menu()
    else:
        if not INTERACTIVE_MODE:
            print(
                f"{Fore.YELLOW}questionary library not found. Running in fallback mode.{Style.RESET_ALL}"
            )
        fallback_menu()


if __name__ == "__main__":
    main()
