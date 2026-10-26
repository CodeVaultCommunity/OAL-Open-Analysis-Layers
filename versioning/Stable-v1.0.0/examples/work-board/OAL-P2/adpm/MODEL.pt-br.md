# Work Board · modelo do programa L2/ADPM

[English](MODEL.md) · [UCS](../../OAL-P1/UCS.pt-br.md) · [Exemplo](../../README.pt-br.md)

**Origem:** [UCS do projeto](../../OAL-P1/ucs.json), versão 0.2.1.
**Classificação:** artefato de projeto do componente de modelo do programa (ADPM) da L2 sob o OAL Stable-v1.0.0; instanciando OAL-EX-M2-PROGRAM-SCENARIOS 0.1.0; consulte `model-instances.json` para a declaração da instância.

O modelo tem uma identidade de caso para cada ID da UCS. `CreateItem` valida projeto, título, descrição e prioridade e cria o item no backlog. `AssignItem` e `TransitionItem` conferem a versão esperada; a transição permite apenas a próxima etapa. `AddComment` valida o texto e registra o ator de execução. `ViewBoard` filtra sem alterar dados, e `ViewComments` consulta a discussão de um item.

`WorkItem` e `Comment` carregam dados validados. As regras dos casos e as permissões dos atores ficam nos casos de uso. O contrato `WorkStore` oferece criação, consulta, atribuição, transição, comentários e leitura. Provedores de identificador e relógio fornecem valores sem escolher um canal. A [composição](../../src/work_board/composition.py) injeta o armazenamento SQLite nas seis [classes de casos](../../src/work_board/usecases/operations.py); o armazenamento concreto é escolha da L3. A [rastreabilidade](traceability.json) nomeia cada caso, identidade de teste, implementação e exposição na interface.

O modelo não escolhe URLs, HTML, HTTP Basic, códigos de resposta JSON ou controles do navegador. Essas decisões estão em [P4](../../OAL-P4/HTTP.pt-br.md).

## Contratos de ator e armazenamento

A entrada explícita `principal` é a representação de um contexto de ator resolvido escolhida por este modelo. Todos os casos deste exemplo exigem chamadores autenticados; o ponto de entrada confiável estabelece o papel e cada caso autoriza sua própria operação.

[`WorkStore`](../../src/work_board/tools/contracts.py) declara `Conflict`, `Missing` e `Unavailable` separadamente. Os casos propagam o resultado estável `Unavailable`. O resultado da escrita é `not_applied` somente quando uma falha anterior à escrita ou uma reversão confirmada estabelece essa condição; confirmação ou reversão não confirmada produz `unknown`. O cliente consulta o estado antes de repetir uma escrita com resultado desconhecido. O armazenamento concreto pode informar esgotamento de capacidade como indisponibilidade, enquanto o domínio da versão esperada continua abrangendo todo inteiro positivo. Incompatibilidade de versão e item ausente continuam produzindo, respectivamente, conflito e ausência.
