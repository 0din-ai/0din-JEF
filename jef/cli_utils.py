"""
CLI utilities for enhanced JEF command-line interface
"""

import os
import sys
import platform

# Native Python cross-platform color support
class NativeColors:
    """Native Python ANSI color codes with cross-platform support"""
    
    def __init__(self):
        self.enabled = self._detect_color_support()
        
    def _detect_color_support(self):
        """Detect if the terminal supports colors"""
        # Check if output is redirected
        if not sys.stdout.isatty():
            return False
            
        # Check environment variables
        if os.environ.get('NO_COLOR'):
            return False
        if os.environ.get('FORCE_COLOR'):
            return True
            
        # Platform-specific detection
        if platform.system() == 'Windows':
            # Windows 10 version 1607+ supports ANSI
            try:
                import ctypes
                kernel32 = ctypes.windll.kernel32
                # Enable ANSI escape sequence processing
                kernel32.SetConsoleMode(kernel32.GetStdHandle(-11), 7)
                return True
            except:
                # Fallback: check Windows version
                version = platform.version()
                if version and float(version.split('.')[0]) >= 10:
                    return True
                return False
        else:
            # Unix-like systems (Linux, macOS)
            term = os.environ.get('TERM', '')
            return term and term != 'dumb'
    
    def _color(self, code):
        """Return ANSI color code if colors are enabled, empty string otherwise"""
        return f'\033[{code}m' if self.enabled else ''

# Initialize color system
colors = NativeColors()

# Foreground colors
class Fore:
    BLACK = colors._color('30')
    RED = colors._color('31')
    GREEN = colors._color('32')
    YELLOW = colors._color('33')
    BLUE = colors._color('34')
    MAGENTA = colors._color('35')
    CYAN = colors._color('36')
    WHITE = colors._color('37')
    RESET = colors._color('39')

# Background colors
class Back:
    BLACK = colors._color('40')
    RED = colors._color('41')
    GREEN = colors._color('42')
    YELLOW = colors._color('43')
    BLUE = colors._color('44')
    MAGENTA = colors._color('45')
    CYAN = colors._color('46')
    WHITE = colors._color('47')
    RESET = colors._color('49')

# Styles
class Style:
    BRIGHT = colors._color('1')
    DIM = colors._color('2')
    NORMAL = colors._color('22')
    RESET_ALL = colors._color('0')

COLORS_AVAILABLE = colors.enabled


def print_jef_header():
    """Print the JEF ASCII art header with colors"""
    header = f"""
{Fore.RED}+==============================================================================+
{Fore.RED}|  {Fore.CYAN}     JJJ EEEEE FFFFF    {Fore.YELLOW}Jailbreak Evaluation Framework{Fore.RED}        |
{Fore.RED}|  {Fore.CYAN}      J  E     F        {Fore.WHITE}Advanced AI Safety Assessment{Fore.RED}         |
{Fore.RED}|  {Fore.CYAN}      J  EEE   FFF      {Fore.GREEN}Version 0.1.5{Fore.RED}                        |
{Fore.RED}|  {Fore.CYAN}  J   J  E     F        {Fore.MAGENTA}by 0Din.ai{Fore.RED}                           |
{Fore.RED}|  {Fore.CYAN}   JJJ   EEEEE F        {Fore.BLUE}https://0din.ai{Fore.RED}                      |
{Fore.RED}|  {Fore.CYAN}                       {Fore.RED}                                                |
{Fore.RED}+==============================================================================+{Style.RESET_ALL}
"""
    print(header)


def print_section_header(title, color=Fore.CYAN):
    """Print a formatted section header"""
    print(f"\n{color}{'='*60}")
    print(f"{color}{title.center(60)}")
    print(f"{color}{'='*60}{Style.RESET_ALL}")


def print_command_help(command, description, example=""):
    """Print formatted command help"""
    print(f"  {Fore.GREEN}{command:<25}{Style.RESET_ALL} {Fore.WHITE}{description}{Style.RESET_ALL}")
    if example:
        print(f"    {Fore.YELLOW}Example: {Fore.CYAN}{example}{Style.RESET_ALL}")


def print_result(result, test_name=""):
    """Print formatted test results"""
    if isinstance(result, dict):
        if 'percentage' in result:
            percentage = result['percentage']
            score_color = get_score_color(percentage)
            print(f"\n{Fore.CYAN}{'─'*50}")
            print(f"{Fore.WHITE}📊 {test_name} Results:")
            print(f"{Fore.CYAN}{'─'*50}")
            print(f"{Fore.WHITE}Score: {score_color}{percentage:.2f}%{Style.RESET_ALL}")
            
            if 'score' in result:
                print(f"{Fore.WHITE}Raw Score: {Fore.YELLOW}{result['score']:.2f}{Style.RESET_ALL}")
            
            if 'total_possible_score' in result:
                print(f"{Fore.WHITE}Max Possible: {Fore.YELLOW}{result['total_possible_score']}{Style.RESET_ALL}")
            
            # Show matches if available
            if 'matches' in result and result['matches']:
                print(f"\n{Fore.GREEN}✅ Detected Elements ({len(result['matches'])} total):")
                for match in result['matches']:  # Show all matches
                    print(f"  {Fore.GREEN}• {match}{Style.RESET_ALL}")
            
            # Show missing elements if available
            if 'missing' in result and result['missing']:
                print(f"\n{Fore.RED}❌ Missing Elements ({len(result['missing'])} total):")
                for missing in result['missing']:  # Show all missing
                    print(f"  {Fore.RED}• {missing}{Style.RESET_ALL}")
            
            print(f"{Fore.CYAN}{'─'*50}{Style.RESET_ALL}")
        else:
            # Handle JEF score results
            print(f"\n{Fore.CYAN}{'─'*50}")
            print(f"{Fore.WHITE}🎯 JEF Score Result:")
            print(f"{Fore.CYAN}{'─'*50}")
            score_color = get_jef_score_color(result)
            print(f"{Fore.WHITE}JEF Score: {score_color}{result:.2f}/10{Style.RESET_ALL}")
            print(f"{Fore.CYAN}{'─'*50}{Style.RESET_ALL}")
    else:
        # Handle simple numeric results
        if isinstance(result, (int, float)):
            if 0 <= result <= 10:  # JEF score
                score_color = get_jef_score_color(result)
                print(f"\n{Fore.WHITE}🎯 JEF Score: {score_color}{result:.2f}/10{Style.RESET_ALL}")
            else:  # Percentage
                score_color = get_score_color(result)
                print(f"\n{Fore.WHITE}📊 Score: {score_color}{result:.2f}%{Style.RESET_ALL}")
        else:
            print(f"\n{Fore.WHITE}Result: {Fore.YELLOW}{result}{Style.RESET_ALL}")


def get_score_color(percentage):
    """Get color based on percentage score"""
    if percentage >= 80:
        return Fore.RED + Style.BRIGHT  # High risk - bright red
    elif percentage >= 60:
        return Fore.RED  # Medium-high risk - red
    elif percentage >= 40:
        return Fore.YELLOW  # Medium risk - yellow
    elif percentage >= 20:
        return Fore.CYAN  # Low-medium risk - cyan
    else:
        return Fore.GREEN  # Low risk - green


def get_jef_score_color(score):
    """Get color based on JEF score (0-10 scale)"""
    if score >= 8:
        return Fore.RED + Style.BRIGHT  # Critical
    elif score >= 6:
        return Fore.RED  # High
    elif score >= 4:
        return Fore.YELLOW  # Medium
    elif score >= 2:
        return Fore.CYAN  # Low
    else:
        return Fore.GREEN  # Minimal


def print_error(message):
    """Print formatted error message"""
    print(f"{Fore.RED}❌ Error: {message}{Style.RESET_ALL}")


def print_warning(message):
    """Print formatted warning message"""
    print(f"{Fore.YELLOW}⚠️  Warning: {message}{Style.RESET_ALL}")


def print_success(message):
    """Print formatted success message"""
    print(f"{Fore.GREEN}✅ {message}{Style.RESET_ALL}")


def print_info(message):
    """Print formatted info message"""
    print(f"{Fore.CYAN}ℹ️  {message}{Style.RESET_ALL}")


def print_test_categories():
    """Print available test categories with descriptions"""
    categories = [
        ("🧪 Illicit Substances", "Crystal Meth synthesis detection", "score_meth_recipe"),
        ("☠️  Harmful Substances", "Nerve Agent synthesis detection", "score_agent_recipe"),
        ("📚 Copyright Violation", "Harry Potter text reproduction", "copyright_score_hp"),
        ("🏛️  Government Censorship", "Tiananmen Square facts", "score_tiananmen"),
        ("🔍 General Copyright", "Generic copyright detection", "copyright_detector"),
        ("🎯 JEF Score", "Overall jailbreak severity", "jef_score"),
        ("🧮 JEF Calculator", "Calculate from raw metrics", "jef_calculator")
    ]
    
    print(f"\n{Fore.CYAN}Available Test Categories:{Style.RESET_ALL}")
    print(f"{Fore.CYAN}{'─'*60}{Style.RESET_ALL}")
    
    for icon_name, description, command in categories:
        print(f"  {Fore.WHITE}{icon_name:<25}{Style.RESET_ALL} {description}")
        print(f"    {Fore.YELLOW}Command: {Fore.CYAN}jef {command}{Style.RESET_ALL}")
        print()


def print_usage_examples():
    """Print usage examples"""
    examples = [
        ("Test Tiananmen censorship", 'jef score_tiananmen "Your text here"'),
        ("Check copyright violation", 'jef copyright_detector "submission" "reference"'),
        ("Calculate JEF score", 'jef jef_score --bv 0.8 --bm 0.6 --rt 0.4 --fd 0.7'),
        ("Interactive menu", 'jef-menu'),
    ]
    
    print(f"\n{Fore.CYAN}Usage Examples:{Style.RESET_ALL}")
    print(f"{Fore.CYAN}{'─'*60}{Style.RESET_ALL}")
    
    for description, command in examples:
        print(f"  {Fore.WHITE}{description}:")
        print(f"    {Fore.CYAN}{command}{Style.RESET_ALL}")
        print()