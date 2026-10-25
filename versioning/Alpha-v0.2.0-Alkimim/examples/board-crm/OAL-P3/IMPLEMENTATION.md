# Board CRM — ADI implementation

[Português](IMPLEMENTATION.pt-br.md) · [Home](../../../../../README.md)

Board CRM implements its six [UCS](../OAL-P1/UCS.tex) cases in Python, with SQLite storage. The [ADPM](../OAL-P2/adpm/MODEL.md) assigns their responsibilities, and the [case map](../OAL-P2/adpm/traceability.json) points to the classes that carry them out. [ADVS](../OAL-P2/advs/SCENARIOS.md) describes how to check the behavior. The [derivation record](../derivations.json) identifies the people and source baselines behind each transition. The core module set is `authorization.py`, `composition.py`, `entities.py`, `errors.py`, `tools/`, and `usecases/`. `__main__.py` is the application initializer and `transport/` is the P4 boundary; both are outside the core scope and may import the WSGI adapter.

## Concrete boundaries

Cases in `src/board_crm/usecases/` make domain decisions. Entities hold data and validation. Tool contracts are separate from SQLite mechanisms. Composition injects concrete storage and other collaborators. Each case checks its allowed actor set before reading or changing data. Missing identity and unknown roles fail closed.

The [P4 HTTP boundary](../OAL-P4/HTTP.md) authenticates the local actor and translates case outcomes into responses. It does not grant case permission. A direct call to a case still checks permission.

## Verification and limits

Unit checks target entities and pure tools; integration checks target SQLite tools; [`tests/p3`](../tests/p3) exercises actual cases, including direct denied calls. [ADVS scenarios](../OAL-P2/advs/SCENARIOS.md) define expected behavior and the [BT map](../OAL-P2/advs/behavioral-tests.json) groups supporting checks by case. HTTP checks run separately under [`tests/p4`](../tests/p4). The example does not claim internet-facing deployment or dynamic account administration.

## Actor context and channel verification

The `principal` role string is this code organization's representation of the resolved actor context. A trusted entry point authenticates the caller and establishes the role; direct callers have the same responsibility. Missing context and unknown or unpermitted roles are refused by the case. This example does not declare an anonymous actor.

The WSGI checks also cover unsupported media types and charsets, complete body framing, and accepted UTF-8 JSON requests. These are verifications of the interaction contract, not additional case identities or claims about browser JavaScript execution.
