# Board CRM — especificação de verificação ADVS

[English](SCENARIOS.md) · [Início](../../../../../../README.pt-br.md)

**Origem:** [UCS do projeto](../../OAL-P1/ucs.json), versão 0.2.0.
**Classificação:** artefato de projeto do componente de verificação da L2 (ADVS) sob o OAL Alpha-v0.2.0-Alkimim; instanciando OAL-EX-M2-PROGRAM-SCENARIOS 0.1.0; consulte `model-instances.json` para a declaração da instância. Estes são cenários planejados; a presença de arquivos de teste não demonstra que eles foram executados.
**Registro de derivação:** [derivations.json](../../derivations.json). Estes são cenários planejados; as verificações diretas dos casos estão em [`tests/p3`](../../tests/p3), e as de canal em [`tests/p4`](../../tests/p4).

## Um teste comportamental por caso

O [mapa dos testes comportamentais](behavioral-tests.json) define BT-CRM-001 a BT-CRM-006, cada qual vinculado diretamente a um único caso UCS. Cada BT é um teste lógico composto pelas verificações executáveis de apoio indicadas. Seu resultado só é aprovado numa execução relatada quando todas essas verificações passam nessa execução. Os cenários por critério abaixo apoiam o BT do respectivo caso; a verificação compartilhada de permissão apoia os seis sem criar outro teste comportamental diretamente vinculado.

## Famílias de cenários

| ID | Casos | Ator e ação | Resultado esperado |
| --- | --- | --- | --- |
| VS-01 | UC-CRM-001, UC-CRM-002, UC-CRM-003, UC-CRM-004, UC-CRM-005, UC-CRM-006 | Ator permitido envia pedido válido | Resultado e efeitos especificados |
| VS-02 | UC-CRM-001, UC-CRM-002, UC-CRM-003, UC-CRM-004, UC-CRM-005, UC-CRM-006 | Identidade ausente envia pedido | Falha de autenticação; nenhum efeito de domínio ou persistência |
| VS-03 | UC-CRM-001, UC-CRM-002, UC-CRM-003, UC-CRM-005, UC-CRM-006 | Ator conhecido sem permissão envia pedido | Acesso negado; nenhum efeito de domínio ou persistência. Não aplicável a UC-CRM-004: $F_u = A \setminus A_u$ é vazio porque os três papéis conhecidos podem consultar o quadro. |
| VS-04 | UC-CRM-001, UC-CRM-002, UC-CRM-003, UC-CRM-004, UC-CRM-005, UC-CRM-006 | Ator permitido envia dados inválidos | Falha de validação prevista; nenhum efeito indevido |
| VS-05 | UC-CRM-001, UC-CRM-002, UC-CRM-003, UC-CRM-004, UC-CRM-005, UC-CRM-006 | Falha de persistência ou limite de versão | Falha prevista; nenhum sucesso falso |

Cada critério de aceite preserva seu ID da UCS nas verificações executáveis voltadas aos casos. Verificações unitárias cobrem entidades e ferramentas puras elegíveis; as de integração cobrem ferramentas concretas. Os cenários de permissão também chamam casos diretamente, portanto esconder um controle no navegador não os satisfaz.

## Preparação dos cenários por caso

| Caso | Ator permitido e ação | Estado inicial e limite observado |
| --- | --- | --- |
| UC-CRM-001 | Operador ou gestor cria cartão. | Começar com quadro vazio; usar campos válidos, vazios ou longos demais; inspecionar cartão persistido e evento inicial. |
| UC-CRM-002 | Operador ou gestor move cartão. | Preparar etapa NEW, QUALIFIED, PROPOSAL ou encerrada e versão atual ou obsoleta; inspecionar etapa, versão e histórico. |
| UC-CRM-003 | Operador ou gestor registra nota. | Preparar cartão ativo ou encerrado com versão conhecida; usar texto válido ou inválido; inspecionar nota e versão. |
| UC-CRM-004 | Leitor, operador ou gestor consulta quadro. | Preparar cartões em todas as etapas e com responsáveis distintos; inspecionar colunas, filtro exato e ordem determinística. |
| UC-CRM-005 | Gestor encerra como WON. | Preparar etapa PROPOSAL, anterior ou encerrada; inspecionar nota de motivo, evento, versão e efeitos da recusa. |
| UC-CRM-006 | Gestor encerra como LOST. | Preparar cada etapa ativa, etapa encerrada ou versão obsoleta; inspecionar nota de motivo, evento, versão e efeitos da recusa. |

Para cada caso, repetir a solicitação com identidades ausente e desconhecida. Repetir com ator reconhecido sem permissão apenas quando $F_u = A \setminus A_u$ não for vazio; quando $F_u$ for vazio, registrar o cenário como não aplicável com essa justificativa. Conferir que a recusa ocorre antes da validação e do armazenamento. Usar SQLite para verificar efeitos atômicos e chamar o caso diretamente e pelo transporte do navegador. O mapa abaixo fornece o resultado específico esperado para cada preparação.

## Cenários de canal (decisões de L4)

| Cenário | Obrigação ou decisão | Observação esperada | Verificação planejada |
| --- | --- | --- | --- |
| CS-01 | Q-07 | Requisição sem credenciais recebe 401; credenciais de demonstração válidas resolvem o chamador e o caso ainda confere a permissão. | `tests/p4/test_http_board.py` |
| CS-02 | Q-06 / Q-08 | O seletor de etapa realiza uma movimentação válida por UC-CRM-002 e atualiza por UC-CRM-004 sem acrescentar regra de negócio. | `tests/p4/test_http_board.py`; revisão manual da interface |
| CS-03 | Q-01 herdada; UC-CRM-004 | Trocar o idioma atualiza o quadro por UC-CRM-004; um chamador negado não altera nada. | `tests/p4/test_http_board.py` |
| CS-04 | Q-06 | A movimentação é acessível sem arrastar e soltar. | Revisão manual da interface |
| CS-05 | CH-CRM-JSON (L4) | Tipo de mídia não admitido ou ausente, ou charset não admitido, produz 415 sem criação; JSON UTF-8 continua aceito. | `tests/p4/test_http_board.py::LocalBoardScenario.test_json_media_type_and_charset` |
| CS-06 | CH-CRM-FRAMING (L4) | Corpo incompleto, comprimento inválido ou enquadramento de transferência não suportado produz 400 sem criação. | `tests/p4/test_http_board.py::LocalBoardScenario.test_incomplete_and_unsupported_framing_are_rejected_without_creation` |

Estes são cenários de canal planejados. Resultados de execução são registrados separadamente e descrevem apenas as configurações exercitadas.

<!-- BEGIN UCS CRITERION SCENARIOS -->
## Mapa de cenários para critérios

Cada linha é um cenário de apoio planejado para o BT do respectivo caso. Preparar o estado descrito na UCS, executar com um ator permitido salvo quando o critério verificar recusa e comparar resultado e efeitos com a expectativa. A execução aprovada é registrada separadamente na evidência ADI.

| Cenário | Critério UCS | Observação esperada |
| --- | --- | --- |
| VS-AC-CRM-001-01 | AC-CRM-001-01 | Campos válidos criam cartão NEW na versão 1. |
| VS-AC-CRM-001-02 | AC-CRM-001-02 | Campos vazios ou grandes demais não criam cartão. |
| VS-AC-CRM-001-03 | AC-CRM-001-03 | A criação produz exatamente um evento inicial de etapa. |
| VS-AC-CRM-001-04 | AC-CRM-001-04 | Ator ausente ou sem permissão é recusado antes de qualquer efeito de domínio ou persistência. |
| VS-AC-CRM-002-01 | AC-CRM-002-01 | Um cartão NEW vai para QUALIFIED com um incremento de versão e evento. |
| VS-AC-CRM-002-02 | AC-CRM-002-02 | Um movimento de NEW diretamente para PROPOSAL é rejeitado. |
| VS-AC-CRM-002-03 | AC-CRM-002-03 | Uma versão desatualizada é rejeitada sem mudar etapa ou histórico. |
| VS-AC-CRM-002-04 | AC-CRM-002-04 | Um cartão encerrado não pode ser arrastado para etapa ativa. |
| VS-AC-CRM-002-05 | AC-CRM-002-05 | Ator ausente ou sem permissão é recusado antes de qualquer efeito de domínio ou persistência. |
| VS-AC-CRM-003-01 | AC-CRM-003-01 | Uma nota válida pode ser consultada e incrementa uma vez a versão do cartão. |
| VS-AC-CRM-003-02 | AC-CRM-003-02 | Notas vazias ou grandes demais são rejeitadas sem mudar a versão. |
| VS-AC-CRM-003-03 | AC-CRM-003-03 | Um cartão encerrado ainda aceita uma nota. |
| VS-AC-CRM-003-04 | AC-CRM-003-04 | Ator ausente ou sem permissão é recusado antes de qualquer efeito de domínio ou persistência. |
| VS-AC-CRM-004-01 | AC-CRM-004-01 | O quadro inclui cartões ativos e encerrados nas colunas corretas. |
| VS-AC-CRM-004-02 | AC-CRM-004-02 | O filtro por responsável é exato e não altera os demais registros. |
| VS-AC-CRM-004-03 | AC-CRM-004-03 | Cartões têm ordem determinística em cada coluna. |
| VS-AC-CRM-004-04 | AC-CRM-004-04 | Ator ausente ou sem permissão é recusado antes de qualquer efeito de domínio ou persistência. |
| VS-AC-CRM-005-01 | AC-CRM-005-01 | Um cartão PROPOSAL é encerrado como WON com uma nota, evento e incremento de versão. |
| VS-AC-CRM-005-02 | AC-CRM-005-02 | Um cartão NEW ou QUALIFIED não pode ser encerrado como WON. |
| VS-AC-CRM-005-03 | AC-CRM-005-03 | Um cartão encerrado não pode ser encerrado novamente. |
| VS-AC-CRM-005-04 | AC-CRM-005-04 | Ator ausente ou sem permissão é recusado antes de qualquer efeito de domínio ou persistência. |
| VS-AC-CRM-006-01 | AC-CRM-006-01 | Cada etapa ativa pode ser encerrada como LOST com uma nota, evento e incremento de versão. |
| VS-AC-CRM-006-02 | AC-CRM-006-02 | Um cartão encerrado não pode ser encerrado novamente como LOST. |
| VS-AC-CRM-006-03 | AC-CRM-006-03 | Uma versão desatualizada mantém cartão, notas e histórico inalterados. |
| VS-AC-CRM-006-04 | AC-CRM-006-04 | Ator ausente ou sem permissão é recusado antes de qualquer efeito de domínio ou persistência. |
<!-- END UCS CRITERION SCENARIOS -->
