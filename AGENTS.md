# Working on OAL

Read VERSION, then resolve the edition before interpreting OAL or choosing files to change. An edition explicitly named by the user, or unambiguously identified by the requested path, takes precedence over VERSION. A comparison may deliberately involve multiple editions; keep their rules and artifacts separate. If no edition is indicated, use the highest available `Stable-vMAJOR.MINOR.PATCH` directory under versioning/ that contains README.md, comparing the three version components numerically. VERSION is the repository's default pointer, not an override of the user's selection; report any disagreement with the latest available Stable. Ask only if the requested edition is missing or ambiguous, or no Stable edition is available. State the selected edition briefly when it matters to the work.

Read `versioning/<selected-edition>/README.md` as the normative source and README.pt-br.md as its translation. English takes precedence. Only that edition's numbered requirements define conformance; marked recommendations remain optional. Guides, FAQs, examples, this file, and skills add no OAL requirements. Do not apply one edition's layer organization, model contracts or validation assumptions to another edition.

Preserve both Alpha directories, including their existing edition-local launchers, operational guides, historical evidence and skills, byte for byte. Earlier operational maintenance is recorded in Git history and does not grant continuing permission to change historical content. Never repair historical instances as a side effect of validating another edition. Released commit/tag snapshots are immutable; follow the selected edition's version policy for subsequent changes.

If the selected edition has a skill/ directory, read its SKILL.md and use that edition's complete informative package. Install it by copying the entire directory to the skills location supported by the target environment, using the name declared in SKILL.md. Keep SKILL.md, LICENSE.txt, and references/. Do not assume a universal installation path or substitute another edition's skill. Alpha-v0.1.0-Alkimim has no bundled skill; use its own manual and examples.

Choose commands from the selected edition's documentation. From the repository root, its local launcher accepts `python versioning/<selected-edition>/run_examples.py NAME`; inside the edition use `python run_examples.py NAME`. Database defaults are edition-local; explicit relative --database paths use the working directory. Preserve existing data.

Repository-wide checks are `python scripts/content_inventory.py --check` and `python scripts/test_release_checks.py`. The launcher regression suite, `python scripts/test_edition_launchers.py`, exercises the three editions it explicitly declares, including nine HTTP smokes; this is not a normative reassessment of Alpha.

For Stable-v1.0.0, use Python 3.12+ and pytest==9.0.2. Run `python -m pytest -q` separately in its tiny-catalog, board-crm and work-board example directories. From the root, also run:

- python versioning/Stable-v1.0.0/run_examples.py --list
- python versioning/Stable-v1.0.0/run_examples.py tiny-catalog --help
- python versioning/Stable-v1.0.0/examples/board-crm/OAL-P1/render_ucs.py --check
- python scripts/check_structure.py --edition Stable-v1.0.0

The current structural verifier applies Stable model and instance assumptions. Do not run it as an Alpha conformance check. For another edition, use its own verification instructions and describe unsupported checks instead of substituting Stable assumptions. Launcher smoke uses --no-browser, temporary databases, a local HTTP response check and process termination; it does not establish browser JavaScript behavior or visual accessibility.

Coordinate English, Portuguese, model/artifact version references, provenance and evidence. Preserve historical authorship and distinguish manual derivation, transformer claims, planned checks and executed checks. Didactic models and Python package versions are independent of the OAL edition.

Follow [the release guide](docs/releasing.md) for changed deliveries. Stage intended additions, modifications and deletions with explicit paths. Finalize source texts, update skill source hashes, record actual verification inputs and results, then generate and check CONTENT-SHA256.json in a canonical clean checkout. The inventory hashes actual bytes of every indexed file except itself, including .github/. Do not normalize only while hashing or rewrite frozen Alpha files to hide local CRLF mismatches. Exclude generated verification outputs and the inventory from execution input hashes and document those exclusions to avoid cycles. Recheck the final archive and its extracted contents; keep its commit ID and ZIP digest outside that same commit.
