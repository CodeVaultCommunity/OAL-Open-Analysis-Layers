# Working on OAL

Read VERSION first. The current normative source is versioning/Stable-v1.0.0/README.md; README.pt-br.md is its translation. English takes precedence. Only the 46 numbered requirements define OAL conformance; marked recommendations remain optional. Guides, FAQs, examples, this file, and skills add no OAL requirements.

Preserve versioning/Alpha-v0.1.0-Alkimim/ and versioning/Alpha-v0.2.0-Alkimim/ byte for byte, including historical evidence and skills. Never repair historical instances as a side effect of validating the current edition. Released commit/tag snapshots are immutable; apply the current edition's version policy to subsequent changes.

The informative, self-contained skill is versioning/Stable-v1.0.0/skill/. Install it by copying that entire directory to the skills location supported by the target agent environment, named oal-stable-v1-0-0. Keep SKILL.md, LICENSE.txt, and references/. Do not assume a universal installation path.

Use Python 3.12+ and pytest==9.0.2. From the root:

- python run_examples.py --list
- python run_examples.py Stable-v1.0.0/tiny-catalog --help
- python versioning/Stable-v1.0.0/examples/board-crm/OAL-P1/render_ucs.py --check
- python scripts/check_structure.py --edition Stable-v1.0.0
- python scripts/test_release_checks.py
- python scripts/content_inventory.py --check

Run python -m pytest -q separately in each current example directory (tiny-catalog, board-crm, work-board). Launcher smoke uses --no-browser, temporary databases, a local HTTP response check, and process termination. It does not establish browser JavaScript behavior or visual accessibility.

Coordinate English, Portuguese, model/artifact version references, provenance, and evidence. Preserve historical authorship and distinguish manual derivation, transformer claims, planned checks, and executed checks. Didactic models and Python package versions are independent of the OAL edition.

For a changed delivery, stage only intended new files so inventory discovery includes them. Finalize source texts, update skill source hashes, record actual verification inputs and results, then run python scripts/content_inventory.py --write followed by --check. The inventory reads actual bytes of every indexed file except itself, including .github/. Recheck a clean candidate checkout; do not normalize bytes only while hashing or alter frozen Alpha files to hide mismatches. Exclude generated reports and the inventory from execution input hashes to avoid circular references, and document the exclusions.
