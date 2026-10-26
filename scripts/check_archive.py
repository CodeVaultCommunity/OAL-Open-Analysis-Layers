"""Verify a Git archive ZIP or extracted directory against its included inventory."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import sys
import zipfile

INVENTORY = 'CONTENT-SHA256.json'


def check(files: dict[str, bytes]) -> list[str]:
    manifest = json.loads(files[INVENTORY])
    errors = []
    if manifest.get('algorithm') != 'SHA-256' or manifest.get('excluded_paths') != [INVENTORY]:
        errors.append('unsupported inventory algorithm or exclusions')
    if files.get('VERSION', b'').decode('utf-8').strip() != manifest.get('oal_edition'):
        errors.append('edition metadata differs')
    entries = manifest['files']
    names = [entry['path'] for entry in entries]
    if names != sorted(set(names)):
        errors.append('inventory paths must be unique and sorted')
    expected = set(names) | {INVENTORY}
    for path in sorted(expected - files.keys()):
        errors.append(f'missing file: {path}')
    for path in sorted(files.keys() - expected):
        errors.append(f'unexpected file: {path}')
    for entry in entries:
        raw = files.get(entry['path'])
        if raw is not None and (len(raw) != entry['size_bytes'] or hashlib.sha256(raw).hexdigest() != entry['sha256']):
            errors.append(f'hash/size differs: {entry["path"]}')
    return errors


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('archive', type=Path, help='ZIP from git archive, or its extracted directory; no Git required')
    args = parser.parse_args()
    try:
        if args.archive.is_dir():
            files = {}
            for path in args.archive.rglob('*'):
                if path.is_symlink():
                    raise ValueError(f'unsupported symlink: {path}')
                if path.is_file():
                    files[path.relative_to(args.archive).as_posix()] = path.read_bytes()
        else:
            with zipfile.ZipFile(args.archive) as archive:
                entries = [entry for entry in archive.infolist() if not entry.is_dir()]
                if len({entry.filename for entry in entries}) != len(entries):
                    raise ValueError('duplicate archive paths')
                files = {entry.filename: archive.read(entry) for entry in entries}
        errors = check(files)
    except (OSError, ValueError, KeyError, zipfile.BadZipFile) as error:
        errors = [str(error)]
    if errors:
        print('\n'.join(errors), file=sys.stderr)
        return 1
    print(f'Archive OK: {len(files) - 1} indexed files plus inventory; actual bytes and complete coverage match.')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
