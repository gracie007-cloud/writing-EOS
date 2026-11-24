import argparse
import csv
from pathlib import Path

CSV_PATH = Path(__file__).resolve().parent.parent / "data" / "llm_identifier_creative_writing_base_models_populated.csv"


def main():
    parser = argparse.ArgumentParser(description="Query creative writing LLM catalog.")
    parser.add_argument("--pen-name", help="Filter by Pen Name (substring match)")
    parser.add_argument("--genre", help="Filter by exact or partial Genre")
    parser.add_argument("--format", dest="mformat", help="Filter by Manuscript Format")
    parser.add_argument("--category", help="Filter by Broader Genre Category (e.g. 'Category A')")
    parser.add_argument("--uncensored", action="store_true", help="Only show Uncensored models")
    args = parser.parse_args()

    with open(CSV_PATH, encoding="utf-8-sig", newline="") as f:
        rows = list(csv.DictReader(f))

    matches = []
    for r in rows:
        if args.pen_name and args.pen_name.lower() not in r["Pen Name"].lower():
            continue
        if args.genre and args.genre.lower() not in r["Genres"].lower():
            continue
        if args.mformat and args.mformat.lower() not in r["Manuscript Format"].lower():
            continue
        if args.category and args.category.lower() not in r["Broader Genre Category"].lower():
            continue
        if args.uncensored and r["Uncensored Model"].strip().lower() != "yes":
            continue
        matches.append(r)

    print(f"Found {len(matches)} matching model(s):\n")
    for m in matches:
        print(f"- {m['Model Name']} [{m['Broader Genre Category']}]")
        print(f"  Pen Names : {m['Pen Name']}")
        print(f"  Genres    : {m['Genres']}")
        print(f"  Formats   : {m['Manuscript Format']}")
        print(f"  Notes     : {m['Notes']}\n")


if __name__ == "__main__":
    main()
