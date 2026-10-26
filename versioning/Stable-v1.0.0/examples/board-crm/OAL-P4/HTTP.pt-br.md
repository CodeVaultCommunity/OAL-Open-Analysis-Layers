# Board CRM — fronteira de interação P4

[English](HTTP.md) · [Início](../../../../../README.pt-br.md)

O servidor WSGI local escuta em `127.0.0.1`. Ele oferece um quadro no navegador e endpoints JSON. A página, o JavaScript e o CSS carregam sem login; os pedidos à API usam credenciais HTTP Basic de demonstração. P4 autentica o chamador e resolve seu contexto de ator como um identificador de papel gestor, operador ou leitor, passando esse contexto a P3. A autenticação é exigida por este exemplo; a string de papel é a representação de contexto escolhida. Cada caso ainda verifica sua própria permissão antes de ler ou alterar registros. A UCS forneceu os resultados e as regras de atores expostos; caminhos HTTP, JSON e página são decisões de P4.

| Rota e estímulo | Caso P3 | Sucesso |
| --- | --- | --- |
| `POST /api/opportunities` com título, empresa e responsável | UC-CRM-001 | 201 e cartão criado |
| `POST /api/opportunities/{id}/move` com etapa e versão esperada | UC-CRM-002 | 200 e cartão atualizado |
| `POST /api/opportunities/{id}/notes` com texto e versão esperada | UC-CRM-003 | 200 e ID/versão da nota |
| `GET /api/board`, opcionalmente com filtro exato `owner` | UC-CRM-004 | 200 e cinco colunas |
| `POST /api/opportunities/{id}/close-won` com motivo e versão esperada | UC-CRM-005 | 200 e cartão atualizado |
| `POST /api/opportunities/{id}/close-lost` com motivo e versão esperada | UC-CRM-006 | 200 e cartão atualizado |

O formulário de criação invoca UC-CRM-001 e depois UC-CRM-004 para atualizar o quadro. O seletor de etapa e a ação de arrastar invocam UC-CRM-002, seguidos de UC-CRM-004. O formulário de nota invoca UC-CRM-003 e depois UC-CRM-004. Carga inicial, filtro por responsável e botão Atualizar invocam UC-CRM-004. Os botões Ganha e Perdida invocam, respectivamente, UC-CRM-005 e UC-CRM-006, seguidos de UC-CRM-004. No sentido inverso, esses são os elementos que expõem cada um dos seis casos. A troca de idioma também invoca UC-CRM-004 para atualizar o quadro; os títulos, as mensagens de estado e os arquivos estáticos pertencem apenas à interface. A rota de criação registra o `owner` do payload como autor do evento de criação; as rotas de movimentação, nota e encerramento registram o principal autenticado como autor do evento. O principal autenticado e o responsável comercial são noções distintas.

**Origem das obrigações do canal.** O requisito de que cada caso recuse um ator sem permissão antes dos efeitos é herdado da UCS Q-01; o caso decide a permissão. Vincular a demonstração a `127.0.0.1` e autenticar as requisições da API com credenciais HTTP Basic de demonstração são decisões de L4 registradas como Q-07. A alternativa sem arrastar exigida pela UCS Q-06 é implementada pelo seletor de etapa registrado como Q-08; o seletor invoca UC-CRM-002 e depois UC-CRM-004, e não introduz nova regra de negócio. A troca de idioma é um controle de L4 que invoca UC-CRM-004 para atualizar o quadro. Nenhuma dessas decisões de L4 transforma o requisito de caso subjacente em restrição externa, e nenhuma altera a autoridade do caso sobre sua própria autorização.

Pedidos JSON podem conter de 1 a 65.536 bytes. Um valor vazio do filtro `owner` é um filtro exato que não corresponde a nenhum cartão; os clientes omitem o parâmetro quando não desejam filtrar. A API retorna `authentication_required` como 401, `access_denied` como 403, dados inválidos do caso como 400, cartão ausente como 404, versão obsoleta como 409 e armazenamento indisponível como 503. Os resultados dos casos são representados em JSON; a presença de um controle no navegador não concede acesso. Rotas desconhecidas retornam 404. O exemplo não declara implantação em produção, administração de usuários nem auditoria completa de acessibilidade.

[`tests/p4`](../tests/p4) verifica rota HTTP local, autenticação, permissão, conflito e representação. As verificações diretas de casos e armazenamento ficam em [`tests/p3`](../tests/p3), `tests/unit` e `tests/integration`. A suíte executada sustenta apenas a configuração examinada; cenários ADVS planejados não são evidência automática.

## Representação JSON e enquadramento do corpo

**CH-CRM-JSON — decisão de representação L4.** Um pedido POST declara `Content-Type: application/json` e contém um objeto JSON em UTF-8. A comparação de tipo de mídia e codificação ignora maiúsculas e minúsculas; o charset opcional pode ser `utf-8` ou `utf8`. Outros parâmetros do tipo de mídia não alteram a representação UTF-8 escolhida. Tipo de mídia ausente ou tipo de mídia ou charset não admitido recebe HTTP 415 com `error: "unsupported_media_type"`, antes da invocação de qualquer caso. A ausência do parâmetro charset é admitida e mantém UTF-8.

**CH-CRM-FRAMING — decisão de enquadramento L4.** O corpo tem `Content-Length` declarado entre 1 e 65.536 bytes. A fronteira lê esse comprimento e verifica o recebimento de todos os bytes declarados. Comprimento ausente ou inválido, corpo incompleto, UTF-8/JSON inválido, valor que não seja objeto ou codificação de transferência não suportada por este adaptador WSGI local recebe HTTP 400. O adaptador não decodifica corpos com `Transfer-Encoding`. Essas recusas de representação não produzem escrita de domínio.

`LocalBoardScenario.test_json_media_type_and_charset` verifica as recusas 415 e a aceitação de JSON UTF-8. `LocalBoardScenario.test_incomplete_and_unsupported_framing_are_rejected_without_creation` verifica recusas de enquadramento e quadro inalterado. Ambas estão em [`tests/p4/test_http_board.py`](../tests/p4/test_http_board.py).
