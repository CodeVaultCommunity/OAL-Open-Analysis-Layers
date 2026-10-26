# Tool contracts — example implementation documentation

[Português](tool-contracts.pt-br.md) · [Home](../../../../../../README.md)

These are code-facing contracts, **not mandatory sections or tool names in a UCS**.

## ItemStore

`insert(item)` returns an independent retained item after acknowledged commit, or
raises StoreConflict for an allocated code. It must atomically preserve uniqueness;
"check then insert" without an atomic guarantee is insufficient. It never replaces
an existing record. The use case assigns the business meaning to StoreConflict.

`get(code)` returns a detached Item or None. `list_all()` returns detached records,
without applying the available-only policy or ordering required by the case.
Neither operation changes persisted data. StoreUnavailable is not a missing record
or an empty successful collection.

`replace(item)` updates an existing code and acknowledges the write; StoreMissing
indicates absence. It does not insert, authorize, decide transitions, or retry.

All operations may raise StoreUnavailable. A failure around a write does not
establish whether the write was committed. The memory substitute implements the
operation shapes and within-test record behavior, **not the durable production
profile**. Its limited scope is explicit in the behavioral execution configuration.

## RecordCodec

`encode(item)` produces detached code/name/integer-flag data. `decode(record)`
returns a validated entity. Invalid data are rejected rather than silently coerced.
The concrete codec consumes only an injected entity constructor, not another tool
or an external service.

## ConnectionProvider

`open()` returns a fresh database connection. The consuming store owns closing it
and manages the transaction. The selected implementation receives the driver
factory, path, and timeout through injection. It does not select business policy.

## Use-case composition

ItemLookup is the callable contract of UC-CAT-002 consumed by UC-CAT-004.
It is **not a tool or a fifth use case**. Its concrete injected value is the already
constructed GetItem instance. Interfaces are declarations, not extra implementations.


## Ready entities and contextual checks

`insert(item)` and `replace(item)` receive a ready `Item`. By contract the entity already satisfies its internal coherence conditions $I_E$; the store must not call the entity validation again or implement an equivalent copy of the field checks. For `ItemKey`, $I_{\mathrm{ItemKey}}(k)$ covers the code's own format and normalization rules; it does not include the presence of other retained items. The contextual condition $Q_{\mathrm{insert}}(k, S) \iff \neg\exists x \in S:\, x.\mathrm{code} = k.\mathrm{code}$ depends on the retained set $S$; the store enforces it atomically. $Q_{\mathrm{insert}}$ is not part of $I_{\mathrm{ItemKey}}$ and does not authorize revalidating entity fields. The store also evaluates the existence of the record for `replace` and storage availability — conditions whose object, purpose, and responsibility are distinct from entity coherence. `decode(record)` is the representation boundary: it may reject malformed raw data, but when it constructs an `Item` it uses the entity's canonical construction and validation. Entity validation does not replace the store's atomic guarantees, and the store does not replace entity validity.
