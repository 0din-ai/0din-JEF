import argparse
import sys

from jef import registry, score, calculator
from jef.cli_utils import Fore, Style


def _register_scorer_subparsers(subparsers):
    """Dynamically register subparsers from the scoring registry."""
    for meta in registry.list_active():
        cli = meta.get("cli")
        if cli is None:
            continue

        command = cli["command"]
        sub = subparsers.add_parser(
            command,
            help=cli["help"],
            description=cli["help"],
        )
        sub.add_argument("text", help="Text to analyze")

        # Add any extra arguments (e.g. --ref for harry_potter)
        for arg in cli.get("extra_args", []):
            flags = arg["flags"]
            kwargs = {k: v for k, v in arg.items() if k != "flags"}
            sub.add_argument(*flags, **kwargs)

        # Stash the registry name so dispatch can find it
        sub.set_defaults(_registry_name=meta["name"])


def print_enhanced_help():
    """Print enhanced help with colors and formatting."""
    from jef.cli_utils import (
        print_jef_header,
        print_section_header,
        print_test_categories,
        print_usage_examples,
    )

    print_jef_header()
    print_section_header("AI Safety Assessment Tool")

    print(f"""{Fore.WHITE}
JEF evaluates the effectiveness of AI jailbreak techniques across four key dimensions:
  {Fore.CYAN}* Vendor Blast Radius{Fore.WHITE} - How many AI companies affected
  {Fore.CYAN}* Model Blast Radius{Fore.WHITE} - How many specific models compromised
  {Fore.CYAN}* Retargetability{Fore.WHITE} - Works across different content categories
  {Fore.CYAN}* Output Fidelity{Fore.WHITE} - Quality and accuracy of harmful outputs
{Style.RESET_ALL}""")

    print_test_categories()
    print_usage_examples()

    print(
        f"\n{Fore.YELLOW}Tip: Use 'jef-menu' for an interactive file browser interface{Style.RESET_ALL}"
    )


def main():
    # Check if no arguments provided - show enhanced help
    if len(sys.argv) == 1:
        print_enhanced_help()
        return

    parser = argparse.ArgumentParser(
        description="Jailbreak Evaluation Framework (JEF) CLI",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        add_help=False,  # We handle help ourselves for the enhanced version
    )

    parser.add_argument("-h", "--help", action="store_true", help="Show enhanced help")

    subparsers = parser.add_subparsers(dest="command")

    # Register all active scorers from the registry
    _register_scorer_subparsers(subparsers)

    # JEF Score (formula command, not a content scorer)
    jef_score_parser = subparsers.add_parser(
        "jef_score",
        help="Calculate the JEF score.",
        description="Calculate JEF score from component values (0-1 scale)",
    )
    jef_score_parser.add_argument(
        "--bv", type=float, required=True, help="Vendor Blast Radius (0.0-1.0)"
    )
    jef_score_parser.add_argument(
        "--bm", type=float, required=True, help="Model Blast Radius (0.0-1.0)"
    )
    jef_score_parser.add_argument(
        "--rt", type=float, required=True, help="Retargetability (0.0-1.0)"
    )
    jef_score_parser.add_argument(
        "--fd", type=float, required=True, help="Fidelity (0.0-1.0)"
    )

    # JEF Calculator (formula command, not a content scorer)
    jef_calc_parser = subparsers.add_parser(
        "jef_calculator",
        help="Calculate the JEF score from raw data.",
        description="Calculate JEF score from raw metrics",
    )
    jef_calc_parser.add_argument(
        "--num_vendors", type=int, required=True, help="Number of vendors affected"
    )
    jef_calc_parser.add_argument(
        "--num_models", type=int, required=True, help="Number of models affected"
    )
    jef_calc_parser.add_argument(
        "--num_subjects", type=int, required=True, help="Number of subjects affected"
    )
    jef_calc_parser.add_argument(
        "--scores", type=int, nargs="+", required=True, help="List of scores (0-100)"
    )
    jef_calc_parser.add_argument(
        "--max_vendors",
        type=int,
        default=5,
        help="Maximum number of vendors (default: 5)",
    )
    jef_calc_parser.add_argument(
        "--max_models",
        type=int,
        default=10,
        help="Maximum number of models (default: 10)",
    )
    jef_calc_parser.add_argument(
        "--max_subjects",
        type=int,
        default=3,
        help="Maximum number of subjects (default: 3)",
    )

    args = parser.parse_args()

    if hasattr(args, "help") and args.help:
        print_enhanced_help()
        return

    from jef.cli_utils import print_result, print_error, print_info

    # Registry-driven scorer dispatch
    if hasattr(args, "_registry_name"):
        name: str = args._registry_name
        meta = registry.get(name)
        if meta is None:
            print_error(f"Unknown scoring type: {name}")
            return
        cli_meta = meta.get("cli", {})
        print_info(f"Running {meta['display_name']} analysis...")
        try:
            kwargs = {}
            for arg in cli_meta.get("extra_args", []):
                # Convert flag name (e.g. "--ref") to attribute name ("ref")
                attr = arg["flags"][-1].lstrip("-").replace("-", "_")
                if hasattr(args, attr):
                    kwargs[attr] = getattr(args, attr)
            result = registry.score(name, args.text, **kwargs)
            print_result(result, meta["display_name"])
        except Exception as e:
            print_error(f"Analysis failed: {e}")

    elif args.command == "jef_score":
        print_info("Calculating JEF score from component values...")
        try:
            result = score(bv=args.bv, bm=args.bm, rt=args.rt, fd=args.fd)
            print_result(result, "JEF Score")

            print(f"\n{Fore.CYAN}Component Breakdown:")
            print(f"  {Fore.WHITE}Vendor Blast Radius: {Fore.YELLOW}{args.bv:.3f}")
            print(f"  {Fore.WHITE}Model Blast Radius:  {Fore.YELLOW}{args.bm:.3f}")
            print(f"  {Fore.WHITE}Retargetability:     {Fore.YELLOW}{args.rt:.3f}")
            print(
                f"  {Fore.WHITE}Fidelity:           {Fore.YELLOW}{args.fd:.3f}{Style.RESET_ALL}"
            )
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

            print(f"\n{Fore.CYAN}Raw Metrics:")
            print(
                f"  {Fore.WHITE}Vendors Affected: {Fore.YELLOW}{args.num_vendors}/{args.max_vendors}"
            )
            print(
                f"  {Fore.WHITE}Models Affected:  {Fore.YELLOW}{args.num_models}/{args.max_models}"
            )
            print(
                f"  {Fore.WHITE}Subjects Affected: {Fore.YELLOW}{args.num_subjects}/{args.max_subjects}"
            )
            print(f"  {Fore.WHITE}Scores: {Fore.YELLOW}{args.scores}{Style.RESET_ALL}")
        except Exception as e:
            print_error(f"Calculation failed: {e}")
    else:
        print_enhanced_help()


if __name__ == "__main__":
    main()
