# Canonical candidate distribution

[Português](DISTRIBUTION.pt-br.md) · [Home](README.md)

Stable-v1.0.0 is being prepared as a local candidate. This work does not publish a tag, release or remote commit. Published snapshots remain immutable. The [Alpha operational allowlist](ALPHA-OPERATIONAL-ALLOWLIST.json) records the only authorized changes to the two historical directories: their independent launchers and operational portions of eight READMEs per edition. Normative manuals, models, instances, application sources, tests, skills and historical evidence remain unchanged from the recorded baseline. This exception changes no OAL requirement.

The root launcher has been removed. Each edition's `run_examples.py` depends only on that edition's `examples/` and stores default databases in its own `data/`. Existing root `data/<edition>/` databases are preserved; pass `--database` explicitly to reuse one. See the [Stable execution guide](versioning/Stable-v1.0.0/examples/README.md#run-an-example).

## Prepare and verify

1. Stage intended additions, modifications and deletions with explicit paths. Finalize source documents and the skill source hashes. Export the staged candidate into a separate, clean Git checkout with canonical bytes, using `.gitattributes` (`text=auto eol=lf`). Preserve protected local Alpha files; do not normalize only while hashing.
2. Run `python scripts/test_edition_launchers.py`, the three Stable pytest suites separately, the Board CRM renderer with `--check`, `python scripts/check_structure.py --edition Stable-v1.0.0`, and `python scripts/test_release_checks.py`. The launcher suite checks all three editions and nine HTTP servers, including isolated renamed copies and existing databases.
3. Preserve previous evidence byte for byte. The [history index](versioning/Stable-v1.0.0/examples/verification/history.json) distinguishes previous snapshot observations from the [current execution](versioning/Stable-v1.0.0/examples/verification/execution.json). Record actual inputs and results; exclude generated verification outputs and the inventory from input hashes to avoid cycles.
4. Stage the final evidence in the clean checkout, then run `python scripts/content_inventory.py --write` and `python scripts/content_inventory.py --check`. This tool hashes actual bytes of every indexed file except the inventory itself. Copy intended final files back to the source repository, stage them explicitly, and commit. Verify that the committed Git tree matches the validated canonical candidate.
5. Create the distribution from that commit with `git archive --format=zip --output=OAL-Stable-v1.0.0.zip HEAD`. Do not ZIP a potentially mixed working directory. No `.git`, environment, cache, database or temporary output belongs in the archive.
6. Run `python scripts/check_archive.py PATH_TO_ZIP`, extract into an empty directory, and run `python scripts/check_archive.py EXTRACTED_DIRECTORY`. Both compare complete file coverage, sizes and actual SHA-256 hashes against the included inventory. They require no Git repository. The index-based `content_inventory.py` instead requires a Git checkout and is not an archive-only check.

Deliver the final commit ID and ZIP digest separately from committed files; putting a commit ID or its ZIP hash inside that same commit would create a circular reference. No publication is implied. Refresh dependent Atlas source snapshots and their baseline hashes if source wording or bytes changed.

## Verification limits

Local execution is recorded with its actual Python, pytest, OS, timestamps and commands. CI configuration does not establish a local Linux execution. HTTP response and process termination do not establish browser JavaScript behavior, visual accessibility, universal correctness or transformer execution. Mocked Ctrl+C and browser controls do not establish OS signal handling or UI behavior. Existing local CRLF differences may cause an actual-byte inventory check of that checkout to fail; only the verified canonical tree and ZIP are distribution evidence.
