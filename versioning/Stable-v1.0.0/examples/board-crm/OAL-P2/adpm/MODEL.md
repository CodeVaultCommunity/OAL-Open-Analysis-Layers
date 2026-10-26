# Board CRM — ADPM program model

[Português](MODEL.pt-br.md) · [Home](../../../../../../README.md)

**Source:** [project UCS](../../OAL-P1/ucs.json), baseline 0.2.0.
**Classification:** project artifact of the L2 program-model component (ADPM) under OAL Stable-v1.0.0; instantiating OAL-EX-M2-PROGRAM-SCENARIOS 0.1.0; see `model-instances.json` for the instance declaration.
**Derivation record:** [derivations.json](../../derivations.json).

## Cases and authorization

The model retains the case identities UC-CRM-001, UC-CRM-002, UC-CRM-003, UC-CRM-004, UC-CRM-005, UC-CRM-006. Each case receives a resolved actor context explicitly. The specified actor is a role; the context is represented here by a role identifier established by a trusted entry point. This example requires authentication for every case. Every case checks its permission before validation, reads, or writes. Missing and unknown actors are denied. The permission matrix is in the [UCS](../../OAL-P1/ucs.json); its concrete realization is in [ADI](../../OAL-P3/IMPLEMENTATION.md).

## Entities, tools, and composition

Entities contain data and assignment validation. Cases own domain decisions and call tool contracts. [Tool contracts](tool-contracts.md) specify persistence operations and guarantees. Composition selects concrete tools and gives each case its dependencies. The identity provider belongs at the entry boundary; it supplies the actor but does not decide case permissions.

## Algorithms

The identity input is distinct from the event author written to history. The entry boundary authenticates an identity; the case checks the permission matrix. The event author remains an explicit case input. Authorization precedes even a storage read.

| UCS case | Permitted roles | Dependencies | Program algorithm |
| --- | --- | --- | --- |
| UC-CRM-001 Create | operator, manager | Store, IdentifierProvider, Clock | Validate title (80), company (80), and owner (40); obtain ID and time; create a NEW opportunity at version 1; atomically store it with its creation event. |
| UC-CRM-002 Move | operator, manager | Store, Clock | Load the card; compare its version; accept only an adjacent move among NEW, QUALIFIED, and PROPOSAL; atomically update stage, version, time, and event. |
| UC-CRM-003 Note | operator, manager | Store, IdentifierProvider, Clock | Validate note text (500); load and compare version; create note ID; atomically add the note and increment the version. |
| UC-CRM-004 View | viewer, operator, manager | Store | Read detached cards, notes, and events; sort by update time descending then ID; filter by exact owner when provided; return all five stage columns. |
| UC-CRM-005 Won | manager | Store, IdentifierProvider, Clock | Validate reason (200); load and compare version; require PROPOSAL; atomically set WON, record the reason, increment version, and append a stage event. |
| UC-CRM-006 Lost | manager | Store, IdentifierProvider, Clock | Validate reason (200); load and compare version; require an active stage; atomically set LOST, record the reason, increment version, and append a stage event. |

Entity constructors check local field validity. They do not decide stage transitions or actor permissions. `Store` provides atomic create/mutate, independent reads, missing-record, conflict, and unavailable outcomes. The case maps these outcomes to UCS results. The [implementation map](traceability.json) preserves one implementation identity for each UCS case.
