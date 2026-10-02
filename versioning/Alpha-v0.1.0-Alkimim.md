<a id="release-notes"></a>
# Release notes — OAL Alpha-v0.1.0-Alkimim

Alpha-v0.1.0-Alkimim is a finalized version within OAL's ongoing alpha stage. It defines UCS (L1), ADPM (L2.1), ADVS (L2.2), ADI (L3), ADIB (L4), and the engines between them. It also specifies how implementations of the same layer or engine can be translated with controlled loss and how neighboring layers can be implemented together. Engines L2-L3 and L3-L4 may consult L1 as an additional source.

The English and Portuguese READMEs include a case-cardinality map. Tiny Catalog, Board CRM, and Work Board are runnable Python examples with P1–P4 artifacts. Their needs baselines were reconstructed from their UCS; they are not independent stakeholder records.

Principal editor of this edition: Douglas de Oliveira Alkimim. Bruno Chevitarese is credited as a co-author of OAL.

---

# OAL Alpha-v0.1.0-Alkimim — reference rules

[Português](Alpha-v0.1.0-Alkimim.pt-br.md) · [Home](../README.md)

OAL stands for Open Analysis Layers. Its five layers cover use-case behavior (UCS), program modeling (ADPM), verification planning (ADVS), the callable core (ADI), and external interaction (ADIB). The model is public and leaves teams free to choose formats, languages, tools, and project layouts. Each layer names a responsibility; a project may combine them in files while keeping their boundaries traceable. The person responsible for a derivation is distinct from the actor who runs a use case.

<a id="oal-layers"></a>
## OAL — cross-layer rules

1. **Reference layers.** Distinguish UCS, ADPM, ADVS, ADI, and ADIB by responsibility. ADPM and ADVS derive in parallel from UCS; ADIB is the interaction boundary around the implemented cases. Physical artifacts may combine or split responsibilities if each remains identifiable and traceable.

2. **Accountable derivations.** For needs-to-UCS, UCS-to-ADPM, UCS-to-ADVS, ADPM-and-ADVS-to-ADI, and ADI-to-ADIB derivations, record source and destination baselines, a named accountable person, scope, and added decisions. UCS may be consulted as an additional source when deriving ADI or ADIB; when used, record its baseline and the decisions it informed. One person may own several derivations; a job title or tool alone does not identify the accountable person.

3. **Case identity and behavioral test.** Within a declared scope, each UCS use case has exactly one corresponding case identity in ADPM, one directly linked behavioral test in ADVS, and one case identity in ADI, with no extra ADPM or ADI cases or directly linked ADVS behavioral tests. The behavioral test is unique for its UCS case. It may consume supporting subtests for criteria, alternatives, permissions, or other checks; subtests are not directly linked to a UCS case and are not behavioral tests by this definition. Channel-only checks may be recorded separately without becoming new use cases. ADIB interface elements and ADI cases may map many to many; this mapping does not create a new case identity.

4. **Changes and claims.** A change to a source contract, permission, or interface decision requires review of affected derived artifacts and verification scenarios. Version and conformance claims name the baselines, interface scope, and evidence actually compared.

5. **Distinct people and actors.** A runtime actor is a person or external system that requests a use case. A derivation owner is the named person who produces or approves an artifact transition. The roles of specifier, program modeler, verification designer, implementer, and interaction designer describe work, not mandatory job titles; none is automatically a runtime actor.

6. **Layer names and implementation claims.** UCS is L1; ADPM is L2.1; ADVS is L2.2; ADI is L3; ADIB is L4. L2.1 and L2.2 derive in parallel from L1. A claim to implement an OAL layer identifies this edition, the layer, the implemented responsibility, its scope, and the artifacts or evidence that support the claim. A layer claim alone does not assert conformance of the entire model.

7. **Derivation engines.** An Engine LX-LY produces an LY artifact from an LX baseline, with any additional inputs required by the named derivation. Production does not imply literal translation or structural equivalence: L4 defines an interaction boundary around L3 callable cases, rather than a translated copy of L3. The canonical names are Engine Needs-L1, Engine L1-L2.1, Engine L1-L2.2, Engine L2-L3, and Engine L3-L4. L2 is shorthand for the L2.1 and L2.2 pair, not another layer: Engine L2-L3 requires both and may also consult L1. Engine L3-L4 requires L3 and may also consult L1. Consulting L1 does not change either engine's name. An implementation of an OAL engine identifies its edition, named transition, accepted inputs, produced outputs, preserved links, added decisions, and validation scope. An engine may be realized by a human process, software, or both; its use in a project still records the accountable person and baselines required by rule 2.

8. **Translation within a layer or engine.** Implementations of the same layer share the defining responsibilities and contracts of that layer. An implementation may therefore be translated into another implementation of that layer, including a different language, format, or architecture. The translation identifies the shared characteristics it preserves and any information or behavior it loses or changes; loss is controlled only when it is explicit, bounded by the declared scope, and does not silently discard a defining characteristic or required contract. The same rule applies to implementations of the same named engine: preserve its required inputs, destination responsibility, case links, and derivation obligations while recording implementation-specific losses and decisions. A common label alone does not establish equivalence.

9. **Combined implementations of neighboring layers.** One specialization may implement responsibilities of neighboring layers connected by a named derivation. When it performs the transition from the source responsibility to the destination responsibility, that specialization also implements the corresponding engine; no separate engine component is required. Source, destination, and transition remain separately identifiable and verifiable. This applies, for example, to L1 with L2.1 and to L3 with L4. For Engine L2-L3, the required L2 source comprises both L2.1 and L2.2 even when either is packaged with L3. L2.1 and L2.2 are parallel branches, not a named derivation between each other.

<a id="ucs"></a>
## UCS — Use Case Specification

1. **Scope.** Define objectives, system boundaries, relevant actors, and external participants without prescribing code organization.

2. **Use cases.** Give each use case a stable identifier, primary objective, initiating actor, and permitted actor set. An actor absent from the set cannot execute the case.

3. **Behavioral contracts.** State triggers, inputs, context, assumptions, checked conditions, results, effects, guarantees, alternatives, and failures, including the observable result of denied access. State externally relevant constraints without prescribing routes, screens, payload encodings, or other ADIB mechanisms.

4. **Entities and rules.** Define the meaning, data, relationships, and validity conditions of entities. State other domain rules explicitly and link them to the use cases responsible for applying them.

5. **Composition and dependencies.** Identify dependencies between use cases and the capabilities required from resources and external systems. Make the conditions, information, and results involved explicit without determining calling, access, or integration mechanisms.

6. **Complementary obligations.** Make applicable requirements for persistence, security and isolation, observability, performance, accessibility, and other relevant constraints explicit. Each obligation has a defined scope and verifiable conditions; channel-specific choices belong to ADIB.

7. **Acceptance and links.** Give each case acceptance criteria and links to relevant needs, actors, entities, rules, and dependencies. Preserve its identity in ADPM and ADI; ADVS links criteria to scenarios; ADIB links exposed interactions to the cases they invoke.

8. **Consistency and evolution.** Shared information has a single definition and explicit references. Changes preserve identity and history; assumptions, open issues, and approved definitions remain distinguishable.

9. **Domains — recommendation.** Organization into domains with delimited responsibilities is optional but strongly recommended. When adopted, it identifies the use cases and entities associated with each domain.

10. **Representative examples.** Examples can clarify contracts but do not replace explicit rules or ADVS scenarios.

<a id="adpm"></a>
## ADPM — Analysis-Driven Program Model

1. **Separation and preservation of responsibilities.** ADPM distinguishes use cases, tools, and entities and requires their responsibilities and relationships to be identifiable and mapped in the eventual architecture. It does not choose a concrete architecture or file structure. The distinctions and mapping remain identifiable in ADI and, consequently, in ADIB. Domains are optional; when modeled, their boundaries and mapping must likewise be preserved.

2. **Use cases.** Each use case fulfills an identifiable objective and contains the necessary domain decisions and rules, except for the validations permitted in entities. It does not determine technological mechanisms. It may use other use cases while respecting their contracts.

3. **Entities.** Entities represent data and relationships and may be manipulated by use cases and tools. Their operations are limited to reading, assigning values, and validating data during assignment. They perform no other behavior and do not depend on use cases or tools.

4. **Tools and contracts.** Model tool operations, results, effects, and guarantees separately from mechanisms. Cases depend on contracts; tools do not invent domain rules.

5. **Dependencies and composition.** Show what each case and tool receives, where implementations are selected, and how collaborators are composed. Do not hide required dependencies behind global lookup.

6. **Persistence.** Persistence is accessed through tools. Data responsibilities and the conditions for reading and changing data must be explicit, regardless of whether storage is shared.

7. **Authorization boundary.** Model the authenticated actor input and a deny-by-default permission decision for every case. The decision precedes domain effects and remains effective beyond user-interface controls.

8. **Faithful representation.** Semantic prose or structured pseudocode may express ADPM. Either form must make responsibilities, contracts, dependency wiring, authorization, and algorithms recoverable.

9. **Domains.** Grouping model responsibilities by domain is recommended when it clarifies boundaries.

10. **Lifetime.** State component lifetime where it matters. One case instance per application scope may be chosen but is not required.

<a id="advs"></a>
## ADVS — Analysis-Driven Verification Specification

1. **UCS derivation and behavioral test.** Define exactly one behavioral test directly linked to each UCS use case in the declared scope, preserving its case identity. Identify the UCS baseline, contracts, and acceptance criteria it covers. A behavioral test may consume supporting subtests, including several scenarios, without creating additional behavioral tests for that case. Physical files may combine several tests if the one-to-one case mapping remains explicit.

2. **Test and subtest contracts.** For the behavioral test and each supporting scenario or subtest, state preconditions, actor where relevant, action, expected result and effects, and observed boundary or configuration. The behavioral test may exercise a case directly or through an ADIB channel; its subtests support that test without having a direct UCS case link.

3. **Permissions.** Cover allowed and denied access for each distinct case permission; verify denial before domain or persistence effects.

4. **Failures and limits.** Cover specified alternatives, failures, and consequential boundaries. When ADIB selects a channel, add scenarios for its own interaction contract, such as parsing, representation, authentication, and accessibility where applicable; name risks outside the selected scenarios.

5. **Trace and status.** Link every UCS acceptance criterion to its case's behavioral test and the supporting checks that cover it; link claimed ADIB-specific obligations to their planned checks. Tool and entity checks are recommended but are not required as separate ADVS specifications; their contract guarantees and validity rules still require the checks needed to support a conformance claim. Keep plans distinct from executed evidence; passing results support only observed configurations. ADIB decisions may therefore cause ADVS to be revised.

<a id="adi"></a>
## ADI — Analysis-Driven Implementation

1. **Program realization.** Implement modeled case identities, entities, tool contracts, composition, algorithms, and error paths as a callable application core. Preserve the ADPM distinction and mapping of cases, tools, entities, and modeled domains in the chosen architecture; physical packaging may differ. Record deviations and affected source artifacts. External channel mechanisms are specified in ADIB.

2. **Authorization enforcement.** Receive the actor identity from a caller and enforce case permission before domain effects. Unknown, absent, or unpermitted actors are denied when a case is invoked directly or through ADIB. The interaction boundary supplies identity but cannot replace case authorization.

3. **Verification execution.** Implement and run the behavioral tests and supporting checks derived from ADVS for the application core, retaining case, criterion, and subtest links. Report failed and unexecuted checks; ADIB-specific checks are also executed against the selected channel.

4. **Tool guarantees.** Concrete tools meet ADPM contracts in the claimed configuration, including relevant persistence, isolation, and failure guarantees.

5. **Evidence.** State implementation version, environment, executed scenarios, results, and limits. Do not present planned or configured checks as completed runs.

<a id="adib"></a>
## ADIB — Analysis-Driven Interaction Boundary

1. **Interaction scope.** Declare the supported interaction channels and the actors or external systems they serve. A channel may be a page, programmatic endpoint, command line, message consumer, or another input/output form. State which use cases are exposed in the claimed scope.

2. **Stimuli and responses.** Specify how each channel receives and parses a stimulus, checks its representation, invokes ADI cases, and presents results and failures. A response may be immediate, deferred, or emitted as an event; the observable contract must be explicit.

3. **Identity at the boundary.** When a case requires an actor, authenticate or resolve the caller through the declared channel mechanism and pass the identity to ADI. ADI still enforces the case permission. Hiding an interface control or checking a route alone does not authorize the case.

4. **Many-to-many mapping.** Record the mapping between interface elements and the ADI case identities they invoke in both directions; either side may have multiple links. Identify interface-only elements and their purpose separately. An interaction that introduces a new business objective or rule requires revision of UCS and its derivations.

5. **Boundary of decisions.** Keep transport, presentation, session, and representation decisions in ADIB. Preserve the ADPM/ADI distinction between cases, tools, entities, and modeled domains across this boundary: ADIB invokes cases rather than absorbing their responsibilities. ADIB may coordinate already specified cases but does not make new domain decisions or access persistence tools directly. Case algorithms and authorization remain in ADI.

6. **Channel contract.** Document the selected channel's routes or views, commands or events, representations, errors, and relevant accessibility, localization, and operational obligations. When UCS is consulted, distinguish requirements inherited from it from decisions introduced in ADIB; otherwise identify the sources of channel obligations. Make each claimed obligation verifiable.

7. **Interaction verification.** Review ADVS when ADIB decisions add observable obligations; link those obligations and exposed UCS criteria to interface scenarios. Record executed results and limits for each claimed channel without treating a working core or a planned scenario as proof of the interface.

## Interpretation

The English text is the source of this edition; the Portuguese text is its translation. Only numbered requirements define conformance. Recommendations are marked.

## Guide to this edition

This guide explains the numbered rules without adding requirements.

### Concepts

In OAL, analysis means writing down needs, rules, decisions, assumptions, and consequences so another person can check them. The rules are open to different documents, languages, frameworks, and tools. A repository can combine artifacts if readers can still find each layer's responsibility.

UCS describes behavior, actors, permissions, data meanings, outcomes, and acceptance criteria without choosing channels. ADPM defines the program model: case responsibilities, entities, tools and their contracts, dependency composition, permissions, and algorithms. ADVS defines one behavioral test for each UCS case. ADI realizes the callable application core and records observed core results. ADIB defines and realizes channels that accept stimuli, call ADI cases, and present immediate, deferred, or event responses. These responsibilities do not impose a construction order. A channel decision may require an ADVS update or reveal a behavioral requirement that belongs in UCS.

A runtime actor is a person or external system requesting a use case. A derivation owner is the named person accountable for producing or approving an artifact from its source baseline. The work roles are specifier (needs to UCS), program modeler (UCS to ADPM), verification designer (UCS to ADVS and later channel scenarios), implementer (ADPM and ADVS to ADI), and interaction designer (ADI to ADIB, optionally consulting UCS). One person may hold several roles. A derivation record names the actual person, source and destination baselines, scope, and added decisions.

The layer names are L1 for UCS, L2.1 for ADPM, L2.2 for ADVS, L3 for ADI, and L4 for ADIB. L2.1 and L2.2 derive in parallel. Each UCS case has one corresponding case model, one directly linked behavioral test, and one implemented case. A behavioral test may consume several supporting subtests; those subtests are not themselves behavioral tests. Interface elements and implemented cases map many to many. Navigation, static content, and other interface-only elements are identified separately. The ADPM distinctions among cases, tools, entities, and any modeled domains stay traceable in ADI and across the ADIB boundary, even if their physical packaging differs.

An engine produces the destination responsibility from source artifacts, not necessarily by translating them. Engine L2-L3 uses both ADPM and ADVS and may consult UCS; Engine L3-L4 uses callable ADI cases to produce interaction channels and may also consult UCS. L4 introduces presentation and transport decisions of its own. An engine implementation declares its edition, named transition, accepted inputs, outputs, preserved links, added decisions, and validation scope. Its use in a project still identifies the accountable person.

Two implementations of one layer can use different media and still preserve that layer's defining contracts. Translation between them may omit details specific to one medium; the omitted details and their consequences belong in the translation record. The same reasoning applies to two implementations of one named engine. A combined implementation may contain adjacent responsibilities and their derivation without dividing them into separate files or services; traceability and checks still distinguish each responsibility.

<a id="versioning"></a>
### Versioning and derivation

**Alpha-v0.1.0-Alkimim** names the alpha stage, version number, and this edition's principal editor. Authorship and credits are recorded separately; a later edition may have another editor. English is the source wording and Portuguese is its translation. This version is closed to normative changes; such changes require a new version.

Project artifacts may have their own baseline versions. A release label alone does not establish conformance or show that verification ran. Changes to contracts, permissions, or interaction decisions require review of affected derivations and scenarios. An implementation claim for one layer or one engine names its edition, scope, and supporting evidence; it does not automatically cover the whole model.

<a id="verification"></a>
### Verification

ADVS records what to check before reporting a result. For each UCS case, its unique behavioral test keeps the direct case link and identifies the covered criteria, actor, preconditions, action, expected result and effects, and relevant boundary or configuration. It may consume supporting subtests for allowed and denied actors, alternatives, and failures; these have no direct UCS case link. ADVS need not prescribe separate checks for every tool or entity, although such checks are recommended. Contract guarantees and entity validity still need enough evidence for the scope claimed.

ADI executes checks of the application core. When ADIB selects a channel, ADVS also records scenarios for that channel's parsing, representation, authentication, accessibility, and other claimed interaction obligations as applicable. ADIB execution evidence states which channels and configurations were exercised. Permission checks cover denial before domain or persistence effects. Planned scenarios and executed results remain distinct.

The examples contain unit checks for entities and pure tools, integration checks for tools using other resources, and case-oriented checks. The use of a substitute, SQLite, or HTTP does not by itself determine whether a check is behavioral: the direct one-to-one link to a UCS case does. From an example directory, `python -m pytest` runs its suite; any reported result describes that execution and environment.

<a id="conformance"></a>
### Conformance and scope

The numbered rules above define conformance. A claim states the edition, project baselines, cases and interaction channels in scope, named derivation owners, and evidence actually reviewed. A claim for the complete model includes ADIB; a narrower claim names the responsibilities covered.

Review UCS for behavior and permitted actors; ADPM for case algorithms, contracts, dependency composition, and permission decisions; ADVS for one behavioral test per UCS case, its supporting subtests, and coverage; ADI for callable cases, enforcement, and observed core results; and ADIB for channel contracts, identity at the boundary, interaction decisions, and observed channel results.

Compare case identities across UCS, ADPM, ADVS behavioral tests, and ADI in both directions. Map each UCS acceptance criterion to its behavioral test and supporting checks. For each claimed ADIB channel, inspect the many-to-many map from interface elements to implemented cases in both directions, identify interface-only elements, and link channel obligations to checks. Counts alone cannot establish contract preservation. A planned check is not an executed result. The [Tiny Catalog review](../examples/Alpha-v0.1.0-Alkimim/tiny-catalog/OAL-P3/CONFORMANCE.md) records a narrower assessment of that example.

### Related work

OAL draws on use-case specification, traceability, dependency boundaries, and test derivation. The links here provide context rather than additional requirements. [Use-Case 2.0](https://www.ivarjacobson.com/publications/white-papers/use-case-20-e-book) describes incremental use-case work from design through testing. [Couto, Ribeiro, and Campos](https://arxiv.org/abs/1603.08632) discuss formalizing use cases and consistency. [Hajri and colleagues](https://arxiv.org/abs/1905.11699) study system-test classification and prioritization from use cases.

The [Python sqlite3 documentation](https://docs.python.org/3.13/library/sqlite3.html) supports the examples' storage implementation. [GitHub's Python workflow guide](https://docs.github.com/en/actions/tutorials/build-and-test-code/python) informs the repository workflow. Neither technology is required by OAL.
