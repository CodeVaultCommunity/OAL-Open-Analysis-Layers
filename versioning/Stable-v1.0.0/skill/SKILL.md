---
name: oal-stable-v1-0-0
description: >-
  Informational reference for OAL (Open Analysis Layers), edition
  Stable-v1.0.0. Relevant to questions and discussions about OAL layers,
  metamodels, reusable models, project artifacts, UCS, ADMV, ADPM, ADVS, ADI,
  ADIB, code organization, actors, authorization, validation responsibilities,
  derivation engines, Build, deterministic transformers, mathematical notation,
  traceability, and conformance. Referência conceitual sobre camadas, modelos,
  artefatos, motores e conformidade do OAL. Descriptive knowledge only.
---

# OAL — Stable-v1.0.0

This is an informational account of **Open Analysis Layers**, edition
**Stable-v1.0.0**. Its content describes concepts, relationships and
conformance properties. It contains no execution procedure, implementation
workflow or task assignment.

The edition's numbered requirements define conformance; its explanatory guide
and this knowledge package explain those requirements without adding new ones.
English is the edition's source wording, and Brazilian Portuguese is its
translation. The exact source snapshot is identified in the
[source map](references/source-map.md).

## Reference map

| Subject | Included reference |
| --- | --- |
| All four layers and their 37 numbered layer requirements | [Layers](references/layers.md) |
| Formal notation, engines, construction, execution, determinism and composition | [Engines and notation](references/engines-and-notation.md) |
| Actor context, permissions, validation, persistence and channel boundaries | [Actors and boundaries](references/actors-and-boundaries.md) |
| Derivation provenance, conformance claims, evidence and didactic examples | [Conformance and evidence](references/conformance-and-evidence.md) |
| Edition identity, source hashes, rule coverage and bilingual terminology | [Source map](references/source-map.md) |

All these references are contained in this folder. Their explanations are
independent of a particular programming language, framework, harness, directory
layout or named family of reusable models.

## Layers, models and artifacts are different objects

A layer identifies a **development responsibility** and defines a metamodel.
A reusable model satisfies that metamodel. Concrete project artifacts instantiate
a selected reusable model.

$$
M_i \models L_i,
\qquad
a \models M_i.
$$

Here $L_i$ is the layer metamodel, $M_i$ a selected model and $a$ a concrete
artifact. The symbol $\models$ reads “satisfies the requirements of”, for the
declared edition, versions and scope.

$$
\mathcal{M}_i = \{M \mid M \models L_i\},
\qquad
A(M) = \{a \mid a \models M\}.
$$

Thus $\mathcal{M}_i$ is the class of models satisfying layer $L_i$, and $A(M)$ is
the class of artifacts satisfying model $M$. The artifact relation is:

$$
a \in A(M_i) \iff a \models M_i.
$$

Membership is in the class $A(M_i)$, not directly in $M_i$. Model conformance and
artifact conformance are separate claims; neither the symbols nor their
combination constitute evidence that a particular object conforms.

Layer number and metalevel are different axes: L1 is not the metalevel above L2.
An artifact can consist of several files and can have several representations of
the same content. File count, serialization format and number of models are
different quantities. “An L3 artifact” is shorthand for an artifact of a model
associated with L3.

OAL is independent of the particular models chosen to instantiate its layers.
The reusable models illustrated in its repository are examples, not constituents
of OAL's definition.

## The four responsibilities

| Layer | Name | Responsibility |
| --- | --- | --- |
| L1 | **UCS — Use Case Specification** | Observable use-case contracts: objectives, actors, permissions, domain meaning, behavior, outcomes, acceptance criteria and complementary obligations. |
| L2 | **ADMV — Analysis-Driven Modeling and Verification** | An integrated program model and verification specification, with both ADPM and ADVS present and distinguishable. |
| L3 | **ADI — Analysis-Driven Implementation** | A callable application core, concrete collaborators and verification integration under a selected reusable code organization. |
| L4 | **ADIB — Analysis-Driven Interaction Boundary** | Interaction channels that receive stimuli, invoke core cases and present results or failures. |

ADMV contains two required components:

- **ADPM — Analysis-Driven Program Model:** case, entity and tool
  responsibilities; contracts; algorithms; dependencies; composition;
  authorization; and locations of domain validity.
- **ADVS — Analysis-Driven Verification Specification:** behavioral tests,
  supporting scenarios, expected results, permission coverage and traceability
  to the specified criteria.

ADPM and ADVS may be prepared in parallel, but they are components of one L2 and
one L1-to-L2 derivation. Either component alone is insufficient for L2 coverage.

**An L3 model is a reusable code organization.** It describes how responsibilities,
dependencies, callable cases and verification are organized in code. An
architecture can be one choice within that organization; architecture alone is
not the definition of an L3 model.

Client needs are external source material under a declared needs model. They are
not an additional OAL layer.

## Case identity and cardinality

Within the declared scope, each UCS use-case identity corresponds to exactly:

- one ADPM case identity;
- one ADVS behavioral test directly linked to that UCS case;
- one ADI case identity.

There are no extra ADPM or ADI case identities or directly linked behavioral
tests in that scope. A behavioral test can encompass many scenarios and
supporting subtests. This identity mapping does not mean one test function,
assertion, file or scenario per use case.

A shared integration criterion has a defined scope, affected cases and one
authoritative definition. Its shared supporting checks support the behavioral
tests of those cases without creating an additional directly linked behavioral
test.

ADIB interface elements and ADI cases have a many-to-many relation recorded in
both directions. Interface-only elements have their own identified purpose.
An interface element is not a new use-case identity merely because it coordinates
several exposed cases.

## Actors and authority at runtime

An **actor** is a specified interaction role played by a person or system. The
**caller** is the concrete person or system on whose behalf a request occurs.
An **actor context** carries the relevant roles and, when the contract requires
them, identity and authentication information. The model gives that context a
representation, resolution path, origin and trust assumptions.

Authentication verifies a claimed identity when required by the contract.
Authorization decides whether the requested case may execute under the
presented conditions. Every case retains its own deny-by-default authorization
decision before domain effects, including during direct invocation.

A missing, unresolved, unknown, unpermitted or insufficient context is denied.
An explicitly admitted anonymous context is a separate modeling choice, not a
fallback for missing context or failed authentication. System actors are also
explicit choices. OAL prescribes no universal actor class, fixed context fields
or authentication technology.

ADIB resolves context and authenticates when required; ADI evaluates the case
policy. A direct caller supplies context through the model's declared trusted
path. A caller-provided role label by itself does not establish trust. A case
calling another case supplies pertinent context, and the called case retains
its own policy. Internal invocation alone grants no additional permission.

The named person responsible for an artifact derivation is distinct from a
runtime actor. Work roles describe responsibilities, not mandatory job titles.

## Responsibilities inside the program and its boundary

ADPM distinguishes cases, entities, tools and any modeled domains. Those
distinctions remain traceable in ADI and across ADIB even when physical files or
modules are combined.

Cases hold the domain decisions assigned to them. Entities may be predominantly
data or may have domain behavior when the selected model explicitly allocates
that behavior. Entity contracts, invariants and rule ownership remain
identifiable; entities do not depend on cases or tools.

A tool realizes its technical contract. For a ready entity, its internal
coherence is an input assumption. The tool does not duplicate that internal
validation, even as a generated or renamed equivalent check. Distinct contextual
conditions—atomic uniqueness, expected version, persisted-resource existence or
service availability—can belong to the tool's own contract. They do not transfer
case authorization or domain-rule ownership to the tool.

Raw records are not ready entities. Codecs may reject malformed representation;
entity construction during hydration still uses canonical entity validation.
Entity validation does not replace atomic persistence guarantees with
race-prone preliminary queries.

Dependency selection and composition are explicit, with no required dependency
hidden in global lookup. OAL imposes no universal dependency-injection framework,
folder organization or case-instance lifetime.

Domain persistence is accessed through tools within the case responsibilities.
ADIB invokes cases for domain state. It may use storage exclusively for technical
channel state, such as sessions or correlation, with an explicit contract for
data, access, lifetime and failure behavior.

Externally imposed interaction restrictions can appear in UCS with their origin.
Routes, screens, payload encodings and other interaction decisions introduced by
the solution belong to ADIB. New domain decisions, objectives or transactions
belong to case responsibilities reflected in UCS and its derivations.

## Engines, construction and execution

An **engine is a metamodel** describing the construction of a deterministic
transformer for selected source and destination models, and the execution of
that transformer on artifacts.

| Canonical engine | Source and destination responsibilities |
| --- | --- |
| Engine Needs-L1 | Artifacts of a declared external needs model to artifacts of a selected L1 model. |
| Engine L1-L2 | UCS to complete ADMV, including ADPM and ADVS. |
| Engine L2-L3 | Complete ADMV to ADI; UCS can be an additional explicit versioned source. |
| Engine L3-L4 | ADI to ADIB; UCS can be an additional explicit versioned source. |

For an adjacent-layer transition, a successful construction can be written as:

$$
\mathrm{Build}_E(M_n,M_{n+1})
\longrightarrow T[M_n,M_{n+1}].
$$

The arrow represents a construction with fixed choices. Other choices may yield
a different transformer, and construction can fail. `Build` is explanatory
notation for construction, not a mandatory executable factory or extra service.

For that constructed transformer $T$, the successful execution guarantee is:

$$
T(a)=b,
\qquad
a\in D_T\subseteq A(M_n),
\qquad
b\in A(M_{n+1}).
$$

The guarantee applies under the declared preconditions and operational
conditions. Valid source artifacts outside $D_T$ are outside its coverage.
Output validity and preservation of source identities, contracts, criteria,
permissions and other obligations are distinct requirements.

Determinism concerns repeated execution with the same selected models and
versions, transformer and version, configuration and valid input, under the
declared equality or equivalence criterion. It does not imply a unique
construction, universal coverage, correctness merely from repeatability, or
deterministic behavior of every application produced.

A manual derivation can have accountable provenance without demonstrating a
constructed or executed transformer. A variable interpretation performed anew at
each invocation is not, by itself, a deterministic transformation.

Representation conversion, translation between models of one layer,
cross-layer derivation and substitution between realizations of one engine have
different contracts. Composition of transformers has its own domain and
preservation claim. A package containing several layers demonstrates coexistence;
it does not by itself demonstrate transformation.

## Conformance and evidence

Four claims remain distinct: model conformance to a layer metamodel, artifact
conformance to a selected model, coverage of a named set of layers, and complete
coverage of all four layers. Coverage including L2 includes both ADPM and ADVS.
A transformer construction, execution or composition is a separately identified
claimed object.

Claims have an edition, selected models and versions, an object, a scope and
supporting evidence. A label or a mathematical expression is not a conformance
certificate. “Unspecified”, “not evaluated”, “not demonstrated”, “inconclusive”
and “nonconforming” have different meanings.

Verification planning, test code and observed execution results are distinct.
A test file does not establish that it ran; a passing result supports the
observed scenarios and configuration. A working core does not establish that a
particular interface was verified.

Domains are optional and recommended where they clarify responsibilities.
Dedicated entity/tool verification specifications are recommended rather than
universally required, while the claimed guarantees still need supporting
evidence. Formats, programming languages, frameworks and deployment mechanisms
remain choices of the selected models.
