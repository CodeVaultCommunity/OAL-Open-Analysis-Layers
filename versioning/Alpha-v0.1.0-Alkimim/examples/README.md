# OAL examples — Alpha-v0.1.0-Alkimim

[Português](README.pt-br.md) · [Home](../../../README.md) · [Historical reference rules](../README.md#reference-rules)

These are the historical examples of the Alpha-v0.1.0-Alkimim edition, preserved as historical reference. They are not the current edition. Each package contains UCS (P1), ADPM and ADVS (P2), ADI (P3), ADIB (P4), and a derivation record. Their needs baselines were reconstructed from the UCS for teaching purposes; they are not independent stakeholder records.

## Tiny Catalog

[Tiny Catalog](tiny-catalog/README.md) manages a small item catalog. Its four cases register, retrieve, list, and deactivate items. A **maintainer** may use all four cases; a **reader** may retrieve and list. Start it at `http://127.0.0.1:8000/` with the demonstration accounts `maintainer` / `maintainer-demo` or `reader` / `reader-demo`. See the [UCS](tiny-catalog/OAL-P1/UCS.md), [ADPM](tiny-catalog/OAL-P2/adpm/MODEL.md), [ADVS](tiny-catalog/OAL-P2/advs/SCENARIOS.md), [ADI](tiny-catalog/OAL-P3/IMPLEMENTATION.md), [ADIB](tiny-catalog/OAL-P4/HTTP.md), and [derivation record](tiny-catalog/derivations.json).

## Board CRM

[Board CRM](board-crm/README.md) presents opportunities on a drag-and-drop sales board. Its six cases create, move, annotate, view, close as won, and close as lost. A **manager** may use all six cases; an **operator** may create, move, note, and view; a **viewer** may only view. Start it at `http://127.0.0.1:8001/` with `manager` / `manager-demo`, `operator` / `operator-demo`, or `viewer` / `viewer-demo`. See the [UCS JSON](board-crm/OAL-P1/ucs.json), [ADPM](board-crm/OAL-P2/adpm/MODEL.md), [ADVS](board-crm/OAL-P2/advs/SCENARIOS.md), [ADI](board-crm/OAL-P3/IMPLEMENTATION.md), [ADIB](board-crm/OAL-P4/HTTP.md), and [derivation record](board-crm/derivations.json).

## Work Board

[Work Board](work-board/README.md) is a small issue tracker. Its six cases create, assign, and advance work items, add comments, and read the board and discussion. Start it at `http://127.0.0.1:8002/` with `manager` / `manager-demo`, `contributor` / `contributor-demo`, or `viewer` / `viewer-demo`. See the [UCS](work-board/OAL-P1/UCS.md), [ADPM](work-board/OAL-P2/adpm/MODEL.md), [ADVS](work-board/OAL-P2/advs/SCENARIOS.md), [ADI](work-board/OAL-P3/IMPLEMENTATION.md), and [ADIB](work-board/OAL-P4/HTTP.md).

## Run an example

Use Python 3.12 or later and [this edition's launcher](../run_examples.py). From the repository root:

```bash
python versioning/Alpha-v0.1.0-Alkimim/run_examples.py --list
python versioning/Alpha-v0.1.0-Alkimim/run_examples.py tiny-catalog
python versioning/Alpha-v0.1.0-Alkimim/run_examples.py board-crm
python versioning/Alpha-v0.1.0-Alkimim/run_examples.py work-board
```

Inside `versioning/Alpha-v0.1.0-Alkimim/`, use `python run_examples.py NAME` or `python run_examples.py --list`. The list contains only this edition's three examples; selection accepts a bare name without `EDITION/`. Choose another edition through its own launcher path. An isolated copy of the edition directory, even renamed, retains its identity and works without repository-root files. From an unrelated working directory, supply the launcher's absolute path.

The launcher reads only its sibling `examples/*/runner.json`, imports the selected example's `src`, binds to `127.0.0.1`, and opens a browser by default. Stop with Ctrl+C. It only starts applications; it is not an OAL derivation engine.

Options come **after** the example name:

| Option | Effect |
| --- | --- |
| `--port 8011` | Override the port declared in `runner.json` (8000, 8001, or 8002). |
| `--database PATH` | Use the specified SQLite file; relative paths use the current working directory, and absolute paths are accepted. |
| `--no-browser` | Start without opening a browser. |
| `--help` | Show the selected example's options. |

For example, from the root: `python versioning/Alpha-v0.1.0-Alkimim/run_examples.py board-crm --port 8011 --no-browser`.

The default database is `versioning/Alpha-v0.1.0-Alkimim/data/<database_name>`, next to `examples/`, independently of the working directory. Existing databases under the root's `data/Alpha-v0.1.0-Alkimim/` stay in place: there is no automatic migration or deletion. To reuse one from the root, run `python versioning/Alpha-v0.1.0-Alkimim/run_examples.py work-board --database data/Alpha-v0.1.0-Alkimim/work-board.sqlite3`; from another directory, supply the old database's absolute path.

Demonstration passwords are for local use; each README explains the environment variables. `PythonWSGIExecutor` interprets the local `runner.json` declarations; the launcher needs no shared module in another edition or at the repository root.
