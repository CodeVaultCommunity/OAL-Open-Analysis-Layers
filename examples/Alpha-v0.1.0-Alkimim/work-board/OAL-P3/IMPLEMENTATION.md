# Work Board · P3 implementation

[Português](IMPLEMENTATION.pt-br.md) · [Model](../OAL-P2/adpm/MODEL.md) · [Example](../README.md)

The callable application core is under [`src/work_board`](../src/work_board). [`usecases`](../src/work_board/usecases) holds workflow and permission decisions; [`entities.py`](../src/work_board/entities.py) holds data shapes and field validation; [`tools`](../src/work_board/tools) contains the storage contract, SQLite adapter, and identifier and clock providers. [`composition.py`](../src/work_board/composition.py) selects concrete tools and constructs six case instances. No core module imports the browser or HTTP adapter.

Assignment and transition use an expected version. SQLite updates compare that version atomically and increase it on success. A transition is additionally restricted to the next state. Comments are stored separately and do not alter the item version. [`tests/p3`](../tests/p3) exercises the callable cases directly; its functions support the [six ADVS identities](../OAL-P2/advs/behavioral-tests.json).

The [P4 adapter](../OAL-P4/HTTP.md) receives requests, authenticates the caller, invokes a case, and maps results to HTTP. It contains no workflow or permission rule.
