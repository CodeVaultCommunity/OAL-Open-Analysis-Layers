# Actors, validation and boundaries

This reference describes the responsibility boundaries in
**Alpha-v0.2.0-Alkimim**. Its source is OAL-5, UCS-2/3/4/5/6,
ADPM-1/2/3/4/5/6/7/10, ADI-1/2/4 and ADIB-3/5/6. The statements are explanatory
properties of the edition, not instructions for an agent to carry out a task.

## Contents

- [The actor vocabulary](#the-actor-vocabulary)
- [Where permissions are decided](#where-permissions-are-decided)
- [Cases, entities and tools](#cases-entities-and-tools)
- [Three different validation questions](#three-different-validation-questions)
- [Persistence and dependency composition](#persistence-and-dependency-composition)
- [Interaction restrictions and decisions](#interaction-restrictions-and-decisions)
- [Illustrative distinctions](#illustrative-distinctions)

## The actor vocabulary

| Term | Meaning |
| --- | --- |
| Actor | Interaction role declared in a use-case specification. A person or system can play it. |
| Caller | Concrete person or system on whose behalf a request occurs. |
| Actor context | Resolved representation of the relevant roles and, when required, identity and authentication information. |
| Context resolution | The declared process by which context is established, including origin and trust assumptions. |
| Authentication | Verification of a claimed identity when the applicable contract requires it. |
| Authorization | The use case's decision about whether execution is permitted under the presented conditions. |
| Derivation owner | Named person accountable for producing or approving an artifact transition. |

The context's form is selected by the model. It may be a simple role identifier
under explicit trust assumptions or a richer value containing several claims.
OAL does not prescribe a class, fields, protocol or identity provider.

An initiating actor and the set of actors permitted to execute a case are
related but distinct specification subjects. A use-case contract also identifies
the context information and authorization conditions needed for execution.

Anonymous and system actors are explicitly modeled possibilities. Anonymous
participation has a resolved context and an express permission. An absent
context, an unresolved context and failed authentication do not mean the caller
is anonymous. A system caller is not automatically privileged.

The people who specify models, construct transformers, execute derivations or
approve their results can be different people or the same person. Their work
roles do not automatically become actors in the resulting application.

## Where permissions are decided

ADIB resolves actor context through the declared channel mechanism and
authenticates when required by the case and channel contracts. Its result has a
declared origin and trust assumptions; a role label supplied by a request does
not establish trust on its own.

ADI receives context through an explicit invocation path. Each case applies its
own policy before domain effects and denies absent, unresolved, unknown,
unpermitted or otherwise insufficient contexts. The same authorization boundary
is effective during direct calls and through an interface.

A direct caller establishes context through the selected model's declared trusted
path. There is no rule that every call has to arrive over HTTP or through a
particular authentication library.

A case may use another case through an explicit dependency while respecting the
called case's contract and supplying pertinent actor context. The called case
still applies its own policy. Delegation or acting on behalf of another
participant has an explicit rule; merely calling from inside the core does not
grant extra permission.

Interface controls may prevent an action from being offered, and channel checks
may reject requests, but these mechanisms do not replace the case decision.
Authorization is not a persistence-tool responsibility.

ADVS permission scenarios cover the distinct permissions of each case, including
missing, unknown and insufficient contexts and expressly anonymous participation
when relevant. Denial before domain or persistence effects is observable.
A deliberately missing context can therefore be a valid negative-test setup
without being a valid execution context.

## Cases, entities and tools

Cases have identifiable objectives and the domain decisions allocated to them.
They can depend on tools and other cases through explicit contracts. The
selected model may allocate domain validation or behavior to entities; the
allocation remains visible rule by rule.

Entities represent data and relationships and do not depend on cases or tools.
A model can describe predominantly data entities or entities with domain
behavior. In both cases, contracts, invariants and dependencies remain explicit.
Entities do not absorb a case responsibility merely because they contain methods.

Tools have operations, results, effects and guarantees specified separately
from their technological mechanisms. Cases depend on those contracts. Tools do
not invent domain rules, and a technical name for an operation does not change
its actual responsibility.

The term “tool” in this program model refers to a program collaborator.
Instruments used to inspect OAL schemas, models or traceability are a different
category; the rule about program tools does not prohibit those verification
instruments.

## Three different validation questions

The edition distinguishes entity coherence, contextual tool guarantees and
raw-data representation. Their responsibilities remain separate.

### Entity coherence

For an entity $e$, let $I_E$ describe its internal coherence conditions:

$$
V_E = \{e \mid I_E(e)\}.
$$

A tool operation receiving a ready entity receives $e \in V_E$ by contract.
Re-running the entity's validation or implementing a semantically equivalent
copy of $I_E$ in that tool is prohibited by ADPM-4. Automatic generation,
renaming and describing the duplicate as a “technical guarantee” do not change
that prohibition.

Domain validity belongs to the entity or consuming case according to the
selected model's allocation. Validation helpers can centralize rules used by
entities and cases; they do not relocate or duplicate those rules in tools.
Authoritative validity is effective through a direct core call even when a user
interface offers earlier error prevention.

### Contextual conditions of a tool contract

A different condition $Q_t(e,c)$ can concern the tool's operation and context:
expected version, concurrency conflict, atomic global uniqueness, existence of a
persisted resource or availability of an external service.

Such a condition has an identifiable object, purpose and responsibility. It is
not an alternate implementation of the entity's internal coherence, and it does
not decide case authorization or take ownership of the domain rule.

For example, the validity of a product code's format differs from whether that
code already exists in the retained collection. The first can be internal
entity validity; the second can be a contextual uniqueness guarantee made
atomic by the persistence contract. The domain meaning and case response remain
in the model's declared domain responsibility.

### Raw representation and hydration

A serialized record is not already a valid entity. A codec or adapter can check
its technical representation and reject malformed data. When it constructs an
entity, the entity's canonical construction and validation still apply.

Channel JSON, encoding, request-body shape and channel parameters belong to L4.
The technical form of a persistence record and its serialization or
deserialization belong to a codec or adapter under a representation contract.
Neither boundary acquires a parallel implementation of entity validity.

## Persistence and dependency composition

Domain persistence is accessed through tools. The model makes data
responsibilities and read/write conditions explicit whether storage is shared
or separated. Concrete implementations meet the guarantees of their contracts
in the claimed configuration, including relevant isolation and failure behavior.

Entity validation and persistence guarantees are complementary. A preliminary
query in the core does not replace an atomic uniqueness or version-conditioned
write when another operation can intervene before the mutation.

ADIB invokes cases to read or change domain state. Storage exclusively for
technical channel state is allowed under an explicit contract identifying the
data, access conditions, lifetime and failure behavior. Sessions and request
correlation are examples. This exception does not permit direct domain-state
access, additional business-data rules or replacement of case authorization.

The selected models describe what cases and tools receive, where implementations
are selected and how collaborators are composed. Required dependencies are not
hidden behind global lookup. This does not prescribe a dependency-injection
framework or particular language mechanism.

Component lifetime is specified where relevant. One case instance per
application scope is an admissible choice, not a universal OAL requirement.
Shared storage likewise does not imply a mandatory singleton or packaging
structure.

## Interaction restrictions and decisions

L1 can inherit an interaction restriction imposed from outside the solution.
Its identified origin is what makes it an external restriction; mentioning a
protocol, representation or route does not by itself decide ownership.

An externally mandated gateway protocol can therefore appear in UCS. A route,
screen or payload encoding introduced by the solution is an L4 decision even
when UCS contains a reference to it. Copying that decision into UCS does not
turn it into stakeholder evidence or change its ownership.

ADIB can coordinate already specified cases while preserving their contracts
and responsibilities. Coordination that introduces a new domain decision,
objective or transaction belongs to a case responsibility reflected in UCS and
the affected derivations. It is not merely a presentation convenience.

A channel contract identifies its observable stimuli and results, including
immediate, deferred and event responses. Its routes or views, commands or
events, representations, errors, and relevant accessibility, localization and
operational obligations belong to the interaction boundary. Channel choices may
create additional ADVS scenarios.

## Illustrative distinctions

| Situation | Interpretation in this edition |
| --- | --- |
| A public case receives an explicitly resolved anonymous context that its policy permits. | Anonymous participation can be valid under that contract. |
| Authentication fails and the request has no valid context. | Failure does not establish anonymous participation. |
| An internal case calls a privileged case. | The called case still evaluates its own policy; the call itself adds no privilege. |
| A persistence tool repeats a ready entity's internal field checks. | This duplicates entity coherence and violates the stated boundary. |
| A persistence tool performs atomic version matching during an update. | This can be a distinct contextual guarantee of its own contract. |
| A channel stores request-correlation information under a technical contract. | This can remain exclusively technical channel state. |
| An endpoint directly updates business records to coordinate a new transaction. | The new domain responsibility belongs to the case specification and core. |

These illustrations explain the distinctions; their concrete roles,
representations and mechanisms are not additional OAL requirements.
