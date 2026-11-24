"""Create a local workspace for a new modeling problem."""

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
    try:
        case.mkdir(parents=True)
    except FileExistsError:
        parser.error(f"case already exists: {case.relative_to(ROOT)}")

    for directory in ("inputs", "src", "outputs", "paper"):
        (case / directory).mkdir()
    (case / "CASE.md").write_text(instructions, encoding="utf-8")
    print(f"Case ready: {case.relative_to(ROOT).as_posix()}")


if __name__ == "__main__":
    main()
