# OAL examples — Alpha-v0.1.0-Alkimim

[Português](README.pt-br.md) · [Home](../../../README.md) · [Historical reference rules](../README.md)

These are the historical examples of the Alpha-v0.1.0-Alkimim edition, preserved as historical reference. They are not the current edition. Each package contains UCS (P1), ADPM and ADVS (P2), ADI (P3), ADIB (P4), and a derivation record. Their needs baselines were reconstructed from the UCS for teaching purposes; they are not independent stakeholder records.

## Tiny Catalog

[Tiny Catalog](tiny-catalog/README.md) manages a small item catalog. Its four cases register, retrieve, list, and deactivate items. A **maintainer** may use all four cases; a **reader** may retrieve and list. Start it at `http://127.0.0.1:8000/` with the demonstration accounts `maintainer` / `maintainer-demo` or `reader` / `reader-demo`. See the [UCS](tiny-catalog/OAL-P1/UCS.md), [ADPM](tiny-catalog/OAL-P2/adpm/MODEL.md), [ADVS](tiny-catalog/OAL-P2/advs/SCENARIOS.md), [ADI](tiny-catalog/OAL-P3/IMPLEMENTATION.md), [ADIB](tiny-catalog/OAL-P4/HTTP.md), and [derivation record](tiny-catalog/derivations.json).

## Board CRM

[Board CRM](board-crm/README.md) presents opportunities on a drag-and-drop sales board. Its six cases create, move, annotate, view, close as won, and close as lost. A **manager** may use all six cases; an **operator** may create, move, note, and view; a **viewer** may only view. Start it at `http://127.0.0.1:8001/` with `manager` / `manager-demo`, `operator` / `operator-demo`, or `viewer` / `viewer-demo`. See the [UCS JSON](board-crm/OAL-P1/ucs.json), [ADPM](board-crm/OAL-P2/adpm/MODEL.md), [ADVS](board-crm/OAL-P2/advs/SCENARIOS.md), [ADI](board-crm/OAL-P3/IMPLEMENTATION.md), [ADIB](board-crm/OAL-P4/HTTP.md), and [derivation record](board-crm/derivations.json).

## Work Board

[Work Board](work-board/README.md) is a small issue tracker. Its six cases create, assign, and advance work items, add comments, and read the board and discussion. Start it at `http://127.0.0.1:8002/` with `manager` / `manager-demo`, `contributor` / `contributor-demo`, or `viewer` / `viewer-demo`. See the [UCS](work-board/OAL-P1/UCS.md), [ADPM](work-board/OAL-P2/adpm/MODEL.md), [ADVS](work-board/OAL-P2/advs/SCENARIOS.md), [ADI](work-board/OAL-P3/IMPLEMENTATION.md), and [ADIB](work-board/OAL-P4/HTTP.md).

## Run an example

From the repository root, use the shared [launcher](../../../run_examples.py). Because this is a historical edition, name the edition explicitly:

```bash
python run_examples.py Alpha-v0.1.0-Alkimim/tiny-catalog
python run_examples.py Alpha-v0.1.0-Alkimim/board-crm
python run_examples.py Alpha-v0.1.0-Alkimim/work-board
```

`python run_examples.py --list` lists every example of every edition. A bare example name resolves to the current edition; use `EDITION/NAME` for historical editions.

Each example directory contains a `runner.json` with its executor, entrypoint, default port, and database name. The launcher creates the default SQLite files under the repository's ignored `data/` directory, in an edition-specific subdirectory. The options come after the selection, for example:

```bash
python run_examples.py Alpha-v0.1.0-Alkimim/tiny-catalog --port 8010 --no-browser
```

The demonstration passwords are for local use; each example README explains how to change them with environment variables. The launcher only starts applications; it is not an OAL derivation engine.
