import argparse
import sys
from jef import tiananmen, nerve_agent, meth, harry_potter, copyrights, score, calculator

from jef.cli_utils import Fore, Back, Style, COLORS_AVAILABLE


def print_enhanced_help():
    """Print enhanced help with colors and formatting"""
    from jef.cli_utils import print_jef_header, print_section_header, print_test_categories, print_usage_examples
    
    print_jef_header()
    print_section_header("AI Safety Assessment Tool")
    
    print(f"""{Fore.WHITE}
JEF evaluates the effectiveness of AI jailbreak techniques across four key dimensions:
  {Fore.CYAN}• Vendor Blast Radius{Fore.WHITE} - How many AI companies affected
  {Fore.CYAN}• Model Blast Radius{Fore.WHITE} - How many specific models compromised  
  {Fore.CYAN}• Retargetability{Fore.WHITE} - Works across different content categories
  {Fore.CYAN}• Output Fidelity{Fore.WHITE} - Quality and accuracy of harmful outputs
{Style.RESET_ALL}""")
    
    print_test_categories()
    print_usage_examples()
    
    print(f"\n{Fore.YELLOW}Tip: Use 'jef-menu' for an interactive file browser interface{Style.RESET_ALL}")


def main():
    # Check if no arguments provided - show enhanced help
    if len(sys.argv) == 1:
        print_enhanced_help()
        return
    
    parser = argparse.ArgumentParser(
        description="Jailbreak Evaluation Framework (JEF) CLI",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        add_help=False  # We'll handle help ourselves
    )
    
    # Add custom help argument
    parser.add_argument('-h', '--help', action='store_true', help='Show enhanced help')
    
    subparsers = parser.add_subparsers(dest="command")

    # ScoreTiananmen
    tiananmen_parser = subparsers.add_parser("score_tiananmen", 
                                           help="Score text against Tiananmen Square facts.",
                                           description="Analyze text for historical facts about the 1989 Tiananmen Square events")
    tiananmen_parser.add_argument("text", help="Text to analyze for Tiananmen Square facts")

    # ScoreAgent110Recipe
    agent_parser = subparsers.add_parser("score_agent_recipe", 
                                       help="Score text against nerve agent recipe.",
                                       description="Analyze text for nerve agent synthesis instructions")
    agent_parser.add_argument("text", help="Text to analyze for nerve agent synthesis")

    # ScoreMethRecipe
    meth_parser = subparsers.add_parser("score_meth_recipe", 
                                      help="Score text against meth recipe.",
                                      description="Analyze text for methamphetamine synthesis instructions")
    meth_parser.add_argument("text", help="Text to analyze for meth synthesis")

    # CopyRightScoreHarryPotter
    hp_parser = subparsers.add_parser("copyright_score_hp", 
                                    help="Score text against Harry Potter text.",
                                    description="Check for Harry Potter copyright violations")
    hp_parser.add_argument("text", help="Text to check for copyright violation")
    hp_parser.add_argument("reference", help="Harry Potter reference text to compare against")

    # CopyrightDetector
    copyright_parser = subparsers.add_parser("copyright_detector", 
                                           help="Detect copyright infringement.",
                                           description="General copyright infringement detection")
    copyright_parser.add_argument("text", help="Text to check for copyright violation")
    copyright_parser.add_argument("reference", help="Reference text to compare against")

    # JEFScore
    jef_score_parser = subparsers.add_parser("jef_score", 
                                           help="Calculate the JEF score.",
                                           description="Calculate JEF score from component values (0-1 scale)")
    jef_score_parser.add_argument("--bv", type=float, required=True, help="Vendor Blast Radius (0.0-1.0)")
    jef_score_parser.add_argument("--bm", type=float, required=True, help="Model Blast Radius (0.0-1.0)")
    jef_score_parser.add_argument("--rt", type=float, required=True, help="Retargetability (0.0-1.0)")
    jef_score_parser.add_argument("--fd", type=float, required=True, help="Fidelity (0.0-1.0)")

    # JEFScore Calculator
    jef_calc_parser = subparsers.add_parser("jef_calculator", 
                                          help="Calculate the JEF score from raw data.",
                                          description="Calculate JEF score from raw metrics")
    jef_calc_parser.add_argument("--num_vendors", type=int, required=True, help="Number of vendors affected")
    jef_calc_parser.add_argument("--num_models", type=int, required=True, help="Number of models affected")
    jef_calc_parser.add_argument("--num_subjects", type=int, required=True, help="Number of subjects affected")
    jef_calc_parser.add_argument("--scores", type=int, nargs='+', required=True, help="List of scores (0-100)")
    jef_calc_parser.add_argument("--max_vendors", type=int, default=5, help="Maximum number of vendors (default: 5)")
    jef_calc_parser.add_argument("--max_models", type=int, default=10, help="Maximum number of models (default: 10)")
    jef_calc_parser.add_argument("--max_subjects", type=int, default=3, help="Maximum number of subjects (default: 3)")

    args = parser.parse_args()
    
    # Handle custom help
    if hasattr(args, 'help') and args.help:
        print_enhanced_help()
        return

    # Import CLI utilities for enhanced output
    from jef.cli_utils import print_result, print_error, print_success, print_info

    if args.command == "score_tiananmen":
        print_info("Analyzing text against Tiananmen Square historical facts...")
        try:
            result = tiananmen.score(args.text)
            print_result(result, "Tiananmen Square Analysis")
        except Exception as e:
            print_error(f"Analysis failed: {e}")
            
    elif args.command == "score_agent_recipe":
        print_info("Analyzing text for nerve agent synthesis instructions...")
        try:
            result = nerve_agent.score(args.text)
            print_result(result, "Nerve Agent Analysis")
        except Exception as e:
            print_error(f"Analysis failed: {e}")
            
    elif args.command == "score_meth_recipe":
        print_info("Analyzing text for methamphetamine synthesis instructions...")
        try:
            result = meth.score(args.text)
            print_result(result, "Methamphetamine Analysis")
        except Exception as e:
            print_error(f"Analysis failed: {e}")
            
    elif args.command == "copyright_score_hp":
        print_info("Checking for Harry Potter copyright violations...")
        try:
            result = harry_potter.score(args.text, args.reference)
            print_result(result, "Harry Potter Copyright Analysis")
        except Exception as e:
            print_error(f"Analysis failed: {e}")
            
    elif args.command == "copyright_detector":
        print_info("Performing general copyright analysis...")
        try:
            result = copyrights.score(args.text, args.reference)
            print_result(result, "Copyright Analysis")
        except Exception as e:
            print_error(f"Analysis failed: {e}")
            
    elif args.command == "jef_score":
        print_info("Calculating JEF score from component values...")
        try:
            result = score(bv=args.bv, bm=args.bm, rt=args.rt, fd=args.fd)
            print_result(result, "JEF Score")
            
            # Show component breakdown
            print(f"\n{Fore.CYAN}Component Breakdown:")
            print(f"  {Fore.WHITE}Vendor Blast Radius: {Fore.YELLOW}{args.bv:.3f}")
            print(f"  {Fore.WHITE}Model Blast Radius:  {Fore.YELLOW}{args.bm:.3f}")
            print(f"  {Fore.WHITE}Retargetability:     {Fore.YELLOW}{args.rt:.3f}")
            print(f"  {Fore.WHITE}Fidelity:           {Fore.YELLOW}{args.fd:.3f}{Style.RESET_ALL}")
            
        except Exception as e:
            print_error(f"Calculation failed: {e}")
            
    elif args.command == "jef_calculator":
        print_info("Calculating JEF score from raw metrics...")
        try:
            result = calculator(
                num_vendors=args.num_vendors,
                num_models=args.num_models,
                num_subjects=args.num_subjects,
                scores=args.scores,
                max_vendors=args.max_vendors,
                max_models=args.max_models,
                max_subjects=args.max_subjects,
            )
            print_result(result, "JEF Score")
            
            # Show raw metrics
            print(f"\n{Fore.CYAN}Raw Metrics:")
            print(f"  {Fore.WHITE}Vendors Affected: {Fore.YELLOW}{args.num_vendors}/{args.max_vendors}")
            print(f"  {Fore.WHITE}Models Affected:  {Fore.YELLOW}{args.num_models}/{args.max_models}")
            print(f"  {Fore.WHITE}Subjects Affected: {Fore.YELLOW}{args.num_subjects}/{args.max_subjects}")
            print(f"  {Fore.WHITE}Scores: {Fore.YELLOW}{args.scores}{Style.RESET_ALL}")
            
        except Exception as e:
            print_error(f"Calculation failed: {e}")
    else:
        print_enhanced_help()

if __name__ == "__main__":
    main()