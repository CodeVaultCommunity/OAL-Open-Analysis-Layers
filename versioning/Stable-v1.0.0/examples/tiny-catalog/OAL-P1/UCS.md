# Tiny Catalog — UCS

[Português](UCS.pt-br.md) · [Home](../../../../../README.md)

[Run the example](../README.md) · [UCS classification](../../../README.md#ucs)

**Project specification version:** 0.2.0. **Classification:** UCS artifact of the Stable-v1.0.0 edition, adapted from the 0.1.0 baseline.
**Status:** baseline of an illustrative example, not a commissioned production system.
**Reference language:** English for this example; the Portuguese file is a translation.

This is **one document that belongs to the UCS classification**, not a mandatory UCS template.
Technology selections and callable code contracts are outside this document.

**Canonical content:** the [index](index.json) is authoritative for identifiers, sets, relations, the common actor policy, and the complete shared integration criteria. This English narrative is authoritative for the detailed case, entity, rule, and obligation contracts; structured summaries do not replace omitted details. Reproduced statements and references must agree. The Portuguese narrative is a translation. The field-group authority and consistency rule are recorded in `index.json`.

## 1. Purpose, scope, and assumptions

Tiny Catalog lets a maintainer register and deactivate items. A maintainer or reader may retrieve and list them. No other actor may execute these cases.
The entire scope consists of the four use cases below. Internal steps are not
additional use cases.

**N-01:** retain a catalog item under an unambiguous code.
**N-02:** consult known items and identify which are currently available.
**N-03:** remove an item from availability without losing its current record.

**Actors:** ACT-CAT-M is the maintainer and may execute all four cases. ACT-CAT-R is the reader and may execute only UC-CAT-002 and UC-CAT-003. An absent, unknown, or unpermitted actor is denied before any read or write. How a channel authenticates a caller and resolves it to one of these roles is an interaction-boundary (L4) decision, recorded in the [ADIB contract](../OAL-P4/HTTP.md); this specification requires only that every request carries an authenticated actor identity from the permitted set.

The actor names above denote roles. A caller performs a role through an explicitly resolved context. This project requires authentication for all four cases and admits no anonymous role. A trusted invocation supplies the resolved context; each case evaluates its own role permission, including when another case invokes it.

**A-01 — checked:** a request has an authenticated actor in the permitted set for the requested case. A denied request has no domain or persistence effect.
**A-02:** the environment supplies functioning persistence and sufficient resources;
unavailability is nevertheless an explicit possible failure.

There is one catalog. Deletion, reactivation, renaming, prices, stock control,
user management, payments, event history, pagination, and multi-tenant operation are excluded.
A retained record is its current data, **not an audit/event history**.

## 2. Optional domain organization

**D-CAT — Catalog.** Responsible for item identity, availability, and retention.
All four use cases and both data entities belong to this domain. This is a
semantic grouping; it imposes no directory layout or inter-domain API.

## 3. Entities and validity conditions

**E-01 — Item key.** Identifies a record by `code`: a text of 1–24 characters drawn
only from `A–Z`, `0–9`, `_`, and `-`. Codes are exact and case-sensitive: no
normalization is promised; lowercase input is invalid.

**E-02 — Item.** Contains an E-01 code, a `name`, and an `active` flag. The name
contains 1–80 Unicode characters and at least one non-whitespace character.
Whitespace is preserved. The active flag is a boolean, not a numeric or textual
substitute. Each item has one E-01 code; uniqueness across retained items is the functional rule R-01, not an entity field condition.

Field validity is checked on assignment; an invalid assignment preserves the
previous field value. Field validation does not consult persistence, authorize
an operation, or decide an availability transition.

## 4. Shared rules

**R-01 — Unique retained code.** Registration cannot reuse a code already allocated
to any retained item, including an inactive item. Applied by UC-CAT-001.

**R-02 — Initial availability.** Successful registration creates an active item.
The caller does not choose its initial availability. Applied by UC-CAT-001.

**R-03 — Retention.** Deactivation changes availability, not identity or name,
and does not delete the record. Lookup may return active or inactive records.
Applied by UC-CAT-002 and UC-CAT-004.

**R-04 — Available listing.** Return only active items, ordered by ascending
ASCII code. An empty collection is a successful result. Applied by UC-CAT-003.

**R-05 — Repeated deactivation.** Deactivating an already inactive item succeeds
without changing its data. Applied by UC-CAT-004.

**R-06 — No implicit persistence through returned data.** Reading returns data
independent from the persisted state. Assigning to a returned entity does not
persist a change. Applied by UC-CAT-002 and supported by the persistence capability.

## 5. Shared obligations and outcomes

**P-01 — Persistence.** Registration must preserve unique codes atomically, even
when two requests use the same code concurrently. A successful write means the
storage mechanism has acknowledged it. Confirmed records remain readable after
normal application reconstruction with the same retained storage. No crash,
power-loss, remote replication, or backup-recovery guarantee is claimed.

**P-02 — Ownership and change.** Catalog is responsible for these records. Writes
are requested through the specified cases; reads do not implicitly update data.
Unknown code and unavailable persistence must remain distinguishable. No public
operation deletes or reactivates an item in this version.

**S-01 — Security and isolation.** Every case checks A-01: a request carries an authenticated actor identity from the permitted set, and denial precedes any domain or persistence effect. The authentication mechanism and network exposure — such as the HTTP Basic demonstration on loopback used by this example's channel — are L4 decisions documented in the [ADIB contract](../OAL-P4/HTTP.md), not requirements of this specification. Multi-tenant operation and internet-facing deployment remain outside this baseline.

**O-01 — Observable outcomes.** Success, invalid data, duplicate code, missing item,
and unavailable persistence are distinguishable as applicable. Failures must not
be represented as successful empty listings or confirmed writes.

**O-02 — Unconfirmed write.** On a persistence failure after a write is attempted,
the final write outcome may be unknown. Do not promise rollback merely from a
failure result. Once persistence is available, lookup can be used to check the
record before deciding whether to repeat the request. No automatic retry is required.

**Q-01 — Resources and performance.** Inputs obey the finite field constraints above.
Listing returns the complete available set: this example assumes a small catalog.
No latency, throughput, availability, or resource-capacity target is specified or
claimed. A production adoption must define the targets it actually requires.

**Outcome vocabulary:** `registered`, `found`, `listed`, `deactivated`,
`invalid_data`, `duplicate_item`, `item_not_found`, `persistence_unavailable`.
These identify meanings, not an HTTP protocol, exception representation, or schema.

## 6. Use cases

### UC-CAT-001 — Register item

**Permitted actors:** maintainer. All others are denied before effects.


**Objective / need:** retain a new available item; N-01.
**Trigger / context:** a maintainer requests registration in the single catalog.
**Inputs:** code and name. **Output:** the registered item.
**Entities / rules:** E-01, E-02; R-01, R-02.
**Assumed conditions:** A-01 and the scope assumptions.
**Checked conditions:** field validity, and whether the code is already allocated.
**Required capability:** atomically record a new item while preserving key uniqueness.
**Use-case dependencies:** none.

On valid data and an unused code, register the item as active and confirm its
record. A duplicate code rejects registration without overwriting the existing
item. Invalid fields reject registration before requesting a write. A resource
failure produces `persistence_unavailable`, subject to O-02, not a success result.

**Effects and guarantees:** one new retained record on success; existing records
unchanged on a duplicate rejection. P-01, P-02, S-01, O-01, O-02, and Q-01 apply.

**Acceptance criteria:**

- **AC-CAT-001-01:** valid registration returns the supplied code/name with active=true;
  a later lookup returns that record.
- **AC-CAT-001-02:** invalid input is rejected and creates no record.
- **AC-CAT-001-03:** a previously allocated code is rejected even if the existing item
  is inactive; its data remain unchanged.
- **AC-CAT-001-04:** two concurrent valid registrations for one unused code yield
  exactly one success and one duplicate rejection when persistence is available.
- **AC-CAT-001-05:** persistence unavailability is distinguishable from confirmed registration.
- **AC-CAT-001-06:** An absent or unpermitted actor is denied before any domain or persistence effect.

### UC-CAT-002 — Get item

**Permitted actors:** maintainer, reader. All others are denied before effects.


**Objective / need:** inspect a retained record; N-02.
**Trigger / context:** a permitted actor requests an item by code.
**Input:** code. **Output:** the item, irrespective of availability.
**Entities / rules:** E-01, E-02; R-03, R-06.
**Assumed conditions:** A-01. **Checked conditions:** code validity and record existence.
**Required capability:** retrieve a retained record by its code.
**Use-case dependencies:** none.

Return a found record independently of its active flag. Invalid code produces
`invalid_data`; a valid absent code produces `item_not_found`; unavailable
persistence produces `persistence_unavailable` rather than absence.

**Effects and guarantees:** no persisted change. P-02, S-01, O-01, and Q-01 apply.

**Acceptance criteria:**

- **AC-CAT-002-01:** active and inactive retained items are both retrievable with their data.
- **AC-CAT-002-02:** a valid absent code produces the missing-item outcome.
- **AC-CAT-002-03:** an invalid code is rejected as invalid data.
- **AC-CAT-002-04:** an unavailable lookup is not reported as a missing item.
- **AC-CAT-002-05:** changing returned data does not change the persisted record.
- **AC-CAT-002-06:** An absent or unpermitted actor is denied before any domain or persistence effect.

### UC-CAT-003 — List available items

**Permitted actors:** maintainer, reader. All others are denied before effects.


**Objective / need:** identify currently available records; N-02.
**Trigger / context:** a permitted actor requests the available catalog.
**Inputs:** none beyond context. **Output:** an ordered collection of items.
**Entities / rules:** E-02; R-04.
**Assumed conditions:** A-01. **Checked conditions:** availability of each returned item.
**Required capability:** retrieve retained item data.
**Use-case dependencies:** none.

Return the active records in ascending code order. Return an empty collection
when no records are available. Unavailable persistence is a failure, not an empty catalog.

**Effects and guarantees:** no persisted change. P-02, S-01, O-01, and Q-01 apply.

**Acceptance criteria:**

- **AC-CAT-003-01:** the result contains exactly the active items in the required order.
- **AC-CAT-003-02:** an empty catalog or one with only inactive items yields an empty collection.
- **AC-CAT-003-03:** persistence failure does not become a successful empty collection.
- **AC-CAT-003-04:** An absent or unpermitted actor is denied before any domain or persistence effect.

### UC-CAT-004 — Deactivate item

**Permitted actors:** maintainer. All others are denied before effects.


**Objective / need:** stop offering an item while retaining its record; N-03.
**Trigger / context:** a maintainer requests deactivation by code.
**Input:** code. **Output:** the retained inactive item.
**Entities / rules:** E-01, E-02; R-03, R-05.
**Assumed conditions:** A-01. **Checked conditions:** valid code, existence, and current availability.
**Required capability:** record the changed data for an existing item, without inserting a missing one.
**Use-case dependency:** UC-CAT-002 obtains the item and supplies its lookup outcomes.

An active item becomes inactive without losing its code/name. An inactive item
is returned successfully without an additional state change. Invalid code and
missing item retain their respective rejection outcomes. Failure of lookup or
persistence is distinguishable; unconfirmed writes follow O-02.

**Effects and guarantees:** only the active flag changes on successful transition.
Repeated deactivation does not erase data. P-01, P-02, S-01, O-01, O-02, and Q-01 apply.

**Acceptance criteria:**

- **AC-CAT-004-01:** the item becomes inactive, leaves the available listing, and stays retrievable.
- **AC-CAT-004-02:** repeating the request succeeds with the same retained data.
- **AC-CAT-004-03:** a missing record is rejected and not implicitly created.
- **AC-CAT-004-04:** invalid code is rejected as invalid data.
- **AC-CAT-004-05:** unavailable lookup or persistence cannot produce a false confirmation.
- **AC-CAT-004-06:** An absent or unpermitted actor is denied before any domain or persistence effect.

## 7. Central acceptance scenarios

The executable case checks are included **by reference** at [tests/p3](../tests/p3); the [ADVS map](../OAL-P2/advs/behavioral-tests.json) identifies the behavioral test for each case.
Each check carries acceptance
criterion identifiers. The readable contracts above remain the source of the
required behavior; execution setup is not part of those contracts.

**AC-SHARED-01 — shared retention integration criterion:** register an item, confirm its deactivation, end that application instance, and reconstruct the application with the same retained storage. Lookup returns the same code and name with `active=false`; the available listing excludes that item. This evaluates normal reconstruction, not a crash or power failure.

Its full canonical definition is the `shared_criteria` entry in [index.json](index.json). It spans UC-CAT-001 through UC-CAT-004 and obligations P-01/P-02. It is distinct from case-owned criteria and is supported by one shared verification linked to BT-CAT-001 through BT-CAT-004; it creates no additional use case or directly linked behavioral test.

The [index](index.json) identifies all four cases and all acceptance criteria.
A central suite is recommended, not necessary for a document to be classified as UCS.
Unit and integration tests are not included in this specification.

## 8. Traceability, status, and evolution

The complete baseline contains exactly UC-CAT-001 through UC-CAT-004. Each is to
correspond to exactly one implementation, with no undocumented architectural use
case. The [implementation correspondence](../OAL-P2/adpm/traceability.json) records that
link separately; it does not prescribe a UCS storage format.

All requirements above are baseline decisions for this educational project.
A-01/A-02 are assumptions; production hosting, account management, crash recovery,
performance targets, and deployment isolation are excluded or explicitly unspecified,
not silently implemented promises. A-01 requires an authenticated actor identity on
every request; the channel mechanism that supplies that identity is specified at the
interaction boundary, and its demonstration credentials are not a production account
system. There are no unresolved requirements for the four-case educational scope.

Version 0.1.0 introduced this scope. Version 0.2.0 adapts the specification to the
Alpha-v0.2.0-Alkimim edition: channel choices (authentication mechanism, loopback
exposure) are separated into L4 references, and the authentication wording of A-01/S-01
is harmonized with the exclusions above. A later version records changes to objectives,
outcomes, dependencies, and guarantees while preserving IDs where meaning is
preserved. An ID is not recycled for an unrelated objective. The English and
Portuguese texts are synchronized translations.
