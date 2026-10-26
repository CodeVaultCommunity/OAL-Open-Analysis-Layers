# Engines and notation

This reference describes the formal relationships and transformation concepts of **OAL Stable-v1.0.0**. Its principal sources are OAL-7, OAL-8 and OAL-9, with the layer/model/artifact distinction of OAL-1 and the provenance concepts of OAL-2. The [source map](source-map.md) identifies the edition snapshot.

## Contents

- [Layers, models and artifacts](#layers-models-and-artifacts)
- [Engine, construction and execution](#engine-construction-and-execution)
- [Named transitions and provenance](#named-transitions-and-provenance)
- [Supported domain and preservation](#supported-domain-and-preservation)
- [Determinism, failures and evidence](#determinism-failures-and-evidence)
- [Four distinct operations](#four-distinct-operations)
- [Combined coverage and composition](#combined-coverage-and-composition)

## Layers, models and artifacts

A layer $L_i$ defines a metamodel. A reusable model $M_i$ satisfies that metamodel, and a concrete artifact $a$ satisfies the selected model:

$$
M_i \models L_i,
\qquad
a \models M_i.
$$

For a fixed edition, model versions and declared scope:

$$
\mathcal{M}_i = \{M \mid M \models L_i\},
\qquad
A(M) = \{a \mid a \models M\}.
$$

The symbol $\models$ means satisfaction of the applicable OAL requirements; $\mid$ means “such that”. The relation “is a conforming artifact of the selected model” has the equivalent membership notation:

$$
a \in A(M_i) \iff a \models M_i.
$$

Here $\in$ means membership, and $\iff$ means “if and only if”. Membership is in the class $A(M_i)$ of conforming artifacts. Model conformance and artifact conformance concern different objects; the two satisfaction statements do not establish a direct artifact-to-layer instantiation.

Layer numbers describe development responsibilities. They are distinct from the metamodel–model–artifact instantiation axis. An artifact can span several files and have several representations of the same content. A physical file count or serialization format does not determine the number of models or layers.

## Engine, construction and execution

An **engine** is a metamodel specifying the construction and execution of deterministic transformation logic. A **transformer** is the logic specialized for a selected source/destination model pair. A **concrete execution** applies that constructed transformer to an input artifact.

For adjacent OAL layers, the source and destination models satisfy:

$$
M_n \models L_n,
\qquad
M_{n+1} \models L_{n+1}.
$$

A successful construction according to engine $E$ is represented by:

$$
\mathrm{Build}_E(M_n, M_{n+1})
\longrightarrow T[M_n, M_{n+1}].
$$

The arrow describes one construction with its fixed choices. Construction can fail, and different mapping, representation, technology or policy choices can produce different transformers for the same model pair. Those choices are frozen at construction or incorporated into the selected models.

$\mathrm{Build}$ is explanatory notation. It does not imply an executable factory, a separate service or another mandatory metalevel.

For $T = T[M_n, M_{n+1}]$, successful execution has the form:

$$
T(a)=b.
$$

The input $a$ and output $b$ instantiate the selected source and destination models, respectively. This execution transforms project artifacts; it is distinct from running a use case in the application those artifacts describe or implement.

## Named transitions and provenance

| Canonical engine | Source and destination responsibilities |
| --- | --- |
| Engine Needs-L1 | Artifacts of a declared external needs model $M_{\mathrm{Needs}}$ become artifacts of a selected UCS model. |
| Engine L1-L2 | UCS artifacts become complete ADMV artifacts, containing both ADPM and ADVS. |
| Engine L2-L3 | Complete ADMV artifacts become ADI artifacts; UCS may supply additional versioned information. |
| Engine L3-L4 | ADI artifacts become ADIB artifacts; UCS may supply additional versioned information. |

Needs are external source material, not an OAL layer. ADPM and ADVS may be prepared in parallel but remain components of one L2 and one canonical L1-to-L2 derivation.

Additional UCS information has explicit versioned references within the fixed inputs or contract. A mutable UCS consulted freely during execution would be a hidden dependency. Extra UCS references do not rename the canonical engine.

L3-to-L4 derivation introduces presentation, transport and other channel decisions belonging to the destination model or the construction choices. A produced interaction boundary surrounds callable ADI cases; production does not imply literal translation, structural equivalence or new domain requirements.

Model provenance, transformer construction and concrete execution are separate records. Derivations identify source/destination baselines, an accountable person, scope and added decisions. Reconstructed needs retain that provenance and are not independent stakeholder evidence. Manual derivation records can carry the same provenance and preservation obligations without demonstrating a constructed or executed transformer.

An engine-implementation claim identifies its edition, named transition, accepted inputs, produced outputs, preserved links, added decisions and validation scope. Its concrete use in a project retains the accountable person and baselines of that project's derivation record.

## Supported domain and preservation

A transformer's declared contract includes model identities, versions and edition; pair compatibility and required capabilities; construction choices; input validity and preconditions; supported coverage; output guarantees; determinism; failures and termination; verification results; and construction/execution traceability.

Its supported domain is a declared subset of valid source artifacts:

$$
D_T \subseteq A(M_n),
\qquad
T\colon D_T \to A(M_{n+1}).
$$

This signature describes the guarantee under the declared preconditions and operational conditions. Every supported input satisfying those conditions has a terminating execution producing a valid destination artifact. The output satisfies the **selected** destination model, not merely another model associated with that layer.

Partial coverage may leave valid source artifacts outside $D_T$. A complete-coverage claim concerns the entire announced set. A failed execution does not justify retrospectively shrinking $D_T$ to remove the input. Arbitrary model pairs do not necessarily admit complete or automatic transformation.

Preservation concerns the applicable source identities, contracts, acceptance criteria, permissions and other announced relations:

$$
P_T \subseteq A(M_n)\times A(M_{n+1}).
$$

Within the declared execution conditions:

$$
(a,T(a))\in P_T
\qquad \text{for every }a\in D_T.
$$

Output validity and preservation are separate obligations. An output can satisfy its destination model while losing a case identity, permission or contract that the transformation was required to preserve.

## Determinism, failures and evidence

Determinism is relative to fixed models and versions, transformer and version, configuration, and valid input. The equality criterion may be byte identity, canonical structure or a strictly delimited semantic equivalence. Time, randomness, environment and external queries do not silently change the compared result; operational metadata outside that result is explicitly distinguished.

When determinism uses an equivalence relation $\equiv$, differences ignored by that relation can matter to a later transformer. Compatible composition therefore depends on the later transformer respecting that equivalence on the relevant domain, or consuming an explicitly fixed canonical form.

Determinism does not imply a unique construction from a model pair. Nor does it establish correctness: a function returning the same error for every input is deterministic but does not produce the valid destination artifacts promised for its supported domain.

The failure categories distinguish invalid input, valid unsupported input, incompatible model pair, operational failure and invalid output. Inconclusive evidence is not approval.

Finite tests support the cases and configurations actually observed; they do not prove universal transformer correctness. Humans and AI may participate in constructing deterministic rules. Free interpretation or a variable service consulted at every execution does not, by itself, establish deterministic transformation. An engine can be realized by a human process, software or both, and its determinism does not require all executions of the resulting applications to be deterministic.

## Four distinct operations

### Representation conversion

A conversion $C_{rs}$ changes a valid document from representation $r$ to representation $s$ of the same model $M$. On its declared domain, preservation of model content is expressed by:

$$
\mathrm{decode}_s(C_{rs}(x))
\equiv_M
\mathrm{decode}_r(x).
$$

The decoding functions recover model content, and $\equiv_M$ is its declared equivalence. A round-trip claim also identifies an equivalence criterion for the return. Byte equality and editorial conventions outside the model neither establish nor universally define content preservation.

### Translation between models of one layer

Models $M,N\in\mathcal{M}_i$ share their layer's defining responsibilities. Translation between them still has an explicit mapping, declared domain and preservation obligations. Membership in the same layer supplies no universal, total, invertible or lossless translator. Information or behavior lost or changed outside the mapping remains identifiable.

### Derivation between layers

A derivation produces artifacts of the selected destination model while preserving applicable source obligations and adding decisions belonging to the destination responsibility. It carries provenance and decision records. A correct derivation can change structure; manual derivation and a claim of constructed or executed transformer remain distinct.

### Substitution between engine realizations

Substitution of realizations of the same named engine depends on the selected source/destination models and versions, declared domains, required inputs, destination responsibility, preserved case links and derivation guarantees. Implementation-specific losses and decisions remain part of the description.

Equal model pairs alone are insufficient. A substitution claim with differing supported domains is limited to their shared use domain, with equivalent outputs under the stated criterion and the announced obligations preserved.

A documented loss remains incompatible with a contract requiring that information to be preserved. Two persistence tools satisfying one tool contract illustrate substitution of L3 collaborators; that fact alone does not establish realizations of an OAL engine.

## Combined coverage and composition

A combined model or package may cover adjacent layer responsibilities without constructing the transformer between them. Internal construction is optional, including for L1 and L2; a claim of transformation is separate from coexistence or coverage. Any L2 coverage includes both ADPM and ADVS.

For transformers with compatible selected intermediate model and version:

$$
\begin{aligned}
T_{12}&\colon D_{12}\to A(M_2),
&D_{12}&\subseteq A(M_1),\\
T_{23}&\colon D_{23}\to A(M_3),
&D_{23}&\subseteq A(M_2),
\end{aligned}
$$

a claimed composition has:

$$
T_{13}(a)=T_{23}(T_{12}(a)),
\qquad
D_{13}\subseteq
\{a\in D_{12}\mid T_{12}(a)\in D_{23}\}.
$$

The equality holds on the declared composition domain. Sharing $M_2$ and its version is insufficient: a valid $M_2$ output can remain outside $D_{23}$. Equivalent outputs under the first transformer's determinism criterion can also produce different acceptance or results at the second transformer.

Composition consequently includes domain compatibility, compatible equivalence or canonicalization, failure handling and preserved traces. Component guarantees support the composition only within their own domains and where the first preserves what the second requires as input and the second preserves the announced destination obligations.

For example, $M_2$ may admit synchronous and asynchronous operations while $T_{23}$ supports only synchronous ones. An output $T_{12}(a)$ can satisfy $M_2$ and contain an unsupported asynchronous operation. The produced artifact, rather than $T_{12}$ itself, is the object satisfying $M_2$.

A composition is a separate claimed object. The notation $T_{13}$ does not introduce a canonical Engine L1-L3; this edition names no canonical non-adjacent engine.

Related concepts are described in [layers](layers.md), [actors and boundaries](actors-and-boundaries.md), and [conformance and evidence](conformance-and-evidence.md).
