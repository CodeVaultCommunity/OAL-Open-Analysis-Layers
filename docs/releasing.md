# Preparing and publishing an OAL release

[Português](releasing.pt-br.md) · [Home](../README.md) · [Agent guidance](../AGENTS.md)

This maintenance procedure adds no OAL conformance requirements. Select the intended edition before choosing its manual, examples, skill or checks. VERSION identifies the repository's default edition. A release freezes a verified commit and its distributed bytes; published commit/tag snapshots remain immutable.

## Prepare the sources

The canonical repository is [CodeVaultCommunity/OAL_OpenAnalysisLayers](https://github.com/CodeVaultCommunity/OAL_OpenAnalysisLayers). Keep local remotes and active dependent-project references current after a rename; preserve old URLs where they identify historical evidence. Repository maintenance after a published tag belongs in a new commit. It does not move the tag or rewrite the released evidence. The [Windows launcher-path verification](verification/windows-launcher-paths/README.md) records the maintenance check separately from the published Stable execution.

Check the branch, working tree and published tags/releases first. Preserve user changes and historical editions. Finalize English and Portuguese documentation, version references, provenance and the selected skill's source hashes before recording final evidence. Preserve model and application versions when their independent contracts have not changed. Release notes describe the actual scope and limits; publication dates and DOIs must reflect real publication or assignment.

Preserve earlier execution records and logs byte for byte, with their original commands and snapshot identity. Point current evidence to the new verification set. A removed path or earlier input hash in an archived run describes that snapshot; it is not a current command or permission to edit historical content. Do not rewrite old observations to match the new delivery.

Use a clean checkout or Git-index export with the repository's .gitattributes (text=auto eol=lf). A working directory with pre-existing CRLF differences is unsuitable as the source of an actual-byte inventory or ZIP. Keep protected working files intact; do not normalize only while hashing or regenerate the manifest to accept mixed bytes.

## Verify the selected edition

Run checks supported by the edition's own documentation. For Stable-v1.0.0, use Python 3.12+ with pytest 9.0.2 and, from the repository root:

```bash
python scripts/test_edition_launchers.py
python versioning/Stable-v1.0.0/examples/board-crm/OAL-P1/render_ucs.py --check
python scripts/check_structure.py --edition Stable-v1.0.0
python scripts/test_release_checks.py
```

Run `python -m pytest -q` separately in versioning/Stable-v1.0.0/examples/tiny-catalog, board-crm and work-board. The launcher suite checks the three declared editions, including nine HTTP servers, isolated renamed copies and preservation of existing databases. The structural verifier checks Stable model declarations and local links, including operational Alpha guides; it does not reassess Alpha conformance.

Record actual commands, Python/pytest/OS versions, timestamps, results and fixed input hashes. Exclude generated verification reports/logs and CONTENT-SHA256.json from execution inputs to avoid cycles, and declare the exclusions. Update current evidence pointers from observed results, then check the final source and metadata again.

## Freeze and inspect the package

Stage intended additions, modifications and deletions with explicit paths before generating the inventory; the script discovers files through the Git index. In the canonical clean checkout, run:

```bash
python scripts/content_inventory.py --write
python scripts/content_inventory.py --check
```

Stage the resulting inventory and commit the final tree. Verify that the committed tree matches the canonical tree used for checks. Generate the ZIP from that commit with `git archive --format=zip --output=OAL-Stable-v1.0.0.zip HEAD`, substituting the selected edition in the filename when appropriate. The package must contain that commit's intended files without .git, environments, caches, databases or temporary build outputs.

The command above exports the complete repository and its root inventory. An archive containing only one edition is a separate distribution scope: label it explicitly and provide an inventory of that package, its license and a check of its extracted local links. The root inventory cannot verify a package that omits indexed root files and other editions. Keep filenames, hashes and verification claims distinct; a maintenance archive from a later commit is not the original published release asset.

Run `python scripts/check_archive.py PATH_TO_ZIP`, extract into an empty directory, then run `python scripts/check_archive.py EXTRACTED_DIRECTORY`. Both compare complete coverage, byte sizes and actual SHA-256 hashes against the included inventory without requiring Git. The index-based content_inventory.py instead requires a Git checkout. There is no permanent expected file count.

Deliver the final commit ID and ZIP digest in an external receipt or release metadata. Embedding the final commit ID or its ZIP hash inside that same commit would create a circular reference. When normative source files or their introductory text change, provide dependent projects such as Atlas with the exact new source bytes, license, commit and hashes; update their pinned snapshots and inventories before claiming synchronization.

## Publish the verified commit

After publication is authorized, send the intended commit and require successful CI for that exact revision on the supported Windows and Linux jobs. CI configuration alone does not establish a successful run. Create the edition's annotated tag and release from the verified commit, attach the checked ZIP and SHA-256, and confirm that the published tag, release and asset identify the intended revision. Never replace a published snapshot to incorporate a later correction.

Each edition's launcher remains self-contained, with default databases in its own data/. Existing root `data/<edition>/` databases stay in place and can be selected explicitly with --database; publication does not migrate or delete them.

## Evidence limits

Report execution for the environment actually exercised. HTTP response and process termination do not establish browser JavaScript behavior, visual accessibility, universal correctness or OAL transformer execution. Mocked Ctrl+C/browser controls do not establish OS-signal or UI integration. Retain these distinctions in release notes and evidence.
