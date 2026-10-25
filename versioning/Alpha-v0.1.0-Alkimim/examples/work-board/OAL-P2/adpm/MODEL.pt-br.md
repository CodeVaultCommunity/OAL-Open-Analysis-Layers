# Work Board · modelo do programa P2.1

[English](MODEL.md) · [UCS](../../OAL-P1/UCS.pt-br.md) · [Exemplo](../../README.pt-br.md)

O modelo tem uma identidade de caso para cada ID da UCS. `CreateItem` valida projeto, título, descrição e prioridade e cria o item no backlog. `AssignItem` e `TransitionItem` conferem a versão esperada; a transição permite apenas a próxima etapa. `AddComment` valida o texto e registra o ator de execução. `ViewBoard` filtra sem alterar dados, e `ViewComments` consulta a discussão de um item.

`WorkItem` e `Comment` carregam dados validados. As regras dos casos e as permissões dos atores ficam nos casos de uso. O contrato `WorkStore` oferece criação, consulta, atribuição, transição, comentários e leitura. Provedores de identificador e relógio fornecem valores sem escolher um canal. A [composição](../../src/work_board/composition.py) injeta o armazenamento SQLite nas seis [classes de casos](../../src/work_board/usecases/operations.py); o armazenamento concreto é escolha da L3. A [rastreabilidade](traceability.json) nomeia cada caso, identidade de teste, implementação e exposição na interface.

O modelo não escolhe URLs, HTML, HTTP Basic, códigos de resposta JSON ou controles do navegador. Essas decisões estão em [P4](../../OAL-P4/HTTP.pt-br.md).
