# Work Board · P4 browser and HTTP boundary

[Português](HTTP.pt-br.md) · [P3](../OAL-P3/IMPLEMENTATION.md) · [Example](../README.md)

[`transport`](../src/work_board/transport) serves a local browser page and JSON API on `127.0.0.1`. The page, CSS, and JavaScript are public; API calls require demonstration HTTP Basic credentials. The adapter resolves a manager, contributor, or viewer role. Every callable case checks that role again. URLs, JSON, status codes, credentials, and browser controls are P4 decisions. The [bidirectional map](traceability.json) records their links to the six P3 case identities.

| Stimulus | Case | Success |
| --- | --- | --- |
| `POST /api/items` | UC-WB-001 | 201, new backlog item |
| `POST /api/items/{id}/assign` | UC-WB-002 | 200, assigned item |
| `POST /api/items/{id}/transition` | UC-WB-003 | 200, advanced item |
| `POST /api/items/{id}/comments` | UC-WB-004 | 201, new comment |
| `GET /api/items` with optional `project` or `status` | UC-WB-005 | 200, matching items |
| `GET /api/items/{id}/comments` | UC-WB-006 | 200, comments |

The creation form also refreshes the board, as do the assignment, advance, and comment controls. Thus each of these browser controls invokes its action case and then UC-WB-005; each API route invokes only the case shown above. The refresh control and initial page load invoke UC-WB-005. The comments control invokes UC-WB-006. Headings, messages, and static resources are interface-only elements.

The adapter returns 401 for missing credentials, 403 for denied cases, 400 for invalid requests or case data, 404 for absent items or routes, 409 for stale versions, and 503 for unavailable storage. JSON bodies are limited to 65,536 bytes. An empty `project` or `status` query value is rejected as invalid; clients omit the parameter when no filter is desired. The example is intended for loopback demonstration; it has no user administration or public deployment claim. [`tests/p4`](../tests/p4) checks this channel independently of the direct [P3 checks](../tests/p3).

## Unavailable result

Storage unavailability maps to HTTP 503 with `error: "unavailable"`, a stable message, and `write_outcome`. The value `not_applied` identifies a known pre-write failure or confirmed rollback; `unknown` means that the write result could not be confirmed. A client reloads and inspects current state before deciding to repeat an operation after `unknown`; receiving 503 alone does not establish absence of effects. An expected version beyond SQLite representation still maps to 409 for an existing item or 404 for an absent one.

The role string supplied as `principal` is the resolved actor context selected for this demonstration. HTTP Basic authenticates the caller at this boundary; every case retains its authorization decision.
