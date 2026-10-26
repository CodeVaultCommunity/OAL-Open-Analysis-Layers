# OAL-EX-M4-HTTP-BOUNDARY — Local HTTP Boundary (L4)

[Português](MODEL.pt-br.md) · [Models](../README.md) · [Reference rules](../../../README.md#reference-rules)

**Identity:** `OAL-EX-M4-HTTP-BOUNDARY`
**Version:** 0.1.0
**Layer:** L4 (ADIB)
**OAL edition declared:** Stable-v1.0.0
**Status:** example of a reusable model. This document specifies the model; it does not certify any project artifact.

## 1. Objective and scope

The model defines a local HTTP interaction boundary around a callable core. It fixes the channel contract, endpoints, actor-context resolution, error mapping, interface elements, many-to-many links, and channel obligations that an L4 artifact must expose. HTTP, JSON, and local execution are choices of this model, not requirements of L4.

The model does not choose a web framework, an HTML design, a credential store, or a deployment topology. It requires the boundary to invoke cases, not to absorb them.

## 2. Constructions and relations

| Construction | Meaning |
| --- | --- |
| `Channel` | The declared interaction channel: kind, base configuration, pages, authentication scheme, actor-context resolution. |
| `Endpoint` | A stimulus: method, path, invoked ADI case, inputs, identity, success, failures, representation. |
| `InterfaceElement` | A page control, route, or static element; it may invoke one or more cases or be interface-only. |
| `Obligation` | A channel requirement with nature, statement, origin (`external`, `ucs`, or `l4-decision`), scope, verifiable conditions, and check references. |
| `ChannelCheck` | A planned or executed check of the boundary. |
| `ExposureScope` | The set of ADI cases exposed by this channel. |

Relations: $H$ is the set of interface elements and $U_3$ the set of ADI cases; the invocation relation $R \subseteq H \times U_3$ is many-to-many and is recorded in both directions. Elements with no case link are classified interface-only. Every endpoint invokes a declared ADI case and passes the resolved actor context explicitly. The channel authenticates when required by that case's contract. An explicitly admitted anonymous role is resolved as such; a missing context or failed authentication is not converted to anonymous access.

## 3. Fields

The machine-readable template is [`template.json`](template.json).

| Object | Field | Kind | Notes |
| --- | --- | --- | --- |
| Root | `model`, `model_version`, `layer`, `oal_edition`, `project`, `source_l3` | R | `source_l3` names the M3 instance and version. |
| Channel | `kind`, `configuration`, `pages`, `authentication`, `identity_resolution` | R | Local demonstration settings are declared; `identity_resolution` describes how the actor context is established. |
| Endpoint | `id`, `method`, `path`, `case_id`, `inputs`, `identity`, `success`, `failures`, `representation` | R | `case_id` must be an exposed ADI case. |
| InterfaceElement | `id`, `description`, `invokes`, `interface_only` | R | `invokes` lists ADI cases; interface-only elements have an empty list and a purpose. |
| Obligation | `id`, `nature`, `statement`, `origin`, `origin_reference`, `scope`, `verifiable_conditions`, `check_refs` | R | `origin` distinguishes external/ucs restriction from an L4 decision. |
| ChannelCheck | `id`, `obligation_ids`, `case_ids`, `criteria`, `scenario`, `boundary`, `status` | R | Planned and executed states are separate. |
| Technical storage | `technical_storage` | C | If used, declares channel-only state, scope, access, failures, and lifetime. An empty list means no such storage. |
| Exposure | `exposure_scope`, `interface_only`, `persistence_access` | R | `persistence_access` states that domain persistence is accessed through cases; any strictly technical channel storage has a separate declared contract. |

## 4. Validity conditions

- **V-M4-01 — Identity.** Model identity `OAL-EX-M4-HTTP-BOUNDARY`, version `0.1.0`, layer `L4`, and the declared OAL edition are present.
- **V-M4-02 — Channel declared.** The channel kind, configuration, authentication requirements, and actor-context resolution mechanism are declared. Demonstration credentials are identified as such.
- **V-M4-03 — Endpoint mapping.** Every endpoint invokes exactly one declared ADI case and passes the resolved actor context explicitly. Inputs, authentication requirements, success, failures, and representation are stated.
- **V-M4-04 — Authorization boundary.** The boundary resolves actor context and authenticates when the case contract requires it; it does not replace case authorization. Endpoints, pages, or scripts do not implement domain permission decisions.
- **V-M4-05 — Domain persistence and technical state.** The boundary accesses domain records and their persistence tools through cases. Strictly technical channel state, such as a session, may use storage under a separately declared contract for scope, access, failures, and lifetime. Such storage cannot contain domain decisions or bypass case authorization. The current demonstration channels use no persistent session store.
- **V-M4-06 — Many-to-many links.** $R \subseteq H \times U_3$ is recorded in both directions; every interface element is either linked to declared ADI cases or classified interface-only with a purpose. The exposure scope is explicit.
- **V-M4-07 — Obligation origin.** Each obligation states its origin. External restrictions cite their source; UCS-inherited requirements are marked `ucs`; decisions introduced by the boundary are marked `l4-decision` and are not presented as external requirements.
- **V-M4-08 — Channel checks.** Each claimed obligation is linked to at least one planned check. Planned checks and executed results are separate; `execution.status` is truthful.
- **V-M4-09 — No new domain rules.** The boundary does not introduce a new transaction, decision, or domain objective in an endpoint, page, or script. If interaction reveals a new domain need, UCS and the affected derivations are revised.
- **V-M4-10 — Partial exposure.** If only part of the ADI cases is exposed, `exposure_scope` names the exposed set.

## 5. Mapping to the OAL L4 rules (Stable-v1.0.0)

| OAL ADIB rule | Model construction or condition |
| --- | --- |
| 1. Interaction scope | `Channel`, `ExposureScope`. |
| 2. Stimuli and responses | `Endpoint` fields. |
| 3. Actor context at the boundary | `Channel.identity_resolution`, `Endpoint.identity`; V-M4-04. |
| 4. Many-to-many mapping | `InterfaceElement`, $R$, V-M4-06. |
| 5. Boundary of decisions | V-M4-05, V-M4-09. |
| 6. Channel contract | `Obligation` with origin, scope, conditions; V-M4-07. |
| 7. Interaction verification | `ChannelCheck`, V-M4-08. |

## 6. Template, example, and counterexample

- [`template.json`](template.json) is the logical template.
- [`example.json`](example.json) is a **partial slice** of Tiny Catalog: two endpoints, two interface elements, and the channel obligations. The complete instance is the project's HTTP contract and traceability map.
- [`counterexample.json`](counterexample.json) lets an endpoint read SQLite directly, delegates authorization to the route, introduces a business rule in JavaScript, and leaves a reverse link missing. The expected violations are listed in the file.

## 7. Evidence and limits

The model was reviewed against the ADIB rules above. It is deliberately partial: it does not prescribe a UI design, a credential product, a session mechanism, or an accessibility audit. It also does not prove that the interface works in a browser; the declared checks and their execution status bound the evidence.

A structural check can check structural links, endpoint-to-case mapping, interface-only classification, and the declared evidence state. It does not execute JavaScript or prove visual behavior.

## 8. Instantiating and verifying

1. Start from the selected M3 instance and list its ADI cases.
2. Declare the channel and the exposed cases.
3. Map each endpoint to one case and declare identity, inputs, success, failures, and representation.
4. Record interface elements and the many-to-many links in both directions; classify interface-only elements.
5. Record obligations with their origin and link them to channel checks.
6. Add the L4 entry to `model-instances.json` and run the selected test commands and the selected channel tests.

## Stable compatibility assessment

Origin: Alpha-v0.2.0-Alkimim, model version 0.1.0. For Stable-v1.0.0, the numbered OAL rules and this model's fields and validity conditions were compared with that baseline; they are unchanged. The mapping above therefore carries forward for the same educational scope. This is a compatibility review, not external certification or a transformer execution. The [assessment report](../../../COMPATIBILITY.md) records scope and limits; project executions are recorded separately.
