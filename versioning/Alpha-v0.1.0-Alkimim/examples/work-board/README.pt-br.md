# Work Board · exemplo OAL Alpha-v0.1.0-Alkimim

[English](README.md) · [Início](../../../../README.pt-br.md) · [Exemplos](../README.pt-br.md)

Work Board é um pequeno gerenciador local de itens de trabalho com projetos, backlog, atribuição, fluxo de três estados, comentários e filtros. Usa Python e SQLite. Seus seis casos de uso estão na [UCS](OAL-P1/UCS.pt-br.md). A [base de necessidades](needs-baseline.json) foi reconstruída desses casos para fins didáticos; não é evidência independente das partes interessadas.

## Onde ficam as responsabilidades

| Responsabilidade OAL | Especificação | Implementação Python |
| --- | --- | --- |
| P1 · L1 | [UCS](OAL-P1/UCS.pt-br.md) e [dados dos casos](OAL-P1/ucs.json) | IDs e verificações de permissão em [`usecases`](src/work_board/usecases) |
| P2 · L2.1 e L2.2 | [Modelo do programa](OAL-P2/adpm/MODEL.pt-br.md), [mapa dos casos](OAL-P2/adpm/traceability.json) e [testes comportamentais](OAL-P2/advs/behavioral-tests.json) | Contratos em [`tools`](src/work_board/tools); verificações em [`tests/p3`](tests/p3) |
| P3 · L3 | [Decisões de implementação](OAL-P3/IMPLEMENTATION.pt-br.md) | [`entities`](src/work_board/entities.py), [`usecases`](src/work_board/usecases), [`tools`](src/work_board/tools) e [`composition`](src/work_board/composition.py) |
| P4 · L4 | [Contrato HTTP](OAL-P4/HTTP.pt-br.md) e [mapa da interface](OAL-P4/traceability.json) | [`transport`](src/work_board/transport) e [`tests/p4`](tests/p4) |

A direção das dependências é P4 → P3. Os casos não conhecem rotas, formulários, JSON, códigos HTTP nem credenciais Basic. O [registro de derivações](derivations.json) nomeia as cinco transições.

## Executar

Na raiz do repositório, use `python versioning/Alpha-v0.1.0-Alkimim/run_examples.py work-board`. Abra `http://127.0.0.1:8002/`. As contas locais de demonstração são `manager` / `manager-demo`, `contributor` / `contributor-demo` e `viewer` / `viewer-demo`. Gestores podem atribuir; colaboradores podem criar, avançar e comentar; leitores podem consultar. Altere as senhas com `OAL_WORK_BOARD_MANAGER_PASSWORD`, `OAL_WORK_BOARD_CONTRIBUTOR_PASSWORD` e `OAL_WORK_BOARD_VIEWER_PASSWORD`. Os dados ficam no arquivo ignorado `versioning/Alpha-v0.1.0-Alkimim/data/work-board.sqlite3`. Encerre com Ctrl+C.

Dentro da pasta da edição, use `python run_examples.py work-board`. O banco padrão fica em `versioning/Alpha-v0.1.0-Alkimim/data/work-board.sqlite3`. `--database` aceita um caminho absoluto ou relativo ao diretório de trabalho atual; o [guia operacional](../README.pt-br.md#executar-um-exemplo) explica como reutilizar bancos antigos sem movê-los.

Execute `python -m pytest -q --basetemp .pytest_cache/oal-work-board-temp` na pasta do exemplo para verificar casos e HTTP. A demonstração escuta apenas em loopback e não é um sistema de contas de produção.
