# Conformance, provenance and evidence

This reference explains OAL-1/2/3/4/5/6, relevant ADVS and ADI evidence rules, and
the status of the examples in **Alpha-v0.2.0-Alkimim**.

## Contents

- [The object of a claim](#the-object-of-a-claim)
- [Provenance, construction and execution](#provenance-construction-and-execution)
- [Case identity and shared criteria](#case-identity-and-shared-criteria)
- [Verification and evidence states](#verification-and-evidence-states)
- [Change and retained identity](#change-and-retained-identity)
- [Didactic models and project instances](#didactic-models-and-project-instances)

## The object of a claim

| Claim | Meaning | Limit |
| --- | --- | --- |
| Model conformance | A reusable model satisfies a determined layer's metamodel in the declared scope. | It says nothing by itself about another layer or a concrete project's validity. |
| Artifact conformance | A project artifact satisfies its selected model in the declared scope. | It does not establish that the model was assessed or that every other artifact is valid. |
| Layer coverage | A declared set of models and artifacts covers a named set of layers. | Coverage of one layer does not establish another layer's coverage. |
| Complete layer coverage | All four OAL layers are covered. | L2 coverage still includes both ADPM and ADVS. |

A transformer construction, transformer execution or composition of transformers
can also be the object of a separate claim against the applicable engine
requirements. These claims are not synonyms for model or artifact conformance.

A claim identifies the edition, layer or layers, selected models and versions,
object, scope, preserved links and supporting evidence. Its source and
destination baselines are explicit where applicable. “Complete model” has a
definite meaning only when the model, version and sense of completeness are
unambiguous.

The symbols $M_i \models L_i$ and $a \models M_i$ state relationships. Writing
them does not demonstrate either claim. A file's location, an acronym in a
heading, a version label or a collection of folders likewise does not establish
conformance.

A model covering L2 includes both required components with their responsibilities
distinguishable. A claim concerning only ADPM or only ADVS is a component claim,
not full L2 coverage.

## Provenance, construction and execution

Three records have different subjects:

| Record | Subject |
| --- | --- |
| Model provenance | Edition, model identity, model version and the baselines involved. |
| Transformer construction | A selected source/destination pair, construction choices, compatibility and the transformer produced or construction failure. |
| Concrete execution | Actual input, transformer and configuration, observed result or failure, and the supported claim. |

A derivation is accountable to a named person and identifies source and
destination baselines, scope and added decisions. A job title or a tool alone
does not identify that person. Model specification, construction and execution
are distinguishable responsibilities that may be held by one person or several.

The Needs-to-L1 derivation identifies the external needs model and selected L1
model. Needs reconstructed from an existing UCS remain reconstructed material;
they are not independent stakeholder evidence.

L1-to-L2 produces one ADMV with both components, even when several people
prepare them in parallel. Additional UCS sources in L2-to-L3 or L3-to-L4 have
explicit, versioned references and identifiable decisions they informed. At
execution, such sources form part of the fixed inputs or contract.

Manual derivation carries provenance, scope, decisions and applicable
preservation obligations. That record does not, by itself, claim a constructed
or executed transformer. The stronger claim has the additional engine contract
described in [engines and notation](engines-and-notation.md).

## Case identity and shared criteria

Within a declared scope, the UCS cases, ADPM case identities, directly linked
ADVS behavioral tests and ADI case identities correspond one to one. Their
identity mapping is independent of physical file, class or test-function count.

Each case-specific acceptance criterion is linked to its case's behavioral test
and the supporting checks that cover it. A declared shared integration
criterion has one authoritative definition, explicit scope and affected cases.
It is linked to those cases' existing behavioral tests and shared supporting
checks. It does not create an extra directly linked behavioral test or a new
use-case identity solely because its scenario spans cases.

Channel-only checks can be recorded without becoming new use cases. Interface
elements have many-to-many links to ADI cases in both directions, with
interface-only elements identified separately.

## Verification and evidence states

ADVS describes intended verification. Test code is an implementation of checks.
Observed execution results describe what actually ran, in which environment and
against which boundary or configuration. Those are three different objects.

Behavioral tests and supporting scenarios describe preparation, preconditions,
relevant actor context, action, oracle and observed boundary. The oracle
includes expected results and effects, including the absence of prohibited
effects during denial.

Core verification is integrated with ADI. ADIB-specific checks concern the
selected channels and their claimed obligations. A successful core check does
not establish that a browser, endpoint, CLI or other channel was exercised.
A planned scenario, a test file and a configured test runner are not completed
executions.

Passing finite tests supports the observed cases and configuration; it does not
prove universal transformer correctness or the validity of every future
instance of a reusable model. Failed and unexecuted checks remain distinct
from passing results. Evidence records the implementation version, environment,
executed scenarios, results and limits.

The states “unspecified”, “not evaluated”, “not demonstrated”, “inconclusive”
and “nonconforming” are different from one another. None of the first four is
an approval, and missing evidence does not automatically constitute the same
finding as a demonstrated violation.

Separate ADVS specifications for tool and entity checks are recommended rather
than universally required. The contract guarantees and validity rules still
need the evidence appropriate to the claim. Likewise, domain grouping is an
explicitly optional recommendation, not an extra mandatory layer.

## Change and retained identity

A change to a source contract, permission or interaction decision affects
related models, transformer constructions, artifacts and verification scenarios.
The edition associates such changes with impact on rebuild, revalidation,
rederivation or rechecking claims. Evidence identifies the baselines actually
compared rather than treating unchanged labels as proof of unchanged content.

Physical artifacts can combine or split responsibilities when the relevant
layer, selected model and case links remain identifiable and traceable. Multiple
representations of one artifact still express one selected model's content.
Their authoritative definitions and references remain explicit.

This alpha edition has been revised in place under the same
`Alpha-v0.2.0-Alkimim` label. Its content snapshot matters independently of that
label. The prior `Alpha-v0.1.0-Alkimim` remains historical. The knowledge in this
folder corresponds to the snapshot identified in [source map](source-map.md);
it does not automatically describe later edits retaining the same edition name.

## Didactic models and project instances

The source repository specifies four reusable didactic models:

| Model identity | Associated layer | Scope illustrated |
| --- | --- | --- |
| `OAL-EX-M1-CASE-CONTRACTS` | L1 | Structured case and entity contracts. |
| `OAL-EX-M2-PROGRAM-SCENARIOS` | L2 | Program modeling and verification scenarios together. |
| `OAL-EX-M3-PYTHON-CORE` | L3 | A reusable Python code organization for a callable core. |
| `OAL-EX-M4-HTTP-BOUNDARY` | L4 | HTTP interaction and channel adaptation. |

Their retained model version is `0.1.0`. Tiny Catalog, Board CRM and Work Board
declare four project instances each, twelve declarations in total. Those
declarations identify model identity/version, edition, artifact files and
symbols, scope, canonical content, mappings, evidence state and limits.

The models were applied manually. The records do not demonstrate construction
or execution of deterministic OAL transformers. The needs baselines were
reconstructed from UCS, with no specified external needs model.

The examples illustrate permitted choices; they are not the definition of OAL
and do not impose Python, HTTP, SQLite, browser interfaces, role strings,
authentication mechanisms or a particular directory layout on other models.
Their authenticated actor policies are project choices; other models can
expressly admit anonymous or system participation under their own contracts.

Identity/reference checks establish structural facts about the declared files
and mappings. They do not certify semantic conformance. The presence of four
models and twelve declarations is therefore an illustrative organization of
examples, not proof that an engine chain exists.
