"""Read and verify the third-party skill inventory."""

from hashlib import sha256
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SKILLS = ROOT / ".agents" / "skills"
MANIFEST = ROOT / "third-party-skills.json"
REFERENCE_SKILLS = {"mcm", "math-modeling-solver", "math-modeling-paper"}


def load_manifest():
    return json.loads(MANIFEST.read_text(encoding="utf-8"))


def bundled_files(directory):
    for path in directory.rglob("*"):
        relative = path.relative_to(directory)
        if path.is_file() and "__pycache__" not in relative.parts and path.suffix not in (".pyc", ".pyo"):
            yield relative.as_posix(), path.read_bytes()


def bundle_sha256(files):
    entries = sorted((name, sha256(content).hexdigest()) for name, content in files)
    inventory = json.dumps(entries, ensure_ascii=False, separators=(",", ":")).encode("utf-8")
    return sha256(inventory).hexdigest()


def verify_skill(skill, directory):
    actual = bundle_sha256(bundled_files(directory))
    if actual != skill.get("sha256"):
        raise ValueError(f"Vendored skill checksum mismatch: {skill['name']}")
