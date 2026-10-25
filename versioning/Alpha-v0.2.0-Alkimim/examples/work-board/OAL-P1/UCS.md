# Work Board · P1 use cases

[Português](UCS.pt-br.md) · [Example](../README.md) · [Structured UCS](ucs.json)

The six stable case IDs in [ucs.json](ucs.json) define the goals, actors, results, and acceptance criteria. Managers may use all six cases. Contributors may create, advance, comment, and read. Viewers may only read. Missing identity and roles outside each case's permission set are denied before effects.

This Markdown is a partial narrative projection of the canonical structured source [ucs.json](ucs.json). It does not reproduce every identifier, set, rule, obligation, or criterion. Identifiers cited here must exist in the JSON, and reproduced statements must agree with it; fields and sets not covered by this summary are intentionally omitted. A divergence in reproduced content is a defect.


## Field, version, and ordering rules

- **R-WB-01:** project is 1–40 characters, title 1–120, and description at most 2000 after trimming surrounding whitespace; a whitespace-only value counts as empty. Assignee is 1–80 characters and comment text 1–1000 characters after trimming.
- **R-WB-02:** priority is `low`, `normal`, or `high`; `normal` is the default and any other value is invalid.
- **R-WB-03:** an expected version is a positive integer. Assignment and advance are atomic compare-and-set operations: a stale version is rejected without changing the item.
- **R-WB-04:** the workflow is `backlog → in_progress → done`; only the next step is allowed, and a skipped step is rejected without changing the item.
- **R-WB-05:** a comment records the authenticated actor, trimmed text, and timestamp. Comments are append-only, ordered by timestamp then identifier, and do not change the item version or its records.
- **R-WB-06:** the board applies exact project and status filters and returns items ordered by project, title, and identifier, without mutation.

An item belongs to a project, has a priority, and moves through `backlog → in_progress → done`. Assignment uses a version check so a stale request cannot overwrite a newer value. Comments do not change the item version. The board and comment views do not mutate records. Interface routes, forms, and credentials belong to [P4](../OAL-P4/HTTP.md), not this contract.

The [needs baseline](../needs-baseline.json) was reconstructed from these cases to make the teaching derivation explicit. It is not a historical record of stakeholder interviews.

Version 0.2.0 makes the field limits, priority values, whitespace normalization, expected-version checks, and ordering rules explicit. They describe this example's implemented contract and were not stated in the 0.1.0 text; they are recorded as 0.2.0 baseline decisions, not as historical requirements. This document is a project artifact of the L1 responsibility that instantiates OAL-EX-M1-CASE-CONTRACTS 0.1.0; the instance declaration is in `model-instances.json`.

## Actor context

The specified actors are roles. This example requires authentication for all six cases. A trusted entry point resolves the caller and supplies `principal` as the role identifier used to represent its actor context; the case applies its own permission policy. Direct callers are responsible for supplying a context from that trusted resolution. A missing context is refused, and this example declares no anonymous actor.

## Storage failure and version limits

Every case can report `unavailable` under O-WB-AVAIL. The failure includes a write outcome: `not_applied` means that a pre-write failure or a confirmed rollback establishes the absence of a write; `unknown` means that commit or rollback was not confirmed. A caller inspects the current state before deciding whether to retry an unknown outcome. Atomicity still excludes partial records; it does not turn every failed acknowledgement into proof that nothing was written.

R-WB-03 accepts every positive integer as an expected version. A value too large to match any stored version produces `conflict` for an existing item or `not_found` for an absent one. This does not add a database-specific limit to the domain. Each case has a third acceptance criterion (AC-WB-001-03 through AC-WB-006-03) covering its stable unavailable outcome.
