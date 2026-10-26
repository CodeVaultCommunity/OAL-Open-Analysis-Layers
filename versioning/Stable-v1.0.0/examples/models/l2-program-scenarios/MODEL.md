# OAL-EX-M2-PROGRAM-SCENARIOS — Program and Scenario Records (L2)

[Português](MODEL.pt-br.md) · [Models](../README.md) · [Reference rules](../../../README.md#reference-rules)

**Identity:** `OAL-EX-M2-PROGRAM-SCENARIOS`
**Version:** 0.1.0
**Layer:** L2 (ADMV: ADPM + ADVS)
**OAL edition declared:** Stable-v1.0.0
**Status:** example of a reusable model. This document specifies the model; it does not certify any project artifact.

## 1. Objective and scope

The model defines the L2 artifact as a pair $a_2 = (p, v)$, where $p$ is the ADPM component (program model) and $v$ is the ADVS component (verification specification). Both are required. The model covers the obligations of the L2 rules and the correspondence between UCS cases, program cases, behavioral tests, and acceptance criteria.

The model does not choose a programming language, an architecture, a test framework, or a file layout. It fixes the logical records that an L2 artifact must contain and the conditions that make it valid.

## 2. Constructions and relations

**ADPM ($p$)**

| Construction | Meaning |
| --- | --- |
| `ProgramCase` | One program case: linked UCS case, collaborators, sequence/decisions, results, effects, errors, permission input. |
| `ProgramEntity` | Entity record: linked UCS entity and the canonical location of its validity conditions. |
| `ToolContract` | Operation, inputs, outputs, guarantees, failures, ready-entity assumptions, and contextual conditions. |
| `Dependency` / `Composition` | What each case and tool receives, where implementations are selected, how collaborators are wired. |
| `Authorization` | The explicitly resolved actor context, authentication required by its contract, and the deny-by-default decision of each case. |
| `Lifetime` | Component lifetime when relevant. |

**ADVS ($v$)**

| Construction | Meaning |
| --- | --- |
| `BehavioralTest` | Exactly one per UCS case: linked case, covered criteria, boundary, planned scenarios, supporting checks, status. |
| `Scenario` | Preparation, actor context, action, observed boundary, configuration, expected result and effects, criteria verified, applicability. |
| `SupportingCheck` | An executable or reviewable check that supports a behavioral test; not another directly linked behavioral test. |
| `EvidenceRecord` | Observed execution evidence, separate from the plan. |

Relations: $p$ has a bijection $f\colon U \to P$ between UCS cases and program cases and $v$ has a bijection $g\colon U \to B$ between UCS cases and behavioral tests. Each criterion of a UCS case must be verified by at least one scenario or supporting check of that case's behavioral test. Sharing a supporting check between behavioral tests is allowed when the link is explicit. A shared integration criterion declared by M1 is covered by a shared supporting scenario or check with explicit links to all pertinent behavioral tests; it does not acquire a direct UCS-case link of its own.

The program record declares how the caller supplies actor context and where each case authorizes it. A case-to-case call passes the relevant context; each called case applies its policy. Authentication is required according to the selected case contract. Missing context is distinct from an explicitly admitted anonymous role.

## 3. Fields

The machine-readable template is [`template.json`](template.json).

| Object | Field | Kind | Notes |
| --- | --- | --- | --- |
| Root | `model`, `model_version`, `layer`, `oal_edition`, `project`, `source_l1` | R | `source_l1` names the M1 instance and version. |
| Root | `adpm`, `advs` | R | Both components are mandatory and non-empty. |
| ProgramCase | `id`, `ucs_case_id`, `collaborators`, `sequence`, `results`, `effects`, `errors`, `permission` | R | `sequence` records decisions and order. |
| ProgramCase | `domains`, `lifetime` | O | Required when the model uses domains or lifetime choices. |
| ProgramEntity | `id`, `ucs_entity_id`, `validity_location` | R | The location is canonical for that entity. |
| ToolContract | `id`, `operation`, `inputs`, `outputs`, `guarantees`, `failures`, `ready_entity_assumption`, `contextual_conditions` | R | `contextual_conditions` are $Q_t(e,c)$ checks distinct from entity coherence. |
| ToolContract.contextual_condition | `condition`, `object`, `purpose`, `responsibility` | R | The four fields make the condition identifiable. |
| BehavioralTest | `id`, `ucs_case_id`, `criteria`, `boundary`, `scenarios`, `supporting_checks`, `status` | R | Exactly one BT per UCS case. |
| Scenario | `id`, `preparation`, `actor`, `action`, `observed_boundary`, `configuration`, `expected_result`, `expected_effects`, `criteria_verified`, `applicability` | R | `applicability` is `applicable` or `not_applicable` with justification. |
| Shared supporting check | `id`, `criteria_verified`, `case_ids`, `obligation_ids`, `behavioral_test_ids`, `reference`, `scenario` | C | Required when a shared integration criterion is covered; links resolve to its cases and their BTs. |
| Evidence | `planned_checks`, `execution` | R | `execution.status` is `not_recorded`, `recorded`, or `not_applicable`. |
| Channel additions | `l4_obligations` | O | When present, the ADVS must reference the related channel scenarios. |

## 4. Validity conditions

- **V-M2-01 — Identity.** Model identity `OAL-EX-M2-PROGRAM-SCENARIOS`, version `0.1.0`, layer `L2`, and the declared OAL edition are present.
- **V-M2-02 — Both components.** `adpm` and `advs` are present, non-empty, and structurally complete.
- **V-M2-03 — Program bijection.** Every UCS case in the declared scope has exactly one `ProgramCase` with `ucs_case_id` equal to it; there are no extra program cases.
- **V-M2-04 — Behavioral-test bijection.** Every UCS case has exactly one `BehavioralTest` with `ucs_case_id` equal to it; behavioral-test identities are unique; there are no extra directly linked behavioral tests.
- **V-M2-05 — Criterion coverage reference.** Every criterion owned by a UCS case appears in `criteria_verified` of at least one scenario or supporting check of that case's behavioral test. A criterion referenced by a scenario must resolve either to the linked case or to a separately declared shared integration criterion in the selected L1 artifact. For the latter, the scenario identifies the participating cases, obligations, and all pertinent behavioral tests; the shared criterion and its full verification contract remain recoverable. No additional directly linked behavioral test is created.
- **V-M2-06 — Supporting checks.** Each supporting-check reference resolves to a file and, when a symbol is given, to that symbol. Sharing checks is allowed with explicit links.
- **V-M2-07 — Applicability.** A scenario marked `not_applicable` states a justification. For the permission scenario of a case $u$, let $A$ be the known actors and $A_u$ the permitted actors; the scenario is required when $F_u = A \setminus A_u$ is non-empty, and may be `not_applicable` with justification only when $F_u$ is empty. Absent and unknown actor contexts remain distinct situations and are not covered by this exemption.
- **V-M2-08 — Tools and coherence.** Every tool contract states that a ready entity satisfies the entity's internal coherence conditions, and its contextual conditions are distinct from those conditions. It must not contain a redundant copy of an entity-internal check.
- **V-M2-09 — Plan, code, execution.** Planned scenarios and supporting-check references are distinct from execution records. A test file reference does not count as an executed result; `execution.status` is truthful.
- **V-M2-10 — Channel additions.** If `l4_obligations` is present, the related channel scenarios are referenced and their status is recorded.

## 5. Mapping to the OAL L2 rules (Stable-v1.0.0)

| OAL rule | Model construction or condition |
| --- | --- |
| ADPM 1. Responsibilities | `ProgramCase`, `ProgramEntity`, `ToolContract`, `Dependency`, `Composition`. |
| ADPM 2. Use cases | `ProgramCase.sequence`, decisions, results, effects, errors; V-M2-03. |
| ADPM 3. Entities | `ProgramEntity`; V-M2-08; entity validity remains canonical. |
| ADPM 4. Tools and validation | `ToolContract.ready_entity_assumption`, `contextual_conditions` with object, purpose, and responsibility; V-M2-08. |
| ADPM 5. Dependencies/composition | `Dependency`, `Composition`. |
| ADPM 6. Persistence | Tool contract guarantees and failures. |
| ADPM 7. Authorization | `ProgramCase.permission` and `Authorization`. |
| ADPM 8. Faithful representation | The logical records and this mapping. |
| ADPM 9. Domains | Optional `domains` field. |
| ADPM 10. Lifetime | Optional `lifetime` field. |
| ADVS 1. UCS derivation and BT | `BehavioralTest`, V-M2-04. |
| ADVS 2. Test/subtest contracts | `Scenario` fields. |
| ADVS 3. Permissions | Permission scenarios; V-M2-07. |
| ADVS 4. Failures and limits | Scenario failures and channel scenarios. |
| ADVS 5. Trace and status | `criteria_verified`, `supporting_checks`, `EvidenceRecord`; V-M2-05, V-M2-09. |

## 6. Template, example, and counterexample

- [`template.json`](template.json) is the logical template.
- [`example.json`](example.json) is a **partial slice** of Tiny Catalog for two cases. It is labeled as partial and does not replace the project's complete L2 artifact.
- [`counterexample.json`](counterexample.json) omits the ADVS for one case, duplicates a behavioral-test identity, marks a required permission scenario `not_applicable`, gives a tool contract a redundant entity check, and references an undeclared shared criterion. The expected violations are listed in the file.

## 7. Evidence and limits

The model was reviewed against the ADPM and ADVS rules above. The review is documented here; it is not machine-certified. The model is deliberately partial: it does not define a programming language, a state-machine notation, a test runner, or an algorithm to derive scenarios. It also does not prove that the scenarios are behaviorally sufficient; that remains a review obligation.

The bijections and criterion references are structural. A structural check can verify that identifiers resolve and that every criterion appears in the declared support; it cannot verify that a scenario actually exercises the condition.

## 8. Instantiating and verifying

1. Start from the project's L1 instance and list every UCS case, actor set, and criterion.
2. For each case, produce one `ProgramCase` and one `BehavioralTest`; do not add directly linked tests for functions or subtests.
3. Record tool contracts with ready-entity assumptions and contextual conditions.
4. Record scenarios with applicability; compute $F_u = A \setminus A_u$ and only mark the permission scenario `not_applicable` when $F_u$ is empty.
5. Record planned checks and execution separately.
6. Add the L2 entry to `model-instances.json` and run the selected test commands.

## Stable compatibility assessment

Origin: Alpha-v0.2.0-Alkimim, model version 0.1.0. For Stable-v1.0.0, the numbered OAL rules and this model's fields and validity conditions were compared with that baseline; they are unchanged. The mapping above therefore carries forward for the same educational scope. This is a compatibility review, not external certification or a transformer execution. The [assessment report](../../../COMPATIBILITY.md) records scope and limits; project executions are recorded separately.
