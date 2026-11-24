"""Check the public bundle and its examples."""

import argparse
import ast
import csv
from hashlib import sha256
from html.parser import HTMLParser
from itertools import product
from pathlib import Path
import re
import shutil
import subprocess
import sys
from tempfile import TemporaryDirectory
from urllib.parse import unquote, urlsplit
from zipfile import ZipFile

from check_ai_disclosure import PDF_NAME, check_disclosure
from vendor_bundle import REFERENCE_SKILLS, ROOT, SKILLS, load_manifest, verify_skill


GITHUB_PROJECT = "/szy0387-beep/mcm-agent-skills/"
HTML_PAGE = ROOT / "docs/index.html"
PAPER_FILES = {"main.tex", "base-schedule.tex", "scenario-schedule.tex", "comparison.tex"}


def require(condition, message):
    if not condition:
        raise ValueError(message)


def check_skills():
    manifest = load_manifest()
    names = []
    for source in manifest["sources"]:
        require(re.fullmatch(r"[a-f0-9]{40}", source["ref"]), f"Unpinned source: {source['repo']}")
        for skill in source["skills"]:
            name = skill["name"]
            names.append(name)
            verify_skill(skill, SKILLS / name)
            config = (SKILLS / name / "agents/openai.yaml").read_text(encoding="utf-8")
            policy = re.findall(r"^  allow_implicit_invocation: (true|false)\s*$", config, re.M)
            require(policy == ["false" if name in REFERENCE_SKILLS else "true"],
                    f"Unexpected invocation policy: {name}")
    require(len(names) == len(set(names)), "Duplicate third-party skill name")

    installed = {}
    for spec in SKILLS.glob("*/SKILL.md"):
        frontmatter = spec.read_text(encoding="utf-8-sig").split("---", 2)
        require(len(frontmatter) == 3, f"Missing frontmatter: {spec.parent.name}")
        name = re.search(r"""^name:\s*['"]?([a-z0-9-]+)""", frontmatter[1], re.M)
        require(name and name[1] == spec.parent.name, f"Skill name mismatch: {spec.parent.name}")
        require(re.search(r"^description:\s*\S", frontmatter[1], re.M),
                f"Missing skill description: {spec.parent.name}")
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


def markdown_links(markdown):
    fence = None
    for line in markdown.splitlines():
        marker = re.match(r"^ {0,3}(`{3,}|~{3,})", line)
        if marker:
            token = marker[1]
            if fence is None:
                fence = token
            elif token.startswith(fence) and line[marker.end():].strip() == "":
                fence = None
            continue
        if fence is not None:
            continue
        for match in re.finditer(r"\]\((<[^>]+>|[^\s)]+)|^ {0,3}\[[^\]]+\]:\s*(<[^>]+>|\S+)", line):
            yield (match[1] or match[2]).strip("<>")


def check_links():
    files = list(ROOT.glob("*.md"))
    for folder in ("docs", "templates", "examples", "figures", ".agents/skills"):
        files.extend((ROOT / folder).rglob("*.md"))
    for file in files:
        for href in markdown_links(file.read_text(encoding="utf-8-sig")):
            link = urlsplit(href)
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


def compile_latex(source):
    with TemporaryDirectory(prefix="mcm-tex-check-") as directory:
        output = Path(directory)
        subprocess.run(["tectonic", "--keep-logs", "--outdir", directory, "main.tex"],
                       cwd=source, check=True, timeout=150)
        with (output / "main.pdf").open("rb") as pdf:
            require(pdf.read(5) == b"%PDF-", f"Missing valid PDF from {source.name}")
        log = (output / "main.log").read_text(encoding="utf-8", errors="replace")
        require(not re.search(r"undefined references|Citation .+ undefined|Reference .+ undefined", log, re.I),
                f"Unresolved citation or cross-reference in {source.name}")


def check_dispatch(build_pdf):
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
            if build_pdf:
                unpacked = output / "unpacked"
                archive.extractall(unpacked)
                compile_latex(unpacked)


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


def check_disclosure_and_rules():
    rules = ROOT / "docs/rules/2026-apmcm-en-rules.pdf"
    notes = rules.with_name("2026-apmcm-en.md").read_text(encoding="utf-8")
    require(sha256(rules.read_bytes()).hexdigest() in notes, "Official rules snapshot checksum mismatch")
    with TemporaryDirectory(prefix="mcm-ai-disclosure-check-") as directory:
        submitted = Path(directory) / PDF_NAME
        shutil.copyfile(rules, submitted)
        check_disclosure(submitted.parent)
        mismatched = submitted.with_name(submitted.stem + " (1).pdf")
        submitted.rename(mismatched)
        try:
            check_disclosure(submitted.parent)
        except ValueError:
            pass
        else:
            raise ValueError("Disclosure preflight accepted a mismatched filename")


def check_python_syntax():
    for directory in ("scripts", "examples", "tests", ".agents/skills"):
        for file in (ROOT / directory).rglob("*.py"):
            source = file.read_text(encoding="utf-8-sig")
            ast.parse(source, filename=str(file.relative_to(ROOT)), feature_version=(3, 10))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--compile-latex", action="store_true", help="compile the three paper examples using Tectonic")
    args = parser.parse_args()
    count = check_skills()
    check_links()
    check_python_syntax()
    check_dispatch(args.compile_latex)
    check_case_status()
    check_disclosure_and_rules()
    if args.compile_latex:
        compile_latex(ROOT / "templates/apmcm-paper")
        compile_latex(ROOT / "examples/references")
    print(f"Verified {count} skills, vendor hashes, links, Python syntax, examples, and disclosure checks.")


if __name__ == "__main__":
    try:
        main()
    except (ValueError, SyntaxError, OSError, subprocess.SubprocessError) as error:
        raise SystemExit(f"Package check failed: {error}") from None
