# Tiny Catalog — ADVS verification specification

[Português](SCENARIOS.pt-br.md) · [Home](../../../../../../README.md)

**Source:** [project UCS](../../OAL-P1/UCS.md), baseline 0.2.0.
**Classification:** project artifact of the L2 verification component (ADVS) under OAL Alpha-v0.2.0-Alkimim; instantiating OAL-EX-M2-PROGRAM-SCENARIOS 0.1.0; see `model-instances.json` for the instance declaration.
**Derivation record:** [derivations.json](../../derivations.json). These are planned scenarios; executable case checks are in [`tests/p3`](../../tests/p3), and channel checks are in [`tests/p4`](../../tests/p4). The presence of a test file does not demonstrate that it was executed.

## One behavioral test per case

The [behavioral-test map](behavioral-tests.json) defines BT-CAT-001 through BT-CAT-004, each directly linked to exactly one UCS case. Each BT is a logical test made up of the listed executable supporting checks. It passes for a reported run only when all of those checks pass in that run. Criterion scenarios below support the BT of their case; shared permission and retention checks can support more than one BT without becoming additional directly linked behavioral tests.

**Shared integration criterion:** `AC-SHARED-01` is defined in `OAL-P1/index.json` and spans UC-CAT-001..004 and obligations P-01/P-02. `SC-CAT-RETENTION`, declared in [behavioral-tests.json](behavioral-tests.json), supplies the full scenario and executable reference and explicitly supports BT-CAT-001..004. It is a shared supporting check, not a fifth behavioral test.

## Scenario families

| ID | Cases | Actor and action | Expected result |
| --- | --- | --- | --- |
| VS-01 | UC-CAT-001, UC-CAT-002, UC-CAT-003, UC-CAT-004 | Permitted actor executes a valid request | Specified result and effects |
| VS-02 | UC-CAT-001, UC-CAT-002, UC-CAT-003, UC-CAT-004 | Missing identity executes a request | Authentication failure; no domain or persistence effect |
| VS-03 | UC-CAT-001, UC-CAT-004 | Known but unpermitted actor executes a request | Access denied; no domain or persistence effect. Not applicable to UC-CAT-002 and UC-CAT-003: $F_u = A \setminus A_u$ is empty because both known roles are permitted. |
| VS-04 | UC-CAT-001, UC-CAT-002, UC-CAT-003, UC-CAT-004 | Permitted actor sends invalid input | Specified validation failure; no unintended effect |
| VS-05 | UC-CAT-001, UC-CAT-002, UC-CAT-003, UC-CAT-004 | Persistence or version boundary fails | Specified failure; no false success |

Each acceptance criterion retains its UCS ID in the executable case-oriented checks. Unit checks cover eligible entities and pure tools; integration checks cover concrete tools. The permission scenarios also call cases directly, so hiding a browser control cannot satisfy them.

## Case scenario setup

| Case | Permitted actor and action | Starting state and boundary |
| --- | --- | --- |
| UC-CAT-001 | Maintainer registers an item. | Use an empty or preallocated code as the criterion requires; run against the injected in-memory or SQLite store. |
| UC-CAT-002 | Maintainer or reader gets an item. | Prepare an active, inactive, or missing code as required; read through the case, not directly through storage. |
| UC-CAT-003 | Maintainer or reader lists items. | Prepare an empty, active, inactive, or mixed catalog as required; observe the complete returned collection. |
| UC-CAT-004 | Maintainer deactivates an item. | Prepare an active, inactive, or missing item; compare both subsequent lookup and available listing. |

For every case, run the denial criterion with absent and unknown identities. Run a known unpermitted role only when $F_u = A \setminus A_u$ is non-empty; when $F_u$ is empty, record the scenario as not applicable with that justification. Absent and unknown identities remain separate situations. Inject unavailable storage for failure criteria. Concurrent registration uses two requests against one SQLite file. The criterion map below provides the specific expected result and effect for each setup.

<!-- BEGIN UCS CRITERION SCENARIOS -->
## Scenario to criterion map

Each case-owned criterion row is a planned supporting scenario for its case's BT. The AC-SHARED-01 row is the shared integration scenario linked to all four BTs as declared above. Set up the case state described by the UCS, execute it with the case's permitted actor unless the criterion tests denial, and compare the result and effects with the stated expectation. A passing run is recorded separately in ADI evidence.

| Scenario | UCS criterion | Expected observation |
| --- | --- | --- |
| VS-AC-CAT-001-01 | AC-CAT-001-01 | valid registration returns the supplied code/name with active=true; a later lookup returns that record. |
| VS-AC-CAT-001-02 | AC-CAT-001-02 | invalid input is rejected and creates no record. |
| VS-AC-CAT-001-03 | AC-CAT-001-03 | a previously allocated code is rejected even if the existing item is inactive; its data remain unchanged. |
| VS-AC-CAT-001-04 | AC-CAT-001-04 | two concurrent valid registrations for one unused code yield exactly one success and one duplicate rejection when persistence is available. |
| VS-AC-CAT-001-05 | AC-CAT-001-05 | persistence unavailability is distinguishable from confirmed registration. |
| VS-AC-CAT-001-06 | AC-CAT-001-06 | An absent or unpermitted actor is denied before any domain or persistence effect. |
| VS-AC-CAT-002-01 | AC-CAT-002-01 | active and inactive retained items are both retrievable with their data. |
| VS-AC-CAT-002-02 | AC-CAT-002-02 | a valid absent code produces the missing-item outcome. |
| VS-AC-CAT-002-03 | AC-CAT-002-03 | an invalid code is rejected as invalid data. |
| VS-AC-CAT-002-04 | AC-CAT-002-04 | an unavailable lookup is not reported as a missing item. |
| VS-AC-CAT-002-05 | AC-CAT-002-05 | changing returned data does not change the persisted record. |
| VS-AC-CAT-002-06 | AC-CAT-002-06 | An absent or unpermitted actor is denied before any domain or persistence effect. |
| VS-AC-CAT-003-01 | AC-CAT-003-01 | the result contains exactly the active items in the required order. |
| VS-AC-CAT-003-02 | AC-CAT-003-02 | an empty catalog or one with only inactive items yields an empty collection. |
| VS-AC-CAT-003-03 | AC-CAT-003-03 | persistence failure does not become a successful empty collection. |
| VS-AC-CAT-003-04 | AC-CAT-003-04 | An absent or unpermitted actor is denied before any domain or persistence effect. |
| VS-AC-CAT-004-01 | AC-CAT-004-01 | the item becomes inactive, leaves the available listing, and stays retrievable. |
| VS-AC-CAT-004-02 | AC-CAT-004-02 | repeating the request succeeds with the same retained data. |
| VS-AC-CAT-004-03 | AC-CAT-004-03 | a missing record is rejected and not implicitly created. |
| VS-AC-CAT-004-04 | AC-CAT-004-04 | invalid code is rejected as invalid data. |
| VS-AC-CAT-004-05 | AC-CAT-004-05 | unavailable lookup or persistence cannot produce a false confirmation. |
| VS-AC-CAT-004-06 | AC-CAT-004-06 | An absent or unpermitted actor is denied before any domain or persistence effect. |
| VS-AC-SHARED-01 | AC-SHARED-01 | register an item, deactivate it, end that application instance, and reconstruct the application with the same retained storage. Lookup still finds the inactive record, and the available listing excludes it. This evaluates normal reconstruction, not a crash or power failure. |
<!-- END UCS CRITERION SCENARIOS -->
