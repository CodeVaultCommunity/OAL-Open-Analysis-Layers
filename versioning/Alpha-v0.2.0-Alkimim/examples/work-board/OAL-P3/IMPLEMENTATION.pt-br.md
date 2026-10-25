# Work Board · implementação P3

[English](IMPLEMENTATION.md) · [Modelo](../OAL-P2/adpm/MODEL.pt-br.md) · [Exemplo](../README.pt-br.md)

O núcleo invocável está em [`src/work_board`](../src/work_board). [`usecases`](../src/work_board/usecases) contém as decisões de fluxo e permissão; [`entities.py`](../src/work_board/entities.py) contém os formatos de dados e o auxiliar `required_text` aplicado pelos casos; [`tools`](../src/work_board/tools) reúne contrato de armazenamento, adaptador SQLite e provedores de identificador e relógio. [`composition.py`](../src/work_board/composition.py) seleciona ferramentas concretas e constrói seis instâncias de casos. Nenhum módulo do núcleo importa o adaptador de navegador ou HTTP. O conjunto de módulos do núcleo é `authorization.py`, `composition.py`, `entities.py`, `errors.py`, `tools/` e `usecases/`. `__main__.py` é o inicializador da aplicação e `transport/` é a fronteira P4; ambos ficam fora do escopo do núcleo e podem importar o adaptador.

Atribuição e transição usam uma versão esperada. A atualização SQLite compara essa versão de modo atômico e a aumenta ao concluir. A transição também se limita à próxima etapa. Comentários ficam em armazenamento separado e não alteram a versão do item. [`tests/p3`](../tests/p3) exercita os casos diretamente; suas funções sustentam as [seis identidades ADVS](../OAL-P2/advs/behavioral-tests.json).

O [adaptador P4](../OAL-P4/HTTP.pt-br.md) recebe pedidos, autentica o solicitante, invoca um caso e mapeia resultados para HTTP. Ele não contém regras de fluxo nem de permissão.

## Decisões de erro e representação

Erros SQLite são traduzidos para `Unavailable` na fronteira de armazenamento. Erros anteriores à confirmação produzem `write_outcome=not_applied` quando a reversão é concluída; erro durante a confirmação ou falha de reversão produz `unknown`. O resultado da atualização é lido dentro da transação de escrita e só retorna após sua confirmação; assim, não há uma segunda leitura posterior que possa ocultar o resultado de uma alteração concluída.

A capacidade inteira do SQLite é uma restrição de representação. Uma versão esperada acima de `2**63-1` não pode corresponder à versão armazenada e é classificada como conflito ou ausência sem passar um inteiro excessivo ao banco. Um contador já em `2**63-1` não pode ser incrementado neste adaptador; ele produz `Unavailable` com `not_applied` antes da alteração. A comparação e escrita atômica continua sendo a condição de atualização para valores representáveis.

`principal` representa o contexto de ator resolvido por uma string de papel nesta organização de código. O chamador o estabelece pelo mecanismo de entrada confiável; a autorização permanece em cada caso.
