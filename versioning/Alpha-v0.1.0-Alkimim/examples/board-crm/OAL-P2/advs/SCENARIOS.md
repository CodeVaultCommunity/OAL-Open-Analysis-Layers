# Board CRM — ADVS verification specification

[Português](SCENARIOS.pt-br.md) · [Home](../../../../../../README.md)

**Source:** [project UCS](../../OAL-P1/ucs.json), baseline 0.1.0.
**Derivation record:** [derivations.json](../../derivations.json). These are planned scenarios; executable case checks are in [`tests/p3`](../../tests/p3), and channel checks are in [`tests/p4`](../../tests/p4).

## One behavioral test per case

The [behavioral-test map](behavioral-tests.json) defines BT-CRM-001 through BT-CRM-006, each directly linked to exactly one UCS case. Each BT is a logical test made up of the listed executable supporting checks. It passes for a reported run only when all of those checks pass in that run. Criterion scenarios below support the BT of their case; the shared permission check supports all six without becoming another directly linked behavioral test.

## Scenario families

| ID | Cases | Actor and action | Expected result |
| --- | --- | --- | --- |
| VS-01 | UC-CRM-001, UC-CRM-002, UC-CRM-003, UC-CRM-004, UC-CRM-005, UC-CRM-006 | Permitted actor executes a valid request | Specified result and effects |
| VS-02 | UC-CRM-001, UC-CRM-002, UC-CRM-003, UC-CRM-004, UC-CRM-005, UC-CRM-006 | Missing identity executes a request | Authentication failure; no domain or persistence effect |
| VS-03 | UC-CRM-001, UC-CRM-002, UC-CRM-003, UC-CRM-004, UC-CRM-005, UC-CRM-006 | Known but unpermitted actor executes a request | Access denied; no domain or persistence effect |
| VS-04 | UC-CRM-001, UC-CRM-002, UC-CRM-003, UC-CRM-004, UC-CRM-005, UC-CRM-006 | Permitted actor sends invalid input | Specified validation failure; no unintended effect |
| VS-05 | UC-CRM-001, UC-CRM-002, UC-CRM-003, UC-CRM-004, UC-CRM-005, UC-CRM-006 | Persistence or version boundary fails | Specified failure; no false success |

Each acceptance criterion retains its UCS ID in the executable case-oriented checks. Unit checks cover eligible entities and pure tools; integration checks cover concrete tools. The permission scenarios also call cases directly, so hiding a browser control cannot satisfy them.

## Case scenario setup

| Case | Permitted actor and action | Starting state and boundary |
| --- | --- | --- |
| UC-CRM-001 | Operator or manager creates a card. | Start with an empty board; use valid, blank, or oversized fields; inspect the stored card and initial event. |
| UC-CRM-002 | Operator or manager moves a card. | Prepare NEW, QUALIFIED, PROPOSAL, or closed stage and current or stale version; inspect stage, version, and history. |
| UC-CRM-003 | Operator or manager records a note. | Prepare active or closed card with a known version; use valid or invalid note text; inspect note and version. |
| UC-CRM-004 | Viewer, operator, or manager views the board. | Prepare cards across all stages and owners; inspect columns, exact owner filter, and deterministic order. |
| UC-CRM-005 | Manager closes a card as WON. | Prepare PROPOSAL, earlier, or closed stage; inspect reason note, event, version, and rejection effects. |
| UC-CRM-006 | Manager closes a card as LOST. | Prepare each active stage, a closed stage, or stale version; inspect reason note, event, version, and rejection effects. |

For every case, repeat the request with absent identity and a recognized but unpermitted actor. Check that denial precedes validation and storage. Use the SQLite tool for atomic effect checks and call the case directly as well as through the browser transport. The criterion map below gives the specific expected result for each setup.

<!-- BEGIN UCS CRITERION SCENARIOS -->
## Scenario to criterion map

Each row is a planned supporting scenario for its case's BT. Set up the case state described by the UCS, execute it with the case's permitted actor unless the criterion tests denial, and compare the result and effects with the stated expectation. A passing run is recorded separately in ADI evidence.

| Scenario | UCS criterion | Expected observation |
| --- | --- | --- |
| VS-AC-CRM-001-01 | AC-CRM-001-01 | Valid fields create a NEW card at version 1. |
| VS-AC-CRM-001-02 | AC-CRM-001-02 | Blank or oversized fields create no card. |
| VS-AC-CRM-001-03 | AC-CRM-001-03 | Creation produces exactly one initial stage event. |
| VS-AC-CRM-001-04 | AC-CRM-001-04 | A missing or unpermitted actor is denied before any domain or persistence effect. |
| VS-AC-CRM-002-01 | AC-CRM-002-01 | A NEW card moves to QUALIFIED with one version increment and event. |
| VS-AC-CRM-002-02 | AC-CRM-002-02 | A move from NEW directly to PROPOSAL is rejected. |
| VS-AC-CRM-002-03 | AC-CRM-002-03 | A stale version is rejected without changing stage or history. |
| VS-AC-CRM-002-04 | AC-CRM-002-04 | A closed card cannot be dragged to an active stage. |
| VS-AC-CRM-002-05 | AC-CRM-002-05 | A missing or unpermitted actor is denied before any domain or persistence effect. |
| VS-AC-CRM-003-01 | AC-CRM-003-01 | A valid note is retrievable and increments the card version once. |
| VS-AC-CRM-003-02 | AC-CRM-003-02 | Blank or oversized notes are rejected without version change. |
| VS-AC-CRM-003-03 | AC-CRM-003-03 | A closed card still accepts a note. |
| VS-AC-CRM-003-04 | AC-CRM-003-04 | A missing or unpermitted actor is denied before any domain or persistence effect. |
| VS-AC-CRM-004-01 | AC-CRM-004-01 | The board includes active and closed cards in their correct columns. |
| VS-AC-CRM-004-02 | AC-CRM-004-02 | Owner filtering is exact and leaves other records unchanged. |
| VS-AC-CRM-004-03 | AC-CRM-004-03 | Cards have deterministic order within every column. |
| VS-AC-CRM-004-04 | AC-CRM-004-04 | A missing or unpermitted actor is denied before any domain or persistence effect. |
| VS-AC-CRM-005-01 | AC-CRM-005-01 | A PROPOSAL card closes as WON with one note, event, and version increment. |
| VS-AC-CRM-005-02 | AC-CRM-005-02 | A NEW or QUALIFIED card cannot close as WON. |
| VS-AC-CRM-005-03 | AC-CRM-005-03 | A closed card cannot close again. |
| VS-AC-CRM-005-04 | AC-CRM-005-04 | A missing or unpermitted actor is denied before any domain or persistence effect. |
| VS-AC-CRM-006-01 | AC-CRM-006-01 | Each active stage may close as LOST with one note, event, and version increment. |
| VS-AC-CRM-006-02 | AC-CRM-006-02 | A closed card cannot close as LOST again. |
| VS-AC-CRM-006-03 | AC-CRM-006-03 | A stale version leaves the card, notes, and history unchanged. |
| VS-AC-CRM-006-04 | AC-CRM-006-04 | A missing or unpermitted actor is denied before any domain or persistence effect. |
<!-- END UCS CRITERION SCENARIOS -->
