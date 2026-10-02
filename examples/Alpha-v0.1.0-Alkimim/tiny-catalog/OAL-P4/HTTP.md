# Tiny Catalog — P4 interaction boundary

[Português](HTTP.pt-br.md) · [Home](../../../../README.md)

The P4 adapter serves the browser and HTTP API on `127.0.0.1`.
The four API routes require HTTP Basic credentials. The entry boundary resolves
them to a maintainer or reader role; the use case independently checks its
permission. The fixed default passwords are documented in the example README
and can be replaced with environment variables. The page and static files can
be loaded before authentication; the first API request prompts for credentials.

`GET /` serves the browser page. Its CSS and JavaScript submit requests to the
four case routes below; they add no domain operation.

- `POST /items` consumes exactly `code` and `name` in a JSON object; invokes UC-CAT-001.
- `GET /items/{code}` invokes UC-CAT-002, including inactive records.
- `GET /items` invokes UC-CAT-003; returns `{"items": [...]}`.
- `POST /items/{code}/deactivate` takes no body and invokes UC-CAT-004.

An item is represented as `{"code": "A", "name": "Pencil", "active": true}`.
Registration returns 201, other successes 200. Duplicate code returns 409,
invalid entity data 422, absent item 404, and unavailable persistence 503.
Missing or invalid credentials return 401; a recognized but unpermitted role
returns 403. A rejected call does not read or change catalog records.
Malformed transport input returns 400. Unknown routes return 404; unsupported
methods on known routes return 405. The demonstration does not promise a full
production HTTP feature set.

JSON request bodies are limited to 16,384 bytes and must declare Content-Length.
Chunked transfer is not supported. Error responses do not include tracebacks or
raw database errors. Technical failures are reported to the injected error sink.
No special domain API is introduced to support this transport.

A 503 on a write is **not proof of rollback**. Recover and consult the record before
assuming whether a repeated registration/deactivation is needed.

## Interface links

| Interface element | ADI case invoked |
| --- | --- |
| Registration form and its refresh | UC-CAT-001, then UC-CAT-003 |
| `POST /items` | UC-CAT-001 |
| Lookup form and `GET /items/{code}` | UC-CAT-002 |
| Initial catalog load, refresh button, and `GET /items` | UC-CAT-003 |
| Item deactivate button and its refresh | UC-CAT-004, then UC-CAT-003 |
| `POST /items/{code}/deactivate` | UC-CAT-004 |

In the reverse direction, UC-CAT-001 is exposed by the registration form and POST route; UC-CAT-002 by the lookup form and GET-by-code route; UC-CAT-003 by initial load, refresh, post-registration refresh, and post-deactivation refresh; and UC-CAT-004 by the item button and deactivate route. The language button, static content, and status messages are interface-only elements. They do not create additional use cases.

## Verification and scope

The channel checks in [`tests/p4`](../tests/p4) exercise request parsing, authentication, status mapping, and case results over HTTP. They support this local WSGI and browser contract, not a claim about public deployment or every accessibility behavior. The [P3 implementation](../OAL-P3/IMPLEMENTATION.md) records direct case checks separately. The L1 contract was consulted for exposed outcomes and permissions; the choice of routes, JSON, and HTTP Basic belongs to P4.
