# Tiny Catalog — ADPM program model

[Português](MODEL.pt-br.md) · [Home](../../../../../../README.md)

**Source:** [project UCS](../../OAL-P1/UCS.md), baseline 0.2.0.
**Derivation record:** [derivations.json](../../derivations.json).
**Classification:** project artifact of the L2 program-model component (ADPM) under OAL Alpha-v0.2.0-Alkimim. It is a model of this catalog project, not a specified reusable L2 model; instantiating OAL-EX-M2-PROGRAM-SCENARIOS 0.1.0; see `model-instances.json` for the instance declaration.

## Cases and authorization

The model retains the case identities UC-CAT-001, UC-CAT-002, UC-CAT-003, UC-CAT-004. A resolved actor context enters each case as an explicit input; this project requires an authenticated caller. The chosen context is a role supplied by a trusted invocation, and the case checks that role's permission. Every case checks its permission before validation, reads, or writes. Missing and unknown actors are denied. The permission matrix is in the [UCS](../../OAL-P1/UCS.md); its concrete realization is in [ADI](../../OAL-P3/IMPLEMENTATION.md).

## Entities, tools, and composition

Entities contain data and assignment validation. Cases own domain decisions and call tool contracts. [Tool contracts](tool-contracts.md) specify persistence operations and guarantees. Composition selects concrete tools and gives each case its dependencies. The identity provider belongs at the entry boundary; it supplies the actor but does not decide case permissions.

## Algorithms

The identity provider authenticates the principal at the entry boundary. The same principal is passed explicitly to every case. A case checks permission before input validation or a storage read. Deactivation calls the already specified lookup case using that principal.

| UCS case | Permitted roles | Dependencies | Program algorithm |
| --- | --- | --- | --- |
| UC-CAT-001 Register | maintainer | Item factory, ItemStore | Construct a valid active item; insert it under an atomically unique code; map a store conflict to duplicate item. |
| UC-CAT-002 Get | maintainer, reader | Key factory, ItemStore | Validate the code; read the retained record even if inactive; distinguish missing record from unavailable storage. |
| UC-CAT-003 List | maintainer, reader | ItemStore | Read independent records; keep active items; sort by exact ASCII code; return an empty list when none qualify. |
| UC-CAT-004 Deactivate | maintainer | UC-CAT-002 lookup, ItemStore | Obtain the item through lookup; return it unchanged when already inactive; otherwise set inactive and replace the retained record; map a concurrent disappearance to missing item. |

`ItemKey` and `Item` validate assigned fields; cases own uniqueness, availability, and retention decisions. `ItemStore` provides atomic insert, detached reads, and replacement without deciding those rules. `RecordCodec` and `ConnectionProvider` support the SQLite adapter. The [implementation map](traceability.json) preserves one implementation identity for each UCS case.
