# Work Board · implementação P3

[English](IMPLEMENTATION.md) · [Modelo](../OAL-P2/adpm/MODEL.pt-br.md) · [Exemplo](../README.pt-br.md)

O núcleo invocável está em [`src/work_board`](../src/work_board). [`usecases`](../src/work_board/usecases) contém as decisões de fluxo e permissão; [`entities.py`](../src/work_board/entities.py) contém formatos de dados e validação de campos; [`tools`](../src/work_board/tools) reúne contrato de armazenamento, adaptador SQLite e provedores de identificador e relógio. [`composition.py`](../src/work_board/composition.py) seleciona ferramentas concretas e constrói seis instâncias de casos. Nenhum módulo do núcleo importa o adaptador de navegador ou HTTP.

Atribuição e transição usam uma versão esperada. A atualização SQLite compara essa versão de modo atômico e a aumenta ao concluir. A transição também se limita à próxima etapa. Comentários ficam em armazenamento separado e não alteram a versão do item. [`tests/p3`](../tests/p3) exercita os casos diretamente; suas funções sustentam as [seis identidades ADVS](../OAL-P2/advs/behavioral-tests.json).

O [adaptador P4](../OAL-P4/HTTP.pt-br.md) recebe pedidos, autentica o solicitante, invoca um caso e mapeia resultados para HTTP. Ele não contém regras de fluxo nem de permissão.
