# Example self-assessment — OAL Alpha-v0.1.0-Alkimim

[Português](CONFORMANCE.pt-br.md) · [Home](../../../../README.md)

This self-review checks the four Tiny Catalog cases against the UCS and ADPM characteristics. The executable checks are in `tests/p3` and `tests/p4`. The [needs baseline](../needs-baseline.json) was reconstructed from the UCS; it does not represent a separate stakeholder review.

## UCS characteristics

1. **Scope:** UCS §1 identifies needs, participants, boundaries, assumptions, and exclusions.
2. **Behavioral organization:** UCS §6 contains the four stable case IDs.
3. **Contracts:** each case describes trigger, inputs, conditions, outcomes, effects, and failures.
4. **Entities/rules:** UCS §§3–4 distinguish field validity and case-applied rules.
5. **Dependencies:** each case identifies capabilities; deactivation names lookup explicitly.
6. **Complementary obligations:** UCS §5 defines persistence/outcome obligations and states limits.
7. **Acceptance/traceability:** criteria, the [ADPM case map](../OAL-P2/adpm/traceability.json), and the [ADVS test map](../OAL-P2/advs/behavioral-tests.json) link all four cases.
8. **Evolution:** baseline, translation authority, assumptions, and stable IDs are explicit; later contract changes require a recorded version change.
9. **Domains (optional):** adopted as logical Catalog grouping, without domain folders.
10. **Representative scenarios:** acceptance scenarios are linked to `tests/p3`; channel checks are in `tests/p4`.

## ADPM characteristics

1. **Responsibilities:** `entities`, `usecases`, and `tools` are distinguishable.
2. **Cases:** decisions remain in four case implementations; deactivation composes lookup.
3. **Entities:** only assignment, reading, and assignment validation; no domain operations.
4. **Tools:** declared contracts, codec and connection/store implementations; contract tests supplied.
5. **Injection:** `composition.py` supplies collaborators and data constructors; no hidden case-level selection.
6. **Persistence:** accessed by ItemStore; catalog record responsibility and read/write conditions documented.
7. **Bijection:** four specified IDs map to four distinct implemented case identities and vice versa.
8. **Domains (optional):** logical grouping adopted; physical responsibility-based folders retained.
9. **Singletons (optional):** one instance of each case per CatalogApplication; request-local inputs.
10. **Tests (optional):** all three categories adopted using this proposal's definitions.

## Limits of this review

The local HTTP boundary authenticates demonstration credentials, and every
case enforces its actor permission before effects. The memory profile is a test
substitute and is not listed as a durable production storage implementation.
The [P4 contract](../OAL-P4/HTTP.md) and [bidirectional interface map](../OAL-P4/traceability.json) document the ADIB boundary.
Run the tests in the example directory to obtain results for the current
environment.
