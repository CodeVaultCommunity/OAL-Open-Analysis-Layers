# OAL examples — Alpha-v0.1.0-Alkimim

[Português](README.pt-br.md) · [Home](../README.md) · [Reference rules](../versioning/Alpha-v0.1.0-Alkimim.md)

The three examples use Python and SQLite, but solve different problems: a small catalog, a sales board, and a work-item board. Each includes UCS (P1), ADPM and ADVS (P2), ADI (P3), ADIB (P4), and a derivation record. Their needs baselines were reconstructed from the UCS for teaching purposes; they are not independent stakeholder records. The individual READMEs show where the case rules end and the browser and HTTP adapters begin.

## Tiny Catalog

[Tiny Catalog](Alpha-v0.1.0-Alkimim/tiny-catalog/README.md) manages a small item catalog. Its four cases register an item, retrieve one item, list available items, and deactivate an item. Deactivation retains the record; code uniqueness is checked atomically in SQLite. A **maintainer** may use all four cases; a **reader** may retrieve and list. Case permissions are enforced even when a case is called outside the browser.

Start it at `http://127.0.0.1:8000/`. The local HTTP Basic demonstration accounts are `maintainer` / `maintainer-demo` and `reader` / `reader-demo`. See the [UCS](Alpha-v0.1.0-Alkimim/tiny-catalog/OAL-P1/UCS.md), [ADPM](Alpha-v0.1.0-Alkimim/tiny-catalog/OAL-P2/adpm/MODEL.md), [ADVS](Alpha-v0.1.0-Alkimim/tiny-catalog/OAL-P2/advs/SCENARIOS.md), [ADI notes](Alpha-v0.1.0-Alkimim/tiny-catalog/OAL-P3/IMPLEMENTATION.md), [ADIB contract](Alpha-v0.1.0-Alkimim/tiny-catalog/OAL-P4/HTTP.md), and [derivation record](Alpha-v0.1.0-Alkimim/tiny-catalog/derivations.json).

## Board CRM

[Board CRM](Alpha-v0.1.0-Alkimim/board-crm/README.md) presents opportunities on a drag-and-drop sales board. Its six cases create an opportunity, move it between stages, record an interaction, view the board, close an opportunity as won, and close one as lost. It retains notes and stage history in SQLite and checks versions when changing a card. A **manager** may use all six cases; an **operator** may create, move, note, and view; a **viewer** may only view.

Start it at `http://127.0.0.1:8001/`. The local HTTP Basic demonstration accounts are `manager` / `manager-demo`, `operator` / `operator-demo`, and `viewer` / `viewer-demo`. The [UCS JSON](Alpha-v0.1.0-Alkimim/board-crm/OAL-P1/ucs.json) also has [English](Alpha-v0.1.0-Alkimim/board-crm/OAL-P1/UCS.tex) and [Portuguese](Alpha-v0.1.0-Alkimim/board-crm/OAL-P1/UCS.pt-br.tex) LaTeX representations. See its [ADPM](Alpha-v0.1.0-Alkimim/board-crm/OAL-P2/adpm/MODEL.md), [ADVS](Alpha-v0.1.0-Alkimim/board-crm/OAL-P2/advs/SCENARIOS.md), [ADI notes](Alpha-v0.1.0-Alkimim/board-crm/OAL-P3/IMPLEMENTATION.md), [ADIB contract](Alpha-v0.1.0-Alkimim/board-crm/OAL-P4/HTTP.md), and [derivation record](Alpha-v0.1.0-Alkimim/board-crm/derivations.json).

## Work Board

[Work Board](Alpha-v0.1.0-Alkimim/work-board/README.md) is a small issue tracker for project backlogs. Its six cases create, assign, and advance work items, add comments, and read the board and discussion. It uses a three-state workflow and checks versions when assigning or advancing. Start it at `http://127.0.0.1:8002/` with the local accounts `manager` / `manager-demo`, `contributor` / `contributor-demo`, or `viewer` / `viewer-demo`. The [UCS](Alpha-v0.1.0-Alkimim/work-board/OAL-P1/UCS.md), [ADPM](Alpha-v0.1.0-Alkimim/work-board/OAL-P2/adpm/MODEL.md), [ADVS](Alpha-v0.1.0-Alkimim/work-board/OAL-P2/advs/SCENARIOS.md), [ADI](Alpha-v0.1.0-Alkimim/work-board/OAL-P3/IMPLEMENTATION.md), and [ADIB](Alpha-v0.1.0-Alkimim/work-board/OAL-P4/HTTP.md) describe the boundaries.

## Run an example

The current examples require Python 3.12 or later. From the repository root, use [run_examples.py](run_examples.py):

```bash
python examples/run_examples.py tiny-catalog
python examples/run_examples.py board-crm
python examples/run_examples.py work-board
```

From the `examples` directory, use `python run_examples.py NAME`, with `NAME` set to `tiny-catalog`, `board-crm`, or `work-board`. The launcher imports each Python example from its `src` directory, starts a server bound to `127.0.0.1`, and opens the page in a browser. It creates the default SQLite files under the repository's ignored `data/` directory. Stop the server with Ctrl+C.

The options come **after** the example name:

| Option | Effect |
| --- | --- |
| `--port 8010` | Use another local port instead of 8000, 8001, or 8002. |
| `--database PATH` | Use a specified SQLite file instead of the default under `data/`. |
| `--no-browser` | Start the server without opening a browser. |
| `--help` | Show options for the selected example. |

For example, `python examples/run_examples.py tiny-catalog --port 8010 --no-browser` starts Tiny Catalog on port 8010. The demonstration passwords are for local use; each example README explains how to change them with environment variables.

## Adding another execution language

The launcher selects an executor from the `EXECUTORS` registry. `ExampleExecutor` is its interface; `PythonWSGIExecutor` handles the current examples. A new language can provide another executor and register its examples in `EXAMPLES`, with its own entry point and arguments. The main command stays in this directory.
