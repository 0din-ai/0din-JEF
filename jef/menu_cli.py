import os
import sys
from jef import tiananmen, nerve_agent, meth, harry_potter, copyrights

try:
    import questionary
    INTERACTIVE_MODE = True
except (ImportError, Exception):
    INTERACTIVE_MODE = False

# Import native color system from cli_utils
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from cli_utils import Fore, Back, Style, COLORS_AVAILABLE


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
        print(f"{Fore.RED}Error reading file: {e}{Style.RESET_ALL}")
        return None


def print_menu_header():
    """Print the JEF menu header"""
    from jef.cli_utils import print_jef_header, print_section_header
    print_jef_header()
    print_section_header("Interactive File Browser & JEF Analyzer")
    print(f"{Fore.WHITE}Navigate through files and analyze them with JEF scoring algorithms{Style.RESET_ALL}\n")


def interactive_menu():
    print_menu_header()
    current_path = os.getcwd()
    
    while True:
        folders, files = list_files_and_folders(current_path)
        
        # Plain choices without color codes for questionary
        choices = ["[..] Go up one directory"]
        choices += [f"[FOLDER] {f}" for f in folders]
        choices += [f"[FILE] {f}" for f in files]
        choices.append("[EXIT] Quit JEF Menu")
        
        # Display current directory with colors
        print(f"\n{Fore.CYAN}Current directory: {Fore.WHITE}{current_path}{Style.RESET_ALL}")
        
        selection = questionary.select(
            "Choose an option:",
            choices=choices,
            qmark=">",
            pointer="->"
        ).ask()

        if selection is None: 
            break
        
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
    from jef.cli_utils import print_result, print_info, print_section_header
    
    print_section_header(f"JEF Analysis for: {file_name}")
    
    scoring_functions = {
        "Tiananmen Square Analysis": ("tiananmen", tiananmen.score),
        "Nerve Agent Detection": ("nerve_agent", nerve_agent.score),
        "Methamphetamine Detection": ("meth", meth.score),
        "Harry Potter Copyright": ("harry_potter", harry_potter.score),
        "General Copyright Detection": ("copyright", copyrights.score),
    }
    
    choices = list(scoring_functions.keys()) + ["Back to file browser"]
    
    print(f"\n{Fore.WHITE}Choose analysis type for {Fore.YELLOW}{file_name}{Fore.WHITE}:{Style.RESET_ALL}")
    
    scoring_choice = questionary.select(
        "Select analysis:",
        choices=choices,
        qmark=">",
        pointer="->"
    ).ask()

    if scoring_choice is None or "Back" in scoring_choice: 
        return

    # Get the function info
    func_info = None
    for choice, info in scoring_functions.items():
        if choice == scoring_choice:
            func_info = info
            break
    
    if not func_info:
        return
        
    test_type, func = func_info

    if test_type in ["harry_potter", "copyright"]:
        reference_text = questionary.text(
            f"{Fore.WHITE}Enter the reference text to compare against:",
            style=questionary.Style([('question', 'fg:#ffffff')])
        ).ask()
        if reference_text:
            print_info(f"Running {test_type} analysis...")
            try:
                result = func(file_content, reference_text)
                print_result(result, f"{test_type.replace('_', ' ').title()} Analysis")
            except Exception as e:
                print(f"{Fore.RED}Error during analysis: {e}{Style.RESET_ALL}")
        
        # Wait for user input before continuing
        input(f"\n{Fore.CYAN}Press Enter to continue...{Style.RESET_ALL}")
    else:
        print_info(f"Running {test_type} analysis...")
        try:
            result = func(file_content)
            print_result(result, f"{test_type.replace('_', ' ').title()} Analysis")
        except Exception as e:
            print(f"{Fore.RED}Error during analysis: {e}{Style.RESET_ALL}")
        
        # Wait for user input before continuing
        input(f"\n{Fore.CYAN}Press Enter to continue...{Style.RESET_ALL}")


def fallback_menu():
    from jef.cli_utils import print_result, print_info, print_error
    
    current_path = os.getcwd()
    while True:
        folders, files = list_files_and_folders(current_path)
        print(f"\n{Fore.CYAN}Current directory: {Fore.WHITE}{current_path}{Style.RESET_ALL}")
        print(f"{Fore.CYAN}{'─'*60}{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}0. [..] Go up{Style.RESET_ALL}")
        
        for i, folder in enumerate(folders, 1): 
            print(f"{Fore.BLUE}{i}. [FOLDER] {folder}{Style.RESET_ALL}")
        
        for i, file in enumerate(files, len(folders) + 1): 
            print(f"{Fore.GREEN}{i}. [FILE] {file}{Style.RESET_ALL}")
        
        print(f"{Fore.RED}exit. Quit JEF Menu{Style.RESET_ALL}")
        print(f"{Fore.CYAN}{'─'*60}{Style.RESET_ALL}")
        
        try:
            choice = input(f"{Fore.MAGENTA}> {Style.RESET_ALL}").strip()
            if not choice: continue
            if choice.lower() == 'exit': 
                print(f"{Fore.GREEN}Thank you for using JEF! Stay safe!{Style.RESET_ALL}")
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
    from jef.cli_utils import print_result, print_info, print_section_header, print_error
    
    print_section_header(f"JEF Analysis for: {file_name}")
    
    scoring_functions = {
        "1": ("Tiananmen Square Analysis", tiananmen.score),
        "2": ("Nerve Agent Detection", nerve_agent.score),
        "3": ("Methamphetamine Detection", meth.score),
        "4": ("Harry Potter Copyright", harry_potter.score),
        "5": ("General Copyright Detection", copyrights.score),
    }
    
    print(f"{Fore.WHITE}Choose analysis type:")
    for k, (name, _) in scoring_functions.items(): 
        print(f"  {Fore.CYAN}{k}. {name}{Style.RESET_ALL}")
    print(f"  {Fore.YELLOW}back. Return to file browser{Style.RESET_ALL}")
    
    choice = input(f"{Fore.MAGENTA}> {Style.RESET_ALL}").strip().lower()
    if choice == 'back' or not choice: 
        return

    if choice not in scoring_functions:
        print_error("Invalid choice.")
        return
        
    func_name, func = scoring_functions[choice]

    if "Copyright" in func_name:
        reference_text = input(f"{Fore.WHITE}Enter the reference text: {Style.RESET_ALL}")
        if reference_text:
            print_info(f"Running {func_name.lower()}...")
            try:
                result = func(file_content, reference_text)
                print_result(result, func_name)
            except Exception as e:
                print_error(f"Analysis failed: {e}")
        
        input(f"\n{Fore.CYAN}Press Enter to continue...{Style.RESET_ALL}")
    else:
        print_info(f"Running {func_name.lower()}...")
        try:
            result = func(file_content)
            print_result(result, func_name)
        except Exception as e:
            print_error(f"Analysis failed: {e}")
        
        input(f"\n{Fore.CYAN}Press Enter to continue...{Style.RESET_ALL}")


def main():
    # Print header for both modes
    from jef.cli_utils import print_jef_header, print_section_header
    
    print_jef_header()
    print_section_header("Interactive File Browser & JEF Analyzer")
    print(f"{Fore.WHITE}Navigate through files and analyze them with JEF scoring algorithms{Style.RESET_ALL}\n")
    
    # Simple check for non-interactive environment
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
            print(f"{Fore.YELLOW}questionary library not found. Running in fallback mode.{Style.RESET_ALL}")
        fallback_menu()


if __name__ == "__main__":
    main()