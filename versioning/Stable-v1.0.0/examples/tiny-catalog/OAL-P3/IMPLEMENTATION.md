# Tiny Catalog — ADI implementation

[Português](IMPLEMENTATION.pt-br.md) · [Home](../../../../../README.md)

Tiny Catalog implements its four [UCS](../OAL-P1/UCS.md) cases in Python, with SQLite storage. The [ADPM](../OAL-P2/adpm/MODEL.md) assigns their responsibilities, and the [case map](../OAL-P2/adpm/traceability.json) points to the classes that carry them out. [ADVS](../OAL-P2/advs/SCENARIOS.md) describes how to check the behavior. The [derivation record](../derivations.json) identifies the people and source baselines behind each transition. The core module set is `authorization.py`, `composition.py`, `entities/`, `errors.py`, `tools/`, and `usecases/`. `__main__.py` is the application initializer and `transport/` is the P4 boundary; both are outside the core scope and may import the WSGI adapter.

## Concrete boundaries

Cases in `src/tiny_catalog/usecases/` make domain decisions. Entities hold data and validation. Tool contracts are separate from SQLite mechanisms. Composition injects concrete storage and other collaborators. Every case checks its allowed actor set before reading or changing data. Missing identity and unknown roles fail closed.

The [P4 HTTP boundary](../OAL-P4/HTTP.md) authenticates the local actor and translates case outcomes into responses. It does not grant case permission. A direct call to a case still checks permission.

## Actor-context representation

This code organization represents an already resolved actor context by the `principal` role string (`maintainer` or `reader`). HTTP Basic resolves that role from credentials at P4. Trusted direct callers supply the resolved role themselves, including through `Application.for_actor`; the role argument is not itself a credential verifier. The case checks the role permission before effects, rejects `None` and unknown roles, and passes the same context to a called case, which authorizes independently. No anonymous role is admitted by these project contracts.

## Verification and limits

Unit checks target entities and pure tools; integration checks target SQLite tools; [`tests/p3`](../tests/p3) exercises actual cases, including direct denied calls. [ADVS scenarios](../OAL-P2/advs/SCENARIOS.md) define expected behavior and the [BT map](../OAL-P2/advs/behavioral-tests.json) groups supporting checks by case. HTTP checks run separately under [`tests/p4`](../tests/p4). The example does not claim internet-facing deployment or dynamic account administration.
