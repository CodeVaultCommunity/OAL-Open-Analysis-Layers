# Work Board · L2/ADPM program model

[Português](MODEL.pt-br.md) · [UCS](../../OAL-P1/UCS.md) · [Example](../../README.md)

**Source:** [project UCS](../../OAL-P1/ucs.json), baseline 0.2.0.
**Classification:** project artifact of the L2 program-model component (ADPM) under OAL Alpha-v0.2.0-Alkimim; instantiating OAL-EX-M2-PROGRAM-SCENARIOS 0.1.0; see `model-instances.json` for the instance declaration.

The model has one case identity per UCS ID. `CreateItem` validates project, title, description, and priority, then creates a backlog item. `AssignItem` and `TransitionItem` apply an expected-version check; transition permits only the next state. `AddComment` validates text and records the runtime actor. `ViewBoard` filters without mutation, and `ViewComments` reads one item's discussion.

`WorkItem` and `Comment` carry validated data. Case policy and actor permissions stay in the use cases. The `WorkStore` contract provides create, get, assign, transition, comment, and read capabilities. Identifier and clock providers supply values without choosing a transport. [Composition](../../src/work_board/composition.py) injects a SQLite store into the six [case classes](../../src/work_board/usecases/operations.py); the concrete store is an L3 choice. [Traceability](traceability.json) names each case, test identity, implementation, and interface exposure.

The model does not select URLs, HTML, HTTP Basic, JSON status codes, or browser controls. Those decisions are documented in [P4](../../OAL-P4/HTTP.md).

## Actor and storage contracts

The explicit `principal` input is this model's representation of a resolved actor context. All cases in this example require authenticated callers; the trusted entry point establishes the role and each case authorizes its own operation.

[`WorkStore`](../../src/work_board/tools/contracts.py) declares `Conflict`, `Missing`, and `Unavailable` separately. The cases propagate the stable `Unavailable` result. Its write outcome is `not_applied` only when a pre-write failure or confirmed rollback establishes that result; an unconfirmed commit or rollback yields `unknown`. Clients must inspect state before retrying an unknown write outcome. The concrete store may report capacity exhaustion as unavailable, while the expected-version domain remains every positive integer. A version mismatch and an absent item remain conflict and missing outcomes, respectively.
