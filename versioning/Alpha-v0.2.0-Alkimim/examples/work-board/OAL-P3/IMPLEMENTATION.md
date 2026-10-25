# Work Board · P3 implementation

[Português](IMPLEMENTATION.pt-br.md) · [Model](../OAL-P2/adpm/MODEL.md) · [Example](../README.md)

The callable application core is under [`src/work_board`](../src/work_board). [`usecases`](../src/work_board/usecases) holds workflow and permission decisions; [`entities.py`](../src/work_board/entities.py) holds the data shapes and the `required_text` helper that the cases apply; [`tools`](../src/work_board/tools) contains the storage contract, SQLite adapter, and identifier and clock providers. [`composition.py`](../src/work_board/composition.py) selects concrete tools and constructs six case instances. No core module imports the browser or HTTP adapter. The core module set is `authorization.py`, `composition.py`, `entities.py`, `errors.py`, `tools/`, and `usecases/`. `__main__.py` is the application initializer and `transport/` is the P4 boundary; both are outside the core scope and may import the adapter.

Assignment and transition use an expected version. SQLite updates compare that version atomically and increase it on success. A transition is additionally restricted to the next state. Comments are stored separately and do not alter the item version. [`tests/p3`](../tests/p3) exercises the callable cases directly; its functions support the [six ADVS identities](../OAL-P2/advs/behavioral-tests.json).

The [P4 adapter](../OAL-P4/HTTP.md) receives requests, authenticates the caller, invokes a case, and maps results to HTTP. It contains no workflow or permission rule.

## Error and representation decisions

SQLite errors are translated into `Unavailable` at the storage boundary. Errors before commit are reported with `write_outcome=not_applied` when rollback succeeds; an error during commit or failed rollback is reported as `unknown`. The update result is read within the write transaction and returned only after commit, so there is no second post-commit read that can erase the outcome of a completed mutation.

SQLite integer capacity is a representation constraint. An expected version above `2**63-1` cannot match a stored version and is classified as conflict or missing without binding an oversized integer. A counter already at `2**63-1` cannot be incremented in this adapter; it yields `Unavailable` with `not_applied` before mutation. The atomic compare-and-set remains the write condition for representable updates.

`principal` represents the resolved actor context as a role string in this code organization. The caller establishes it through the trusted entry mechanism; authorization remains in every case.
