# Example self-assessment — OAL Alpha-v0.2.0-Alkimim

[Português](CONFORMANCE.pt-br.md) · [Home](../../../../../README.md)

This self-review checks the four Tiny Catalog cases against the numbered UCS (L1) and ADPM (within L2) rules of the [Alpha-v0.2.0-Alkimim edition](../../../README.md). The executable checks are in `tests/p3` and `tests/p4`. The [needs baseline](../needs-baseline.json) was reconstructed from the UCS; it does not represent a separate stakeholder review. The package instantiates OAL-EX-M1-CASE-CONTRACTS and OAL-EX-M2-PROGRAM-SCENARIOS 0.1.0 (see `model-instances.json`). This review assesses the artifacts against the edition's rules and the selected models; it does not certify semantic conformance and does not demonstrate an engine transformer.

## UCS (L1) rules

1. **Scope:** UCS §1 identifies objectives, boundaries, actors, assumptions, and exclusions.
2. **Use cases:** UCS §6 contains the four stable case IDs, each with objective, initiating actor, and permitted actor set.
3. **Behavioral contracts:** each case describes trigger, inputs, conditions, outcomes, effects, and failures, including the observable result of denied access; channel choices are referenced as L4 decisions with their origin declared.
4. **Entities/rules:** UCS §§3–4 distinguish field validity and case-applied rules.
5. **Composition and dependencies:** each case identifies required capabilities; deactivation names the lookup dependency explicitly.
6. **Complementary obligations:** UCS §5 defines persistence/outcome obligations and states limits.
7. **Acceptance and links:** criteria, the [ADPM case map](../OAL-P2/adpm/traceability.json), and the [ADVS test map](../OAL-P2/advs/behavioral-tests.json) link all four cases.
8. **Consistency and evolution:** baseline, translation authority, assumptions, and stable IDs are explicit; facts, assumptions, and exclusions remain distinguishable; later contract changes require a recorded version change.
9. **Domains (recommendation):** adopted as a logical Catalog grouping, without domain folders.
10. **Representative examples:** acceptance scenarios are linked to `tests/p3`; channel checks are in `tests/p4`.

## ADPM (L2) rules

1. **Separation and preservation of responsibilities:** `entities`, `usecases`, and `tools` are distinguishable and mapped into the implementation.
2. **Use cases:** domain decisions remain in the four case implementations; deactivation composes the lookup case; each case decides its permission before effects.
3. **Entities:** this example's model chooses predominantly data entities — reading, assigning, and validating data during assignment — with no other behavior and no dependency on cases or tools; their contracts and invariants are stated in UCS §3 and MODEL.md.
4. **Tools, contracts, and validation location:** declared contracts, codec, and connection/store implementations; domain validity stays in entities and cases, while tools keep only technical guarantees (atomic uniqueness, representation checks, corruption translation); contract tests supplied.
5. **Dependencies and composition:** `composition.py` supplies collaborators and data constructors; no hidden case-level selection.
6. **Persistence:** accessed through `ItemStore`; catalog record responsibility and read/write conditions are documented.
7. **Authorization boundary:** every case models explicitly resolved actor context and a deny-by-default permission decision before domain effects. Authentication is required by this project contract and established by the trusted caller; the role string is the model-specific context representation.
8. **Faithful representation:** MODEL.md prose keeps responsibilities, contracts, dependency wiring, authorization, validation locations, and algorithms recoverable.
9. **Domains (recommendation):** logical grouping adopted; physical responsibility-based folders retained.
10. **Lifetime:** one instance of each case per `CatalogApplication`; request-local inputs.

Case identity and the one-to-one correspondence between the four specified IDs and the four implemented case identities are assessed under the edition's cross-layer rule 3, through the [ADPM case map](../OAL-P2/adpm/traceability.json) and the [ADVS test map](../OAL-P2/advs/behavioral-tests.json).

## Limits of this review

The local HTTP boundary authenticates demonstration credentials through a mechanism
specified in the [P4 contract](../OAL-P4/HTTP.md); every case enforces its actor
permission before effects. The memory profile is a test substitute and is not listed
as a durable production storage implementation. The [bidirectional interface map](../OAL-P4/traceability.json) documents the ADIB boundary.
This is an artifact-level self-assessment with a declared UCS+ADPM focus; ADVS, ADI,
and ADIB rules are only partially reviewed here. Run the tests in the example
directory to obtain results for the current environment; a passing suite supports the
observed checks and configuration only.
