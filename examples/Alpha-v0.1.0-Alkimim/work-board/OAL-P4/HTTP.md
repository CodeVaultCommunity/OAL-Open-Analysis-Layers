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

The adapter returns 401 for missing credentials, 403 for denied cases, 400 for invalid requests or case data, 404 for absent items or routes, and 409 for stale versions. JSON bodies are limited to 65,536 bytes. The example is intended for loopback demonstration; it has no user administration or public deployment claim. [`tests/p4`](../tests/p4) checks this channel independently of the direct [P3 checks](../tests/p3).
