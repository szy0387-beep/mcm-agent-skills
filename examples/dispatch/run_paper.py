"""Rebuild the English dispatch walkthrough's result tables and LaTeX source."""

import argparse
import csv
import json
from pathlib import Path
import shutil
import subprocess
import sys
from tempfile import NamedTemporaryFile
from zipfile import ZIP_DEFLATED, ZipFile


HERE = Path(__file__).resolve().parent
SOLVER = HERE.parents[1] / ".agents/skills/mcm-fast/scripts/dispatch.py"
SCHEDULE_FIELDS = ("hour", "demand_mw", "unit_1_mw", "unit_2_mw", "cost")
PAPER_SOURCES = ("main.tex", "base-schedule.tex", "scenario-schedule.tex", "comparison.tex")


def read_demand():
    with (HERE / "demand.csv").open(encoding="utf-8", newline="") as source:
        return [(int(row["hour"]), int(row["demand_mw"])) for row in csv.DictReader(source)]


def write_demand(path, rows):
    with path.open("w", encoding="utf-8", newline="") as target:
        writer = csv.writer(target)
        writer.writerow(("hour", "demand_mw"))
        writer.writerows(rows)


def solver_command(demand, destination):
    return [sys.executable, str(SOLVER), str(HERE / "units.csv"), str(demand),
            "--output", str(destination)]


def run_schedule(demand, destination):
    subprocess.run(solver_command(demand, destination), check=True)
    summary = json.loads((destination / "summary.json").read_text(encoding="utf-8"))
    with (destination / "schedule.csv").open(encoding="utf-8", newline="") as source:
        rows = [tuple(int(row[key]) for key in SCHEDULE_FIELDS) for row in csv.DictReader(source)]
    if len(rows) != summary["hours"] or sum(row[-1] for row in rows) != summary["total_cost"]:
        raise ValueError(f"Schedule and summary disagree in {destination}")
    return rows, summary["total_cost"]


def check_feasibility(output, demand):
    path = output / "demand-141.csv"
    write_demand(path, [(hour, 141 if hour == 2 else power) for hour, power in demand])
    result = subprocess.run(solver_command(path, output / "infeasible"),
                            capture_output=True, text=True)
    expected = "Hour 2: no feasible schedule for 141 MW"
    if result.returncode == 0 or expected not in result.stderr:
        raise RuntimeError(f"Unexpected feasibility result: {result.stdout}{result.stderr}")
    (output / "feasibility.txt").write_text(expected + "\n", encoding="utf-8")


def latex_table(path, rows):
    lines = [r"\begin{tabular}{rrrrr}", r"\toprule",
             r"Hour & Demand (MW) & A (MW) & B (MW) & Cost units \\", r"\midrule"]
    lines.extend(" & ".join(map(str, row)) + r" \\" for row in rows)
    lines.extend((r"\bottomrule", r"\end{tabular}"))
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_paper(output, base, scenario):
    paper = output / "paper"
    paper.mkdir(exist_ok=True)
    shutil.copyfile(HERE / "paper.tex", paper / "main.tex")
    base_rows, base_total = base
    scenario_rows, scenario_total = scenario
    latex_table(paper / "base-schedule.tex", base_rows)
    latex_table(paper / "scenario-schedule.tex", scenario_rows)
    cost_scale = 45 / max(1, base_total, scenario_total)
    comparison = (
        f"\\newcommand{{\\BaseCost}}{{{base_total}}}\n"
        f"\\newcommand{{\\ScenarioCost}}{{{scenario_total}}}\n"
        f"\\newcommand{{\\CostIncrease}}{{{scenario_total - base_total}}}\n"
        f"\\newcommand{{\\BaseBar}}{{{cost_scale * base_total:.2f}mm}}\n"
        f"\\newcommand{{\\ScenarioBar}}{{{cost_scale * scenario_total:.2f}mm}}\n"
    )
    (paper / "comparison.tex").write_text(comparison, encoding="utf-8")
    return paper


def package_paper(paper, destination):
    with NamedTemporaryFile(dir=destination.parent, prefix=".overleaf-", delete=False) as staged:
        temporary_path = Path(staged.name)
    try:
        with ZipFile(temporary_path, "w", compression=ZIP_DEFLATED) as archive:
            for name in PAPER_SOURCES:
                archive.write(paper / name, arcname=name)
        temporary_path.replace(destination)
    finally:
        temporary_path.unlink(missing_ok=True)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True, help="Directory for results and paper source")
    parser.add_argument("--overleaf-zip", action="store_true", help="Package the paper sources as overleaf.zip")
    args = parser.parse_args()
    output = args.output.resolve()
    output.mkdir(parents=True, exist_ok=True)

    demand = read_demand()
    base = run_schedule(HERE / "demand.csv", output / "base")
    raised = output / "demand-plus10.csv"
    write_demand(raised, [(hour, power + 10) for hour, power in demand])
    scenario = run_schedule(raised, output / "plus10")
    check_feasibility(output, demand)
    paper = write_paper(output, base, scenario)
    print(f"Base: {base[1]}; plus 10 MW: {scenario[1]}; infeasible case verified.")
    print(f"Paper source: {paper / 'main.tex'}")
    if args.overleaf_zip:
        archive = output / "overleaf.zip"
        package_paper(paper, archive)
        print(f"Overleaf package: {archive}")


if __name__ == "__main__":
    main()
