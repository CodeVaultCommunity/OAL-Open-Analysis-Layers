# Layer responsibilities — Stable-v1.0.0

This reference describes the responsibilities established by the edition's 37 layer requirements. Labels such as UCS-2 identify the section and local number in the source text. A conforming reusable model establishes these subjects; artifacts instantiating it satisfy them within the declared scope. Recommendations retain their optional status.

## Contents

- [L1 — UCS](#ucs)
- [L2 — unified ADMV](#admv)
- [ADPM — program modeling](#adpm)
- [ADVS — verification specification](#advs)
- [L3 — ADI](#adi)
- [L4 — ADIB](#adib)

<a id="ucs"></a>
## L1 — UCS: Use Case Specification

L1 describes the observable contract of the intended system. Semantic prose and structured representations are both possible; OAL specifies no universal JSON schema or document notation.

### Scope, entities and domain rules — UCS-1, UCS-4

The specification identifies objectives, system boundaries, relevant actors and external participants without prescribing code organization. Entities have explicit meanings, data, relationships and validity conditions. Other domain rules are explicit and linked to the cases responsible for applying them.

### Case identity and actor policy — UCS-2

Each case has a stable identifier, main objective, initiating actor, permitted actors and authorization conditions. Its contract identifies the actor-context information needed and the circumstances requiring authentication. Public and system participation are explicit choices. Actors outside the permitted set, and absent, unresolved or insufficient contexts, cannot execute the case. Missing context does not establish anonymous access.

### Behavioral contracts and channel origin — UCS-3

The contract covers triggers, inputs, context, assumptions, checked conditions, results, effects, guarantees, alternatives and failures, including the observable outcome of denied access. An externally imposed interaction restriction can appear in L1 with its origin identified. Routes, screens, payload encodings, protocols and representations introduced by the solution belong to L4.

A reference in L1 does not convert an L4 decision into an external requirement; mentioning a protocol does not change ownership of an external restriction. A newly identified domain need entails a change to UCS and the affected derivations.

### Dependencies and complementary obligations — UCS-5, UCS-6

Dependencies between cases and capabilities required from resources or external systems identify their conditions, information and results. They do not determine calling, access or integration mechanisms.

Applicable persistence, security, isolation, observability, performance, accessibility and other obligations have defined scopes, identified origins and verifiable conditions. Channel-specific choices remain ADIB responsibilities.

### Acceptance and traceability — UCS-7

Each case has acceptance criteria and links to relevant needs, actors, entities, rules and dependencies. Its identity continues into ADPM and ADI. ADVS connects criteria to scenarios; ADIB connects exposed interactions to invoked cases. Explicitly declared shared integration criteria identify their scope, affected cases and single authoritative definition through references.

### Shared information and knowledge status — UCS-8

Shared information has one definition and explicit references. Changes preserve identity and history. Observed facts, desired requirements, inferences, premises and pending issues remain distinguishable; a specification statement is not automatically a proven fact.

### Domains and examples — UCS-9, UCS-10

Organization into domains is optional but strongly recommended. Adopted domains identify their associated cases and entities. Representative examples can clarify a contract, but explicit rules and ADVS scenarios retain their separate roles.

<a id="admv"></a>
## L2 — unified ADMV: Analysis-Driven Modeling and Verification

ADMV combines the program model, ADPM, and the verification specification, ADVS. Both are required, distinguishable components of one layer. Neither component alone completes L2.

ADPM and ADVS may be prepared in parallel from UCS. Their preparation belongs to one L1-to-L2 derivation, and the complete ADMV informs L3. Separate folders, sections or files are packaging choices; ADVS does not require a separate file or package from ADPM.

<a id="adpm"></a>
## ADPM — Analysis-Driven Program Model

### Responsibilities and their mapping — ADPM-1

Cases, tools and entities have distinct responsibilities and identifiable relationships. Their distinctions and mapping continue into the selected L3 code organization and across ADIB. ADPM does not select a concrete code organization or file structure. Domains are optional; modeled domain boundaries and mappings remain identifiable.

### Cases, composition and entity behavior — ADPM-2, ADPM-3

Each case fulfills an identifiable objective and contains the necessary domain decisions and rules, except for validation and behavior explicitly delegated to entities by the model. The distribution of behavior between entities and cases is a model choice. Cases do not determine technological mechanisms.

A case can use another case through a declared dependency while respecting its contract and supplying the pertinent actor context. The called case applies its own authorization policy. Delegation or action on another participant's behalf has an explicit rule; an internal call grants no additional permission. Authorization precedes prohibited effects.

Entities represent data and relationships and do not depend on cases or tools. A model can have predominantly data entities, with reading, assignment and validation during assignment, or entities with domain behavior. Contracts, invariants, dependencies and the entity's responsibility for each enforced rule are explicit. Entity behavior does not absorb responsibilities assigned to cases.

### Tool contracts and validation ownership — ADPM-4

Tool operations, results, effects and guarantees are specified separately from mechanisms. Cases depend on those contracts; tools do not invent domain rules. Domain validity belongs to the entity or consuming case, with an identifiable owner for each rule.

For an entity's internal coherence predicate $I_E$, the valid entities form:

$$
V_E = \{e \mid I_E(e)\}.
$$

A tool receiving a ready entity receives $e \in V_E$ by contract. Re-executing the entity validation, reimplementing an equivalent condition, or generating the same check elsewhere duplicates that responsibility. Renaming such a check as a technical guarantee does not change its nature.

A distinct contextual condition $Q_t(e,c)$ can belong to the tool's own contract: expected version, concurrency conflict, atomic global uniqueness, existence of a persisted resource or external-service availability. Its condition, object, purpose and responsibility are identifiable. This does not transfer case authorization or domain decisions to the tool.

Raw records are not ready entities. Hydration uses the entity's canonical construction and validation. Codecs and adapters can check the technical representation of raw data without acquiring a parallel implementation of entity validity. Entity validation does not replace atomic persistence guarantees with preliminary queries vulnerable to races.

JSON, encoding, body format and channel parameters belong to L4; record shape, serialization and deserialization belong to codecs or adapters under representation contracts. Shared helpers can centralize validation used by entities and cases without moving it into tools or duplicating conditions. UI error prevention coexists with authoritative validation effective through direct core calls.

These restrictions concern collaborating program tools. Verification instruments for OAL schemas, models and traceability are a different category.

### Dependencies, persistence and authorization — ADPM-5, ADPM-6, ADPM-7

Required dependencies, implementation-selection points and collaborator composition are explicit. Global lookup does not hide dependencies the case or tool requires.

Persistence is accessed through tools. Data responsibilities and conditions for reading and changing data are explicit whether storage is shared or separate.

Every case has an explicit input for actor context resolved according to its contract and a deny-by-default authorization decision before domain effects. Missing, unresolved, unknown or insufficient contexts are rejected. Authenticated identity is required when the contract requires it; an anonymous context is admitted only when expressly permitted. This boundary remains effective in direct calls and beyond UI controls.

### Representation, domains and lifetime — ADPM-8, ADPM-9, ADPM-10

Semantic prose or structured pseudocode can express ADPM when responsibilities, contracts, dependency wiring, authorization, validation locations and algorithms remain recoverable.

Grouping responsibilities by domain is recommended when it clarifies boundaries. Component lifetime is explicit where relevant. One case instance per application scope is an available choice, not a universal requirement.

<a id="advs"></a>
## ADVS — Analysis-Driven Verification Specification

### Case identity and behavioral tests — ADVS-1

Each UCS case in the declared scope has exactly one directly linked behavioral test. The test preserves case identity and identifies its UCS baseline, covered contracts and acceptance criteria. It can contain multiple scenarios and supporting subtests for permissions, alternatives, failures or criteria without creating another directly linked behavioral test.

Physical files may combine tests. The cardinality concerns case identities and direct links, not a single physical test function per case.

### Test contracts — ADVS-2

Behavioral tests and supporting scenarios or subtests describe preparation, preconditions, action, oracle and observed boundary or configuration. The oracle states expected results and effects.

Case scenarios identify actor context, including deliberately missing or unresolved context for denial checks. Entity or tool checks may identify actor context as inapplicable. A behavioral test may exercise the case directly or through ADIB; supporting subtests have no direct UCS case link.

### Permissions, alternatives and limits — ADVS-3, ADVS-4

Coverage includes allowed and denied access for distinct case permissions, missing, unknown and insufficient contexts, and explicitly anonymous participation where applicable. Denial precedes domain or persistence effects.

Specified alternatives, failures and consequential boundaries are covered. A selected ADIB channel brings its own interaction-contract scenarios, such as parsing, representation, authentication and applicable accessibility. Risks outside the selected scenarios remain identified.

### Traceability and evidence status — ADVS-5

Each case-specific acceptance criterion links to its case's behavioral test and relevant supporting checks. Shared integration criteria link to affected cases' behavioral tests and shared supporting checks without an additional directly linked behavioral test. Claimed ADIB obligations link to planned checks.

Separate ADVS specifications for tools and entities are recommended rather than universally required; evidence for their guarantees and validity remains necessary for the conformance scope claimed.

Planned verification, test code and observed execution results are three different objects. A test file does not demonstrate execution, and passing results support the configurations actually observed. ADIB decisions can therefore change the verification specification.

<a id="adi"></a>
## L3 — ADI: Analysis-Driven Implementation

An L3 model is a reusable code organization: it defines how responsibilities, dependencies, callable cases and verification are organized and how concrete artifacts are recognized. Architecture can be a choice within such a model. Model specification does not require prior execution of every future project's tests.

### Materialization and authorization — ADI-1, ADI-2

The organization materializes ADPM cases, entities, tools, modeled domains and dependencies. Identities, algorithms and error paths become a callable core. ADPM distinctions and mappings remain identifiable despite different physical packaging. Deviations and affected source artifacts are recorded; external channel mechanisms belong to ADIB.

An explicit invocation path supplies actor context whose origin and trust assumptions are identifiable. The case applies its authorization policy before domain effects, both directly and through ADIB. Absent, unresolved, unknown, unpermitted or otherwise insufficient contexts are denied. Explicitly permitted anonymous context is distinct from absence.

### Verification and composition — ADI-3, ADI-4

ADVS-derived behavioral tests and supporting checks integrate with core execution while retaining case, criterion and subtest links. Artifacts report failed and unexecuted checks. ADIB-specific checks exercise the selected channel.

Implementation selection and composition occur through explicit dependencies. Concrete tools satisfy ADPM contracts in the claimed configuration, including relevant persistence, isolation and failure guarantees.

### Evolution and evidence — ADI-5

Changes remain traceable to L2 sources. Artifact evidence identifies implementation version, environment, executed scenarios, results and limits. Planned or configured checks are distinct from completed runs.

<a id="adib"></a>
## L4 — ADIB: Analysis-Driven Interaction Boundary

### Scope, stimuli and responses — ADIB-1, ADIB-2

The interaction model identifies supported channels, actors or external systems served, capabilities and exposed cases. Channels include pages, programmatic endpoints, commands, message consumers and other input/output forms.

Each channel's contract describes stimulus reception and parsing, representation checks, case invocation and presentation of results and failures. Responses can be immediate, deferred or emitted as events, with explicit observable behavior.

### Context and case mapping — ADIB-3, ADIB-4

The channel resolves actor context through its declared mechanism and passes it to ADI. Authentication applies when required by case and channel contracts. Origin and trust assumptions are explicit; a caller-supplied role label alone does not establish trusted context.

Public access can resolve an expressly permitted anonymous context. Failed or missing resolution does not silently become anonymity. ADI still evaluates case authorization; hiding a control or checking a route alone does not authorize the case.

Mappings between interface elements and invoked ADI case identities exist in both directions. Either side can have multiple links. Interface-only elements have separately identified purposes.

### Decision boundaries and technical storage — ADIB-5

Transport, presentation, session and representation decisions belong to ADIB. The boundary preserves the distinctions among cases, entities, tools and modeled domains. It invokes cases and can coordinate already specified cases without absorbing their responsibilities or introducing new domain decisions.

Domain-persistence tools are accessed through cases. Storage exclusively for technical channel state, such as sessions or request correlation, is permitted under an explicit contract covering data, access conditions, lifetime and failure behavior. Such storage does not introduce business-data rules, bypass cases for domain state or replace authorization.

Coordination that adds a transaction, decision or domain objective belongs to a case responsibility and entails changes to UCS and its derivations. Case algorithms and authorization remain in ADI.

### Channel contracts and verification — ADIB-6, ADIB-7

The channel contract identifies routes, views, commands or events, representations, errors and relevant accessibility, localization and operational obligations. External requirements retain their origins. Inherited UCS requirements and decisions introduced by ADIB remain distinct; sources of channel obligations are identifiable even when UCS was not consulted. Each claimed obligation is verifiable.

New observable ADIB obligations are reflected in ADVS. Interface scenarios link those obligations and exposed UCS criteria to verification. Execution evidence identifies results and limits for each claimed channel; a working core or planned scenario does not establish interface behavior.
