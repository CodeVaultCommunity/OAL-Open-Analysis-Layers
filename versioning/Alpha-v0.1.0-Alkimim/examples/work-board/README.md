# Work Board · OAL Alpha-v0.1.0-Alkimim example

[Português](README.pt-br.md) · [Home](../../../../README.md) · [Examples](../README.md)

Work Board is a small local issue tracker with projects, backlog, assignment, a three-state workflow, comments, and filters. It uses Python and SQLite. Its six use cases are described in the [UCS](OAL-P1/UCS.md). The [needs baseline](needs-baseline.json) was reconstructed from those cases for illustration; it is not independent stakeholder evidence.

## Where the responsibilities live

| OAL responsibility | Specification | Python implementation |
| --- | --- | --- |
| P1 · L1 | [UCS](OAL-P1/UCS.md) and [case data](OAL-P1/ucs.json) | Case IDs and permission checks in [`usecases`](src/work_board/usecases) |
| P2 · L2.1 and L2.2 | [Program model](OAL-P2/adpm/MODEL.md), [case map](OAL-P2/adpm/traceability.json), and [behavioral tests](OAL-P2/advs/behavioral-tests.json) | Contracts in [`tools`](src/work_board/tools); checks in [`tests/p3`](tests/p3) |
| P3 · L3 | [Implementation decisions](OAL-P3/IMPLEMENTATION.md) | [`entities`](src/work_board/entities.py), [`usecases`](src/work_board/usecases), [`tools`](src/work_board/tools), and [`composition`](src/work_board/composition.py) |
| P4 · L4 | [HTTP contract](OAL-P4/HTTP.md) and [interface map](OAL-P4/traceability.json) | [`transport`](src/work_board/transport) and [`tests/p4`](tests/p4) |

The dependency direction is P4 → P3. Cases know nothing about routes, forms, JSON, HTTP statuses, or Basic credentials. The [derivation record](derivations.json) names all five transitions.

## Run

From the repository root, use `python versioning/Alpha-v0.1.0-Alkimim/run_examples.py work-board`. Open `http://127.0.0.1:8002/`. The local demonstration accounts are `manager` / `manager-demo`, `contributor` / `contributor-demo`, and `viewer` / `viewer-demo`. Managers can assign; contributors can create, advance, and comment; viewers can read. Override passwords with `OAL_WORK_BOARD_MANAGER_PASSWORD`, `OAL_WORK_BOARD_CONTRIBUTOR_PASSWORD`, and `OAL_WORK_BOARD_VIEWER_PASSWORD`. Data goes to the ignored `versioning/Alpha-v0.1.0-Alkimim/data/work-board.sqlite3` file. Stop with Ctrl+C.

Inside the edition directory, use `python run_examples.py work-board`. The default database is `versioning/Alpha-v0.1.0-Alkimim/data/work-board.sqlite3`. `--database` accepts an absolute path or a path relative to the working directory; the [operational guide](../README.md#run-an-example) explains how to reuse old databases without moving them.

Run `python -m pytest -q --basetemp .pytest_cache/oal-work-board-temp` from this example directory for direct case and HTTP checks. The demonstration binds to loopback and is not a production account system.
