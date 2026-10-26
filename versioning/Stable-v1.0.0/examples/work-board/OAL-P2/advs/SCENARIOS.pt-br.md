# Work Board · verificação L2/ADVS

[English](SCENARIOS.md) · [UCS](../../OAL-P1/UCS.pt-br.md) · [Exemplo](../../README.pt-br.md)

**Origem:** [UCS do projeto](../../OAL-P1/ucs.json), versão 0.2.1.
**Classificação:** artefato de projeto do componente de verificação da L2 (ADVS) sob o OAL Stable-v1.0.0; instanciando OAL-EX-M2-PROGRAM-SCENARIOS 0.1.0; consulte `model-instances.json` para a declaração da instância. Estes são cenários planejados; a presença de arquivos de teste não demonstra que eles foram executados.

O [mapa de testes comportamentais](behavioral-tests.json) atribui uma identidade de teste diretamente vinculada a cada caso UCS. As funções executáveis em [`tests/p3`](../../tests/p3) são verificações de apoio, não outras identidades de teste comportamental diretamente vinculadas. Elas cobrem os dezoito critérios de aceite: resultados válidos, atores recusados, entradas inválidas, versões antigas, ordem do fluxo, filtros, itens ausentes e falhas estáveis de armazenamento.

## Famílias de cenários

| ID | Casos | Ator e ação | Resultado esperado |
| --- | --- | --- | --- |
| VS-01 | UC-WB-001..006 | Ator permitido executa uma solicitação válida | Resultado e efeitos especificados |
| VS-02 | UC-WB-001..006 | Identidade ausente ou desconhecida executa uma solicitação | Recusa de autenticação ou acesso; nenhum efeito |
| VS-03 | UC-WB-001, UC-WB-002, UC-WB-003, UC-WB-004 | Papel conhecido sem permissão executa uma solicitação | Acesso negado; nenhum efeito. Não aplicável a UC-WB-005 e UC-WB-006: $F_u = A \setminus A_u$ é vazio porque os três papéis conhecidos podem ler. |
| VS-04 | UC-WB-001..006 | Ator permitido envia entrada inválida | Falha de validação especificada; nenhum efeito indevido |
| VS-05 | UC-WB-002, UC-WB-003 | Versão obsoleta ou estado pulado | Resultado de conflito ou inválido; item inalterado |

Para cada caso, execute os cenários de identidade ausente e desconhecida. Execute um papel conhecido sem permissão apenas quando $F_u = A \setminus A_u$ não for vazio; quando for vazio, registre o cenário como não aplicável com essa justificativa. Identidades ausente e desconhecida continuam situações separadas.

[`tests/p4`](../../tests/p4) verifica autenticação HTTP, representação, despacho de rotas e códigos de resposta. Essas verificações sustentam o canal escolhido e não substituem as de P3. Uma suíte aprovada descreve apenas a configuração exercitada naquela execução.

## Cenários de armazenamento e representação

| Cenário | Contrato / critérios | Preparação e observação esperada | Verificação de apoio |
| --- | --- | --- | --- |
| VS-06 | R-WB-03; AC-WB-002-02; AC-WB-003-02 | Itens existentes e ausentes; versões esperadas `2**63` e maiores. Item existente produz conflito, item ausente produz ausência, e o estado fica inalterado. | `tests/p3/test_cases.py::test_large_expected_versions_preserve_contract_and_state` |
| VS-07 | O-WB-AVAIL; AC-WB-001-03 a AC-WB-006-03 | Esquema de armazenamento temporariamente indisponível; cada caso informa indisponibilidade com `not_applied`, sem resultado falso nem alteração. | `tests/p3/test_cases.py::test_storage_failure_is_exposed_by_each_case_without_false_success` |
| VS-08 | O-WB-PERSIST; O-WB-AVAIL | Falha durante o comando de atualização é revertida; falha no reconhecimento da confirmação produz `unknown` tanto quando houve escrita quanto quando não houve. | `tests/integration/test_sqlite_store.py::test_statement_failure_rolls_back_the_update`; `tests/integration/test_sqlite_store.py::test_unconfirmed_commit_is_unknown_even_when_rollback_returns` |
| VS-09 | Capacidade do armazenamento concreto | Contador saturado continua inteiro e inalterado; armazenamento informa indisponibilidade com `not_applied`. | `tests/integration/test_sqlite_store.py::test_exhausted_storage_counter_is_unavailable_without_numeric_promotion` |
| CS-01 | Mapeamento de erros L4 | Versão esperada grande produz 409/404; indisponibilidade produz 503 e preserva `write_outcome`, incluindo `unknown` após perda da confirmação. | `tests/p4/test_http.py::test_large_expected_version_returns_conflict_or_missing`; `test_storage_failure_returns_503_and_known_write_outcome`; `test_unconfirmed_commit_is_reported_as_unknown_over_http` |

As verificações de armazenamento são apoio e não introduzem outra identidade de teste comportamental diretamente vinculada. Os resultados observados da suíte estão preservados no [registro de execução](../../../verification/execution.json) e no seu [log de testes](../../../verification/work-board-pytest.txt).
