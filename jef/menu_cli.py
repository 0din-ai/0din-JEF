import os
import sys
from jef import tiananmen, nerve_agent, meth, harry_potter, copyrights

try:
    import questionary
    INTERACTIVE_MODE = True
except (ImportError, Exception):
    INTERACTIVE_MODE = False

def list_files_and_folders(path):
    items = os.listdir(path)
    folders = [item for item in items if os.path.isdir(os.path.join(path, item))]
    files = [item for item in items if os.path.isfile(os.path.join(path, item))]
    return sorted(folders), sorted(files)

def get_file_content(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            return f.read()
    except Exception as e:
        print(f"Error reading file: {e}")
        return None

def interactive_menu():
    current_path = os.getcwd()
    while True:
        folders, files = list_files_and_folders(current_path)
        choices = ["[..]"] + [f"[FOLDER] {f}" for f in folders] + [f"[FILE] {f}" for f in files]
        
        selection = questionary.select(
            f"Current directory: {current_path}",
            choices=choices,
            qmark=">",
            pointer="->"
        ).ask()

        if selection is None: break
        if selection == "[..]":
            current_path = os.path.dirname(current_path)
        elif selection.startswith("[FOLDER]"):
            current_path = os.path.join(current_path, selection.replace("[FOLDER] ", ""))
        elif selection.startswith("[FILE]"):
            file_name = selection.replace("[FILE] ", "")
            selected_file_path = os.path.join(current_path, file_name)
            file_content = get_file_content(selected_file_path)
            if file_content is not None:
                score_file_interactive(file_name, file_content)

def score_file_interactive(file_name, file_content):
    scoring_functions = {
        "Score Tiananmen": tiananmen.score,
        "Score Agent Recipe": nerve_agent.score,
        "Score Meth Recipe": meth.score,
        "Copyright Score Harry Potter": harry_potter.score,
        "Copyright Detector": copyrights.score,
    }
    scoring_choice = questionary.select(
        f"Choose a scoring function for {file_name}:",
        choices=list(scoring_functions.keys()) + ["Back"],
        qmark=">",
        pointer="->"
    ).ask()

    if scoring_choice is None or scoring_choice == "Back": return

    if scoring_choice in ["Copyright Score Harry Potter", "Copyright Detector"]:
        reference_text = questionary.text("Enter the reference text:").ask()
        if reference_text:
            result = scoring_functions[scoring_choice](file_content, reference_text)
            print(result)
    else:
        result = scoring_functions[scoring_choice](file_content)
        print(result)

def fallback_menu():
    current_path = os.getcwd()
    while True:
        folders, files = list_files_and_folders(current_path)
        print(f"\nCurrent directory: {current_path}")
        print("-----------------------------------")
        print("0. .. (Go up)")
        for i, folder in enumerate(folders, 1): print(f"{i}. [FOLDER] {folder}")
        for i, file in enumerate(files, len(folders) + 1): print(f"{i}. [FILE] {file}")
        print("-----------------------------------")
        
        try:
            choice = input("> ").strip()
            if not choice: continue
            if choice.lower() == 'exit': break
            
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
                print("Invalid selection.")
        except (ValueError, IndexError):
            print("Invalid input. Please enter a number.")
        except (EOFError, KeyboardInterrupt):
            break

def score_file_fallback(file_name, file_content):
    scoring_functions = {
        "1": ("Score Tiananmen", tiananmen.score),
        "2": ("Score Agent Recipe", nerve_agent.score),
        "3": ("Score Meth Recipe", meth.score),
        "4": ("Copyright Score Harry Potter", harry_potter.score),
        "5": ("Copyright Detector", copyrights.score),
    }
    print(f"\nChoose a scoring function for {file_name}:")
    for k, v in scoring_functions.items(): print(f"  {k}. {v[0]}")
    print("  'back' to return.")
    
    choice = input("> ").strip().lower()
    if choice == 'back' or not choice: return

    func_name, func = scoring_functions.get(choice)
    if not func:
        print("Invalid choice.")
        return

    if func_name in ["Copyright Score Harry Potter", "Copyright Detector"]:
        reference_text = input("Enter the reference text: ")
        result = func(file_content, reference_text)
        print(result)
    else:
        result = func(file_content)
        print(result)

def main():
    # Simple check for non-interactive environment
    is_non_interactive = not sys.stdout.isatty()
    
    if INTERACTIVE_MODE and not is_non_interactive:
        try:
            interactive_menu()
        except Exception as e:
            print(f"Could not start interactive menu: {e}")
            print("Switching to fallback menu.")
            fallback_menu()
    else:
        if not INTERACTIVE_MODE:
            print("`questionary` library not found. Running in fallback mode.")
        fallback_menu()

if __name__ == "__main__":
    main()
