# Tiny Catalog · OAL Alpha-v0.1.0-Alkimim example

[Português](README.pt-br.md) · [Home](../../../README.md)

Tiny Catalog stores items by code. Its four cases register, retrieve, list, and deactivate them. Deactivation keeps the record, and SQLite prevents two concurrent registrations from taking the same code.

## UCS and permissions

The [UCS](OAL-P1/UCS.md) gives maintainers all four cases and readers the retrieve and list cases. Each case checks permission before touching catalog data, including when it is called without HTTP.

## OAL artifacts

- [Reconstructed needs baseline](needs-baseline.json) and [UCS](OAL-P1/UCS.md) in OAL-P1.
- [ADPM program model](OAL-P2/adpm/MODEL.md), [tool contracts](OAL-P2/adpm/tool-contracts.md), and [case map](OAL-P2/adpm/traceability.json).
- [ADVS verification scenarios](OAL-P2/advs/SCENARIOS.md) and [behavioral test identities](OAL-P2/advs/behavioral-tests.json).
- [ADI implementation decisions](OAL-P3/IMPLEMENTATION.md) and [case checks](tests/p3).
- [ADIB HTTP contract](OAL-P4/HTTP.md), [interface map](OAL-P4/traceability.json), and [channel checks](tests/p4).
- [Named derivations](derivations.json) for the five transitions.

In code, [`usecases`](src/tiny_catalog/usecases) makes catalog decisions, [`entities`](src/tiny_catalog/entities) validates item data, [`tools`](src/tiny_catalog/tools) defines and implements storage, and [`composition.py`](src/tiny_catalog/composition.py) connects them. HTTP authentication, routes, JSON, and browser files live in [`transport`](src/tiny_catalog/transport). The [repository validator](../../validate_oal.py) checks that the core does not import P4.

## Run in a browser

With Python 3.12 or later, run from the repository root:

```bash
python examples/run_examples.py tiny-catalog
```

The launcher opens `http://127.0.0.1:8000/`. The browser requests HTTP Basic credentials on the first API call. Use `maintainer` / `maintainer-demo` or `reader` / `reader-demo`. To switch accounts, use another private browser session or clear the stored credentials. Defaults can be changed with `OAL_CATALOG_<ROLE>_PASSWORD` environment variables. The demonstration binds to loopback; its fixed example passwords are for local use.

Stop the server with Ctrl+C. The [examples guide](../../README.md#run-an-example) explains the launcher options.

## Verification

Install the example's `test` extra and run `python -m pytest` from this directory. The suite covers entities, SQLite tools, use cases, authorization, and the local HTTP adapter. A passing run describes the scenarios and environment exercised.

## Documentation index

[OAL Alpha-v0.1.0-Alkimim](../../../versioning/Alpha-v0.1.0-Alkimim.md) · [Examples](../../README.md) · [UCS](OAL-P1/UCS.md) · [ADPM](OAL-P2/adpm/MODEL.md) · [ADVS](OAL-P2/advs/SCENARIOS.md) · [ADI](OAL-P3/IMPLEMENTATION.md) · [ADIB](OAL-P4/HTTP.md)
