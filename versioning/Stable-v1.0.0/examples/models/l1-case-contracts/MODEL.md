# OAL-EX-M1-CASE-CONTRACTS — Simple Case Contracts (L1)

[Português](MODEL.pt-br.md) · [Models](../README.md) · [Reference rules](../../../README.md#reference-rules)

**Identity:** `OAL-EX-M1-CASE-CONTRACTS`
**Version:** 0.1.0
**Layer:** L1 (UCS)
**OAL edition declared:** Stable-v1.0.0
**Status:** example of a reusable model. This document specifies the model; it does not certify any project artifact.

## 1. Objective and scope

The model defines a case specification that a project can reuse. It fixes the logical fields, their meanings, and the conditions that make an artifact a valid instance. It is intentionally simpler than a general requirements language: it covers the subjects required by the L1 rules and nothing beyond them.

The model covers one project scope with a closed set of actors, entities, rules, use cases, complementary obligations, and acceptance criteria. It does not prescribe a file layout, a programming language, a serialization format, a user interface, or a domain decomposition. It does not define an external needs model: needs enter as declared sources with their provenance.

## 2. Constructions and relations

| Construction | Meaning |
| --- | --- |
| `ProjectSpecification` | Root object: identity, version, edition, scope, sources, status, canonical content. |
| `Actor` | An interaction role declared in the specification, played by a person or system requesting a case. The concrete caller and the runtime actor context are distinct from the role; the derivation owner is a separate responsibility. |
| `Entity` | Data meaning, fields, relations, invariants, and the canonical location of validity conditions. |
| `Rule` | A shared domain condition, with the cases that apply it. |
| `CaseContract` | One use case: identity, objective, actors, trigger, inputs, context, preconditions, results, effects, alternatives, failures, referenced constructions, obligations, criteria. |
| `Obligation` | A complementary requirement with nature, statement, origin, scope, verifiable conditions, and responsibility. |
| `Criterion` | An acceptance criterion owned by exactly one case. |
| `SharedCriterion` | A separately declared integration criterion spanning named cases and complementary obligations, with one canonical definition. |
| `TraceLink` | A resolved reference from a case or criterion to needs, entities, rules, obligations, capabilities, or other cases. |

Relations: `specification` owns `actors`, `entities`, `rules`, `obligations`, and `cases`; each `case` references actors, entities, rules, obligations, capabilities, dependencies, and owns its `criteria`; each case-owned `criterion` belongs to one case; optional `shared_criteria` belong to the specification and reference their participating cases and obligations; each `rule` names the cases that apply it; each `obligation` names its scope and origin. A shared criterion does not create a new use case or an additional directly linked behavioral test.

Case context and preconditions state how actor context is established, whether authentication is required, and the authorization conditions. Missing or unresolved context is denied. Anonymous access is valid only for an explicitly declared and permitted anonymous role; it is never inferred from a missing context. System callers follow the same rules. A case calling another case passes the relevant context, and the called case applies its own policy. Delegation must be declared.

## 3. Fields

The machine-readable template is [`template.json`](template.json). Required (R), optional (O), and conditional (C) fields:

| Object | Field | Kind | Notes |
| --- | --- | --- | --- |
| ProjectSpecification | `identity`, `version`, `oal_edition`, `scope`, `status` | R | Status distinguishes baseline, draft, and reviewed. |
| ProjectSpecification | `sources` | R | Each source has `id`, `description`, `provenance`; reconstructed needs are marked `reconstructed`. |
| ProjectSpecification | `canonical_content` | R | Names the canonical representation for each field group. |
| ProjectSpecification | `facts` | C | Required when observed facts, requirements, inferences, assumptions, or open items appear. Each entry has `kind`. |
| Actor | `id`, `name`, `description` | R | Roles are runtime actors. |
| Entity | `id`, `meaning`, `fields`, `relations`, `invariants`, `validity_owner`, `validity_location` | R | `validity_owner` is the entity or the consuming case; never a tool. |
| Rule | `id`, `statement`, `applied_by` | R | `applied_by` lists case IDs. |
| CaseContract | `id`, `title`, `objective`, `initiating_actor`, `permitted_actors` | R | The initiating actor must be permitted. |
| CaseContract | `trigger`, `inputs`, `context`, `preconditions`, `results`, `effects`, `alternatives`, `failures` | R | Results include the observable denial of access. |
| CaseContract | `entities`, `rules`, `capabilities`, `dependencies`, `obligations` | O | References must resolve. |
| CaseContract | `criteria` | R | At least one criterion. |
| Obligation | `id`, `nature`, `statement`, `origin`, `scope`, `verifiable_conditions`, `responsibility` | R | `origin` is `external`, `domain`, `assumption`, or `l4-decision`; an external origin cites the source. |
| Criterion | `id`, `statement` | R | Globally unique; belongs to the containing case or its explicit `case_id`. |
| SharedCriterion | `id`, `statement`, `case_ids`, `obligation_ids`, `verifiable_conditions` | C | Required for each declared integration criterion. Case and obligation sets are non-empty and resolve. |

An artifact declares its representations; structured JSON, Markdown narrative, and TeX are examples, not a closed list. It may combine them when all required content remains recoverable. The model requires one canonical source for each field group and an explicit mapping and consistency rule between representations. A review or an existing representation check detects divergence; formatting changes do not create a new model.

## 4. Validity conditions

An artifact is a valid instance of `OAL-EX-M1-CASE-CONTRACTS` 0.1.0 when all conditions hold:

- **V-M1-01 — Identity.** `identity`, `version`, and `oal_edition` are present. The model version declared by the instance is exactly `0.1.0`.
- **V-M1-02 — Unique identifiers.** Actor, entity, rule, obligation, case, and criterion identifiers are unique within the artifact.
- **V-M1-03 — Resolved references.** Every actor, entity, rule, obligation, capability, dependency, and case reference resolves to a declared object.
- **V-M1-04 — Actor sets and context.** Each case has an initiating actor and a permitted actor set; the initiating actor belongs to the permitted set; every permitted actor exists. Its contract declares the required actor context, authentication when required, and authorization conditions. Missing, unresolved, unknown, or disallowed contexts are denied. Any anonymous or system role is explicit; an internal call does not grant additional permission.
- **V-M1-05 — Criteria.** Each case has at least one case-owned criterion; each such criterion belongs to exactly one case and is referenced by that case. A shared integration criterion is declared separately with a unique identifier, full statement, participating case IDs, obligation IDs, and verifiable conditions. It has one canonical definition and does not replace the criteria of its participating cases.
- **V-M1-06 — Shared rules.** Every rule names the cases that apply it; a shared rule has one canonical definition.
- **V-M1-07 — Obligations.** Every obligation has nature, statement, origin, scope, verifiable conditions, and responsibility. An external origin cites a source; a decision introduced by the solution is marked `l4-decision` and is not presented as an external requirement.
- **V-M1-08 — Facts.** Observed facts, desired requirements, inferences, assumptions, and open items are distinguishable. Reconstructed needs are marked `reconstructed`.
- **V-M1-09 — Entity validity.** Every entity states its meaning, fields, relations, invariants, and the canonical location of validity conditions. Validity is assigned to the entity or to the consuming case, never to a tool.
- **V-M1-10 — No smuggled channel decisions.** A case does not state a route, payload encoding, screen, protocol, or representation as a domain requirement. When such a reference appears, its origin is declared.
- **V-M1-11 — Canonical content.** The artifact names its canonical content and, when several representations exist, the mapping and consistency rule between them.

The model does not require a specific naming convention, folder layout, file count, or serialization schema beyond the declared canonical content.

## 5. Mapping to the OAL L1 rules (Stable-v1.0.0)

| OAL L1 rule | Model construction or condition |
| --- | --- |
| 1. Scope | `ProjectSpecification.scope`, sources, and `facts`. |
| 2. Use cases | `CaseContract` identity, objective, initiating actor, permitted set; V-M1-04. |
| 3. Behavioral contracts | Case trigger, inputs, context, preconditions, results, effects, alternatives, failures; denial; V-M1-10. |
| 4. Entities and rules | `Entity`, `Rule`, V-M1-06, V-M1-09. |
| 5. Composition and dependencies | Case `capabilities`, `dependencies`, and `TraceLink`. |
| 6. Complementary obligations | `Obligation` with nature, origin, scope, verifiable conditions; V-M1-07. |
| 7. Acceptance and links | `Criterion`, case criteria, `SharedCriterion` with declared scope, and trace links; V-M1-05. |
| 8. Consistency and evolution | Unique identifiers, resolved references, canonical content, `facts`; V-M1-02, V-M1-08, V-M1-11. |
| 9. Domains (recommendation) | Not required; a domain field may be added without changing the model identity. |
| 10. Representative examples | The model example is explicitly partial; it does not replace the case contracts. |

## 6. Template, example, and counterexample

- [`template.json`](template.json) is the logical template with required and optional fields.
- [`example.json`](example.json) is a **partial slice** of Tiny Catalog, labeled as such. It illustrates the constructions and does not replace the complete UCS.
- [`counterexample.json`](counterexample.json) is an invalid instance. It contains a case whose permitted actor is undeclared, an obligation without origin, a rule applied by an undeclared case, and a case without criteria; the entity also assigns its validity to a tool, and a shared integration criterion has unresolved scope and no verifiable conditions. The expected violations are listed in the file; a validator or review must reject it.

## 7. Evidence and limits

The model was reviewed against the L1 rules above. The review is documented in this file; it is not machine-certified. The model is deliberately partial: it does not define a needs model, a domain taxonomy, a formal temporal logic, or an algorithm for generating cases. Its examples are illustrative slices, not complete project specifications.

The model's validity conditions are structural. Passing them means the declared fields and references are coherent; it does not prove that the case contracts describe the real system or that the criteria are sufficient. That judgment remains a review of the artifact against its sources, as required by the OAL conformance rules.

## 8. Instantiating and verifying

1. Copy the template and fill the project scope, sources, actors, entities, rules, cases, obligations, and criteria.
2. Assign one canonical content source per field group.
3. Check V-M1-01 through V-M1-11. A project may add constraints, but it cannot remove these.
4. Record the artifact version and the model version in `model-instances.json` (L1 entry).
5. A structural review checks identities, references, files, and declared mappings. The semantic review checks that the contracts and criteria are appropriate to the project.

## Stable compatibility assessment

Origin: Alpha-v0.2.0-Alkimim, model version 0.1.0. For Stable-v1.0.0, the numbered OAL rules and this model's fields and validity conditions were compared with that baseline; they are unchanged. The mapping above therefore carries forward for the same educational scope. This is a compatibility review by Codex, not external certification or a transformer execution. The [assessment report](../../../COMPATIBILITY.md) records scope and limits; project executions are recorded separately.
