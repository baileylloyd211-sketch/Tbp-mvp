import argparse
import json
from pathlib import Path
from tbp.model import calculate_tbp

def main():
    parser = argparse.ArgumentParser(description="TBP MVP CLI")
    parser.add_argument("--case", type=str, help="Path to JSON input file")
    args = parser.parse_args()

    if not args.case:
        raise SystemExit("Provide --case path/to/input.json")

    data = json.loads(Path(args.case).read_text())
    result = calculate_tbp(data)
    print(json.dumps(result.__dict__, indent=2))

if __name__ == "__main__":
    main()
