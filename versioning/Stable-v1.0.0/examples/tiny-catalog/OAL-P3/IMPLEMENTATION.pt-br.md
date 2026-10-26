# Tiny Catalog — implementação ADI

[English](IMPLEMENTATION.md) · [Início](../../../../../README.pt-br.md)

O Tiny Catalog implementa em Python seus quatro casos da [UCS](../OAL-P1/UCS.pt-br.md), com armazenamento SQLite. O [ADPM](../OAL-P2/adpm/MODEL.pt-br.md) distribui as responsabilidades, e o [mapa dos casos](../OAL-P2/adpm/traceability.json) aponta para as classes que as executam. A [ADVS](../OAL-P2/advs/SCENARIOS.pt-br.md) descreve como verificar o comportamento. O [registro de derivação](../derivations.json) identifica as pessoas e versões de origem de cada transição. O conjunto de módulos do núcleo é `authorization.py`, `composition.py`, `entities/`, `errors.py`, `tools/` e `usecases/`. `__main__.py` é o inicializador da aplicação e `transport/` é a fronteira P4; ambos ficam fora do escopo do núcleo e podem importar o adaptador WSGI.

## Limites concretos

Os casos em `src/tiny_catalog/usecases/` tomam decisões de domínio. Entidades guardam dados e validação. Contratos de ferramentas são separados dos mecanismos SQLite. A composição injeta armazenamento concreto e outros colaboradores. Cada caso verifica seus atores permitidos antes de ler ou alterar dados. Identidade ausente e papéis desconhecidos são recusados por padrão.

A [fronteira HTTP P4](../OAL-P4/HTTP.pt-br.md) autentica o ator local e traduz resultados dos casos em respostas. Ela não concede a permissão do caso. Chamadas diretas também verificam a permissão.

## Representação do contexto de ator

Esta organização de código representa um contexto de ator já resolvido pela string de papel `principal` (`maintainer` ou `reader`). O HTTP Basic resolve esse papel a partir das credenciais na P4. Chamadores diretos confiáveis fornecem o papel resolvido, inclusive por `Application.for_actor`; o argumento de papel não é, por si, um verificador de credenciais. O caso verifica a permissão antes dos efeitos, recusa `None` e papéis desconhecidos e transmite o mesmo contexto a um caso chamado, que autoriza independentemente. Estes contratos de projeto não admitem papel anônimo.

## Verificação e limites

Verificações unitárias cobrem entidades e ferramentas puras; as de integração cobrem ferramentas SQLite; [`tests/p3`](../tests/p3) exercita os casos reais, incluindo recusa por chamada direta. Os [cenários ADVS](../OAL-P2/advs/SCENARIOS.pt-br.md) definem o comportamento esperado, e o [mapa BT](../OAL-P2/advs/behavioral-tests.json) agrupa as verificações de apoio por caso. O HTTP é verificado separadamente em [`tests/p4`](../tests/p4). O exemplo não afirma atender implantação exposta à internet nem administração dinâmica de contas.
