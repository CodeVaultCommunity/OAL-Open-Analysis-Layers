<a id="release-notes"></a>
# Release notes — OAL Alpha-v0.2.0-Alkimim

Alpha-v0.2.0-Alkimim revises Alpha-v0.1.0-Alkimim in six main directions:

1. **One L2 layer.** The former L2.1 (ADPM, program model) and L2.2 (ADVS, verification specification) become two required, distinguishable components of a single layer, **L2 · ADMV (Analysis-Driven Modeling and Verification)**. Engine L1-L2 produces both; a claim of L2 coverage includes both. The edition has four layers: L1 (UCS), L2 (ADMV), L3 (ADI), and L4 (ADIB). Client needs are not an OAL layer: the Needs-to-L1 derivation consumes a declared external needs model and remains recorded as a derivation.
2. **Layers, models, and artifacts.** Each layer defines a metamodel. A reusable model that satisfies a layer's metamodel is instantiated by concrete project artifacts. For a fixed edition and versions, $\mathcal{M}_i$ denotes the models satisfying layer $L_i$, and $A(M)$ the artifacts satisfying model $M$. The rules state what a model must establish and what artifacts instantiating it must satisfy; conformance claims distinguish model conformance, artifact conformance, coverage of a declared set of layers, and complete coverage of all four layers.
3. **Engines and transformers.** A derivation engine is a metamodel that specifies the construction of a deterministic transformer for a selected pair of source and destination models and the execution of that transformer on artifacts. Construction and execution are separate records, with declared domains, preservation relations, determinism criteria, failure classification, and traceability. A composition of transformers is defined only on a domain whose outputs remain inside the next transformer's supported domain; sharing the intermediate model and version is not sufficient.
4. **Behavior and validation.** An L2 model may distribute behavior between entities and use cases when it makes contracts, invariants, and dependencies explicit. Entities define their internal coherence conditions; a tool receiving a ready entity assumes the entity is coherent and must not re-execute, duplicate, or generate an equivalent internal check. A tool may evaluate distinct contextual conditions of its own contract, with identifiable object, purpose, and responsibility. Domain validity remains in the entity or consuming case; persistence keeps the atomic guarantees of its contract.
5. **Didactic reusable models and instances.** The repository specifies four reusable models, one per layer — OAL-EX-M1-CASE-CONTRACTS, OAL-EX-M2-PROGRAM-SCENARIOS, OAL-EX-M3-PYTHON-CORE, and OAL-EX-M4-HTTP-BOUNDARY — each with identity, version 0.1.0, validity conditions, template, example, counterexample, and limits. Tiny Catalog, Board CRM, and Work Board declare four instances each in `model-instances.json`, twelve declarations in total. The models were applied manually; this is not a demonstration of constructed or executed transformers.
6. **Conversion, translation, and channel origin.** The rules distinguish representation conversion within one model, translation between models of the same layer, derivation between layers, and substitution between realizations of the same engine. L1 may inherit externally imposed interaction restrictions with their origin; interaction decisions introduced by the solution belong to L4, and a reference does not change ownership.

Other rules carry forward from Alpha-v0.1.0-Alkimim. OAL remains in its alpha stage; this edition is a local revision and does not assert a publication date, DOI, or external review. The English and Portuguese READMEs include a case-cardinality map.

### Revision within this edition

This revision retains **Alpha-v0.2.0-Alkimim** and the existing didactic-model version labels. It clarifies actor roles and execution context, defines L3 models as reusable code organizations, distinguishes technical channel storage from domain persistence, and separates manual derivation records from transformer claims. It also reorganizes long requirements, aligns the didactic representations and shared criteria, corrects the executable examples, updates the bilingual diagrams, and renders the mathematical notation in Markdown. The [content inventory](../../CONTENT-SHA256.json) identifies the delivered files, and the [structured execution record](examples/verification/execution.json) preserves the observed application-test results. The edition also includes an [informational skill](skill/oal-alpha-v0-2-0-alkimim/SKILL.md); these changes do not create another edition.

Principal editor of this edition: Douglas de Oliveira Alkimim. Bruno Chevitarese is credited as a co-author of OAL.

---

# OAL Alpha-v0.2.0-Alkimim — reference rules

[Português](README.pt-br.md) · [Home](../../README.md)

OAL stands for Open Analysis Layers. The model organizes development responsibilities into four layers: L1 specifies use cases (UCS); L2 combines program modeling (ADPM) and verification specification (ADVS) as ADMV; L3 implements the callable core (ADI); and L4 provides the external interaction boundary (ADIB). Each layer defines a metamodel; a reusable model satisfying that metamodel is instantiated by concrete project artifacts. OAL acts as a reference model: like other reference models, it separates responsibilities and names conformance without importing the technology of any particular domain, and it leaves teams free to choose formats, languages, tools, and project layouts. The person responsible for a derivation is distinct from the actor who runs a use case.

<a id="oal-layers"></a>
## OAL — cross-layer rules

1. **Layers, metamodels, models, and artifacts.** The OAL layers are UCS (L1), ADMV (L2), ADI (L3), and ADIB (L4). Each layer $L_i$ defines a metamodel: the requirements a reusable model $M_i$ of that layer must satisfy. A concrete project artifact $a$ instantiates a selected model: $M_i \models L_i$, and $a \models M_i$ (equivalently, $a \in A(M_i)$). The layer number names a development responsibility; the metamodel-to-model-to-artifact chain names instantiation. These are different axes: L1 is not the metalevel above L2, and L1–L4 are not automatically equated to metalevels such as M0–M3 of other formalisms.

   An artifact may be a set of files and may have several representations of the same content, such as JSON, Markdown, and TeX; file count, serialization format, and number of models are not the same thing. Physical artifacts may combine or split responsibilities if each layer's responsibility, its model, and its case links remain identifiable and traceable. An abbreviated phrase such as "an L3 artifact" means an artifact of a model associated with L3; it does not make the artifact a direct instance of the layer metamodel, and it may only be used after this distinction is clear in context.

   ADMV contains two required, distinct components: ADPM for program modeling and ADVS for verification specification. They may be prepared in parallel from UCS but do not constitute separate layers; `adpm` and `advs` folders or sections are internal organization of the single L2.

   For a fixed edition and versions, $A(M) = \{a \mid a \models M\}$ denotes the artifacts satisfying model $M$, and $\mathcal{M}_i = \{M \mid M \models L_i\}$ denotes the models satisfying layer $L_i$. The [notation guide](#mathematical-notation) explains these symbols. Client needs are not an OAL layer; when used as a derivation source, they belong to a declared external needs model.

2. **Accountable derivations.** A derivation consumes versioned sources and produces a versioned destination. Three records are distinct and do not replace one another: the provenance of the involved models (edition, identity, version), the construction of a transformer between selected models, and the execution of that transformer on concrete artifacts. For Needs-to-L1, L1-to-L2, L2-to-L3, and L3-to-L4 derivations, record source and destination baselines, a named accountable person, scope, and added decisions. The L1-to-L2 destination is a single ADMV containing both ADPM and ADVS, even if different people prepare them in parallel; there are no two parallel canonical L2 derivations. A Needs-to-L1 derivation names the external needs model consumed ($M_{\mathrm{Needs}}$) and the destination L1 model ($M_1$); needs reconstructed from an existing UCS remain identified as reconstructed and are not presented as independent stakeholder evidence. UCS may be consulted as an additional source when deriving ADI or ADIB; when used, record its baseline and the decisions it informed through explicit, versioned references that are part of the fixed inputs or contract. One person may own several derivations; a job title or tool alone does not identify the accountable person. A manual derivation records the same provenance, scope, added decisions, and applicable preservation obligations. Recording it does not, by itself, claim that a transformer was constructed or executed; a transformer claim additionally satisfies rule 7.

3. **Case identity and behavioral test.** Within a declared scope, each UCS use case has exactly one corresponding ADPM case identity and one directly linked ADVS behavioral test inside L2, plus one case identity in ADI. There are no extra ADPM or ADI cases or directly linked ADVS behavioral tests. The behavioral test is unique for its UCS case. It may comprise several scenarios and consume supporting subtests for criteria, alternatives, permissions, or other checks; subtests are not directly linked to a UCS case and are not behavioral tests by this definition. The one-test-per-case cardinality is not converted into one behavioral test per function, nor does it require a single physical test function per case. Channel-only checks may be recorded separately without becoming new use cases. ADIB interface elements and ADI cases may map many to many; this mapping does not create a new case identity.

4. **Changes and claims.** A change to a source contract, permission, or interface decision requires analysis of the impact on the affected models, constructed transformers, and derived artifacts and verification scenarios: which model changed, which transformers must be rebuilt or revalidated, and which artifacts must be rederived or rechecked. Version and conformance claims name the baselines, interface scope, and evidence actually compared.

5. **Distinct people and actors.** An actor is an interaction role declared in the specification, played by a person or system when requesting a use case. A caller is the concrete person or system on whose behalf the request occurs. Each request is associated with an actor context resolved according to the applicable contract. That context represents the relevant roles and, when required, the caller identity and authentication information. The model defines how the context is represented and resolved, including its origin and trust assumptions; OAL does not prescribe a class, fixed fields, or a technological mechanism. Authentication verifies a claimed identity when required by the contract; authorization determines whether a case may execute under the presented conditions. Anonymous and system actors are explicit modeling choices. Neither a missing or unresolved context nor a failed resolution establishes anonymous participation.

   A derivation owner is the named person who produces or approves an artifact transition. The responsibilities of defining a model, constructing a transformer, and executing a derivation are distinguishable and may belong to different people or to the same person. The roles of specifier, program modeler, verification designer, implementer, and interaction designer describe work, not mandatory job titles; none is automatically a runtime actor. This edition creates no mandatory positions.

6. **Layer names and conformance claims.** UCS is L1; ADMV is L2; ADI is L3; ADIB is L4. ADPM and ADVS are required components of ADMV, not layer names. Conformance claims distinguish four things:

   - **(a)** **Model conformance:** a model $M$ satisfies the metamodel of a determined layer $L_i$ for a declared scope. This says nothing about other layers.
   - **(b)** **Artifact conformance:** an artifact $a$ satisfies its selected model $M$ for a declared scope.
   - **(c)** **Layer coverage:** a declared set of models and artifacts covers a named set of layers. Coverage of one layer does not authorize inferring coverage of another.
   - **(d)** **Complete layer coverage:** coverage of all four OAL layers — L1, L2, L3, and L4. When L2 is in scope, ADPM and ADVS remain required.

   Any claim identifies this edition, the layer or layers, the claimed object (model, artifact, transformer construction, transformer execution, or composition of transformers), its scope, and the artifacts or evidence that support it. A claim of L2 coverage includes both ADPM and ADVS and keeps their respective responsibilities identifiable; a partial component claim is not a claim of L2 coverage. The phrase "complete model" is used only when the model, its version, and the meaning of completeness are unequivocal; otherwise the claim names its scope. "Unspecified", "not evaluated", "not demonstrated", and "inconclusive" are distinguished from each other and from "nonconforming"; none of them is an approval.

7. **Derivation engines.** An Engine LX-LY is a metamodel that specifies the construction of a deterministic logic from a selected source model to a selected destination model, and the execution of that logic on artifacts.

   **Construction and execution.** For a source model $M_n \models L_n$ and a destination model $M_{n+1} \models L_{n+1}$: construction $\mathrm{Build}_E(M_n, M_{n+1})$ yields a transformer $T[M_n, M_{n+1}]$ or a construction failure; execution $T[M_n, M_{n+1}]\,(a)$ yields $b$, where $a \in A(M_n)$ and $b \in A(M_{n+1})$; $a$ and $b$ instantiate the selected source and destination models, respectively. $\mathrm{Build}$ is an explanatory notation for the operation foreseen by the engine metamodel; it does not require an executable factory, another mandatory metalevel, or a separate service. The canonical names are Engine Needs-L1, Engine L1-L2, Engine L2-L3, and Engine L3-L4.

   **Declared contract.** A claimed engine implementation must define, in verifiable form:

   - **(a)** identity, version, and edition of the source and destination models;
   - **(b)** compatibility and capabilities required of the model pair;
   - **(c)** the separation between construction of $T$ and its execution;
   - **(d)** the mapping, representation, technology, and policy decisions resolved and frozen at construction, or incorporated into the models;
   - **(e)** the supported domain $D_T$, input preconditions, and artifact validity criteria;
   - **(f)** the guarantee that a successful output satisfies the selected destination model, not merely some model of the same layer;
   - **(g)** preservation obligations — identities, contracts, criteria, permissions, and other applicable relations — expressed as a relation $P_T \subseteq A(M_n) \times A(M_{n+1})$ such that $(a, T(a)) \in P_T$ for every $a$ in $D_T$;
   - **(h)** the meaning of determinism and the output equality criterion (bytes, canonical structure, or strictly delimited semantic equivalence), so that for the same models and versions, transformer and version, fixed configuration, and valid input, time, randomness, environment, and external queries do not silently change the result, and operational metadata outside the compared artifact is explicitly separated; when determinism is defined by an equivalence relation $\equiv$ on the destination, differences ignored by $\equiv$ must not silently change the acceptance or result of a subsequent transformer — the next transformer must be compatible with $\equiv$ on the relevant domain, or consume a canonical form that it explicitly fixes;
   - **(i)** failures, coverage limits, termination, and the result of the verifications;
   - **(j)** traceability of the construction and of the executions effectively recorded.

   **Supported domain and coverage.** For every input in $D_T$ that satisfies the declared preconditions and operational conditions, $T$ must terminate with a valid artifact of the destination model and preserve the announced obligations; $D_T$ may not be retrospectively reduced to exclude an input because its execution failed. A transformer with partial coverage declares $D_T$ as a subset of the valid source artifacts; one that declares itself complete covers the whole announced set.

   **Construction choices.** Determinism of $T$ does not imply a single possible construction from the model pair: constructions with different frozen choices produce distinct transformers, and not every arbitrary pair of models admits a complete or automatic transformation. A function that always returns the same error is deterministic but does not fulfill the obligation to produce a valid destination in the supported domain.

   **Failure categories.** Failures distinguish invalid input, valid unsupported input, incompatible model pair, operational failure, and invalid output; an inconclusive state is not presented as approval.

   **Preservation and evidence.** Output validity and preservation are distinct obligations: an artifact may satisfy the destination schema and still lose a relation that had to be preserved. Finite tests support the executed cases; they do not prove universal correctness of $T$. Humans and AI may take part in constructing deterministic rules; a free interpretation or a variable service consulted at each execution is not, by itself, a deterministic transformation.

   **Named transitions and additional sources.** Engine Needs-L1 consumes artifacts of a declared external needs model; Engine L1-L2 produces a complete ADMV from one L1 model, and its components' work may proceed in parallel without creating separate layer engines; Engines L2-L3 and L3-L4 may consult UCS as an additional versioned source, which does not change either engine's name, and any additional L1 consultation during execution uses explicit, versioned references that are part of the inputs or the fixed contract, never a free consultation of a mutable UCS as a hidden dependency of $T(a)$.

   **Interaction decisions.** Channel and representation choices in L3-to-L4 belong to the destination model or to the decisions frozen at construction; the engine does not invent preferences or new domain requirements. Production does not imply literal translation or structural equivalence: L4 defines an interaction boundary around L3 callable cases, rather than a translated copy of L3.

   **Claims and realization.** A claimed implementation of an OAL engine identifies its edition, named transition, accepted inputs, produced outputs, preserved links, added decisions, and validation scope; its use in a project still records the accountable person and baselines required by rule 2. An engine may be realized by a human process, software, or both. The determinism of an engine does not require the determinism of every execution of the applications it helps produce.

8. **Conversion, translation, derivation, and realization substitution.** Four operations are distinct and have different obligations:

   - **(a)** **Conversion between representations of one model.** Valid documents of a model may use several representations, such as JSON, Markdown, or TeX. A conversion $C_{rs}$ maps valid documents in representation $r$ to documents in representation $s$ of the same model $M$. For every document $x$ in the declared domain, $\mathrm{decode}_s(C_{rs}(x)) \equiv_M \mathrm{decode}_r(x)$, where $\mathrm{decode}$ recovers the model content and $\equiv_M$ is the declared equivalence of that content. A round-trip claim also states the equivalence criterion for the return. Byte identity and editorial conventions outside the model are neither required nor evidence of content preservation.
   - **(b)** **Translation between distinct models of the same layer.** Models $M, N \in \mathcal{M}_i$ share the layer's defining responsibilities, but membership in the same layer does not imply a total, invertible, or lossless translation. A translation requires an explicit mapping, a declared domain, and the obligations it preserves. Information or behavior outside the mapping is lost or changed and is recorded. A shared layer label does not presume a universal translator.
   - **(c)** **Derivation between layers.** A derivation produces artifacts of the selected destination model, preserves the applicable source identities, contracts, criteria, and permissions, and may add decisions that belong to the destination responsibility. It records provenance and decisions under rule 2. A manual derivation can be documented without claiming a constructed or executed transformer. A claim of engine realization, transformer construction, or transformer execution additionally meets rule 7. Derivation correctness does not require a structural copy of the source.
   - **(d)** **Translation or substitution between realizations of the same named engine.** This is subject to the selected source and destination models, the declared domains, and the guarantees of those realizations. It preserves the required inputs, destination responsibility, case links, and derivation obligations while recording implementation-specific losses and decisions.

   Documenting a loss honestly does not satisfy a contract that requires preserving the lost information. A transformation with losses can be described accurately and still be insufficient for a stronger preservation or conformance claim.

9. **Combined models, engines, transformers, and compositions.** One specialization may implement responsibilities of neighboring layers connected by a named derivation. Three objects are distinct: a combined model or package that gathers artifacts of several layers, a transformer constructed according to an engine metamodel for a selected pair of models, and a composition of transformers. A combined model or the coexistence of artifacts does not, by itself, demonstrate an engine, a transformer, or a transformation.

   Covering both layers does not automatically construct the transformer for the transition between them; if the specialization needs to perform that transition internally, it may construct a transformer according to the corresponding engine metamodel, which then keeps its source, destination, and transition identifiable and verifiable. This is optional, including when both layers are informational, as with L1 and L2. A specialization may likewise combine L3 and L4 and, when needed, construct and execute Engine L3-L4's transformer internally. Any combined implementation claiming L2 coverage includes both ADPM and ADVS, including when L2 is packaged with L1 or L3.

   A composition of transformers, such as an L1-to-L3 transformer defined by $T_{13}(a) = T_{23}(T_{12}(a))$, is a new claimed object. Its declared domain must satisfy $D_{13} \subseteq \{a \in D_{12} \mid T_{12}(a) \in D_{23}\}$, and the equality holds on that domain.

   Sharing the same intermediate model, including its version, is not sufficient to guarantee composition over the whole source domain: $T_{12}$ may produce artifacts inside $A(M_2)$ but outside $D_{23}$, and two outputs equivalent under the determinism criterion of $T_{12}$ may lead $T_{23}$ to a different acceptance or result. A composition therefore requires a compatible intermediate model and version, declared domains, compatibility between the equivalence used for $T_{12}$ and the input expectations of $T_{23}$ (or a canonical form consumed by $T_{23}$), failure handling, and preservation of traces. This edition establishes no canonical non-adjacent engine.

<a id="ucs"></a>
## UCS (L1) — Use Case Specification

A model conforming to L1 must establish the subjects below for its artifacts; the artifacts that instantiate such a model must satisfy them for the declared scope. L1 does not require JSON, one notation, or a single universal schema: semantic prose and structured representations are equally valid when the subjects remain recoverable.

1. **Scope.** The model must define how its artifacts state objectives, system boundaries, relevant actors, and external participants without prescribing code organization.

2. **Use cases.** The model must give each case a stable identifier, main objective, initiating actor, set of permitted actors, and applicable authorization conditions. It states which actor-context information is required and when authentication is required. Public or system participation is declared explicitly. Actors outside the permitted set and contexts absent, unresolved, or insufficient for the contract cannot execute the case; missing context must not be interpreted as anonymous access.

3. **Behavioral contracts.** The model must state triggers, inputs, context, assumptions, checked conditions, results, effects, guarantees, alternatives, and failures, including the observable result of denied access. L1 may record interaction restrictions imposed from outside the solution, with their origin identified. Decisions of interaction introduced by the solution — routes, screens, payload encodings, protocols, representations — belong to L4; a reference made in L1 to such a decision does not turn it into an external requirement. An external restriction does not change responsibility merely because it mentions a protocol, representation, route, or interface. When an interaction decision reveals a new domain need, revise UCS and the affected derivations.

4. **Entities and rules.** The model must define the meaning, data, relationships, and validity conditions of entities, state other domain rules explicitly, and link them to the use cases responsible for applying them.

5. **Composition and dependencies.** The model must identify dependencies between use cases and the capabilities required from resources and external systems, making the conditions, information, and results involved explicit without determining calling, access, or integration mechanisms.

6. **Complementary obligations.** The model must make applicable requirements for persistence, security and isolation, observability, performance, accessibility, and other relevant constraints explicit. Each obligation has a defined scope, an identified origin, and verifiable conditions; channel-specific choices belong to ADIB.

7. **Acceptance and links.** The model must give each case acceptance criteria and links to relevant needs, actors, entities, rules, and dependencies. Case identity is preserved in ADPM and ADI; ADVS links criteria to scenarios; ADIB links exposed interactions to the cases they invoke. When a model declares shared integration criteria, it identifies their scope, affected cases, and single authoritative definition through explicit references.

8. **Consistency and evolution.** Shared information has a single definition and explicit references. Changes preserve identity and history. The model must keep distinguishable, in its artifacts, observed facts, desired requirements, inferences, premises, and pending issues; not every statement of a specification is a proven fact.

9. **Domains — recommendation.** Organization into domains with delimited responsibilities is optional but strongly recommended. When adopted, it identifies the use cases and entities associated with each domain.

10. **Representative examples.** Examples can clarify contracts but do not replace explicit rules or ADVS scenarios.

<a id="admv"></a>
## ADMV (L2) — Analysis-Driven Modeling and Verification

ADMV is the single L2 layer. It gathers the program model (ADPM) and the verification specification (ADVS): an integrated model of program and verification for a project. The components remain distinguishable and may be prepared in parallel, but neither alone completes L2, and there is a single L1-to-L2 derivation. Folders or sections named `adpm` and `advs` are internal organization of the unified L2. A model conforming to L2 must establish the subjects of both components; its artifacts must satisfy them.

<a id="adpm"></a>
### ADPM — Analysis-Driven Program Model

Within the L2 model, the ADPM component must establish the subjects below; the artifacts that instantiate the model must satisfy them for the declared scope.

1. **Separation and preservation of responsibilities.** The model must distinguish use cases, tools, and entities and require their responsibilities and relationships to be identifiable and mapped in the selected L3 code organization. It does not choose a concrete code organization or file structure. The distinctions and mapping remain identifiable in ADI and, consequently, in ADIB. Domains are optional; when modeled, their boundaries and mapping must likewise be preserved.

2. **Use cases.** Each use case fulfills an identifiable objective and contains the domain decisions and rules necessary for it, except for the validation and behavior the model explicitly delegates to entities. How behavior is distributed between cases and entities is a choice of the model, not a universal prescription. A case does not determine technological mechanisms. It may use other use cases while respecting their contracts and supplying the pertinent actor context through the declared dependency. The called case applies its own authorization policy. Delegation or acting on behalf of another participant requires an explicit rule; an internal call alone grants no additional permission. The permission to execute the case is decided by the case itself, before any prohibited effect.

3. **Entities.** Entities represent data and relationships and do not depend on use cases or tools. The model may define predominantly data entities — whose operations are reading, assigning values, and validating data during assignment — or entities with domain behavior, distributing behavior between entities and use cases. In either case, the model must make each entity's contracts, invariants, and dependencies explicit, and the rules an entity enforces must be identifiable rule by rule. Entities do not absorb case responsibilities that the model assigned to cases.

4. **Tools, contracts, and validation location.** The model must state tool operations, results, effects, and guarantees separately from mechanisms. Cases depend on contracts; tools do not invent domain rules. Domain validity required by an entity or a case is implemented in that entity or in the consuming case, and responsibility for each rule is identifiable.

   Each entity $e$ defines its internal coherence conditions $I_E$, and $V_E = \{e \mid I_E(e)\}$. A tool operation that receives a ready entity receives $e \in V_E$ by contract and must not re-execute $I_E$, call a redundant validation, or implement a semantically equivalent copy of that check. Generating the same condition automatically elsewhere does not make its duplication permitted; renaming the operation or calling it a "technical guarantee" does not authorize repeating the entity's internal validation.

   A tool may evaluate distinct conditions $Q_t(e, c)$ that depend on its own contract and context — for example expected version, concurrency conflict, atomic global uniqueness, existence of a persisted resource, or availability of an external service — provided the condition, its object, its purpose, and its responsibility are identifiable. Evaluating a distinct condition does not transfer case authorization or domain decisions to the tool.

   Raw records used in hydration are not ready entities; constructing an entity from them still uses the entity's canonical construction and validation.

   Codecs and adapters may verify aspects of the representation of raw data, but they do not gain a parallel implementation of entity validity.

   Validation in the entity does not replace atomic guarantees required by the persistence contract with pre-queries subject to concurrency.

   JSON, encoding, body format, and channel parameters belong to the L4 boundary; the technical form of a record, its serialization and deserialization, belong to a codec or adapter under a representation contract.

   Validation helpers used by entities and cases may centralize rules; they are not moved into tools and do not evolve as duplicated conditions. A user interface may offer error prevention, but authoritative validation also works through a direct call to the core. Collaborating program tools are distinct from verification instruments of schemas, models, and traceability of OAL itself, which this rule does not restrict.

5. **Dependencies and composition.** The model must show what each case and tool receives, where implementations are selected, and how collaborators are composed. It does not hide required dependencies behind global lookup.

6. **Persistence.** Persistence is accessed through tools. Data responsibilities and the conditions for reading and changing data must be explicit, regardless of whether storage is shared.

7. **Authorization boundary.** The model must state an explicit input for the actor context resolved according to the contract and a deny-by-default authorization decision for every case. The case rejects missing, unresolved, unknown, or insufficient contexts. It requires authenticated identity when the contract requires it and admits an anonymous context only when expressly permitted. The decision precedes domain effects and remains effective both in direct calls and beyond user-interface controls.

8. **Faithful representation.** Semantic prose or structured pseudocode may express ADPM. Either form must make responsibilities, contracts, dependency wiring, authorization, validation locations, and algorithms recoverable.

9. **Domains — recommendation.** Grouping model responsibilities by domain is recommended when it clarifies boundaries.

10. **Lifetime.** The model must state component lifetime where it matters. One case instance per application scope may be chosen but is not required.

<a id="advs"></a>
### ADVS — Analysis-Driven Verification Specification

Within the L2 model, the ADVS component must establish the subjects below; the artifacts that instantiate the model must satisfy them for the declared scope. ADVS need not be a separate file or package from ADPM.

1. **UCS derivation and behavioral test.** Define exactly one behavioral test directly linked to each UCS use case in the declared scope, preserving its case identity. Identify the UCS baseline, contracts, and acceptance criteria it covers. A behavioral test may comprise several scenarios and consume supporting subtests — for permissions, alternatives, failures, and criteria — without creating additional behavioral tests for that case. Physical files may combine several tests if the one-to-one case mapping remains explicit.

2. **Test and subtest contracts.** For the behavioral test and each supporting scenario or subtest, state preparation and preconditions, actor context for case scenarios, action, oracle (expected result and effects), and observed boundary or configuration. A case scenario may deliberately supply a missing or unresolved context to verify denial. Supporting checks of entities or tools may state that actor context is not applicable. The behavioral test may exercise a case directly or through an ADIB channel; its subtests support that test without having a direct UCS case link.

3. **Permissions.** Cover allowed and denied access for each distinct case permission, including missing, unknown, and insufficient contexts and explicitly anonymous participation when applicable to the contract. Verify denial before domain or persistence effects.

4. **Failures and limits.** Cover specified alternatives, failures, and consequential boundaries. When ADIB selects a channel, add scenarios for its own interaction contract, such as parsing, representation, authentication, and accessibility where applicable; name risks outside the selected scenarios.

5. **Trace and status.** Link each case-specific UCS acceptance criterion to its case’s behavioral test and the supporting checks that cover it. Link explicitly declared shared integration criteria to the behavioral tests of the affected cases and their shared supporting checks, without creating additional directly linked behavioral tests. Link claimed ADIB-specific obligations to their planned checks.

   Tool and entity checks are recommended but are not required as separate ADVS specifications; their contract guarantees and validity rules still require the checks needed to support a conformance claim.

   Keep three objects distinct: the planned verification, the test code, and the observed result of an execution. The presence of a test file does not demonstrate that it was executed, and passing results support only observed configurations. ADIB decisions may therefore cause ADVS to be revised.

<a id="adi"></a>
## ADI (L3) — Analysis-Driven Implementation

An L3 model is a reusable code organization. It defines how responsibilities, dependencies, callable cases, and verification are organized in code, and the criteria by which its concrete artifacts are recognized. An architecture may be one choice within such a model. The model does not need to have executed the tests of every future project that will instantiate it. Its artifacts are concrete code organized according to that model.

1. **Materialization of L2 roles and dependencies.** The code-organization model must define how the ADPM roles — cases, entities, tools, and modeled domains — and their dependencies are materialized in code, and how case identities, algorithms, and error paths become a callable application core. Artifacts must preserve the ADPM distinction and mapping in the selected code organization; physical packaging may differ. Deviations and affected source artifacts are recorded. External channel mechanisms are specified in ADIB.

2. **Authorization.** The code-organization model must define how an actor context is received through an explicit, declared invocation path and how the case applies its authorization policy before domain effects. The context’s origin and trust assumptions remain identifiable. Missing, unresolved, unknown, unpermitted, or otherwise insufficient contexts are denied in direct calls and through ADIB. An explicitly permitted anonymous context is distinct from absent context. ADIB or the declared direct-call mechanism supplies the context; the case evaluates its own policy.

3. **Verification integration.** The code-organization model must define how the behavioral tests and supporting checks derived from ADVS are integrated and executed against the core, retaining case, criterion, and subtest links. Artifacts report failed and unexecuted checks; ADIB-specific checks are also executed against the selected channel.

4. **Composition and collaborator selection.** The code-organization model must define where implementations are selected and how collaborators are composed and supplied through explicit dependencies. Concrete tools meet ADPM contracts in the claimed configuration, including relevant persistence, isolation, and failure guarantees.

5. **Evolution, traceability, and evidence.** The code-organization model must define how changes propagate and remain traceable to their L2 sources. Artifacts state implementation version, environment, executed scenarios, results, and limits, and do not present planned or configured checks as completed runs.

<a id="adib"></a>
## ADIB (L4) — Analysis-Driven Interaction Boundary

A model conforming to L4 must establish the interaction subjects below; the artifacts that instantiate it must satisfy them for the declared scope.

1. **Interaction scope.** Declare the supported interaction channels, the actors or external systems they serve, and their capabilities. A channel may be a page, programmatic endpoint, command line, message consumer, or another input/output form. State which use cases are exposed in the claimed scope.

2. **Stimuli and responses.** Specify how each channel receives and parses a stimulus, checks its representation, invokes ADI cases, and presents results and failures. A response may be immediate, deferred, or emitted as an event; the observable contract must be explicit.

3. **Actor context at the boundary.** Resolve the actor context through the declared channel mechanism and pass it to ADI. Authenticate the caller when required by the case and channel contracts. The model states the context’s origin and trust assumptions; a caller-supplied role label alone does not establish a trusted context. Public access may resolve an explicitly permitted anonymous context. Missing or failed resolution must not silently become anonymous access. ADI still applies the case authorization policy. Hiding an interface control or checking a route alone does not authorize the case.

4. **Many-to-many mapping.** Record the mapping between interface elements and the ADI case identities they invoke in both directions; either side may have multiple links. Identify interface-only elements and their purpose separately.

5. **Boundary of decisions.** Keep transport, presentation, session, and representation decisions in ADIB. Preserve the ADPM/ADI distinction between cases, tools, entities, and modeled domains across this boundary: ADIB invokes cases rather than absorbing their responsibilities. ADIB may coordinate already specified cases but does not make new domain decisions or access domain-persistence tools directly.

   It may use storage exclusively for technical channel state, such as sessions or request correlation, under an explicit contract that identifies the data, access conditions, lifetime, and failure behavior. This storage must not introduce business-data rules, bypass cases to read or change domain state, or replace case authorization.

   Interface coordination that introduces a new transaction, decision, or domain objective requires specifying it as a case responsibility, revising UCS and its derivations; a new business rule is not placed in an endpoint or interface script only to avoid revising L1 or L2. Case algorithms and authorization remain in ADI.

6. **Channel contract.** Document the selected channel's routes or views, commands or events, representations, errors, and relevant accessibility, localization, and operational obligations. Requirements imposed externally are inherited with their origin identified; decisions introduced by the boundary are recorded as L4 decisions. When UCS is consulted, distinguish requirements inherited from it from decisions introduced in ADIB; otherwise identify the sources of channel obligations. Make each claimed obligation verifiable.

7. **Interaction verification.** Review ADVS when ADIB decisions add observable obligations; link those obligations and exposed UCS criteria to interface scenarios. Record executed results and limits for each claimed channel without treating a working core or a planned scenario as proof of the interface.

## Interpretation

The English text is the source of this edition; the Portuguese text is its translation. Only numbered requirements define conformance. Recommendations are marked. The guide below is informative and does not add requirements; the normative content on engines and conformance is in the numbered rules above.

## Guide to this edition

This guide explains the numbered rules without adding requirements.

### Concepts

<a id="mathematical-notation"></a>

In OAL, analysis means writing down needs, rules, decisions, assumptions, and consequences so another person can check them. The rules are open to different documents, languages, frameworks, and tools. A repository can combine artifacts if readers can still find each layer's responsibility.

Each layer defines a metamodel; a reusable model conforms to the layer; concrete project artifacts instantiate the model:

| Symbol | Meaning |
| --- | --- |
| $L_i$ | Metamodel defined by layer $i$. |
| $M_i$ | Selected reusable model associated with $L_i$. |
| $a$, $b$ | Concrete project artifacts, which may consist of several files. |
| $\models$ | “Satisfies the requirements of”, under the OAL conformance rules. |
| $\mathcal{M}_i$ | Class of reusable models satisfying $L_i$. |
| $A(M)$ | Class of artifacts satisfying the selected model $M$. |
| $\in$ | Membership in the indicated class or set. |
| $\iff$ | “If and only if”: the two statements are equivalent. |

The model and artifact relations are:

$$
M_i \models L_i,
\qquad
a \models M_i.
$$

An artifact's membership in the class of conforming artifacts is written as:

$$
a \in A(M_i) \iff a \models M_i.
$$

Read this as: “$a$ is an artifact satisfying $M_i$ if and only if $a$ satisfies that model's requirements.” The membership is in $A(M_i)$, the class of artifacts; model conformance and artifact conformance remain separate claims.

The table below illustrates the categories; it does not attribute generic models to the examples in this repository:

| Layer | Instance of the layer (reusable model) | Instance of that model (project artifact) |
| --- | --- | --- |
| L1 | Generic model for specifying projects | Specification of a concrete project |
| L2 | Integrated generic model of program and verification | Program modeling and verification plan of a project |
| L3 | Reusable code organization | Concrete code organized under that model |
| L4 | Reusable model of interaction and channel adaptation | Concrete interfaces and adapters of a project |

For a fixed edition, model versions, and declared scope, the classes are defined by:

$$
\mathcal{M}_i = \{M \mid M \models L_i\},
\qquad
A(M) = \{a \mid a \models M\}.
$$

The symbol $\mid$ reads “such that”. The symbol $\models$ denotes the OAL conformance relation defined by the numbered rules. The notation records the intended relation among layer, model, and artifact; it does not, by itself, prove a conformance claim. Every claim also states its scope and the evidence reviewed.

The Markdown uses inline LaTeX with `$...$` and displayed formulas with `$$...$$`, as supported by [GitHub's mathematical-expression rendering](https://docs.github.com/en/get-started/writing-on-github/working-with-advanced-formatting/writing-mathematical-expressions). The formulas summarize the existing requirements; the prose supplies their meaning and conditions.

UCS describes behavior, actors, permissions, data meanings, outcomes, and acceptance criteria. It may record externally imposed interaction restrictions with their origin; interaction choices introduced by the solution belong to ADIB. ADMV is L2: its ADPM component defines the program model — case responsibilities, entities, tools and their contracts, dependency composition, permissions, validation locations, and algorithms — while ADVS defines one behavioral test for each UCS case. ADI realizes the callable application core and records observed core results. ADIB defines and realizes channels that accept stimuli, call ADI cases, and present immediate, deferred, or event responses. These responsibilities do not impose a construction order. A channel decision may require an ADVS update or reveal a behavioral requirement that belongs in UCS.

The location of validation follows the same division of responsibilities:

| Situation | Responsible |
| --- | --- |
| Required field, domain limit, admissible transition | Entity or consuming case |
| Permission to execute the case | Case, before prohibited effects |
| JSON, encoding, body format, channel parameters | L4 boundary |
| Technical form of a record, serialization, deserialization | Codec or adapter under the representation contract |
| Entity construction during hydration | The entity still executes its canonical validation |
| Atomic uniqueness, transactions, persistent references, version-conditioned writes | Technical guarantee of persistence, with domain meaning and response defined in the core |

A technical storage guarantee does not transfer the definition of domain validity to the tool or to SQL, and validation in the core does not replace the atomic guarantees with pre-queries that create a concurrency race.

The table separates three questions that are easy to conflate. Internal coherence $I_E$ belongs to the entity: $V_E = \{e \mid I_E(e)\}$, and a tool that receives a ready entity receives $e \in V_E$ by contract. A forbidden repetition is a tool that calls the entity's validation or reimplements the same length, format, or transition condition under another name, including when the condition is generated automatically or presented as a technical guarantee. A permitted distinct check is a contextual condition $Q_t(e, c)$ from the tool's own contract — an expected version, a concurrency conflict, atomic global uniqueness, or availability of an external resource, for example. Such a condition has its own object, purpose, and responsibility and does not decide domain validity or case authorization. A third question is the technical form of a raw record: a codec may reject malformed serialized data, but when it constructs an entity it uses the entity's canonical construction and validation. Validation in the entity does not replace the atomic guarantees of persistence with pre-queries that create a concurrency race.

An L1 contract may inherit an interaction restriction imposed from outside, for example "the customer's gateway accepts only JSON over HTTPS", citing the external contract as its origin. A route invented by the implementation, for example `POST /api/board`, is an L4 decision even when L1 records the underlying outcome. Naming a protocol or a route in L1 does not transfer ownership of the decision; recording an L4 decision in L1 does not turn it into an external requirement. If a channel decision reveals a new domain need, UCS and the affected derivations are revised.

Client needs are not a layer. A Needs-to-L1 derivation consumes artifacts of a declared external needs model ($M_{\mathrm{Needs}}$) and produces artifacts of an L1 model ($M_1$). Needs reconstructed from an existing UCS keep that provenance visible.

An actor is a specified interaction role; the caller is the person or system playing that role. The actor context carries the information required by the contract and has a declared resolution path. Authentication is required when the contract requires it, while the case always evaluates its authorization policy. For example, a model may admit an authenticated human role, a system role resolved for a scheduled process, or an explicitly anonymous role for a public operation. A missing context is not an anonymous context, and a call through another case does not itself grant permission. A simple model may represent the context by a role identifier when it declares the origin, meaning, and trust assumptions of that identifier.

A derivation owner is the named person accountable for producing or approving an artifact from its source baseline. The work roles are specifier (needs to UCS), program modeler (ADPM within L2), verification designer (ADVS within L2 and later channel scenarios), implementer (complete L2 to ADI), and interaction designer (ADI to ADIB, optionally consulting UCS). One person may hold several roles. A derivation record names the actual person, source and destination baselines, scope, and added decisions.

The layer names are L1 for UCS, L2 for ADMV, L3 for ADI, and L4 for ADIB. Within L2, ADPM and ADVS may be prepared in parallel from L1; they remain distinct components of one layer. Each UCS case has one corresponding ADPM case model, one directly linked ADVS behavioral test, and one implemented ADI case. A behavioral test may consume several supporting subtests; those subtests are not themselves behavioral tests. Interface elements and implemented cases map many to many. Navigation, static content, and other interface-only elements are identified separately. The ADPM distinctions among cases, tools, entities, and any modeled domains stay traceable in ADI and across the ADIB boundary, even if their physical packaging differs.

An engine is a metamodel, not merely a process that receives one document and produces another. Construction and execution are different moments:

For a transition between adjacent OAL layers, the selected models satisfy their respective layer metamodels:

$$
M_n \models L_n,
\qquad
M_{n+1} \models L_{n+1}.
$$

**Construction.** A successful construction according to engine $E$ is written as:

$$
\mathrm{Build}_E(M_n, M_{n+1})
\longrightarrow T[M_n, M_{n+1}].
$$

The arrow records one construction with its fixed choices. Other choices may produce a different transformer, and construction may fail. $\mathrm{Build}$ names the construction operation specified by the engine; it does not prescribe an executable factory.

**Execution.** Let $T = T[M_n, M_{n+1}]$ be that constructed transformer. Under its declared preconditions and operational conditions:

$$
T(a) = b,
\qquad
a \in D_T \subseteq A(M_n),
\qquad
b \in A(M_{n+1}).
$$

Here $D_T$ is the supported input domain, $a$ is the source artifact, and $b$ is the produced artifact. The output satisfies the selected destination model: $b \models M_{n+1}$. Valid source artifacts outside $D_T$ remain outside the coverage claim. The notation describes successful execution; the declared failure categories still apply.

The transformer $T$ is specialized for that pair of models and must satisfy the engine contract as specialized. Construction freezes mapping, representation, technology, and policy decisions; execution applies $T$ to a valid input of the supported domain and must terminate with an artifact that satisfies the selected destination model and preserves the announced obligations. Engine Needs-L1 consumes a declared external needs model; Engine L1-L2 produces ADMV with both ADPM and ADVS; Engine L2-L3 uses both L2 components and may consult UCS; Engine L3-L4 uses callable ADI cases to produce interaction channels and may also consult UCS. L4 introduces presentation and transport decisions of its own. An engine implementation declares its edition, named transition, accepted inputs, outputs, preserved links, added decisions, and validation scope. Its use in a project still identifies the accountable person.

For selected models $M_1$, $M_2$, and $M_3$, the successful behavior can be written as:

$$
\begin{aligned}
T_{12}&\colon D_{12} \to A(M_2),
& D_{12} &\subseteq A(M_1),\\
T_{23}&\colon D_{23} \to A(M_3),
& D_{23} &\subseteq A(M_2).
\end{aligned}
$$

These signatures describe what is guaranteed inside the supported domain, under the declared preconditions and operational conditions; the failure categories remain separate. Preservation is a relation $P_T \subseteq A(M) \times A(N)$ with $(a, T(a)) \in P_T$ for every $a$ in $D_T$. Validity of the output and preservation are different obligations: an artifact can satisfy the destination model and still lose an identity, contract, criterion, permission, or relation that had to be preserved.

A composition $T_{13}(a) = T_{23}(T_{12}(a))$ is defined only on $D_{13} \subseteq \{a \in D_{12} \mid T_{12}(a) \in D_{23}\}$. Sharing the same intermediate model and version is not sufficient: $T_{12}$ may produce a valid $M_2$ artifact outside $D_{23}$, and two outputs equivalent under $T_{12}$'s determinism criterion may lead $T_{23}$ to a different acceptance or result. The composition therefore requires compatibility between that equivalence and $T_{23}$'s input expectations, or a canonical form explicitly consumed by $T_{23}$. The guarantees announced for a composition are supported by the component guarantees only on its declared domain: $T_{12}$ must preserve what $T_{23}$ requires as input, and $T_{23}$ must preserve the announced destination obligations; neither component guarantee applies outside its own domain. Example: $M_2$ admits synchronous and asynchronous operations, but $T_{23}$ supports only synchronous ones. The output $T_{12}(a)$ may satisfy $M_2$ and still contain an asynchronous operation outside $T_{23}$'s supported domain, so $T_{12}(a) \notin D_{23}$; $D_{13}$ must exclude those inputs, or $T_{12}$ must be restricted or rebuilt so that its outputs stay inside $D_{23}$. Counterexample: assuming that every $M_2$-conforming output is acceptable to $T_{23}$ because both components are called deterministic or because the pair declares the same $M_2$ version.

Two models conforming to the same layer may admit different representations while preserving that layer’s defining contracts. Four operations remain distinct: converting representations of the same model, translating between distinct models of the same layer, deriving between layers, and substituting realizations of the same named engine.

For representations $r$ and $s$ of one model $M$, a lossless conversion of model content can be written as $\mathrm{decode}_s(C_{rs}(x)) \equiv_M \mathrm{decode}_r(x)$, with a declared domain for $C_{rs}$, a definition of the decoding functions, and a declared equivalence $\equiv_M$; round-trip claims also state the equivalence criterion for the return. A conversion is not a derivation, a shared layer is not a universal translator, and a documented loss does not satisfy a contract that requires preserving the lost information.

Examples: converting the Board CRM UCS JSON into its LaTeX renderings is a representation conversion of one model; translating two L1 models with different field names requires a mapping; deriving ADMV from UCS adds ADPM and ADVS decisions and is not a copy of the UCS.

For engine-realization substitution, consider two hypothetical transformers $T_{12}^{A}\colon D_A \to A(M_2)$ and $T_{12}^{B}\colon D_B \to A(M_2)$, with $D_A, D_B \subseteq A(M_1)$, for the same selected $M_1$ and $M_2$ versions. A substitution claim is limited to a declared use domain: on that domain both transformers must preserve the announced identities, contracts, criteria, and permissions and produce outputs equivalent under the declared criterion. Equal source and destination models alone are not sufficient, and if the domains differ the claim holds only on their shared domain. These transformers are conceptual examples; they are not implemented or executed.

Two stores that implement the same tool contract are a substitution of tool implementations in L3, not a realization of an OAL engine.

A combined implementation may cover neighboring responsibilities without constructing the transformer between them; it may construct that transformer internally when needed and make a separate claim when the transition is evidenced. A combined model or a package that merely gathers artifacts demonstrates coexistence, not transformation.

### The examples of this repository

The repository specifies four didactic reusable models, one per layer, under `examples/models/`: OAL-EX-M1-CASE-CONTRACTS (L1), OAL-EX-M2-PROGRAM-SCENARIOS (L2), OAL-EX-M3-PYTHON-CORE (L3), and OAL-EX-M4-HTTP-BOUNDARY (L4). Each model has its own identity, version 0.1.0, scope, constructions, validity conditions, template, filled example, counterexample, and stated limits. These are examples of models that declare conformance to this edition; specifying a model and assessing its conformance are not the same operation, and neither proves that every future artifact is correct.

The project packages declare four instances each — one per model — in `model-instances.json`: Tiny Catalog, Board CRM, and Work Board, twelve declarations in total. An instance declaration identifies the model, its version, the edition, the files and symbols that compose the artifact, the scope, the mappings, the evidence, and the limits. The declarations record the scope, mappings, evidence state, and limits. A structural review can check identities, references, and declared files; it does not certify semantic conformance.

The needs baselines were reconstructed from the UCS and remain identified as reconstructed; no external needs model is specified. The records do not demonstrate the construction or execution of deterministic transformers between models: the models were applied to adapt the existing projects manually, not produced by an engine chain. Four objects are evaluated separately: a model against the layer metamodel; an artifact against its selected model; a specialized transformer against the engine metamodel; and a concrete execution against its declared inputs, outputs, and guarantees.

<a id="versioning"></a>
### Versioning and derivation

**Alpha-v0.2.0-Alkimim** names the alpha stage, version number, and this edition's principal editor. It carries forward Alpha-v0.1.0-Alkimim except for the unification of L2 as ADMV; the layer/model/artifact framework and the conformance-coverage distinctions; the engine metamodel with separated construction and execution, composition domains, and the preservation relation; the removal of any needs layer in favor of a declared external needs model; the relaxed entity-behavior prescription combined with the prohibition of duplicating entity-internal validation in tools; the distinction among representation conversion, same-layer translation, layer derivation, and engine-realization substitution; the channel-origin rules; and the four didactic models with their twelve instance declarations. Authorship and credits are recorded separately; a later edition may have another editor. English is the source wording and Portuguese is its translation. Alpha-v0.1.0-Alkimim remains closed to normative changes, and its examples are preserved as history.

Project artifacts may have their own baseline versions. While this alpha edition is revised in place, the retained labels are accompanied by an identifiable content snapshot for each reported verification. A release label alone does not establish conformance or show that verification ran. Changes to contracts, permissions, or interaction decisions require review of affected derivations and scenarios, including the impact on models, transformers, and artifacts required by rule 4. A claim identifies the model, artifact, transformer construction, execution, or composition being assessed, together with its edition, scope, fixed source and destination baselines where applicable, and supporting evidence. A declaration of conformance for one object does not authorize inferring conformance of other objects or coverage of layers outside its declared scope.

<a id="verification"></a>
### Verification

ADVS records what to check before reporting a result. For each UCS case, its unique behavioral test keeps the direct case link and identifies the covered criteria, actor context, preparation and preconditions, action, oracle (expected result and effects), and relevant boundary or configuration. It may consume supporting subtests for allowed and denied actors, alternatives, and failures; these have no direct UCS case link. ADVS need not prescribe separate checks for every tool or entity, although such checks are recommended. Contract guarantees and entity validity still need enough evidence for the scope claimed. Planned verification, test code, and observed execution results are three distinct objects; a test file on disk does not prove that it ran.

ADI executes checks of the application core. When ADIB selects a channel, ADVS also records scenarios for that channel's parsing, representation, authentication, accessibility, and other claimed interaction obligations as applicable. ADIB execution evidence states which channels and configurations were exercised. Permission checks cover denial before domain or persistence effects. Planned scenarios and executed results remain distinct.

The examples contain unit checks for entities and pure tools, integration checks for tools using other resources, and case-oriented checks. The use of a substitute, SQLite, or HTTP does not by itself determine whether a check is behavioral: the direct one-to-one link to a UCS case does. From an example directory, `python -m pytest` runs its suite; any reported result describes that execution and environment.

<a id="conformance"></a>
### Conformance and scope

The numbered rules above define conformance. Four claims are distinct: model conformance to a determined layer; artifact conformance to its selected model; coverage of a declared set of layers; and complete layer coverage of L1, L2, L3, and L4. A model $M_1$ can fully conform to L1 without covering L4. When L2 is in scope, both ADPM and ADVS remain required. The phrase "complete model" is used only when the model, version, and meaning of completeness are unambiguous; otherwise the claim names its scope.

A claim states the edition, project baselines, the claimed object (model, artifact, transformer construction, transformer execution, or composition of transformers), the layers and cases in scope, named derivation owners, and the evidence actually reviewed. Model conformance and artifact conformance are separate claims with separate limits. A claim of all-layer coverage includes L1, L2, L3, and L4; a narrower claim names the responsibilities covered.

Review UCS for behavior and permitted actors; ADMV (L2) for both ADPM's case algorithms, contracts, dependency composition, validation locations, and permission decisions and ADVS's one behavioral test per UCS case, supporting subtests, and coverage; ADI for callable cases, enforcement, and observed core results; and ADIB for channel contracts, actor-context resolution, interaction decisions, and observed channel results.

Compare case identities across UCS, ADPM, ADVS behavioral tests, and ADI in both directions. Map each case-specific UCS acceptance criterion to its behavioral test and supporting checks; map declared shared integration criteria to the affected cases’ behavioral tests and shared checks. For each claimed ADIB channel, inspect the many-to-many map from interface elements to implemented cases in both directions, identify interface-only elements, and link channel obligations to checks. Counts alone cannot establish contract preservation. A planned check is not an executed result. The [Tiny Catalog review](examples/tiny-catalog/OAL-P3/CONFORMANCE.md) records a narrower assessment of that example's artifacts.

### Related work

OAL draws on use-case specification, traceability, dependency boundaries, and test derivation. The links here provide context rather than additional requirements. [Use-Case 2.0](https://www.ivarjacobson.com/publications/white-papers/use-case-20-e-book) describes incremental use-case work from design through testing. [Couto, Ribeiro, and Campos](https://arxiv.org/abs/1603.08632) discuss formalizing use cases and consistency. [Hajri and colleagues](https://arxiv.org/abs/1905.11699) study system-test classification and prioritization from use cases.

The [Python sqlite3 documentation](https://docs.python.org/3.13/library/sqlite3.html) supports the examples' storage implementation. [GitHub's Python workflow guide](https://docs.github.com/en/actions/tutorials/build-and-test-code/python) informs the repository workflow. Neither technology is required by OAL.
