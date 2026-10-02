# Work Board · fronteira P4 de navegador e HTTP

[English](HTTP.md) · [P3](../OAL-P3/IMPLEMENTATION.pt-br.md) · [Exemplo](../README.pt-br.md)

[`transport`](../src/work_board/transport) serve uma página local e uma API JSON em `127.0.0.1`. A página, o CSS e o JavaScript são públicos; chamadas à API exigem credenciais HTTP Basic de demonstração. O adaptador identifica o papel gestor, colaborador ou leitor. Cada caso invocável confere novamente esse papel. URLs, JSON, códigos de resposta, credenciais e controles do navegador são decisões de P4. O [mapa bidirecional](traceability.json) registra os vínculos com as seis identidades de casos P3.

| Estímulo | Caso | Sucesso |
| --- | --- | --- |
| `POST /api/items` | UC-WB-001 | 201, item novo no backlog |
| `POST /api/items/{id}/assign` | UC-WB-002 | 200, item atribuído |
| `POST /api/items/{id}/transition` | UC-WB-003 | 200, item avançado |
| `POST /api/items/{id}/comments` | UC-WB-004 | 201, comentário novo |
| `GET /api/items` com `project` ou `status` opcionais | UC-WB-005 | 200, itens correspondentes |
| `GET /api/items/{id}/comments` | UC-WB-006 | 200, comentários |

O formulário de criação também atualiza o quadro, assim como os controles de atribuição, avanço e comentário. Portanto, cada controle do navegador invoca seu caso de ação e depois UC-WB-005; cada rota API invoca somente o caso mostrado acima. Atualização manual e carregamento inicial invocam UC-WB-005. O controle de comentários invoca UC-WB-006. Cabeçalhos, mensagens e arquivos estáticos pertencem apenas à interface.

O adaptador retorna 401 para credenciais ausentes, 403 para casos negados, 400 para pedidos ou dados inválidos, 404 para itens ou rotas inexistentes e 409 para versões antigas. Corpos JSON têm limite de 65.536 bytes. O exemplo é destinado à demonstração local; não há administração de usuários nem declaração de implantação pública. [`tests/p4`](../tests/p4) verifica esse canal separadamente dos [testes diretos P3](../tests/p3).
