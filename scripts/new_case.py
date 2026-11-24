"""Prepare a modeling case without overwriting existing files."""

import argparse
from pathlib import Path
import re


ROOT = Path(__file__).resolve().parents[1]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("name", help="A case folder name using letters, numbers, underscores or hyphens")
    args = parser.parse_args()
    if not re.fullmatch(r"[\w-]{1,64}", args.name):
        parser.error("use a case name with letters, numbers, underscores or hyphens")

    instructions = (ROOT / "templates/CASE.md").read_text(encoding="utf-8")
    case = ROOT / "cases" / args.name
    case_file = case / "CASE.md"
    try:
        case.mkdir(parents=True, exist_ok=True)
        for directory in ("inputs", "src", "outputs", "paper"):
            (case / directory).mkdir(exist_ok=True)
        try:
            with case_file.open("x", encoding="utf-8") as record:
                record.write(instructions)
        except FileExistsError:
            if not case_file.is_file():
                raise
            print("Existing CASE.md kept.")
    except OSError as error:
        parser.error(str(error))
    print(f"Case ready: {case.relative_to(ROOT).as_posix()}")


if __name__ == "__main__":
    main()
