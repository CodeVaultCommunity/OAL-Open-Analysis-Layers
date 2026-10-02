# Board CRM — implementação ADI

[English](IMPLEMENTATION.md) · [Início](../../../../README.pt-br.md)

O Board CRM implementa em Python seus seis casos da [UCS](../OAL-P1/UCS.pt-br.tex), com armazenamento SQLite. O [ADPM](../OAL-P2/adpm/MODEL.pt-br.md) distribui as responsabilidades, e o [mapa dos casos](../OAL-P2/adpm/traceability.json) aponta para as classes que as executam. A [ADVS](../OAL-P2/advs/SCENARIOS.pt-br.md) descreve como verificar o comportamento. O [registro de derivação](../derivations.json) identifica as pessoas e versões de origem de cada transição.

## Limites concretos

Os casos em `src/board_crm/usecases/` tomam decisões de domínio. Entidades guardam dados e validação. Contratos de ferramentas são separados dos mecanismos SQLite. A composição injeta armazenamento concreto e outros colaboradores. Cada caso verifica seus atores permitidos antes de ler ou alterar dados. Identidade ausente e papéis desconhecidos são recusados por padrão.

A [fronteira HTTP P4](../OAL-P4/HTTP.pt-br.md) autentica o ator local e traduz resultados dos casos em respostas. Ela não concede a permissão do caso. Chamadas diretas também verificam a permissão.

## Verificação e limites

Verificações unitárias cobrem entidades e ferramentas puras; as de integração cobrem ferramentas SQLite; [`tests/p3`](../tests/p3) exercita os casos reais, incluindo recusa por chamada direta. Os [cenários ADVS](../OAL-P2/advs/SCENARIOS.pt-br.md) definem o comportamento esperado, e o [mapa BT](../OAL-P2/advs/behavioral-tests.json) agrupa as verificações de apoio por caso. O HTTP é verificado separadamente em [`tests/p4`](../tests/p4). O exemplo não afirma atender implantação exposta à internet nem administração dinâmica de contas.
