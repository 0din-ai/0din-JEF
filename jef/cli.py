import argparse
from jef import tiananmen, nerve_agent, meth, harry_potter, copyrights, score, calculator


def main():
    parser = argparse.ArgumentParser(description="Jailbreak Evaluation Framework (JEF) CLI")
    subparsers = parser.add_subparsers(dest="command")

    # ScoreTiananmen
    tiananmen_parser = subparsers.add_parser("score_tiananmen", help="Score text against Tiananmen Square facts.")
    tiananmen_parser.add_argument("text", help="Text to score.")

    # ScoreAgent110Recipe
    agent_parser = subparsers.add_parser("score_agent_recipe", help="Score text against nerve agent recipe.")
    agent_parser.add_argument("text", help="Text to score.")

    # ScoreMethRecipe
    meth_parser = subparsers.add_parser("score_meth_recipe", help="Score text against meth recipe.")
    meth_parser.add_argument("text", help="Text to score.")

    # CopyRightScoreHarryPotter
    hp_parser = subparsers.add_parser("copyright_score_hp", help="Score text against Harry Potter text.")
    hp_parser.add_argument("text", help="Text to score.")
    hp_parser.add_argument("reference", help="Harry Potter reference text.")

    # CopyrightDetector
    copyright_parser = subparsers.add_parser("copyright_detector", help="Detect copyright infringement.")
    copyright_parser.add_argument("text", help="Text to check.")
    copyright_parser.add_argument("reference", help="Reference text to compare against.")

    # JEFScore
    jef_score_parser = subparsers.add_parser("jef_score", help="Calculate the JEF score.")
    jef_score_parser.add_argument("--bv", type=float, required=True, help="Vendor Blast Radius")
    jef_score_parser.add_argument("--bm", type=float, required=True, help="Model Blast Radius")
    jef_score_parser.add_argument("--rt", type=float, required=True, help="Retargetability")
    jef_score_parser.add_argument("--fd", type=float, required=True, help="Fidelity")

    # JEFScore Calculator
    jef_calc_parser = subparsers.add_parser("jef_calculator", help="Calculate the JEF score from raw data.")
    jef_calc_parser.add_argument("--num_vendors", type=int, required=True, help="Number of vendors affected.")
    jef_calc_parser.add_argument("--num_models", type=int, required=True, help="Number of models affected.")
    jef_calc_parser.add_argument("--num_subjects", type=int, required=True, help="Number of subjects affected.")
    jef_calc_parser.add_argument("--scores", type=int, nargs='+', required=True, help="List of scores.")
    jef_calc_parser.add_argument("--max_vendors", type=int, default=5, help="Maximum number of vendors.")
    jef_calc_parser.add_argument("--max_models", type=int, default=10, help="Maximum number of models.")
    jef_calc_parser.add_argument("--max_subjects", type=int, default=3, help="Maximum number of subjects.")

    args = parser.parse_args()

    if args.command == "score_tiananmen":
        result = tiananmen.score(args.text)
        print(result)
    elif args.command == "score_agent_recipe":
        result = nerve_agent.score(args.text)
        print(result)
    elif args.command == "score_meth_recipe":
        result = meth.score(args.text)
        print(result)
    elif args.command == "copyright_score_hp":
        result = harry_potter.score(args.text, args.reference)
        print(result)
    elif args.command == "copyright_detector":
        result = copyrights.score(args.text, args.reference)
        print(result)
    elif args.command == "jef_score":
        result = score(bv=args.bv, bm=args.bm, rt=args.rt, fd=args.fd)
        print(result)
    elif args.command == "jef_calculator":
        result = calculator(
            num_vendors=args.num_vendors,
            num_models=args.num_models,
            num_subjects=args.num_subjects,
            scores=args.scores,
            max_vendors=args.max_vendors,
            max_models=args.max_models,
            max_subjects=args.max_subjects,
        )
        print(result)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
