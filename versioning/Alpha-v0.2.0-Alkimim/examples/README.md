# OAL examples — Alpha-v0.2.0-Alkimim

[Português](README.pt-br.md) · [Home](../../../README.md) · [Reference rules](../README.md#reference-rules)

The runnable examples of this edition are in this directory, adapted from the [Alpha-v0.1.0-Alkimim examples](../../Alpha-v0.1.0-Alkimim/examples/README.md), which are preserved unchanged as history. Each package presents project artifacts associated with the OAL responsibilities: UCS (L1), the ADPM and ADVS components of L2, ADI (L3), ADIB (L4), and derivation records. The artifacts instantiate four reusable models, one per layer, defined under [models/](models/README.md). The records do not demonstrate the construction or execution of deterministic transformers between models: the models were applied manually. Their needs baselines were reconstructed from the UCS for teaching purposes; they are not independent stakeholder records. The individual READMEs show where the case rules end and the browser and HTTP adapters begin.

The three examples use Python and SQLite but solve different problems: a small catalog, a sales board, and a work-item board.

## Models and instance manifests

The four models are OAL-EX-M1-CASE-CONTRACTS (L1), OAL-EX-M2-PROGRAM-SCENARIOS (L2), OAL-EX-M3-PYTHON-CORE (L3), and OAL-EX-M4-HTTP-BOUNDARY (L4), each at version 0.1.0. The family README documents the common manifest format. Each project declares its four instances in model-instances.json, twelve declarations in total. A declaration identifies the model and version, the files and symbols that compose the artifact, the scope, the case and interface mappings, the evidence state, and the limits.

The models are example models: their conformance review is documented in each MODEL.md, while the project instances are reviewed against the selected model. Specifying a model, declaring an instance, and executing a check are three different results.

## Tiny Catalog

[Tiny Catalog](tiny-catalog/README.md) manages a small item catalog. Its four cases register an item, retrieve one item, list available items, and deactivate an item. Deactivation retains the record; code uniqueness is checked atomically in SQLite. A **maintainer** may use all four cases; a **reader** may retrieve and list. Case permissions are enforced even when a case is called outside the browser.

Start it at `http://127.0.0.1:8000/`. The local HTTP Basic demonstration accounts are `maintainer` / `maintainer-demo` and `reader` / `reader-demo`. See the [UCS](tiny-catalog/OAL-P1/UCS.md), [ADPM](tiny-catalog/OAL-P2/adpm/MODEL.md), [ADVS](tiny-catalog/OAL-P2/advs/SCENARIOS.md), [ADI notes](tiny-catalog/OAL-P3/IMPLEMENTATION.md), [ADIB contract](tiny-catalog/OAL-P4/HTTP.md), and [derivation record](tiny-catalog/derivations.json).

## Board CRM

[Board CRM](board-crm/README.md) presents opportunities on a drag-and-drop sales board. Its six cases create an opportunity, move it between stages, record an interaction, view the board, close an opportunity as won, and close one as lost. It retains notes and stage history in SQLite and checks versions when changing a card. A **manager** may use all six cases; an **operator** may create, move, note, and view; a **viewer** may only view.

Start it at `http://127.0.0.1:8001/`. The local HTTP Basic demonstration accounts are `manager` / `manager-demo`, `operator` / `operator-demo`, and `viewer` / `viewer-demo`. The [UCS JSON](board-crm/OAL-P1/ucs.json) also has [English](board-crm/OAL-P1/UCS.tex) and [Portuguese](board-crm/OAL-P1/UCS.pt-br.tex) LaTeX representations rendered from that source. See its [ADPM](board-crm/OAL-P2/adpm/MODEL.md), [ADVS](board-crm/OAL-P2/advs/SCENARIOS.md), [ADI notes](board-crm/OAL-P3/IMPLEMENTATION.md), [ADIB contract](board-crm/OAL-P4/HTTP.md), and [derivation record](board-crm/derivations.json).

## Work Board

[Work Board](work-board/README.md) is a small issue tracker for project backlogs. Its six cases create, assign, and advance work items, add comments, and read the board and discussion. It uses a three-state workflow and checks versions when assigning or advancing. Start it at `http://127.0.0.1:8002/` with the local accounts `manager` / `manager-demo`, `contributor` / `contributor-demo`, or `viewer` / `viewer-demo`. The [UCS](work-board/OAL-P1/UCS.md), [ADPM](work-board/OAL-P2/adpm/MODEL.md), [ADVS](work-board/OAL-P2/advs/SCENARIOS.md), [ADI](work-board/OAL-P3/IMPLEMENTATION.md), and [ADIB](work-board/OAL-P4/HTTP.md) describe the boundaries.

## Run an example

Use Python 3.12 or later and [this edition's launcher](../run_examples.py). From the repository root:

```bash
python versioning/Alpha-v0.2.0-Alkimim/run_examples.py --list
python versioning/Alpha-v0.2.0-Alkimim/run_examples.py tiny-catalog
python versioning/Alpha-v0.2.0-Alkimim/run_examples.py board-crm
python versioning/Alpha-v0.2.0-Alkimim/run_examples.py work-board
```

Inside `versioning/Alpha-v0.2.0-Alkimim/`, use `python run_examples.py NAME` or `python run_examples.py --list`. The list contains only this edition's three examples; selection accepts a bare name without `EDITION/`. Choose another edition through its own launcher path. An isolated copy of the edition directory, even renamed, retains its identity and works without repository-root files. From an unrelated working directory, supply the launcher's absolute path.

The launcher reads only its sibling `examples/*/runner.json`, imports the selected example's `src`, binds to `127.0.0.1`, and opens a browser by default. Stop with Ctrl+C. It only starts applications; it is not an OAL derivation engine.

Options come **after** the example name:

| Option | Effect |
| --- | --- |
| `--port 8011` | Override the port declared in `runner.json` (8000, 8001, or 8002). |
| `--database PATH` | Use the specified SQLite file; relative paths use the current working directory, and absolute paths are accepted. |
| `--no-browser` | Start without opening a browser. |
| `--help` | Show the selected example's options. |

For example, from the root: `python versioning/Alpha-v0.2.0-Alkimim/run_examples.py board-crm --port 8011 --no-browser`.

The default database is `versioning/Alpha-v0.2.0-Alkimim/data/<database_name>`, next to `examples/`, independently of the working directory. Existing databases under the root's `data/Alpha-v0.2.0-Alkimim/` stay in place: there is no automatic migration or deletion. To reuse one from the root, run `python versioning/Alpha-v0.2.0-Alkimim/run_examples.py work-board --database data/Alpha-v0.2.0-Alkimim/work-board.sqlite3`; from another directory, supply the old database's absolute path.

Demonstration passwords are for local use; each README explains the environment variables. `PythonWSGIExecutor` interprets the local `runner.json` declarations; the launcher needs no shared module in another edition or at the repository root.

## Execution evidence

The [structured execution record](verification/execution.json) preserves the application-test run of **2026-10-24**, with its original timestamps, environment, commands, results, and logs. That run recorded 90 passed tests for Tiny Catalog, 23 passed tests and 36 passed subtests for Board CRM, and 32 passed tests for Work Board: **145 passed tests and 36 passed subtests**. The same record includes the Board CRM TeX representation check.

The suites exercise the callable cores and WSGI adapters; Tiny Catalog also exercises a real loopback HTTP server. They do not execute browser JavaScript or assess visual accessibility. Work Board commit-failure checks use controlled SQLite faults and do not establish arbitrary crash or power-loss guarantees. These finite observations do not constitute a general proof of conformance or a constructed or executed OAL derivation transformer.

The mathematical-notation refinement and skill integration were documentation and packaging updates. Application source code and tests remain unchanged from the recorded run, and the application suites were not rerun for those updates. The [structural checks](verification/structural-checks.json) were refreshed for the final package; the [content inventory](../../../CONTENT-SHA256.json) identifies all delivered bytes, including the retained execution evidence and the informational skill.
