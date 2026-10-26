"""Inventory actual bytes of every indexed delivery file (no newline conversion)."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
INVENTORY = "CONTENT-SHA256.json"


def tracked_files(root: Path) -> list[str]:
    result = subprocess.run(
        ["git", "ls-files", "--cached", "-z"], cwd=root,
        check=True, stdout=subprocess.PIPE,
    )
    paths = result.stdout.decode("utf-8").split("\0")[:-1]
    if len(paths) != len(set(paths)):
        raise ValueError("duplicate/unmerged paths in Git index")
    return sorted(path for path in paths if path != INVENTORY)


def build(root: Path) -> dict:
    entries = []
    for name in tracked_files(root):
        path = root / name
        if not path.is_file() or path.is_symlink():
            raise ValueError(f"missing or unsupported indexed file: {name}")
        raw = path.read_bytes()
        entries.append({"path": name, "size_bytes": len(raw),
                        "sha256": hashlib.sha256(raw).hexdigest()})
    return {
        "algorithm": "SHA-256",
        "oal_edition": (root / "VERSION").read_text(encoding="utf-8").strip(),
        "scope": "All Git-indexed delivery files, using actual working-tree bytes; stage new delivery files before generation.",
        "excluded_paths": [INVENTORY],
        "files": entries,
    }


def check(root: Path) -> list[str]:
    actual = build(root)
    stored = json.loads((root / INVENTORY).read_text(encoding="utf-8"))
    errors = []
    for key in ("algorithm", "oal_edition", "scope", "excluded_paths"):
        if stored.get(key) != actual[key]:
            errors.append(f"inventory metadata differs: {key}")
    entries = stored.get("files", [])
    names = [entry["path"] for entry in entries]
    if len(names) != len(set(names)):
        errors.append("duplicate inventory paths")
    if names != sorted(names):
        errors.append("inventory paths are not sorted")
    expected = {entry["path"]: entry for entry in actual["files"]}
    recorded = {entry["path"]: entry for entry in entries}
    for name in sorted(expected.keys() - recorded.keys()):
        errors.append(f"omitted indexed file: {name}")
    for name in sorted(recorded.keys() - expected.keys()):
        errors.append(f"unexpected inventory file: {name}")
    for name in sorted(expected.keys() & recorded.keys()):
        if expected[name] != recorded[name]:
            errors.append(f"hash/size/fields differ: {name}")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--write", action="store_true")
    mode.add_argument("--check", action="store_true")
    args = parser.parse_args()
    try:
        if args.write:
            content = build(ROOT)
            (ROOT / INVENTORY).write_text(
                json.dumps(content, indent=2, ensure_ascii=False) + "\n",
                encoding="utf-8", newline="\n",
            )
            print(f"Wrote {len(content['files'])} files to {INVENTORY}")
        else:
            errors = check(ROOT)
            if errors:
                print("\n".join(errors), file=sys.stderr)
                return 1
            print(f"Inventory OK: {len(tracked_files(ROOT))} files (actual bytes)")
    except (OSError, ValueError, KeyError, TypeError, subprocess.CalledProcessError) as error:
        print(f"Inventory failed: {error}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
