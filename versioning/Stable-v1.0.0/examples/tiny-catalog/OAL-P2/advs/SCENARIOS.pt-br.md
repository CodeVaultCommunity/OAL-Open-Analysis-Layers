# Tiny Catalog — especificação de verificação ADVS

[English](SCENARIOS.md) · [Início](../../../../../../README.pt-br.md)

**Origem:** [UCS do projeto](../../OAL-P1/UCS.pt-br.md), versão 0.2.0.
**Classificação:** artefato de projeto do componente de verificação da L2 (ADVS) sob o OAL Stable-v1.0.0; instanciando OAL-EX-M2-PROGRAM-SCENARIOS 0.1.0; consulte `model-instances.json` para a declaração da instância.
**Registro de derivação:** [derivations.json](../../derivations.json). Estes são cenários planejados; as verificações diretas dos casos estão em [`tests/p3`](../../tests/p3), e as de canal em [`tests/p4`](../../tests/p4). A presença de um arquivo de teste não demonstra que ele foi executado.

## Um teste comportamental por caso

O [mapa dos testes comportamentais](behavioral-tests.json) define BT-CAT-001 a BT-CAT-004, cada qual vinculado diretamente a um único caso UCS. Cada BT é um teste lógico composto pelas verificações executáveis de apoio indicadas. Seu resultado só é aprovado numa execução relatada quando todas essas verificações passam nessa execução. Os cenários por critério abaixo apoiam o BT do respectivo caso; verificações compartilhadas de permissão e retenção podem apoiar mais de um BT sem criar outros testes comportamentais diretamente vinculados.

**Critério transversal de integração:** `AC-SHARED-01` é definido em `OAL-P1/index.json` e abrange UC-CAT-001..004 e as obrigações P-01/P-02. `SC-CAT-RETENTION`, declarado em [behavioral-tests.json](behavioral-tests.json), fornece o cenário completo e a referência executável e apoia explicitamente BT-CAT-001..004. É uma verificação de apoio compartilhada, não um quinto teste comportamental.

## Famílias de cenários

| ID | Casos | Ator e ação | Resultado esperado |
| --- | --- | --- | --- |
| VS-01 | UC-CAT-001, UC-CAT-002, UC-CAT-003, UC-CAT-004 | Ator permitido envia pedido válido | Resultado e efeitos especificados |
| VS-02 | UC-CAT-001, UC-CAT-002, UC-CAT-003, UC-CAT-004 | Identidade ausente envia pedido | Falha de autenticação; nenhum efeito de domínio ou persistência |
| VS-03 | UC-CAT-001, UC-CAT-004 | Ator conhecido sem permissão envia pedido | Acesso negado; nenhum efeito de domínio ou persistência. Não aplicável a UC-CAT-002 e UC-CAT-003: $F_u = A \setminus A_u$ é vazio porque os dois papéis conhecidos são permitidos. |
| VS-04 | UC-CAT-001, UC-CAT-002, UC-CAT-003, UC-CAT-004 | Ator permitido envia dados inválidos | Falha de validação prevista; nenhum efeito indevido |
| VS-05 | UC-CAT-001, UC-CAT-002, UC-CAT-003, UC-CAT-004 | Falha de persistência ou limite de versão | Falha prevista; nenhum sucesso falso |

Cada critério de aceite preserva seu ID da UCS nas verificações executáveis voltadas aos casos. Verificações unitárias cobrem entidades e ferramentas puras elegíveis; as de integração cobrem ferramentas concretas. Os cenários de permissão também chamam casos diretamente, portanto esconder um controle no navegador não os satisfaz.

## Preparação dos cenários por caso

| Caso | Ator permitido e ação | Estado inicial e limite observado |
| --- | --- | --- |
| UC-CAT-001 | Mantenedor cadastra um item. | Usar código livre ou já atribuído conforme o critério; executar com armazenamento injetado em memória ou SQLite. |
| UC-CAT-002 | Mantenedor ou leitor consulta um item. | Preparar código ativo, inativo ou ausente conforme necessário; ler pelo caso, não diretamente pelo armazenamento. |
| UC-CAT-003 | Mantenedor ou leitor lista itens. | Preparar catálogo vazio, ativo, inativo ou misto conforme necessário; observar a coleção completa retornada. |
| UC-CAT-004 | Mantenedor desativa um item. | Preparar item ativo, inativo ou ausente; comparar consulta posterior e lista de disponíveis. |

Para cada caso, executar o critério de recusa com identidades ausente e desconhecida. Executar um papel conhecido sem permissão apenas quando $F_u = A \setminus A_u$ não for vazio; quando $F_u$ for vazio, registrar o cenário como não aplicável com essa justificativa. Identidades ausente e desconhecida continuam situações separadas. Injetar armazenamento indisponível para critérios de falha. O cadastro concorrente usa duas solicitações no mesmo arquivo SQLite. O mapa abaixo fornece o resultado e o efeito esperado de cada preparação.

<!-- BEGIN UCS CRITERION SCENARIOS -->
## Mapa de cenários para critérios

Cada linha de critério próprio de caso é um cenário de apoio planejado para o BT do caso. A linha AC-SHARED-01 é o cenário compartilhado de integração vinculado aos quatro BTs conforme declarado acima. Preparar o estado descrito na UCS, executar com um ator permitido salvo quando o critério verificar recusa e comparar resultado e efeitos com a expectativa. A execução aprovada é registrada separadamente na evidência ADI.

| Cenário | Critério UCS | Observação esperada |
| --- | --- | --- |
| VS-AC-CAT-001-01 | AC-CAT-001-01 | cadastro válido retorna código/nome informados e active=true; consulta posterior retorna o registro. |
| VS-AC-CAT-001-02 | AC-CAT-001-02 | entrada inválida é rejeitada e não cria registro. |
| VS-AC-CAT-001-03 | AC-CAT-001-03 | código já atribuído é rejeitado mesmo que o item esteja inativo; seus dados permanecem inalterados. |
| VS-AC-CAT-001-04 | AC-CAT-001-04 | dois cadastros válidos simultâneos para um código livre resultam em exatamente um sucesso e uma rejeição por duplicidade, com persistência disponível. |
| VS-AC-CAT-001-05 | AC-CAT-001-05 | indisponibilidade é distinguível de cadastro confirmado. |
| VS-AC-CAT-001-06 | AC-CAT-001-06 | Ator ausente ou sem permissão é recusado antes de qualquer efeito de domínio ou persistência. |
| VS-AC-CAT-002-01 | AC-CAT-002-01 | registros ativos e inativos são consultáveis com seus dados. |
| VS-AC-CAT-002-02 | AC-CAT-002-02 | código válido ausente produz resultado de item inexistente. |
| VS-AC-CAT-002-03 | AC-CAT-002-03 | código inválido é rejeitado como dado inválido. |
| VS-AC-CAT-002-04 | AC-CAT-002-04 | indisponibilidade da consulta não é informada como ausência. |
| VS-AC-CAT-002-05 | AC-CAT-002-05 | alterar dados retornados não altera o registro persistido. |
| VS-AC-CAT-002-06 | AC-CAT-002-06 | Ator ausente ou sem permissão é recusado antes de qualquer efeito de domínio ou persistência. |
| VS-AC-CAT-003-01 | AC-CAT-003-01 | resultado contém exatamente os ativos na ordem exigida. |
| VS-AC-CAT-003-02 | AC-CAT-003-02 | catálogo vazio ou apenas com inativos resulta em coleção vazia. |
| VS-AC-CAT-003-03 | AC-CAT-003-03 | falha de persistência não se transforma em coleção vazia de sucesso. |
| VS-AC-CAT-003-04 | AC-CAT-003-04 | Ator ausente ou sem permissão é recusado antes de qualquer efeito de domínio ou persistência. |
| VS-AC-CAT-004-01 | AC-CAT-004-01 | item torna-se inativo, sai da listagem e continua consultável. |
| VS-AC-CAT-004-02 | AC-CAT-004-02 | repetir tem sucesso com os mesmos dados retidos. |
| VS-AC-CAT-004-03 | AC-CAT-004-03 | registro ausente é rejeitado, sem criação implícita. |
| VS-AC-CAT-004-04 | AC-CAT-004-04 | código inválido é rejeitado como dado inválido. |
| VS-AC-CAT-004-05 | AC-CAT-004-05 | indisponibilidade da consulta ou persistência não gera falsa confirmação. |
| VS-AC-CAT-004-06 | AC-CAT-004-06 | Ator ausente ou sem permissão é recusado antes de qualquer efeito de domínio ou persistência. |
| VS-AC-SHARED-01 | AC-SHARED-01 | cadastrar, desativar, encerrar aquela instância da aplicação e reconstruí-la com o mesmo armazenamento retido. A consulta encontra o registro inativo; a listagem de disponíveis o exclui. Avalia reconstrução normal, não queda abrupta ou falta de energia. |
<!-- END UCS CRITERION SCENARIOS -->
