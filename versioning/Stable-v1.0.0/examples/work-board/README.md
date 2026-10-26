# Work Board · OAL Stable-v1.0.0 example

[Português](README.pt-br.md) · [Home](../../../../README.md) · [Examples](../README.md)

Work Board is a small local issue tracker with projects, backlog, assignment, a three-state workflow, comments, and filters. It uses Python and SQLite. Its six use cases are described in the [UCS](OAL-P1/UCS.md). The [needs baseline](needs-baseline.json) was reconstructed from those cases for illustration; it is not independent stakeholder evidence.

> This package presents project artifacts associated with the OAL responsibilities (L1–L4), adapted from the Alpha-v0.1.0-Alkimim example. The artifacts instantiate the four reusable models under `../models/` (version 0.1.0); the declarations are in [`model-instances.json`](model-instances.json). The models were applied manually, so the records do not demonstrate the construction or execution of deterministic transformers. The needs baseline remains reconstructed. The [derivation records](derivations.json) are didactic derivation records, not engine executions.

## Where the responsibilities live

| OAL responsibility | Specification | Python implementation |
| --- | --- | --- |
| P1 · L1 | [UCS](OAL-P1/UCS.md) and [case data](OAL-P1/ucs.json) | Case IDs and permission checks in [`usecases`](src/work_board/usecases) |
| P2 · L2 (ADPM and ADVS) | [Program model](OAL-P2/adpm/MODEL.md), [case map](OAL-P2/adpm/traceability.json), and [behavioral tests](OAL-P2/advs/behavioral-tests.json) | Contracts in [`tools`](src/work_board/tools); checks in [`tests/p3`](tests/p3) |
| P3 · L3 | [Implementation decisions](OAL-P3/IMPLEMENTATION.md) | [`entities`](src/work_board/entities.py), [`usecases`](src/work_board/usecases), [`tools`](src/work_board/tools), and [`composition`](src/work_board/composition.py) |
| P4 · L4 | [HTTP contract](OAL-P4/HTTP.md) and [interface map](OAL-P4/traceability.json) | [`transport`](src/work_board/transport) and [`tests/p4`](tests/p4) |

The dependency direction is P4 → P3. Cases know nothing about routes, forms, JSON, HTTP statuses, or Basic credentials. Core modules do not import the interaction adapter. The [derivation record](derivations.json) names the four transitions (needs→L1, L1→L2, L2→L3, L3→L4).

## Run

From the repository root, use `python run_examples.py work-board`. Open `http://127.0.0.1:8002/`. The local demonstration accounts are `manager` / `manager-demo`, `contributor` / `contributor-demo`, and `viewer` / `viewer-demo`. Managers can assign; contributors can create, advance, and comment; viewers can read. Override passwords with `OAL_WORK_BOARD_MANAGER_PASSWORD`, `OAL_WORK_BOARD_CONTRIBUTOR_PASSWORD`, and `OAL_WORK_BOARD_VIEWER_PASSWORD`. Data goes to the ignored `data/Stable-v1.0.0/work-board.sqlite3` file. Stop with Ctrl+C.

To run checks from this example directory, create and activate an isolated environment, install the declared test extra with `python -m pip install -e ".[test]"`, then run `python -m pytest -q`. The extra pins pytest 9.0.2. The suite covers direct cases, storage contracts, and WSGI HTTP handling, including oversized expected versions, unavailable storage, and unconfirmed commit outcomes. The demonstration binds to loopback and is not a production account system.

## Documentation index

[OAL Stable-v1.0.0](../../README.md) · [Examples](../README.md) · [UCS](OAL-P1/UCS.md) · [ADPM](OAL-P2/adpm/MODEL.md) · [ADVS](OAL-P2/advs/SCENARIOS.md) · [ADI](OAL-P3/IMPLEMENTATION.md) · [ADIB](OAL-P4/HTTP.md)
