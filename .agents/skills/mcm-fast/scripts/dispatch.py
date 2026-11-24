"""Solve a small, synthetic generator dispatch problem by exact enumeration."""

import argparse
import csv
from dataclasses import dataclass
from itertools import chain
import json
from pathlib import Path


@dataclass(frozen=True)
class Unit:
    name: str
    minimum: int
    maximum: int
    fixed: int
    marginal: int

    def cost(self, power):
        return self.fixed + power * self.marginal if power else 0


def read_rows(path, fields):
    with path.open(encoding="utf-8-sig", newline="") as source:
        reader = csv.DictReader(source)
        if not set(fields) <= set(reader.fieldnames or []):
            raise ValueError(f"{path.name}: required columns are {', '.join(fields)}")
        rows = []
        for row in reader:
            values = [row[field] for field in fields]
            if any(value is None for value in values):
                raise ValueError(f"{path.name}:{reader.line_num}: incomplete row")
            rows.append(tuple(value.strip() for value in values))
        return rows


def load_units(path):
    fields = ("unit", "min_mw", "max_mw", "fixed_cost", "cost_per_mw")
    units = [Unit(name, *map(int, values)) for name, *values in read_rows(path, fields)]
    if len(units) != 2 or not all(unit.name for unit in units) or units[0].name == units[1].name:
        raise ValueError("Expected two units with distinct, nonempty names")
    if any(not 1 <= unit.minimum <= unit.maximum or min(unit.fixed, unit.marginal) < 0
           for unit in units):
        raise ValueError("Expected positive MW bounds and nonnegative costs")
    return units


def load_demand(path):
    demand = [tuple(map(int, row)) for row in read_rows(path, ("hour", "demand_mw"))]
    if not demand or len({hour for hour, _ in demand}) != len(demand):
        raise ValueError("Expected at least one hour with unique hour IDs")
    if any(hour < 1 or load < 0 for hour, load in demand):
        raise ValueError("Expected positive hour IDs and nonnegative demand")
    return sorted(demand)


def solve(units, demand):
    first, second = units
    schedule = []
    for hour, load in demand:
        options = chain((0,), range(max(first.minimum, load - second.maximum),
                                   min(first.maximum, load) + 1))
        best = None
        for power in options:
            other = load - power
            if other and not second.minimum <= other <= second.maximum:
                continue
            candidate = (first.cost(power) + second.cost(other), power, other)
            if best is None or candidate < best:
                best = candidate
        if best is None:
            raise ValueError(f"Hour {hour}: no feasible schedule for {load} MW")
        cost, power, other = best
        schedule.append((hour, load, power, other, cost))
    return schedule


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("units", type=Path)
    parser.add_argument("demand", type=Path)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    try:
        units = load_units(args.units)
        schedule = solve(units, load_demand(args.demand))
    except (OSError, ValueError) as error:
        parser.error(str(error))

    summary = {"hours": len(schedule), "unit_ids": [unit.name for unit in units],
               "total_cost": sum(row[-1] for row in schedule)}
    args.output.mkdir(parents=True, exist_ok=True)
    with (args.output / "schedule.csv").open("w", encoding="utf-8", newline="") as output:
        writer = csv.writer(output)
        writer.writerow(("hour", "demand_mw", "unit_1_mw", "unit_2_mw", "cost"))
        writer.writerows(schedule)
    (args.output / "summary.json").write_text(
        json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print(f"Hours: {summary['hours']} | Total cost: {summary['total_cost']} | {args.output}")


if __name__ == "__main__":
    main()
