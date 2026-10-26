# Work Board · exemplo OAL Stable-v1.0.0

[English](README.md) · [Início](../../../../README.pt-br.md) · [Exemplos](../README.pt-br.md)

Work Board é um pequeno gerenciador local de itens de trabalho com projetos, backlog, atribuição, fluxo de três estados, comentários e filtros. Usa Python e SQLite. Seus seis casos de uso estão na [UCS](OAL-P1/UCS.pt-br.md). A [base de necessidades](needs-baseline.json) foi reconstruída desses casos para fins didáticos; não é evidência independente das partes interessadas.

> Este pacote apresenta artefatos de projeto associados às responsabilidades do OAL (L1–L4), adaptados do exemplo Alpha-v0.1.0-Alkimim. Os artefatos instanciam os quatro modelos reutilizáveis em `../models/` (versão 0.1.0); as declarações estão em [`model-instances.json`](model-instances.json). Os modelos foram aplicados manualmente, então os registros não demonstram a construção nem a execução de transformadores determinísticos. A base de necessidades continua reconstruída. Os [registros de derivação](derivations.json) são registros didáticos de derivação, não execuções de motor.

## Onde ficam as responsabilidades

| Responsabilidade OAL | Especificação | Implementação Python |
| --- | --- | --- |
| P1 · L1 | [UCS](OAL-P1/UCS.pt-br.md) e [dados dos casos](OAL-P1/ucs.json) | IDs e verificações de permissão em [`usecases`](src/work_board/usecases) |
| P2 · L2 (ADPM e ADVS) | [Modelo do programa](OAL-P2/adpm/MODEL.pt-br.md), [mapa dos casos](OAL-P2/adpm/traceability.json) e [testes comportamentais](OAL-P2/advs/behavioral-tests.json) | Contratos em [`tools`](src/work_board/tools); verificações em [`tests/p3`](tests/p3) |
| P3 · L3 | [Decisões de implementação](OAL-P3/IMPLEMENTATION.pt-br.md) | [`entities`](src/work_board/entities.py), [`usecases`](src/work_board/usecases), [`tools`](src/work_board/tools) e [`composition`](src/work_board/composition.py) |
| P4 · L4 | [Contrato HTTP](OAL-P4/HTTP.pt-br.md) e [mapa da interface](OAL-P4/traceability.json) | [`transport`](src/work_board/transport) e [`tests/p4`](tests/p4) |

A direção das dependências é P4 → P3. Os casos não conhecem rotas, formulários, JSON, códigos HTTP nem credenciais Basic. Os módulos do núcleo não importam o adaptador de interação. O [registro de derivações](derivations.json) nomeia as quatro transições (needs→L1, L1→L2, L2→L3, L3→L4).

## Executar

Na raiz do repositório, use `python run_examples.py work-board`. Abra `http://127.0.0.1:8002/`. As contas locais de demonstração são `manager` / `manager-demo`, `contributor` / `contributor-demo` e `viewer` / `viewer-demo`. Gestores podem atribuir; colaboradores podem criar, avançar e comentar; leitores podem consultar. Altere as senhas com `OAL_WORK_BOARD_MANAGER_PASSWORD`, `OAL_WORK_BOARD_CONTRIBUTOR_PASSWORD` e `OAL_WORK_BOARD_VIEWER_PASSWORD`. Os dados ficam no arquivo ignorado `data/Stable-v1.0.0/work-board.sqlite3`. Encerre com Ctrl+C.

Para verificar o exemplo, crie e ative um ambiente isolado na pasta do exemplo, instale o extra de testes declarado com `python -m pip install -e ".[test]"` e execute `python -m pytest -q`. O extra fixa pytest 9.0.2. A suíte cobre casos diretos, contratos de armazenamento e tratamento HTTP via WSGI, incluindo versões esperadas grandes, indisponibilidade e resultado de confirmação desconhecido. A demonstração escuta apenas em loopback e não é um sistema de contas de produção.

## Índice da documentação

[OAL Stable-v1.0.0](../../../Stable-v1.0.0/README.pt-br.md) · [Exemplos](../README.pt-br.md) · [UCS](OAL-P1/UCS.pt-br.md) · [ADPM](OAL-P2/adpm/MODEL.pt-br.md) · [ADVS](OAL-P2/advs/SCENARIOS.pt-br.md) · [ADI](OAL-P3/IMPLEMENTATION.pt-br.md) · [ADIB](OAL-P4/HTTP.pt-br.md)
