# OAL example models — Alpha-v0.2.0-Alkimim

[Português](README.pt-br.md) · [Examples](../README.md) · [Reference rules](../../README.md)

This directory contains four small reusable models, one per OAL layer. They are examples of models that declare conformance to the numbered rules of Alpha-v0.2.0-Alkimim. They are deliberately narrow: they take concrete decisions that are sufficient to admit or reject project artifacts, with a declared educational scope.

| Layer | Model | Identity | Version | Directory |
| --- | --- | --- | --- | --- |
| L1 | Simple Case Contracts | `OAL-EX-M1-CASE-CONTRACTS` | 0.1.0 | [`l1-case-contracts/`](l1-case-contracts/MODEL.md) |
| L2 | Program and Scenario Records | `OAL-EX-M2-PROGRAM-SCENARIOS` | 0.1.0 | [`l2-program-scenarios/`](l2-program-scenarios/MODEL.md) |
| L3 | Injected Python Core | `OAL-EX-M3-PYTHON-CORE` | 0.1.0 | [`l3-python-core/`](l3-python-core/MODEL.md) |
| L4 | Local HTTP Boundary | `OAL-EX-M4-HTTP-BOUNDARY` | 0.1.0 | [`l4-http-boundary/`](l4-http-boundary/MODEL.md) |

The model version is independent of the OAL edition. A model declares the edition it was assessed against; a later OAL edition or a new model version requires a new assessment. This in-place correction keeps the current edition and model version identifiers. The revision notes describe the corrections, and the [content inventory](../../../../CONTENT-SHA256.json) identifies the delivered bytes; the unchanged version string alone does not identify the reviewed content. Observed application-test results remain in the [structured execution record](../verification/execution.json).

## What these models are and are not

- They are **reusable**: Tiny Catalog, Board CRM, and Work Board instantiate the same four models.
- They are **logical schemas plus validity conditions**, not serialization formats. Each model admits the representations its instances declare and names the canonical content.
- They are **not** new applications and do not replace the projects. The complete executable instances remain in the three project directories.
- They do **not** demonstrate a transformer. The projects were adapted manually; `engine_status` remains `not_demonstrated`.

## Instance manifest format

Each project contains a `model-instances.json` manifest with exactly four entries, one per layer. The common format is:

```json
{
  "manifest_version": "1.0.0",
  "project": "Project name",
  "oal_edition": "Alpha-v0.2.0-Alkimim",
  "artifact_version": "0.2.0",
  "instances": [
    {
      "id": "project-m1",
      "layer": "L1",
      "model": {
        "identity": "OAL-EX-M1-CASE-CONTRACTS",
        "version": "0.1.0",
        "definition": "../models/l1-case-contracts/MODEL.md"
      },
      "artifact": {
        "scope": "declared scope of this instance",
        "canonical_content": ["OAL-P1/index.json"],
        "files": ["OAL-P1/index.json", "OAL-P1/UCS.md"],
        "symbols": []
      },
      "mapping": {
        "cases": {"UC-...": "declared case identity in this layer"},
        "criteria": {"AC-...": "declared criterion reference"}
      },
      "evidence": {
        "assessment": "reviewed",
        "planned_checks": ["what is planned"],
        "execution": {"status": "not_recorded", "reference": null}
      },
      "limits": "what this instance does not claim"
    }
  ]
}
```

Field rules:

- `instances` has exactly four entries with layers `L1`, `L2`, `L3`, and `L4`, in that order.
- `model.identity`, `model.version`, and `model.definition` must match the model directory definition.
- `artifact.files` and `artifact.symbols` must exist. Symbols use `path::qualified.name`.
- For L2, `artifact.files` must include both the ADPM and ADVS components. `artifact.canonical_content` may be an object with `adpm` and `advs` arrays naming the authoritative sources of each component; `files` remains the list of integrant files, not the authority declaration.
- For L3, `artifact.canonical_content` lists the core modules (not merely a physical container). `artifact.boundary_files` may name the application initializer and interaction-boundary paths that are outside the core scope.
- For L1, `canonical_content` may identify one complete source or assign a canonical source to each field group. If a representation is a partial projection, the consistency rule states which omissions are permitted and requires reproduced content to agree with its canonical source. Shared integration criteria have a complete canonical definition, associated cases and obligations, and explicit links to supporting verification.
- `mapping.cases` must preserve the project case identities; identifiers of different categories need not be the same string.
- `evidence.execution.status` is `not_recorded`, `recorded`, or `not_applicable`. A `recorded` execution names the command or reference; a planned check is never presented as executed.
- `limits` names what the instance does not cover. An empty or generic value is rejected by a validator or review.

## How to instantiate a model

1. Select one model per layer and record its identity, version, and definition.
2. Produce the artifact fields the model requires. Adapt existing files rather than creating a parallel project.
3. Declare the canonical content and the mapping between representations.
4. Check the model's validity conditions (`V-M1-…`, `V-M2-…`, `V-M3-…`, `V-M4-…`).
5. Record the assessment: what was reviewed, what was executed, and what remains unverified.
6. Add the instance to `model-instances.json`, review it against the model's validity conditions, and run the project test suite.

A structural review can check identities, references, files, symbols, case correspondences, component presence, mappings, and evidence states. It does not replace the semantic assessment of the model or the artifact.

## Model assessment

Each `MODEL.md` contains its own mapping to the applicable OAL rules and a section on evidence and limits. The models were assessed against Alpha-v0.2.0-Alkimim by reading each numbered rule and identifying the construction or constraint that addresses it. That assessment is documented in the model file; it is a review, not a machine-certified conformance result.

The three project instances were reviewed against the selected models. The manifests record the scope, evidence, and limits. A structural check is not a semantic approval and does not turn a planned check into executed evidence.
