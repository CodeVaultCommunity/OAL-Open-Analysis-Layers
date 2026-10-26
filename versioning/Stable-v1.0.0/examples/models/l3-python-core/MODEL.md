# OAL-EX-M3-PYTHON-CORE — Injected Python Core (L3)

[Português](MODEL.pt-br.md) · [Models](../README.md) · [Reference rules](../../../README.md#reference-rules)

**Identity:** `OAL-EX-M3-PYTHON-CORE`
**Version:** 0.1.0
**Layer:** L3 (ADI)
**OAL edition declared:** Stable-v1.0.0
**Status:** example of a reusable model. This document specifies the model; it does not certify any project artifact.

## 1. Objective and scope

The model defines a reusable Python code organization whose callable application core realizes the cases of an L2 artifact. It fixes the symbols, callable conventions, dependency injection, authorization point, tool contracts, composition, and verification links that an L3 artifact must expose. Python is a choice of this model, not a requirement of L3.

The model does not choose a web framework, a persistence engine, a package layout beyond the declared core, or a test runner. It requires the core to be callable without the interaction boundary.

## 2. Constructions and relations

| Construction | Meaning |
| --- | --- |
| `Core` | The declared module set that contains cases, entities, tool contracts, and composition. It excludes the application initializer and the interaction boundary, and does not import the interaction adapter. |
| `ApplicationInitializer` | A module that composes the application and/or starts a channel. It may import the boundary and is outside the core scope. |
| `EntitySymbol` | The module/class where an entity's canonical validity is established, by the entity itself or by the consuming case. |
| `CaseSymbol` | The class or function that implements one ADI case, with its callable convention and authorization point. |
| `ToolContractSymbol` | The protocol or contract that cases consume; implementations are selected outside the cases. |
| `ImplementationSymbol` | A concrete tool implementation bound by composition. |
| `CompositionSymbol` | The module or factory that selects implementations and injects collaborators. |
| `VerificationLink` | The command, check reference, or evidence record that exercises the core. |

Relations: each ADPM case maps to exactly one ADI case; each ADI case references its UCS case and its M2 program case; each case consumes tool contracts and receives its collaborators from composition; the declared validity owner (entity or consuming case) establishes canonical validity; tools receive ready entities and do not repeat internal coherence checks.

The separation between the core and the application initializer is logical. A file does not need to move out of the package: the model requires the artifact to declare exactly which modules belong to the core and which modules compose or start the boundary.

## 3. Fields

The machine-readable template is [`template.json`](template.json).

| Object | Field | Kind | Notes |
| --- | --- | --- | --- |
| Root | `model`, `model_version`, `layer`, `oal_edition`, `project`, `source_l2` | R | `source_l2` names the M2 instance and version. |
| Core | `package`, `modules`, `excluded`, `language`, `transport_imports` | R | `modules` is the exact core scope. `excluded` names files inside the container that are not core. `transport_imports` must be empty. |
| ApplicationInitializer | `symbol`, `role`, `imports_transport` | R | The composition/startup module, outside the core scope; it may import the boundary. |
| EntitySymbol | `ucs_entity_id`, `symbol`, `validity_owner` | R | `symbol` uses `path::qualified.name`; `validity_owner` is `entity` or `consuming-case`. |
| CaseSymbol | `id`, `ucs_case_id`, `adpm_case_id`, `symbol`, `callable_convention`, `authorization` | R | `authorization` states where the denial occurs before effects. |
| ToolContractSymbol | `id`, `symbol`, `ready_entity_assumption`, `contextual_conditions` | R | `contextual_conditions` must not include a copy of $I_E$. |
| ImplementationSymbol | `contract_id`, `symbol`, `configuration` | R | Concrete tool selection. |
| CompositionSymbol | `symbol`, `injected_collaborators`, `selection_point` | R | No hidden global lookup. |
| VerificationLink | `bt_ids`, `checks`, `execution` | R | `execution.status` is `not_recorded`, `recorded`, or `not_applicable`. |
| Mapping | `cases`, `criteria`, `bt_links` | R | Preserves identities from M1 and M2. |

`validity_owner` identifies who establishes canonical validity before a tool receives a ready entity:

- `entity`: the entity's construction or assignment enforces $I_E$; a ready instance satisfies it by construction.
- `consuming-case`: the entity is a data shape, and the case that creates or accepts it applies the canonical validation, directly or through a canonical helper, before calling a tool or otherwise treating the entity as ready.

`validity_location` in the selected M1 model and the case symbols in this model identify the code that establishes that validity. When the owner is a consuming case, the artifact must identify the construction/validation path and the tool call it precedes. The tool then assumes $e \in V_E$ and checks only its own contextual conditions. This is distinct from other case preconditions, such as permission, expected version, or existence, which are checked separately by the case or the tool as their contracts require.

## 4. Validity conditions

- **V-M3-01 — Identity.** Model identity `OAL-EX-M3-PYTHON-CORE`, version `0.1.0`, layer `L3`, and the declared OAL edition are present.
- **V-M3-02 — Case bijection.** Every case of the selected M2 instance has exactly one ADI case symbol; no extra ADI case identities exist in the declared scope.
- **V-M3-03 — Symbols resolve.** Every declared symbol resolves in the referenced file through the Python AST. A name in a comment or string is not a symbol.
- **V-M3-04 — Core independence.** The core scope is exactly `core.modules`. No core module imports the interaction adapter, a web server module, or a transport-specific representation; `core.transport_imports` is empty. `core.excluded` and `application_initializers` are outside the core scope; an application initializer may import the boundary without violating core independence.
- **V-M3-05 — Authorization.** Each case receives actor context explicitly, through a representation and trusted invocation path declared by the artifact, and applies its policy before domain effects. Missing, unresolved, unknown, or unpermitted contexts are denied; authentication is required as declared by the case contract. An explicit anonymous context is permitted only when the selected case admits it. Calls between cases propagate the relevant context and preserve the called case's policy. Authorization is not delegated to the interface.

The current examples require authenticated callers. Their `principal` or actor role string is the chosen representation of an already resolved context; trusted direct callers supply it, and HTTP adapters resolve it from the demonstration credentials. The core checks the role permission, not HTTP credentials. This convention does not impose a universal actor-context class or make arbitrary external role strings trustworthy.
- **V-M3-06 — Tool coherence.** Tool contracts state that a ready entity satisfies $I_E$. Implementations do not re-execute, duplicate, or generate an equivalent internal entity check; their extra checks are distinct contextual conditions with object, purpose, and responsibility.
- **V-M3-07 — Composition.** Collaborators are injected through a declared composition symbol. Cases do not select concrete tools or read global state.
- **V-M3-08 — Verification links.** Every referenced check exists and is executable or reviewable. `execution.status` is truthful; an unexecuted check is not presented as passed.
- **V-M3-09 — Identity preservation.** ADI case identities and their links to UCS, ADPM, and behavioral tests are recorded and bidirectional.

## 5. Mapping to the OAL L3 rules (Stable-v1.0.0)

| OAL ADI rule | Model construction or condition |
| --- | --- |
| 1. Materialization of L2 roles | `Core`, `CaseSymbol`, `EntitySymbol`, `ToolContractSymbol`, `CompositionSymbol`; V-M3-02, V-M3-03. |
| 2. Authorization | `CaseSymbol.authorization`; V-M3-05. |
| 3. Verification integration | `VerificationLink`; V-M3-08. |
| 4. Composition and collaborators | `CompositionSymbol`, `ImplementationSymbol`; V-M3-07. |
| 5. Evolution, traceability, evidence | `source_l2`, mappings, execution records; V-M3-08, V-M3-09. |

## 6. Template, example, and counterexample

- [`template.json`](template.json) is the logical template.
- [`example.json`](example.json) is a **partial slice** of Tiny Catalog: two case symbols, the store contract, the composition, and the verification links. The complete instance is the project's core and its documents.
- [`counterexample.json`](counterexample.json) delegates authorization to the transport, points a case at a missing symbol, and gives the store implementation a redundant entity-field check. The expected violations are listed in the file.

## 7. Evidence and limits

The model was reviewed against the ADI rules above. It is deliberately partial: it does not prescribe a package layout, a class hierarchy, a dependency-injection container, or a test framework. It also does not prove that the implementation is correct; it fixes the structural and responsibility conditions that a review can check.

Symbol resolution and import boundaries can be checked structurally. Such a check does not execute the core and does not prove behavioral correctness.

## 8. Instantiating and verifying

1. Start from the selected M2 instance and list its cases.
2. Map each case to one ADI case symbol and record the callable convention.
3. Identify entities and their canonical validity symbols, tool contracts, implementations, the composition point, and the application initializer separately from the core module set.
4. State the authorization point for every case.
5. Record verification links and execution status.
6. Add the L3 entry to `model-instances.json` and run the selected test commands.

## Stable compatibility assessment

Origin: Alpha-v0.2.0-Alkimim, model version 0.1.0. For Stable-v1.0.0, the numbered OAL rules and this model's fields and validity conditions were compared with that baseline; they are unchanged. The mapping above therefore carries forward for the same educational scope. This is a compatibility review by Codex, not external certification or a transformer execution. The [assessment report](../../../COMPATIBILITY.md) records scope and limits; project executions are recorded separately.
