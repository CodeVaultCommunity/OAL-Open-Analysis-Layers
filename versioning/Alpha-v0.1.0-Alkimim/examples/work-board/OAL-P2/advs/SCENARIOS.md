# Work Board · P2.2 verification

[Português](SCENARIOS.pt-br.md) · [UCS](../../OAL-P1/UCS.md) · [Example](../../README.md)

The [behavioral-test map](behavioral-tests.json) gives each UCS case one directly linked test identity. The executable functions in [`tests/p3`](../../tests/p3) are supporting checks, not additional directly linked behavioral-test identities. They cover all twelve UCS acceptance criteria: valid outcomes, denied actors, invalid inputs, stale versions, workflow order, filters, and absent items.

[`tests/p4`](../../tests/p4) checks HTTP authentication, representation, route dispatch, and status mapping. Its checks support the chosen interface channel and do not replace the P3 checks. A passing suite reports only the configuration exercised in that run.
