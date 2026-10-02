# Board CRM · OAL Alpha-v0.1.0-Alkimim example

[Português](README.pt-br.md) · [Home](../../../README.md)

Board CRM tracks sales opportunities across five stages. Its six cases create and move opportunities, record notes, show the board, and close a deal as won or lost. SQLite retains the history, and version checks reject changes based on an old card.

## UCS and permissions

The [UCS](OAL-P1/ucs.json) gives managers all six cases, operators the create, move, note, and view cases, and viewers the view case. Each case checks permission before accessing data, including when called without HTTP.

The same UCS content is in [JSON](OAL-P1/ucs.json) and [LaTeX](OAL-P1/UCS.tex). [Portuguese LaTeX](OAL-P1/UCS.pt-br.tex) is rendered from translated JSON fields. The JSON is the content source; format does not define UCS.

## OAL artifacts

- [Reconstructed needs baseline](needs-baseline.json) and [UCS](OAL-P1/ucs.json) in OAL-P1.
- [ADPM program model](OAL-P2/adpm/MODEL.md), [tool contracts](OAL-P2/adpm/tool-contracts.md), and [case map](OAL-P2/adpm/traceability.json).
- [ADVS verification scenarios](OAL-P2/advs/SCENARIOS.md) and [behavioral test identities](OAL-P2/advs/behavioral-tests.json).
- [ADI implementation decisions](OAL-P3/IMPLEMENTATION.md) and [case checks](tests/p3).
- [ADIB HTTP contract](OAL-P4/HTTP.md), [interface map](OAL-P4/traceability.json), and [channel checks](tests/p4).
- [Named derivations](derivations.json) for the five transitions.

In code, [`usecases`](src/board_crm/usecases) makes case and stage decisions, [`entities.py`](src/board_crm/entities.py) defines the data, [`tools`](src/board_crm/tools) defines and implements storage, and [`composition.py`](src/board_crm/composition.py) connects them. HTTP authentication, routes, JSON, and browser files live in [`transport`](src/board_crm/transport). The [repository validator](../../validate_oal.py) checks that the core does not import P4.

## Run in a browser

With Python 3.12 or later, run from the repository root:

```bash
python examples/run_examples.py board-crm
```

The launcher opens `http://127.0.0.1:8001/`. The browser requests HTTP Basic credentials on the first API call. Use `manager` / `manager-demo`, `operator` / `operator-demo`, or `viewer` / `viewer-demo`. To switch accounts, use another private browser session or clear the stored credentials. Defaults can be changed with `OAL_CRM_<ROLE>_PASSWORD` environment variables. The demonstration binds to loopback; its fixed example passwords are for local use.

Stop the server with Ctrl+C. The [examples guide](../../README.md#run-an-example) explains the launcher options.

## Verification

Install `pytest==9.0.2` and run `python -m pytest` from this directory. The suite covers entities, SQLite storage, use cases, authorization, and the local HTTP adapter. A passing run describes the scenarios and environment exercised.

## Documentation index

[OAL Alpha-v0.1.0-Alkimim](../../../versioning/Alpha-v0.1.0-Alkimim.md) · [Examples](../../README.md) · [UCS](OAL-P1/ucs.json) · [ADPM](OAL-P2/adpm/MODEL.md) · [ADVS](OAL-P2/advs/SCENARIOS.md) · [ADI](OAL-P3/IMPLEMENTATION.md) · [ADIB](OAL-P4/HTTP.md)
