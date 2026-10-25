# Tiny Catalog — fronteira de interação P4

[English](HTTP.md) · [Início](../../../../../README.pt-br.md)

O adaptador P4 serve a página e a API HTTP em `127.0.0.1`. As quatro rotas de API exigem credenciais HTTP Basic. A fronteira de
entrada as resolve para o papel de mantenedor ou leitor; o caso verifica sua
permissão de forma independente. As senhas fixas de demonstração estão no README
do exemplo e podem ser substituídas por variáveis de ambiente. A página e os
arquivos estáticos carregam antes da autenticação; a primeira chamada de API
solicita as credenciais.

`GET /` serve a página do navegador. Seu CSS e JavaScript enviam solicitações
às quatro rotas de casos abaixo; não acrescentam operação de domínio.

- `POST /items` recebe exatamente `code` e `name` em um objeto JSON e invoca UC-CAT-001.
- `GET /items/{code}` invoca UC-CAT-002, inclusive para registros inativos.
- `GET /items` invoca UC-CAT-003 e retorna `{"items": [...]}`.
- `POST /items/{code}/deactivate` não recebe corpo e invoca UC-CAT-004.

Um item é representado como `{"code": "A", "name": "Pencil", "active": true}`.
O cadastro retorna 201; os demais sucessos, 200. Código duplicado retorna 409,
dados inválidos da entidade, 422, item ausente, 404, e persistência indisponível,
503. Credenciais ausentes ou inválidas retornam 401; um papel reconhecido sem
permissão retorna 403. A chamada recusada não lê nem altera registros do catálogo.
Entrada de transporte malformada retorna 400. Rotas desconhecidas retornam
404; métodos não aceitos em rotas conhecidas retornam 405. A demonstração não
promete todos os recursos de HTTP necessários em produção.

Corpos JSON têm limite de 16.384 bytes e devem declarar `Content-Length`.
Transferência em blocos não é aceita. Respostas de erro não incluem tracebacks nem
erros brutos do banco. Falhas técnicas são encaminhadas ao coletor de erros injetado.
O transporte não introduz uma API de domínio especial.

Uma resposta 503 durante uma escrita **não comprova reversão**. Após a recuperação,
consulte o registro antes de decidir se deve repetir o cadastro ou a desativação.

## Vínculos da interface

| Elemento da interface | Caso ADI invocado |
| --- | --- |
| Formulário de cadastro e atualização da lista | UC-CAT-001, seguido de UC-CAT-003 |
| `POST /items` | UC-CAT-001 |
| Formulário de consulta e `GET /items/{code}` | UC-CAT-002 |
| Carga inicial, botão Atualizar e `GET /items` | UC-CAT-003 |
| Botão Desativar e atualização da lista | UC-CAT-004, seguido de UC-CAT-003 |
| `POST /items/{code}/deactivate` | UC-CAT-004 |

No sentido inverso, UC-CAT-001 aparece no formulário e na rota de cadastro; UC-CAT-002, no formulário e na consulta por código; UC-CAT-003, na carga inicial e nas atualizações após cadastro, desativação ou clique em Atualizar; e UC-CAT-004, no botão do item e na rota de desativação. O botão de idioma, o conteúdo estático e as mensagens de estado pertencem apenas à interface. Não criam novos casos de uso.

## Verificação e escopo

As verificações de canal em [`tests/p4`](../tests/p4) exercitam interpretação do pedido, autenticação, códigos de resposta e resultados dos casos por HTTP. Sustentam este contrato local de WSGI e navegador, sem afirmar implantação pública nem cobertura de todo comportamento de acessibilidade. A [implementação P3](../OAL-P3/IMPLEMENTATION.pt-br.md) registra separadamente as chamadas diretas dos casos. A UCS foi consultada para resultados e permissões expostos; rotas, JSON e HTTP Basic são escolhas de P4.
