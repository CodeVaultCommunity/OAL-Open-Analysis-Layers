# Work Board · L2/ADVS verification

[Português](SCENARIOS.pt-br.md) · [UCS](../../OAL-P1/UCS.md) · [Example](../../README.md)

**Source:** [project UCS](../../OAL-P1/ucs.json), baseline 0.2.1.
**Classification:** project artifact of the L2 verification component (ADVS) under OAL Stable-v1.0.0; instantiating OAL-EX-M2-PROGRAM-SCENARIOS 0.1.0; see `model-instances.json` for the instance declaration. These are planned scenarios; the presence of test files does not demonstrate that they were executed.

The [behavioral-test map](behavioral-tests.json) gives each UCS case one directly linked test identity. The executable functions in [`tests/p3`](../../tests/p3) are supporting checks, not additional directly linked behavioral-test identities. They cover all eighteen UCS acceptance criteria: valid outcomes, denied actors, invalid inputs, stale versions, workflow order, filters, absent items, and stable storage failures.

## Scenario families

| ID | Cases | Actor and action | Expected result |
| --- | --- | --- | --- |
| VS-01 | UC-WB-001..006 | Permitted actor executes a valid request | Specified result and effects |
| VS-02 | UC-WB-001..006 | Absent or unknown identity executes a request | Authentication or access refusal; no effect |
| VS-03 | UC-WB-001, UC-WB-002, UC-WB-003, UC-WB-004 | Known but unpermitted role executes a request | Access denied; no effect. Not applicable to UC-WB-005 and UC-WB-006: $F_u = A \setminus A_u$ is empty because all three known roles may read. |
| VS-04 | UC-WB-001..006 | Permitted actor sends invalid input | Specified validation failure; no unintended effect |
| VS-05 | UC-WB-002, UC-WB-003 | Stale version or skipped state | Conflict or invalid result; item unchanged |

For every case, run the absent and unknown identity scenarios. Run a known unpermitted role only when $F_u = A \setminus A_u$ is non-empty; when it is empty, record the scenario as not applicable with that justification. Absent and unknown identities remain separate situations.

[`tests/p4`](../../tests/p4) checks HTTP authentication, representation, route dispatch, and status mapping. Its checks support the chosen interface channel and do not replace the P3 checks. A passing suite reports only the configuration exercised in that run.

## Storage and representation scenarios

| Scenario | Contract / criteria | Setup and expected observation | Supporting check |
| --- | --- | --- | --- |
| VS-06 | R-WB-03; AC-WB-002-02; AC-WB-003-02 | Existing and absent items; expected versions `2**63` and larger. Existing item yields conflict, absent item yields missing, and state is unchanged. | `tests/p3/test_cases.py::test_large_expected_versions_preserve_contract_and_state` |
| VS-07 | O-WB-AVAIL; AC-WB-001-03 through AC-WB-006-03 | Temporarily unavailable storage schema; each case reports unavailable with `not_applied`, with no false result or mutation. | `tests/p3/test_cases.py::test_storage_failure_is_exposed_by_each_case_without_false_success` |
| VS-08 | O-WB-PERSIST; O-WB-AVAIL | Failure during an update statement rolls back; a commit-acknowledgement failure yields `unknown` both when the write occurred and when it did not. | `tests/integration/test_sqlite_store.py::test_statement_failure_rolls_back_the_update`; `tests/integration/test_sqlite_store.py::test_unconfirmed_commit_is_unknown_even_when_rollback_returns` |
| VS-09 | Concrete storage capacity | Saturated counter remains an integer and is unchanged; storage reports unavailable with `not_applied`. | `tests/integration/test_sqlite_store.py::test_exhausted_storage_counter_is_unavailable_without_numeric_promotion` |
| CS-01 | L4 error mapping | Large expected version maps to 409/404; storage failure maps to 503 and preserves `write_outcome`, including `unknown` after a lost commit acknowledgement. | `tests/p4/test_http.py::test_large_expected_version_returns_conflict_or_missing`; `test_storage_failure_returns_503_and_known_write_outcome`; `test_unconfirmed_commit_is_reported_as_unknown_over_http` |

The storage checks are supporting verification and introduce no additional directly linked behavioral-test identity. Observed suite results are preserved in the [execution record](../../../verification/execution.json) and its [test log](../../../verification/work-board-pytest.txt).
