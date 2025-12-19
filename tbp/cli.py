import argparse
import json
from pathlib import Path
from tbp.model import calculate_tbp


def main():
    parser = argparse.ArgumentParser(description="TBP MVP CLI")
    parser.add_argument("--case", type=str, help="Path to JSON input file (e.g., input.json)")
    parser.add_argument("--json", type=str, help="Inline JSON string for inputs")
    parser.add_argument("--pretty", action="store_true", help="Pretty-print output JSON")
    args = parser.parse_args()

    if not args.case and not args.json:
        raise SystemExit("Provide either --case input.json OR --json '{...}'")

    if args.json:
        data = json.loads(args.json)
    else:
        data = json.loads(Path(args.case).read_text(encoding="utf-8"))

    result = calculate_tbp(data)
    out = result.__dict__

    if args.pretty:
        print(json.dumps(out, indent=2))
    else:
        print(json.dumps(out))


if __name__ == "__main__":
    main()
