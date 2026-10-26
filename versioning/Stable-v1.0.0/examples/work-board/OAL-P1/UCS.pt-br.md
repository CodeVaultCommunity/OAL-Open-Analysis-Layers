# Work Board · casos de uso P1

[English](UCS.md) · [Exemplo](../README.pt-br.md) · [UCS estruturada](ucs.json)

Os seis IDs estáveis em [ucs.json](ucs.json) definem objetivos, atores, resultados e critérios de aceite. O gestor pode executar os seis casos. O colaborador pode criar, avançar, comentar e consultar. O leitor só pode consultar. Identidade ausente e papéis sem permissão são recusados antes de qualquer efeito.

Este Markdown é uma projeção narrativa parcial da fonte canônica estruturada [ucs.json](ucs.json). Ele não reproduz todos os identificadores, conjuntos, regras, obrigações ou critérios. Identificadores citados aqui devem existir no JSON, e afirmações reproduzidas devem concordar com ele; campos e conjuntos não cobertos por este resumo são omitidos intencionalmente. Uma divergência no conteúdo reproduzido é um defeito.


## Regras de campos, versão e ordenação

- **R-WB-01:** projeto tem 1–40 caracteres, título 1–120 e descrição no máximo 2000 após remover espaços nas extremidades; um valor só de espaços conta como vazio. O responsável tem 1–80 caracteres e o texto do comentário 1–1000 caracteres após a remoção de espaços.
- **R-WB-02:** a prioridade é `low`, `normal` ou `high`; `normal` é o padrão e qualquer outro valor é inválido.
- **R-WB-03:** a versão esperada é um inteiro positivo. Atribuição e avanço são operações atômicas de comparação e escrita: uma versão obsoleta é recusada sem alterar o item.
- **R-WB-04:** o fluxo é `backlog → in_progress → done`; somente o próximo passo é permitido, e um passo pulado é recusado sem alterar o item.
- **R-WB-05:** um comentário registra o ator autenticado, o texto sem espaços nas extremidades e o horário. Comentários são acrescentados sem edição, ordenados por horário e depois por identificador, e não alteram a versão do item nem seus registros.
- **R-WB-06:** o quadro aplica filtros exatos de projeto e estado e retorna itens ordenados por projeto, título e identificador, sem mutação.

Um item pertence a um projeto, tem prioridade e passa por `backlog → in_progress → done`. A atribuição confere a versão para impedir que um pedido antigo sobrescreva um valor mais novo. Comentários não mudam a versão do item. As consultas do quadro e dos comentários não alteram registros. Rotas, formulários e credenciais pertencem a [P4](../OAL-P4/HTTP.pt-br.md), não a este contrato.

A [base de necessidades](../needs-baseline.json) foi reconstruída destes casos para explicitar a derivação didática. Ela não é um histórico de entrevistas com as partes interessadas.

A versão 0.2.0 explicita os limites de campos, os valores de prioridade, a normalização de espaços, as verificações de versão esperada e as regras de ordenação. Eles descrevem o contrato implementado deste exemplo e não constavam no texto 0.1.0; são registrados como decisões da baseline 0.2.0, não como requisitos históricos. Este documento é um artefato de projeto da responsabilidade L1 que instancia o modelo `OAL-EX-M1-CASE-CONTRACTS` na versão `0.1.0`; a declaração de instância está em [`model-instances.json`](../model-instances.json).

## Contexto de ator

Os atores especificados são papéis. Este exemplo exige autenticação nos seis casos. Um ponto de entrada confiável resolve o chamador e fornece `principal` como identificador do papel usado para representar seu contexto de ator; o caso aplica sua própria política de permissão. Chamadores diretos são responsáveis por fornecer um contexto proveniente dessa resolução confiável. Contexto ausente é recusado, e este exemplo não declara ator anônimo.

## Falha de armazenamento e limites de versão

Todo caso pode apresentar `unavailable` conforme O-WB-AVAIL. A falha informa o resultado da escrita: `not_applied` significa que uma falha anterior à escrita ou uma reversão confirmada estabelece a ausência de escrita; `unknown` significa que a confirmação ou a reversão da transação não foi confirmada. O chamador consulta o estado atual antes de decidir se repete uma operação com resultado desconhecido. A atomicidade continua excluindo registros parciais; ela não transforma toda falha de confirmação em prova de que nada foi gravado.

R-WB-03 aceita qualquer inteiro positivo como versão esperada. Um valor grande demais para corresponder a uma versão armazenada produz `conflict` para item existente ou `not_found` para item ausente. Isso não acrescenta um limite específico do banco ao domínio. Cada caso tem um terceiro critério de aceite (AC-WB-001-03 a AC-WB-006-03) para seu resultado estável de indisponibilidade.

Revisão 0.2.1: a origem de O-WB-AVAIL passa a domain, preservando origin_reference. Necessidades reconstruídas permanecem em 0.2.0; o comportamento não mudou.
