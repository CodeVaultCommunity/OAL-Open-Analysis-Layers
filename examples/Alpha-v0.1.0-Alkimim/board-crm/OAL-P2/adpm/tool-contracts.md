# Board CRM storage tool contract

[Português](tool-contracts.pt-br.md) · [Home](../../../../../README.md)

`Store` in [contracts.py](../../src/board_crm/tools/contracts.py) is the boundary
used by the six cases. [SQLiteStore](../../src/board_crm/tools/sqlite_store.py) is
one implementation. The case classes receive a `Store`, not a SQLite connection.

## Operations and guarantees

| Operation | Result | Effect and guarantee |
| --- | --- | --- |
| `create(card, actor)` | None | Add one opportunity and its creation event in one transaction. A duplicate ID raises `Conflict`. |
| `get(id)` | Opportunity | Read one independent entity. An unknown ID raises `Missing`. |
| `mutate(id, expected_version, time, actor, ...)` | Updated Opportunity | Compare versions atomically; change the card and append an optional note and/or stage event in the same transaction. A stale version raises `Conflict` without a partial change. |
| `list_records()` | Opportunities with notes and events | Return independent entities. Grouping, owner filtering, and card order are decided by `ViewBoard`. |

Storage errors raise `Unavailable`. A case reports success only after the
transaction has committed. As in the Tiny Catalog example, an unavailable
result during an uncertain write is not proof that no write occurred.

`IdentifierProvider` returns an opaque, nonempty ID. `Clock` returns a
timezone-aware, lexically sortable timestamp. Both contracts are in
`tools/contracts.py`; their local implementations are in `tools/providers.py`.
The storage tool does not call them or select allowed stages. Stage decisions
and text limits remain in the use cases and data entities respectively.

## Documentation index

[Implementation](../../OAL-P3/IMPLEMENTATION.md) · [Traceability](traceability.json) ·
[UCS JSON](../../OAL-P1/ucs.json) · [Example README](../../README.md)
