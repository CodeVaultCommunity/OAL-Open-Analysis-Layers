# Board CRM — P4 interaction boundary

[Português](HTTP.pt-br.md) · [Home](../../../../../README.md)

The local WSGI server binds to `127.0.0.1`. It serves a browser board and JSON endpoints. The page, JavaScript, and CSS load without a login; API requests use demonstration HTTP Basic credentials. P4 authenticates the caller and resolves its actor context to a manager, operator, or viewer role identifier, then passes that context to P3. Authentication is required by this example; the role string is its chosen context representation. Each use case still checks its own permission before reading or changing records. The L1 contract supplied the exposed outcomes and actor rules; HTTP paths, JSON, and the page are P4 decisions.

| Route and stimulus | P3 case | Success |
| --- | --- | --- |
| `POST /api/opportunities` with title, company, owner | UC-CRM-001 | 201 and created card |
| `POST /api/opportunities/{id}/move` with stage and expected version | UC-CRM-002 | 200 and updated card |
| `POST /api/opportunities/{id}/notes` with body and expected version | UC-CRM-003 | 200 and note ID/version |
| `GET /api/board`, optionally with exact `owner` filter | UC-CRM-004 | 200 and five columns |
| `POST /api/opportunities/{id}/close-won` with reason and expected version | UC-CRM-005 | 200 and updated card |
| `POST /api/opportunities/{id}/close-lost` with reason and expected version | UC-CRM-006 | 200 and updated card |

The browser creation form invokes UC-CRM-001 and then UC-CRM-004 to refresh. The stage selector and drag-and-drop both invoke UC-CRM-002, followed by UC-CRM-004. The note form invokes UC-CRM-003, then UC-CRM-004. Initial load, owner filter, and refresh invoke UC-CRM-004. The Won and Lost buttons invoke UC-CRM-005 and UC-CRM-006 respectively, then UC-CRM-004. In reverse, those are the interface elements exposing each of the six cases. The language switch also invokes UC-CRM-004 to refresh the board; headings, status messages, and static resources belong only to the interface. The creation route records the payload `owner` as the author of the creation event; move, note, and close routes record the authenticated principal as the event author. The authenticated principal and the commercial owner are different notions.

**Origin of the channel obligations.** The requirement that each case denies an unpermitted actor before effects is inherited from UCS Q-01; the case decides permission. Binding the demonstration to `127.0.0.1` and authenticating API requests with HTTP Basic demonstration credentials are L4 decisions recorded as Q-07. The non-drag alternative required by UCS Q-06 is implemented by the stage selector recorded as Q-08; the selector invokes UC-CRM-002 and then UC-CRM-004, and it introduces no new business rule. The language switch is an L4 control that invokes UC-CRM-004 to refresh the board. None of these L4 decisions turns the underlying case requirement into an external constraint, and none changes the case's authority over its own authorization.

JSON requests may contain 1–65,536 bytes. An empty `owner` query value is an exact filter that matches no card; clients omit the parameter when no filter is desired. The API returns `authentication_required` as 401, `access_denied` as 403, invalid case data as 400, absent cards as 404, stale versions as 409, and unavailable storage as 503. The case result is represented in JSON; a denied caller does not gain access because a browser control is visible. Unknown routes return 404. The example does not claim production deployment, user administration, or a complete accessibility audit.

[`tests/p4`](../tests/p4) exercises the local HTTP route, authentication, permission, conflict, and representation paths. Direct case and storage checks are recorded under [`tests/p3`](../tests/p3), `tests/unit`, and `tests/integration`. The executed suite supports only the checked configuration and does not turn planned ADVS scenarios into automatic evidence.

## JSON representation and framing

**CH-CRM-JSON — L4 representation decision.** A POST request declares `Content-Type: application/json` and contains a UTF-8 JSON object. Media type and charset matching is case-insensitive; the optional charset may be `utf-8` or `utf8`. Other media-type parameters do not change the selected UTF-8 representation. An absent media type or an unsupported media type or charset receives HTTP 415 with `error: "unsupported_media_type"`, before any case is invoked. Omitting the charset parameter is allowed and retains UTF-8.

**CH-CRM-FRAMING — L4 framing decision.** The body has a declared `Content-Length` of 1–65,536 bytes. The boundary reads that length and verifies that it received all declared bytes. Missing or invalid length, an incomplete body, invalid UTF-8/JSON, a non-object value, or transfer encoding unsupported by this local WSGI adapter receives HTTP 400. The adapter does not decode `Transfer-Encoding` bodies. These representation refusals produce no domain write.

`LocalBoardScenario.test_json_media_type_and_charset` verifies 415 refusals and accepted UTF-8 JSON. `LocalBoardScenario.test_incomplete_and_unsupported_framing_are_rejected_without_creation` verifies framing refusals and an unchanged board. Both checks are in [`tests/p4/test_http_board.py`](../tests/p4/test_http_board.py).
