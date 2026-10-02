<p align="center"><img src="assets/oal-banner-en.png" alt="OAL — Open Analysis Layers" width="100%"></p>

<p align="center"><strong>OAL Alpha-v0.1.0-Alkimim</strong><br>English · <a href="README.pt-br.md">Português brasileiro</a></p>

# OAL — Open Analysis Layers

OAL organizes a system's work into five linked responsibilities: specify use cases, model the program, plan behavioral checks, build the callable core, and expose it through interfaces. Each derivation records its sources, decisions, and responsible person. Teams can use the model with different languages, tools, documents, and folder layouts.

## Contents

- [The five layers](#the-five-layers)
- [Case mapping and cardinality](#case-mapping-and-cardinality)
- [Derivation engines](#derivation-engines)
- [Translations and combined implementations](#translations-and-combined-implementations)
- [Versions](#versions)
- [Examples](#examples)
- [Frequently asked questions](#frequently-asked-questions)
- [Authors and credits](#authors-and-credits)

## The five layers

<p align="center"><img src="assets/oal-layers-en.png" alt="OAL reference layers" width="750"></p>

| Layer | What it contributes |
| --- | --- |
| **L1 · UCS** | Defines use cases: objectives, actors and permissions, behavior, domain rules, outcomes, and acceptance criteria. It describes the observable contract without choosing screens, routes, or code structure. |
| **L2.1 · ADPM** | Models each case's decisions and algorithm, entities, tools and their contracts, and dependency composition. It distinguishes these responsibilities without prescribing a concrete architecture. |
| **L2.2 · ADVS** | Defines exactly one **behavioral test** directly linked to each UCS case. That test may consume supporting subtests for permissions, alternatives, failures, and criteria. Tool and entity checks are recommended but need not be separate ADVS specifications. |
| **L3 · ADI** | Implements the modeled cases as a callable application core. It preserves ADPM distinctions and mappings in the chosen architecture, enforces case permissions, and records observed verification results. |
| **L4 · ADIB** | Builds the external interaction boundary: pages, endpoints, commands, messages, or other channels. It receives requests, invokes L3 cases, and presents results while keeping channel decisions outside the core. |

**L2.1 and L2.2 derive from L1 in parallel.** Within a declared scope, each use case has one corresponding ADPM case, one ADVS behavioral test, and one ADI case. Supporting subtests are not behavioral tests because they do not link directly to a UCS case. An ADIB interface element can invoke several cases, and a case can be exposed by several elements. These links preserve case identity without forcing the same file or class structure in every project. See the [cross-layer rules](versioning/Alpha-v0.1.0-Alkimim.md#oal-layers), [ADPM rules](versioning/Alpha-v0.1.0-Alkimim.md#adpm), and [ADVS rules](versioning/Alpha-v0.1.0-Alkimim.md#advs).

The ADPM separation among cases, tools, entities, and optional domains must remain identifiable in ADI and across ADIB. ADIB derives its interaction boundary from ADI's callable cases and may also consult UCS. ADIB is not a copy of ADI. The [ADI rules](versioning/Alpha-v0.1.0-Alkimim.md#adi) and [ADIB rules](versioning/Alpha-v0.1.0-Alkimim.md#adib) define these boundaries.

## Case mapping and cardinality

<p align="center"><img src="assets/oal-map-en.png" alt="One-to-one case links through L1, L2, and L3; many-to-many mapping from L3 cases to L4 interface elements" width="750"></p>

The one-to-one links concern **use-case identities**: one UCS case, one ADPM case, one ADVS behavioral test, and one ADI case. Supporting checks may be numerous. Between ADI cases and ADIB interface elements, the mapping is many to many.

## Derivation engines

An **OAL engine** produces one layer from source material. It may be a human process, software, or both. Engine LX-LY uses LX to produce LY; it need not translate the source literally. For example, L4 adds interaction choices that do not exist in L3.

| Engine | Inputs → output |
| --- | --- |
| **Engine Needs-L1** | Stakeholder needs → UCS (L1). |
| **Engine L1-L2.1** | UCS → ADPM (L2.1). |
| **Engine L1-L2.2** | UCS → ADVS (L2.2). |
| **Engine L2-L3** | ADPM **and** ADVS → ADI (L3); UCS (L1) may be consulted as an additional source. L2 abbreviates the L2.1/L2.2 pair; it is not another layer. |
| **Engine L3-L4** | ADI → ADIB (L4); UCS (L1) may be consulted as an additional source. |

A concrete derivation records source and destination versions, scope, added decisions, and an accountable person. An implementation may identify itself as an instance of one OAL layer or engine when it states its edition, inputs and outputs where applicable, scope, preserved links, and supporting evidence. See the [engine rule](versioning/Alpha-v0.1.0-Alkimim.md#oal-layers) and [versioning guide](versioning/Alpha-v0.1.0-Alkimim.md#versioning).

## Translations and combined implementations

Implementations of the same layer share its defining contracts, so one can be translated into another even when their languages or formats differ. Such a translation records which shared characteristics survive and which details are lost or changed. The same applies to implementations of the same named engine.

One specialization may cover neighboring layers. When it performs their derivation, it also implements the engine between them. Its source, destination, and transition still need distinct, reviewable evidence. For L2-L3, the required L2 input includes **both** ADPM and ADVS. See the [cross-layer rules](versioning/Alpha-v0.1.0-Alkimim.md#oal-layers).

## Versions

| Edition | Status | Reference rules | Notes |
| --- | --- | --- | --- |
| Alpha-v0.1.0-Alkimim | Finalized alpha version | [English](versioning/Alpha-v0.1.0-Alkimim.md) · [Português](versioning/Alpha-v0.1.0-Alkimim.pt-br.md) | [Release notes](versioning/Alpha-v0.1.0-Alkimim.md#release-notes) |

The [verification guide](versioning/Alpha-v0.1.0-Alkimim.md#verification) and [conformance guide](versioning/Alpha-v0.1.0-Alkimim.md#conformance) explain what a result can support. English is the source text; Portuguese is its translation.

## Examples

The repository includes Tiny Catalog, Board CRM, and Work Board. Their artifacts, features, demonstration credentials, and execution instructions are in the [examples guide](examples/README.md).

## Frequently asked questions

<details><summary>Is OAL a fixed folder structure?</summary>

No. The layers name responsibilities. A project can combine or split physical files and modules while keeping their contracts and derivations identifiable.

</details>

<details><summary>Must ADPM use pseudocode or prescribe an architecture?</summary>

No. Semantic prose and structured pseudocode are both valid if they specify cases, entities, tools, contracts, dependency wiring, permissions, and algorithms. ADPM distinguishes and maps those responsibilities; ADI chooses a concrete architecture that preserves the mapping.

</details>

<details><summary>Why are L2.1 and L2.2 parallel?</summary>

ADPM models the program and ADVS specifies verification. Both derive from UCS. Their numbers do not prescribe an order between them; both inform ADI.

</details>

<details><summary>Can one use case have multiple behavioral tests?</summary>

No. One UCS use case has one directly linked ADVS behavioral test. That test can consume many supporting subtests, which are not behavioral tests themselves. Checks focused on tools, entities, or interface channels can also be recorded without creating another behavioral test for the case.

</details>

<details><summary>What qualifies as an OAL engine implementation?</summary>

It identifies the named transition and edition, accepted inputs, produced outputs, preserved links, added decisions, and validation scope. Each project derivation also identifies a responsible person and source and destination versions.

</details>

<details><summary>Who is the actor?</summary>

A runtime actor is a person or external system requesting a use case. The person responsible for deriving an artifact is named separately. Each case defines permitted actors; missing or unknown actors are denied.

</details>

<details><summary>Is ADIB limited to a programmatic API?</summary>

No. It covers pages, programmatic endpoints, commands, messages, and other interaction channels. OAL uses ADIB for this broader boundary.

</details>

<details><summary>Does ADIB need one interface element per use case?</summary>

No. One element may invoke several specified cases, and one case may be exposed by several elements. Record links in both directions and identify interface-only elements separately.

</details>

<details><summary>Where do authentication and authorization belong?</summary>

ADIB resolves or authenticates the caller and passes the actor identity to ADI. The case in ADI enforces its permission even when invoked directly. Routes, pages, formatting, and sessions belong to ADIB.

</details>

<details><summary>Does a passing test prove the whole model?</summary>

No. It supports the observed check and configuration. ADVS records planned checks; ADI and ADIB report executions for the boundaries and environments they claim.

</details>

<details><summary>Are the Python examples prescribed implementations?</summary>

No. They show possible language, storage, and browser choices. The reference rules allow other choices.

</details>

## Authors and credits

OAL was conceived and written by **Douglas de Oliveira Alkimim** and **Bruno Chevitarese**. See the [citation metadata](CITATION.cff) and [MIT license](LICENSE).

<table align="center" cellspacing="16" cellpadding="8">
  <tr>
    <td width="340" valign="top">
      <div>
        <img src="https://avatars.githubusercontent.com/u/65194413?v=4" alt="Douglas de Oliveira Alkimim" width="88" height="88" align="left" hspace="12">
        <strong>Douglas de Oliveira Alkimim</strong><br>
        <a href="https://github.com/douglas-alkimim"><img src="https://img.shields.io/badge/GitHub-181717?logo=github&amp;logoColor=white" alt="Douglas on GitHub"></a>&nbsp;<a href="https://www.linkedin.com/in/douglas-alkimim/"><img src="https://img.shields.io/badge/LinkedIn-0A66C2?logo=linkedin&amp;logoColor=white" alt="Douglas on LinkedIn"></a>
        <br clear="all">
      </div>
    </td>
    <td width="340" valign="top">
      <div>
        <img src="https://avatars.githubusercontent.com/u/150291749?v=4" alt="Bruno Chevitarese" width="88" height="88" align="left" hspace="12">
        <strong>Bruno Chevitarese</strong><br>
        <a href="https://github.com/chevitaresebruno"><img src="https://img.shields.io/badge/GitHub-181717?logo=github&amp;logoColor=white" alt="Bruno on GitHub"></a>&nbsp;<a href="https://www.linkedin.com/in/bruno-chevitarese/"><img src="https://img.shields.io/badge/LinkedIn-0A66C2?logo=linkedin&amp;logoColor=white" alt="Bruno on LinkedIn"></a>
        <br clear="all">
      </div>
    </td>
  </tr>
</table>
