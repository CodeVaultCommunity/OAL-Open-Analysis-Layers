# Source map and terminology

This package describes **OAL Stable-v1.0.0**, prepared from the historical Alpha baseline with unchanged numbered requirements. It is an informational companion bundled with
that edition, not a new OAL edition or a separate normative specification.

## Contents

- [Source identity](#source-identity)
- [Authority and scope](#authority-and-scope)
- [Coverage of the numbered requirements](#coverage-of-the-numbered-requirements)
- [English and Brazilian Portuguese terminology](#english-and-brazilian-portuguese-terminology)

## Source identity

The paths below identify files in the source OAL repository. They are provenance
identifiers, not dependencies on files outside this skill.

| Source | Role |
| --- | --- |
| `versioning/Stable-v1.0.0/README.md` | English numbered requirements and explanatory guide. |
| `versioning/Stable-v1.0.0/README.pt-br.md` | Brazilian Portuguese translation of that edition. |
| `LICENSE` | Original MIT license and copyright attribution. |

- **Canonical edition label:** `Stable-v1.0.0`.
- **English source SHA-256:** `8e3d82be109b1e8baf1deab32b338b568aa7c98d407858456620336c76ce499e`.
- **Portuguese source SHA-256:** `dec2199d47e04caf65934861cc27308afb264504fce0e54a24391db8d9033bdc`.
- **Original license SHA-256:** `dfee2cfbba02ad5b688116a71e4870843ab88cce92cf01c97dafa7e428c74fd7`.

- **Included license SHA-256:** `dfee2cfbba02ad5b688116a71e4870843ab88cce92cf01c97dafa7e428c74fd7`.

OAL's credited authors are **Douglas de Oliveira Alkimim** and **Bruno
Chevitarese**. The Alpha source credits Douglas de Oliveira Alkimim as its principal editor. Stable preparation by Codex does not assert new human sign-off. The [included license](../LICENSE.txt) preserves the source project's
MIT terms and attribution.

Stable-v1.0.0 is a new edition; released commit/tag snapshots are immutable. These hashes identify the source bytes for this preparation. Historical Alpha editions and their skills remain separate.

In the full OAL repository, the root `CONTENT-SHA256.json` identifies every
delivered file, including this skill, by path, byte size, and SHA-256 digest.
Only the inventory itself is excluded. A final commit or archive digest is supplied outside the package, avoiding a circular dependency.

## Authority and scope

The English text is the edition's source wording; Portuguese is its translation.
Only the numbered requirements define conformance. Their marked recommendations
retain their optional status. The explanatory guide and this skill's summaries
do not add requirements.

The source contains **46 numbered requirements**: nine cross-layer requirements
and 37 layer/component requirements. ADMV has an explanatory introduction
establishing one L2 with both ADPM and ADVS, whose requirements appear in their
respective component sections.

Labels such as OAL-7 or UCS-2 combine the section name with its existing local
requirement number. They are reference labels for the edition, not additional
numbered requirements introduced by this package.

This knowledge package covers the concepts and conformance properties of that
edition. It contains no executable implementation, derivation engine,
verification service or certificate of project conformance. The source
repository's didactic models and project examples appear only as illustrations
with their evidence limits.

## Coverage of the numbered requirements

| Source rule | Subject | Main explanation in this package |
| --- | --- | --- |
| OAL-1 | Layers, metamodels, models and artifacts | [Formal relationships](engines-and-notation.md#layers-models-and-artifacts) |
| OAL-2 | Accountable derivations and distinct records | [Provenance](conformance-and-evidence.md#provenance-construction-and-execution) |
| OAL-3 | Case identity and behavioral-test cardinality | [Case identities](conformance-and-evidence.md#case-identity-and-shared-criteria) |
| OAL-4 | Changes and the baselines of claims | [Evolution](conformance-and-evidence.md#change-and-retained-identity) |
| OAL-5 | Actors, callers and accountable people | [Actor vocabulary](actors-and-boundaries.md#the-actor-vocabulary) |
| OAL-6 | Layer names, conformance and coverage | [Claim objects](conformance-and-evidence.md#the-object-of-a-claim) |
| OAL-7 | Engine metamodel and transformer contract | [Construction](engines-and-notation.md#engine-construction-and-execution), [coverage and preservation](engines-and-notation.md#supported-domain-and-preservation), [determinism and failures](engines-and-notation.md#determinism-failures-and-evidence) |
| OAL-8 | Conversion, translation, derivation and substitution | [Four operations](engines-and-notation.md#four-distinct-operations) |
| OAL-9 | Combined models and transformer composition | [Composition](engines-and-notation.md#combined-coverage-and-composition) |
| UCS-1 through UCS-10 | Ten L1 requirements | [UCS](layers.md#ucs) |
| ADPM-1 through ADPM-10 | Ten program-model requirements within L2 | [ADPM](layers.md#adpm) |
| ADVS-1 through ADVS-5 | Five verification-specification requirements within L2 | [ADVS](layers.md#advs) |
| ADI-1 through ADI-5 | Five L3 requirements | [ADI](layers.md#adi) |
| ADIB-1 through ADIB-7 | Seven L4 requirements | [ADIB](layers.md#adib) |

The [layer reference](layers.md#admv) also explains unified ADMV. The
[boundary reference](actors-and-boundaries.md) expands the actor, validation,
persistence and channel distinctions that appear in several numbered rules.

## English and Brazilian Portuguese terminology

The acronyms and canonical edition label remain the same in both languages.

| English | Português brasileiro |
| --- | --- |
| Open Analysis Layers | Open Analysis Layers; nome próprio do OAL |
| Layer | Camada |
| Metamodel | Metamodelo |
| Reusable model | Modelo reutilizável |
| Project artifact | Artefato de projeto |
| Satisfaction | Satisfação; satisfação dos requisitos |
| Membership | Pertencimento a uma classe ou conjunto |
| Code organization | Organização de código |
| Use case | Caso de uso |
| Actor | Ator; papel de interação especificado |
| Caller | Chamador; participante concreto |
| Actor context | Contexto de ator |
| Authentication | Autenticação |
| Authorization | Autorização |
| Derivation owner | Pessoa responsável pela derivação |
| Program model | Modelo do programa |
| Verification specification | Especificação da verificação |
| Behavioral test | Teste comportamental diretamente vinculado ao caso UCS |
| Supporting subtest | Subteste de apoio |
| Acceptance criterion | Critério de aceite |
| Shared integration criterion | Critério compartilhado de integração |
| Callable core | Núcleo invocável |
| Interaction boundary | Fronteira de interação |
| Engine | Motor; metamodelo de construção e execução |
| Transformer | Transformador especializado para modelos selecionados |
| Construction / Build | Construção do transformador |
| Execution | Execução concreta do transformador, ou do aplicativo conforme o contexto |
| Supported domain | Domínio suportado |
| Preservation obligation | Obrigação de preservação |
| Traceability | Rastreabilidade |
| Baseline | Referência ou estado versionado da origem ou do destino |
| Model conformance | Conformidade de modelo |
| Artifact conformance | Conformidade de artefato |
| Layer coverage | Cobertura de camadas |
