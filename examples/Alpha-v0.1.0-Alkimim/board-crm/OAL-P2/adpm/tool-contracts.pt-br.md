# Contrato da ferramenta de armazenamento do Board CRM

[English](tool-contracts.md) · [Início](../../../../../README.pt-br.md)

`Store` em [contracts.py](../../src/board_crm/tools/contracts.py) é o limite usado
pelos seis casos. [SQLiteStore](../../src/board_crm/tools/sqlite_store.py) é uma
implementação. As classes de casos recebem um `Store`, não uma conexão SQLite.

## Operações e garantias

| Operação | Resultado | Efeito e garantia |
| --- | --- | --- |
| `create(card, actor)` | Nenhum | Adiciona oportunidade e evento de criação numa transação. ID repetido gera `Conflict`. |
| `get(id)` | Opportunity | Lê uma entidade independente. ID desconhecido gera `Missing`. |
| `mutate(id, expected_version, time, actor, ...)` | Opportunity alterada | Compara versões atomicamente; altera o cartão e acrescenta nota e/ou evento na mesma transação. Versão desatualizada gera `Conflict` sem alteração parcial. |
| `list_records()` | Oportunidades com notas e eventos | Retorna entidades independentes. Agrupamento, filtro por responsável e ordem dos cartões são decisões de `ViewBoard`. |

Falhas de armazenamento geram `Unavailable`. Um caso só informa sucesso depois
que a transação é confirmada. Como no Tiny Catalog, um resultado de
indisponibilidade durante uma gravação incerta não prova que nada foi gravado.

`IdentifierProvider` retorna um ID opaco e não vazio. `Clock` retorna um horário
com fuso e ordem lexical. Ambos os contratos estão em `tools/contracts.py`;
suas implementações locais estão em `tools/providers.py`. A ferramenta de
armazenamento não os chama nem seleciona etapas permitidas. As decisões de
etapa ficam nos casos de uso; os limites dos textos, nas entidades.

## Índice da documentação

[Implementação](../../OAL-P3/IMPLEMENTATION.pt-br.md) · [Rastreabilidade](traceability.json) ·
[JSON da UCS](../../OAL-P1/ucs.json) · [README do exemplo](../../README.pt-br.md)
