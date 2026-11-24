"""Install pinned optional skills using Codex's system Skill Installer."""

import argparse
import json
import os
from pathlib import Path
import re
import subprocess
import sys
from urllib.request import Request, urlopen


ROOT = Path(__file__).resolve().parents[1]
DESTINATION = ROOT / ".agents" / "skills"
DEFAULT_INSTALLER = (
    Path(os.environ.get("CODEX_HOME", Path.home() / ".codex"))
    / "skills" / ".system" / "skill-installer" / "scripts" / "install-skill-from-github.py"
)


def set_explicit_policy(skill_dir):
    metadata = skill_dir / "agents" / "openai.yaml"
    existing = metadata.read_text(encoding="utf-8") if metadata.exists() else ""
    if any(line.startswith("policy:") for line in existing.splitlines()):
        print(f"{skill_dir.name}: kept upstream invocation policy", flush=True)
        return
    metadata.parent.mkdir(exist_ok=True)
    separator = "\n\n" if existing.strip() else ""
    metadata.write_text(existing.rstrip() + separator + "policy:\n  allow_implicit_invocation: false\n",
                        encoding="utf-8")


def install_single_file(source, skill, target):
    # Avoid extracting the entire benchmark archive for a standalone SKILL.md.
    url = (f"https://raw.githubusercontent.com/{source['repo']}/{source['ref']}/"
           f"{skill['path']}/SKILL.md")
    with urlopen(Request(url, headers={"User-Agent": "mcm-agent-skills"}), timeout=20) as response:
        data = response.read()
    name = re.search(r"^name:\s*['\"]?([a-z0-9-]+)", data.decode("utf-8-sig"), re.M)
    if not name or name[1] != skill["name"]:
        raise ValueError(f"Unexpected skill metadata at {url}")
    target.mkdir()
    (target / "SKILL.md").write_bytes(data)
    set_explicit_policy(target)
    print(f"Installed {skill['name']} to {target}", flush=True)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    group = parser.add_mutually_exclusive_group()
    group.add_argument("--list", action="store_true")
    group.add_argument("--all", action="store_true")
    parser.add_argument("--installer", type=Path, default=DEFAULT_INSTALLER)
    parser.add_argument("names", nargs="*")
    args = parser.parse_args()
    sources = json.loads((ROOT / "third-party-skills.json").read_text(encoding="utf-8"))["sources"]
    choices = {skill["name"] for source in sources for skill in source["skills"]}

    if args.list:
        if args.names:
            parser.error("--list takes no skill names")
        for source in sources:
            for skill in source["skills"]:
                print(f"{skill['name']:<32} {source['repo']}  {source['ref'][:10]}  {skill['license']}")
        return
    if args.all and args.names:
        parser.error("--all takes no skill names")
    if not args.all and not args.names:
        parser.error("choose skill names, --all, or --list")
    unknown = set(args.names) - choices
    if unknown:
        parser.error(f"unknown skill(s): {', '.join(sorted(unknown))}")
    requested = choices if args.all else set(args.names)
    needs_installer = any(skill["name"] in requested and not skill.get("single_file")
                          for source in sources for skill in source["skills"])
    if needs_installer and not args.installer.is_file():
        parser.error("Codex Skill Installer was not found. Use --installer to give its path.")

    for source in sources:
        paths = []
        pending = []
        for skill in source["skills"]:
            name = skill["name"]
            if name not in requested:
                continue
            target = DESTINATION / name
            if target.exists():
                if not (target / "SKILL.md").is_file():
                    parser.error(f"remove or rename the incomplete destination: {target}")
                print(f"{name}: existing skill kept", flush=True)
                continue
            if skill.get("single_file"):
                install_single_file(source, skill, target)
                continue
            paths.append(skill["path"])
            pending.append(target)

        if paths:
            subprocess.run([
                sys.executable, str(args.installer), "--repo", source["repo"],
                "--ref", source["ref"], "--dest", str(DESTINATION),
                "--method", "download", "--path", *paths,
            ], check=True)
            for skill_dir in pending:
                set_explicit_policy(skill_dir)


if __name__ == "__main__":
    main()
