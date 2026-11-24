"""Restore missing third-party skills from the verified public package."""

import argparse
from io import BytesIO
from pathlib import Path, PurePosixPath
from tempfile import TemporaryDirectory
from urllib.error import URLError
from urllib.request import Request, urlopen
from zipfile import BadZipFile, ZipFile

from vendor_bundle import SKILLS, bundle_sha256, load_manifest, verify_skill


BUNDLE_URL = "https://github.com/szy0387-beep/mcm-agent-skills/archive/refs/heads/main.zip"


def read_bundle(archive, names):
    files = {name: {} for name in names}
    for entry in archive.infolist():
        parts = entry.filename.split("/", 4)
        if entry.is_dir() or len(parts) != 5:
            continue
        root, agents, skills, name, relative = parts
        if not root or (agents, skills) != (".agents", "skills") or name not in files:
            continue
        path = PurePosixPath(relative)
        if not relative or path.is_absolute() or ".." in path.parts or "\\" in relative or ":" in relative:
            raise ValueError(f"Unsafe archive path: {entry.filename}")
        normalized = path.as_posix()
        if normalized in files[name]:
            raise ValueError(f"Duplicate archive path: {entry.filename}")
        files[name][normalized] = archive.read(entry)
    return files


def restore(selected, local_archive):
    pending = {}
    for name, skill in selected.items():
        target = SKILLS / name
        if target.exists():
            verify_skill(skill, target)
            print(f"{name}: already present and verified")
        else:
            pending[name] = skill
    if not pending:
        return

    if local_archive:
        source = local_archive
    else:
        request = Request(BUNDLE_URL, headers={"User-Agent": "mcm-agent-skills"})
        with urlopen(request, timeout=25) as response:
            source = BytesIO(response.read())
    with ZipFile(source) as archive:
        files = read_bundle(archive, pending)

    for name, skill in pending.items():
        if "SKILL.md" not in files[name] or bundle_sha256(files[name].items()) != skill["sha256"]:
            raise ValueError(f"{name}: archive does not match this release; use --archive with its matching ZIP")

    SKILLS.mkdir(parents=True, exist_ok=True)
    with TemporaryDirectory(prefix=".restore-", dir=SKILLS) as stage:
        for name, entries in files.items():
            for relative, data in entries.items():
                target = Path(stage) / name / relative
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_bytes(data)
        for name in pending:
            (Path(stage) / name).rename(SKILLS / name)
            print(f"{name}: restored")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    group = parser.add_mutually_exclusive_group()
    group.add_argument("--list", action="store_true")
    group.add_argument("--all", action="store_true")
    parser.add_argument("--archive", type=Path, help="ZIP of this release, for offline recovery")
    parser.add_argument("names", nargs="*")
    args = parser.parse_args()
    sources = load_manifest()["sources"]
    skills = {skill["name"]: skill for source in sources for skill in source["skills"]}

    if args.list:
        if args.names or args.archive:
            parser.error("--list takes no skill name or archive")
        for source in sources:
            for skill in source["skills"]:
                print(f"{skill['name']:<32} {source['repo']}  {source['ref'][:10]}  {skill['license']}")
        return
    if args.all and args.names:
        parser.error("--all takes no skill names")
    if not args.all and not args.names:
        parser.error("choose skill names, --all, or --list")
    unknown = set(args.names) - skills.keys()
    if unknown:
        parser.error(f"unknown skill(s): {', '.join(sorted(unknown))}")
    requested = skills if args.all else {name: skills[name] for name in args.names}
    try:
        restore(requested, args.archive)
    except (OSError, ValueError, BadZipFile, URLError) as error:
        parser.exit(2, f"Could not restore skills: {error}\n")


if __name__ == "__main__":
    main()
