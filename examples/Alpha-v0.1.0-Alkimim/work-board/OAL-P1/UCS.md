# Work Board · P1 use cases

[Português](UCS.pt-br.md) · [Example](../README.md) · [Structured UCS](ucs.json)

The six stable case IDs in [ucs.json](ucs.json) define the goals, actors, results, and acceptance criteria. Managers may use all six cases. Contributors may create, advance, comment, and read. Viewers may only read. Missing identity and roles outside each case's permission set are denied before effects.

An item belongs to a project, has a priority, and moves through `backlog → in_progress → done`. Assignment uses a version check so a stale request cannot overwrite a newer value. Comments do not change the item version. The board and comment views do not mutate records. Interface routes, forms, and credentials belong to [P4](../OAL-P4/HTTP.md), not this contract.

The [needs baseline](../needs-baseline.json) was reconstructed from these cases to make the teaching derivation explicit. It is not a historical record of stakeholder interviews.
