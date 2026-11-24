"""Check the public skill bundle and replay its dispatch practice."""

import csv
from html.parser import HTMLParser
from itertools import product
import json
from pathlib import Path
import re
import subprocess
import sys
from tempfile import TemporaryDirectory
from urllib.parse import unquote, urlsplit
from zipfile import ZipFile


ROOT = Path(__file__).resolve().parents[1]
SKILLS = ROOT / ".agents/skills"
GITHUB_PROJECT = "/szy0387-beep/mcm-agent-skills/"
HTML_PAGE = ROOT / "docs/index.html"
PAPER_FILES = {"main.tex", "base-schedule.tex", "scenario-schedule.tex", "comparison.tex"}


def require(condition, message):
    if not condition:
        raise ValueError(message)


def check_skills():
    manifest = json.loads((ROOT / "third-party-skills.json").read_text(encoding="utf-8"))
    names = []
    for source in manifest["sources"]:
        require(re.fullmatch(r"[a-f0-9]{40}", source["ref"]), f"Unpinned source: {source['repo']}")
        names.extend(skill["name"] for skill in source["skills"])
    require(len(names) == len(set(names)), "Duplicate third-party skill name")

    installed = {}
    for spec in SKILLS.glob("*/SKILL.md"):
        frontmatter = spec.read_text(encoding="utf-8-sig").split("---", 2)
        require(len(frontmatter) == 3, f"Missing frontmatter: {spec.parent.name}")
        name = re.search(r"""^name:\s*['"]?([a-z0-9-]+)""", frontmatter[1], re.M)
        require(name and name[1] == spec.parent.name, f"Skill name mismatch: {spec.parent.name}")
        installed[name[1]] = spec
    require(set(names) <= installed.keys(), f"Missing bundled skills: {set(names) - installed.keys()}")

    counts = f"{len(installed) - len(names)} 个核心 Skill 和 {len(names)} 个专项 Skill"
    for source in (ROOT / "README.md", HTML_PAGE):
        require(counts in source.read_text(encoding="utf-8"), f"Update skill counts in {source.name}")
    return len(installed)


class LandingLinks(HTMLParser):
    def __init__(self):
        super().__init__()
        self.links = []
        self.anchors = set()

    def handle_starttag(self, tag, attrs):
        for name, value in attrs:
            if name == "id":
                require(value not in self.anchors, f"Duplicate homepage anchor: {value}")
                self.anchors.add(value)
            if name in ("href", "src") and value:
                self.links.append(value)


def check_links():
    files = [
        *ROOT.glob("*.md"), *(ROOT / "docs").glob("*.md"),
        *(ROOT / "templates").rglob("*.md"), *(ROOT / "examples").glob("*/*.md"),
    ]
    for file in files:
        for href in re.findall(r"\]\(([^)\n]+)\)", file.read_text(encoding="utf-8")):
            link = urlsplit(href.strip("<>"))
            if not link.scheme and not link.netloc and link.path:
                target = (file.parent / unquote(link.path)).resolve()
                require(target.is_relative_to(ROOT) and target.exists(),
                        f"Broken Markdown link in {file.relative_to(ROOT)}: {href}")

    page = LandingLinks()
    page.feed(HTML_PAGE.read_text(encoding="utf-8"))
    for href in page.links:
        link = urlsplit(href)
        if link.netloc == "github.com" and link.path.startswith(GITHUB_PROJECT):
            path = link.path.removeprefix(GITHUB_PROJECT)
            if path.startswith(("blob/main/", "tree/main/")):
                target = ROOT / unquote(path.split("/", 2)[2])
                require(target.exists(), f"Homepage target missing: {href}")
        elif not link.netloc and not link.scheme:
            target = HTML_PAGE.parent / unquote(link.path)
            require(target.exists(), f"Homepage resource missing: {href}")
            if not link.path and link.fragment:
                require(unquote(link.fragment) in page.anchors, f"Homepage anchor missing: {href}")


def numeric_rows(path):
    with path.open(encoding="utf-8", newline="") as source:
        return [{key: int(value) for key, value in row.items() if key != "unit"}
                for row in csv.DictReader(source)]


def allowed_power(unit):
    return [0, *range(unit["min_mw"], unit["max_mw"] + 1)]


def dispatch_cost(power, units):
    return sum(unit["fixed_cost"] + amount * unit["cost_per_mw"]
               for amount, unit in zip(power, units) if amount)


def check_dispatch():
    example = ROOT / "examples/dispatch"
    units = numeric_rows(example / "units.csv")
    demand = numeric_rows(example / "demand.csv")
    allowed = [allowed_power(unit) for unit in units]
    optimum = {}
    for power in product(*allowed):
        load = sum(power)
        cost = dispatch_cost(power, units)
        optimum[load] = min(cost, optimum.get(load, cost))

    with TemporaryDirectory(prefix="mcm-check-") as directory:
        output = Path(directory) / "result"
        subprocess.run([sys.executable, str(example / "run_paper.py"), "--output", str(output),
                        "--overleaf-zip"], check=True, cwd=directory)
        for name, increase, expected in (("base", 0, 980), ("plus10", 10, 1120)):
            rows = numeric_rows(output / name / "schedule.csv")
            require(len(rows) == len(demand), f"Incorrect number of hours in {name}")
            for row, source in zip(rows, demand):
                power = (row["unit_1_mw"], row["unit_2_mw"])
                load = source["demand_mw"] + increase
                location = f"{name} hour {source['hour']}"
                require((row["hour"], row["demand_mw"]) == (source["hour"], load),
                        f"Wrong source input in {location}")
                require(sum(power) == load and all(p in choices for p, choices in zip(power, allowed)),
                        f"Invalid allocation in {location}")
                require(row["cost"] == dispatch_cost(power, units) == optimum[load],
                        f"Non-optimal or incorrect cost in {location}")
            require(sum(row["cost"] for row in rows) == expected, f"Incorrect total in {name}")
        require(max(optimum) == 140 and "141 MW" in (output / "feasibility.txt").read_text(encoding="utf-8"),
                "Missing 141 MW infeasibility check")
        with ZipFile(output / "overleaf.zip") as archive:
            require(set(archive.namelist()) == PAPER_FILES, "Incomplete or unexpected Overleaf ZIP files")
            for name in PAPER_FILES:
                require(archive.read(name) == (output / "paper" / name).read_bytes(),
                        f"ZIP differs from generated paper source: {name}")


def check_case_status():
    command = [sys.executable, "-X", "utf8", str(ROOT / "scripts/case_status.py")]
    template = (ROOT / "templates/CASE.md").read_text(encoding="utf-8")
    example = template.replace("官方截止＝—", "官方截止＝2999-11-30T09:00:00+08:00")
    example = example.replace("收尾开始＝—", "收尾开始＝2999-11-29T20:00:00+08:00")
    pending = "| Q2 | 求解与验证 | 需返工 | 编程手 | 需求情景版本变更 | 重跑 Q2 |"
    content = example.replace(
        "\n\n从仓库根目录运行", f"\n{pending}\n\n从仓库根目录运行", 1,
    )
    with TemporaryDirectory(prefix="mcm-status-check-") as directory:
        case = Path(directory) / "CASE.md"
        case.write_text(content, encoding="utf-8")
        output = subprocess.check_output([*command, directory], encoding="utf-8")
        require("需返工 1" in output and "重跑 Q2" in output and "计划收尾" in output,
                "Case status did not report the pending revision and planned finalization")
        require(case.read_text(encoding="utf-8") == content, "Case status modified the notes")
        case.write_text("# 旧案例\n", encoding="utf-8")
        output = subprocess.check_output([*command, str(case)], encoding="utf-8")
        require("进度与交接" in output, "Case status did not report how to read legacy notes")


def main():
    count = check_skills()
    check_links()
    check_dispatch()
    check_case_status()
    print(f"Verified {count} skills, public links, dispatch results, Overleaf sources, and read-only case status.")


if __name__ == "__main__":
    try:
        main()
    except (ValueError, OSError, subprocess.CalledProcessError) as error:
        raise SystemExit(f"Package check failed: {error}") from None
