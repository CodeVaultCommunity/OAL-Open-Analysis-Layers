# Board CRM — P4 interaction boundary

[Português](HTTP.pt-br.md) · [Home](../../../../../README.md)

The local WSGI server binds to `127.0.0.1`. It serves a browser board and JSON endpoints. The page, JavaScript, and CSS load without a login; API requests use demonstration HTTP Basic credentials. P4 resolves the caller to a manager, operator, or viewer and passes that identity to P3. Each use case still checks its own permission before reading or changing records. The L1 contract supplied the exposed outcomes and actor rules; HTTP paths, JSON, and the page are P4 decisions.

| Route and stimulus | P3 case | Success |
| --- | --- | --- |
| `POST /api/opportunities` with title, company, owner | UC-CRM-001 | 201 and created card |
| `POST /api/opportunities/{id}/move` with stage and expected version | UC-CRM-002 | 200 and updated card |
| `POST /api/opportunities/{id}/notes` with body and expected version | UC-CRM-003 | 200 and note ID/version |
| `GET /api/board`, optionally with exact `owner` filter | UC-CRM-004 | 200 and five columns |
| `POST /api/opportunities/{id}/close-won` with reason and expected version | UC-CRM-005 | 200 and updated card |
| `POST /api/opportunities/{id}/close-lost` with reason and expected version | UC-CRM-006 | 200 and updated card |

The browser creation form invokes UC-CRM-001 and then UC-CRM-004 to refresh. The stage selector and drag-and-drop both invoke UC-CRM-002, followed by UC-CRM-004. The note form invokes UC-CRM-003, then UC-CRM-004. Initial load, owner filter, and refresh invoke UC-CRM-004. The Won and Lost buttons invoke UC-CRM-005 and UC-CRM-006 respectively, then UC-CRM-004. In reverse, those are the interface elements exposing each of the six cases. The language switch, headings, status messages, and static resources belong only to the interface.

JSON requests may contain 1–65,536 bytes. The API returns `authentication_required` as 401, `access_denied` as 403, invalid case data as 400, absent cards as 404, stale versions as 409, and unavailable storage as 503. The case result is represented in JSON; a denied caller does not gain access because a browser control is visible. Unknown routes return 404. The example does not claim production deployment, user administration, or a complete accessibility audit.

[`tests/p4`](../tests/p4) exercises the local HTTP route, authentication, permission, conflict, and representation paths. Direct case and storage checks are recorded under [`tests/p3`](../tests/p3), `tests/unit`, and `tests/integration`. The executed suite supports only the checked configuration and does not turn planned ADVS scenarios into automatic evidence.
