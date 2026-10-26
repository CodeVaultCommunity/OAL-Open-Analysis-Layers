# Stable compatibility assessment

[Português](COMPATIBILITY.pt-br.md) · [Reference rules](README.md#reference-rules)

Source: Alpha-v0.2.0-Alkimim at commit 5755a4e4a5b31a9614da5d409d03d1db9cf1e20c. This records a local compatibility review, not external review or new human sign-off.

## Normative comparison

The entire cross-layer and layer-rule region was compared for both languages, from the oal-layers anchor through ADIB and before Interpretation. All 46 numbered items retain identical text: OAL 9, UCS 10, ADPM 10, ADVS 5, ADI 5, ADIB 7. The explanatory ADMV introduction is unchanged. Optional recommendations remain optional.

| Changed region | Reason and compatibility effect |
| --- | --- |
| Release notes and edition heading | Identify the new edition and its Alpha source; no new numbered obligation. |
| Versioning guide | Define immutable commit/tag releases and major/minor/patch evolution; ambiguous corrections require compatibility analysis. |
| Navigation and packaging | Point to the stable copy and new evidence; add reproducible checks and informative agent maps. |
| Normative rule text | No differences in either language. |

No FAQ, skill, guide or agent map introduces additional conformance obligations.

## Four model assessments

The following four model contracts retain version 0.1.0. Their fields, constructions, relations, validity conditions, mapping tables, and templates were compared with the Alpha definitions. Only edition/provenance metadata and the explicit assessment note change. The numbered OAL contract is identical, so the previous documented mapping remains applicable within the same declared educational scope.

| Model | Evidence and conclusion |
| --- | --- |
| OAL-EX-M1-CASE-CONTRACTS | Unchanged case/entity/obligation fields and V-M1 conditions. The permitted origin vocabulary remains external, domain, assumption, l4-decision. Work Board's invalid value is corrected in its instance. |
| OAL-EX-M2-PROGRAM-SCENARIOS | Unchanged ADPM/ADVS contract and V-M2 conditions; both components, case identities, criteria and directly linked tests remain explicit. |
| OAL-EX-M3-PYTHON-CORE | Unchanged reusable code organization and V-M3 conditions; core cases, entities, tools and composition retain their mappings. |
| OAL-EX-M4-HTTP-BOUNDARY | Unchanged boundary contract and V-M4 conditions; many-to-many case mappings and channel obligations remain explicit. |

The models were introduced in Alpha-v0.2.0-Alkimim. Their original assessment is historical; this compatibility assessment and the new structural/application checks are separate evidence. The models are examples external to OAL's definition.

## Artifact revision

Work Board baseline 0.2.1 changes O-WB-AVAIL.origin from baseline-decision to domain because it specifies operational results of the cases. Its origin_reference is retained verbatim, including the baseline decision and absence of independent stakeholder evidence. Reconstructed needs stay 0.2.0. The Needs-to-L1 record explicitly identifies the corrected destination; subsequent source/destination references use 0.2.1.

The derived Work Board artifacts are reviewed for compatibility and retain their behavior, case identities, criteria, implementation and tests. Their 0.2.1 label identifies this reviewed set, not a newly generated implementation. Historical derivation owners remain attributed to the historical work; this correction does not assert a transformer execution or human approval.

Tiny Catalog and Board CRM retain artifact baseline 0.2.0; their current edition metadata and evidence are updated. Board CRM's schema identifier names the historical content format and remains unchanged; its evolution paragraph records historical adaptation. The generated TeX date line identifies the current assessed edition. Python demonstration packages retain 0.2.0a0; OAL stability makes no commercial-stability claim for them.

## Evidence and limits

[Execution](examples/verification/execution.json) records actual commands, times, environment, logs, launcher smoke, and the hashes of the fixed input set. [Structural checks](examples/verification/structural-checks.json) verify explicit references only. Original logs are retained under examples/verification/historical-alpha-v0.2.0/ without changing dates or results.

The structural check is not a prose or code interpreter. Coherent identifiers and passing finite tests do not prove scenario sufficiency, real stakeholder adequacy, universal semantics, browser JavaScript behavior, accessibility or transformer construction/execution. No new engine, application, authentication mechanism or infrastructure is introduced.
