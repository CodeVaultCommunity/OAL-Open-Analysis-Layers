# Board CRM — fronteira de interação P4

[English](HTTP.md) · [Início](../../../../../README.pt-br.md)

O servidor WSGI local escuta em `127.0.0.1`. Ele oferece um quadro no navegador e endpoints JSON. A página, o JavaScript e o CSS carregam sem login; os pedidos à API usam credenciais HTTP Basic de demonstração. P4 resolve o chamador como gestor, operador ou leitor e passa essa identidade a P3. Cada caso ainda verifica sua própria permissão antes de ler ou alterar registros. A UCS forneceu os resultados e as regras de atores expostos; caminhos HTTP, JSON e página são decisões de P4.

| Rota e estímulo | Caso P3 | Sucesso |
| --- | --- | --- |
| `POST /api/opportunities` com título, empresa e responsável | UC-CRM-001 | 201 e cartão criado |
| `POST /api/opportunities/{id}/move` com etapa e versão esperada | UC-CRM-002 | 200 e cartão atualizado |
| `POST /api/opportunities/{id}/notes` com texto e versão esperada | UC-CRM-003 | 200 e ID/versão da nota |
| `GET /api/board`, opcionalmente com filtro exato `owner` | UC-CRM-004 | 200 e cinco colunas |
| `POST /api/opportunities/{id}/close-won` com motivo e versão esperada | UC-CRM-005 | 200 e cartão atualizado |
| `POST /api/opportunities/{id}/close-lost` com motivo e versão esperada | UC-CRM-006 | 200 e cartão atualizado |

O formulário de criação invoca UC-CRM-001 e depois UC-CRM-004 para atualizar o quadro. O seletor de etapa e a ação de arrastar invocam UC-CRM-002, seguidos de UC-CRM-004. O formulário de nota invoca UC-CRM-003 e depois UC-CRM-004. Carga inicial, filtro por responsável e botão Atualizar invocam UC-CRM-004. Os botões Ganha e Perdida invocam, respectivamente, UC-CRM-005 e UC-CRM-006, seguidos de UC-CRM-004. No sentido inverso, esses são os elementos que expõem cada um dos seis casos. A troca de idioma, os títulos, as mensagens de estado e os arquivos estáticos pertencem apenas à interface.

Pedidos JSON podem conter de 1 a 65.536 bytes. A API retorna `authentication_required` como 401, `access_denied` como 403, dados inválidos do caso como 400, cartão ausente como 404, versão obsoleta como 409 e armazenamento indisponível como 503. Os resultados dos casos são representados em JSON; a presença de um controle no navegador não concede acesso. Rotas desconhecidas retornam 404. O exemplo não declara implantação em produção, administração de usuários nem auditoria completa de acessibilidade.

[`tests/p4`](../tests/p4) verifica rota HTTP local, autenticação, permissão, conflito e representação. As verificações diretas de casos e armazenamento ficam em [`tests/p3`](../tests/p3), `tests/unit` e `tests/integration`. A suíte executada sustenta apenas a configuração examinada; cenários ADVS planejados não são evidência automática.
