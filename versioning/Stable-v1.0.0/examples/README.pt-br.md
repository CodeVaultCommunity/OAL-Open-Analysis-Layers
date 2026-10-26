# Exemplos OAL — Stable-v1.0.0

Copiados da Alpha-v0.2.0-Alkimim para a avaliação Stable-v1.0.0. Derivações e evidências originais permanecem identificadas como históricas.

[English](README.md) · [Início](../../../README.pt-br.md) · [Regras de referência](../../Stable-v1.0.0/README.pt-br.md#reference-rules)

Os exemplos executáveis desta edição estão neste diretório, adaptados dos [exemplos Alpha-v0.1.0-Alkimim](../../Alpha-v0.1.0-Alkimim/examples/README.pt-br.md), cujos artefatos históricos permanecem preservados, com instruções operacionais do lançador atualizadas conforme a lista explícita de exceções do repositório. Cada pacote apresenta artefatos de projeto associados às responsabilidades do OAL: UCS (L1), os componentes ADPM e ADVS da L2, ADI (L3), ADIB (L4) e registros de derivação. Os artefatos instanciam quatro modelos reutilizáveis, um por camada, definidos em [models/](models/README.pt-br.md). Os registros não demonstram a construção nem a execução de transformadores determinísticos entre modelos: os modelos foram aplicados manualmente. Suas bases de necessidades foram reconstruídas das UCS para fins didáticos; não são registros independentes das partes interessadas. Os READMEs de cada exemplo mostram onde terminam as regras dos casos e começam os adaptadores de navegador e HTTP.

Os três exemplos usam Python e SQLite, mas resolvem problemas diferentes: um catálogo pequeno, um quadro comercial e um quadro de itens de trabalho.

## Modelos e manifestos de instância

Os quatro modelos são OAL-EX-M1-CASE-CONTRACTS (L1), OAL-EX-M2-PROGRAM-SCENARIOS (L2), OAL-EX-M3-PYTHON-CORE (L3) e OAL-EX-M4-HTTP-BOUNDARY (L4), cada um na versão 0.1.0. O README da família documenta o formato comum do manifesto. Cada projeto declara suas quatro instâncias em model-instances.json, doze declarações no total. Uma declaração identifica o modelo e a versão, os arquivos e símbolos que compõem o artefato, o escopo, os mapeamentos de caso e interface, o estado da evidência e os limites.

Os modelos são modelos de exemplo: a revisão de conformidade de cada um está documentada em seu MODEL.md, enquanto as instâncias de projeto são revisadas contra o modelo selecionado. Especificar um modelo, declarar uma instância e executar uma verificação são três resultados diferentes.

## Tiny Catalog

O [Tiny Catalog](tiny-catalog/README.pt-br.md) gerencia um pequeno catálogo de itens. Seus quatro casos cadastram um item, consultam um item, listam os disponíveis e desativam um item. A desativação preserva o registro; a unicidade dos códigos é verificada atomicamente no SQLite. Um **mantenedor** pode usar os quatro casos; um **leitor** pode consultar e listar. As permissões dos casos são aplicadas mesmo quando um caso é chamado fora do navegador.

Inicie em `http://127.0.0.1:8000/`. As contas locais de demonstração HTTP Basic são `maintainer` / `maintainer-demo` e `reader` / `reader-demo`. Consulte a [UCS](tiny-catalog/OAL-P1/UCS.pt-br.md), o [ADPM](tiny-catalog/OAL-P2/adpm/MODEL.pt-br.md), a [ADVS](tiny-catalog/OAL-P2/advs/SCENARIOS.pt-br.md), as [notas da ADI](tiny-catalog/OAL-P3/IMPLEMENTATION.pt-br.md), o [contrato ADIB](tiny-catalog/OAL-P4/HTTP.pt-br.md) e o [registro de derivações](tiny-catalog/derivations.json).

## Board CRM

O [Board CRM](board-crm/README.pt-br.md) apresenta oportunidades em um quadro comercial de arrastar e soltar. Seus seis casos criam uma oportunidade, movem-na entre etapas, registram uma interação, consultam o quadro, encerram uma oportunidade como ganha e encerram outra como perdida. Ele mantém notas e histórico das etapas no SQLite e confere versões ao alterar um cartão. Um **gestor** pode usar os seis casos; um **operador** pode criar, mover, anotar e consultar; um **leitor** pode somente consultar.

Inicie em `http://127.0.0.1:8001/`. As contas locais de demonstração HTTP Basic são `manager` / `manager-demo`, `operator` / `operator-demo` e `viewer` / `viewer-demo`. A [UCS em JSON](board-crm/OAL-P1/ucs.json) também tem representações LaTeX em [português](board-crm/OAL-P1/UCS.pt-br.tex) e [inglês](board-crm/OAL-P1/UCS.tex), geradas a partir dessa fonte. Consulte o [ADPM](board-crm/OAL-P2/adpm/MODEL.pt-br.md), a [ADVS](board-crm/OAL-P2/advs/SCENARIOS.pt-br.md), as [notas da ADI](board-crm/OAL-P3/IMPLEMENTATION.pt-br.md), o [contrato ADIB](board-crm/OAL-P4/HTTP.pt-br.md) e o [registro de derivações](board-crm/derivations.json).

## Work Board

O [Work Board](work-board/README.pt-br.md) é um pequeno gerenciador de itens de trabalho por projeto. Seus seis casos criam, atribuem e avançam itens, registram comentários e consultam o quadro e a discussão. Usa um fluxo de três estados e confere versões ao atribuir ou avançar. Inicie em `http://127.0.0.1:8002/` com as contas locais `manager` / `manager-demo`, `contributor` / `contributor-demo` ou `viewer` / `viewer-demo`. A [UCS](work-board/OAL-P1/UCS.pt-br.md), o [ADPM](work-board/OAL-P2/adpm/MODEL.pt-br.md), a [ADVS](work-board/OAL-P2/advs/SCENARIOS.pt-br.md), a [ADI](work-board/OAL-P3/IMPLEMENTATION.pt-br.md) e a [ADIB](work-board/OAL-P4/HTTP.pt-br.md) explicam as fronteiras.

## Executar um exemplo

Use Python 3.12 ou posterior e o [lançador desta edição](../run_examples.py). Na raiz do repositório:

```bash
python versioning/Stable-v1.0.0/run_examples.py --list
python versioning/Stable-v1.0.0/run_examples.py tiny-catalog
python versioning/Stable-v1.0.0/run_examples.py board-crm
python versioning/Stable-v1.0.0/run_examples.py work-board
```

Dentro de `versioning/Stable-v1.0.0/`, use `python run_examples.py NOME` ou `python run_examples.py --list`. A lista contém somente os três exemplos desta edição; a seleção aceita somente o nome, sem `EDICAO/`. Para outra edição, escolha seu próprio caminho de lançador. Uma cópia isolada da pasta da edição, mesmo renomeada, mantém essa identidade e funciona sem arquivos da raiz. Em outro diretório de trabalho, informe o caminho absoluto do lançador.

O lançador lê somente `examples/*/runner.json` ao lado dele, importa o `src` do exemplo selecionado, escuta em `127.0.0.1` e abre o navegador por padrão. Encerre com Ctrl+C. Ele apenas inicia aplicações; não é um motor de derivação do OAL.

As opções vêm **depois** do nome do exemplo:

| Opção | Efeito |
| --- | --- |
| `--port 8011` | Substitui a porta declarada em `runner.json` (8000, 8001 ou 8002). |
| `--database CAMINHO` | Usa o SQLite indicado; caminhos relativos partem do diretório de trabalho atual, e caminhos absolutos são aceitos. |
| `--no-browser` | Inicia sem abrir o navegador. |
| `--help` | Mostra as opções do exemplo selecionado. |

Por exemplo, na raiz: `python versioning/Stable-v1.0.0/run_examples.py board-crm --port 8011 --no-browser`.

O banco padrão fica em `versioning/Stable-v1.0.0/data/<database_name>`, ao lado de `examples/`, independentemente do diretório de trabalho. Os bancos antigos em `data/Stable-v1.0.0/` na raiz continuam onde estavam: não há migração nem exclusão automática. Para reutilizá-los, na raiz execute `python versioning/Stable-v1.0.0/run_examples.py work-board --database data/Stable-v1.0.0/work-board.sqlite3`; em outro diretório, informe o caminho absoluto do banco antigo.

As senhas de demonstração são para uso local; cada README explica as variáveis de ambiente. `PythonWSGIExecutor` interpreta as declarações locais `runner.json`; o lançador não depende de módulo compartilhado em outra edição ou na raiz.

## Evidências de execução

O [índice histórico](verification/history.json) também preserva a [execução da candidata Stable inicial](verification/historical-stable-initial/execution.json), com seu commit e comandos originais. O [registro atual](verification/execution.json) contém os comandos efetivos da preparação Stable, horários, ambiente, resultados e hashes das entradas. A [execução histórica Alpha](verification/historical-alpha-v0.2.0/execution.json) preserva suas observações originais de 2026-10-24 e não comprova nova execução. O [relatório estrutural](verification/structural-checks.json) cobre apenas referências explícitas.

As suítes exercitam núcleos e adaptadores WSGI; Tiny Catalog também utiliza HTTP de loopback. O smoke dos lançadores confirma resposta HTTP e encerramento do processo. JavaScript de navegador e acessibilidade visual não são avaliados. Falhas SQLite controladas não estabelecem garantias de crash ou perda de energia arbitrários. Observações finitas não provam conformidade universal nem demonstram um transformador OAL.

OAL é Stable-v1.0.0; modelos mantêm 0.1.0. Artefatos Work Board passam a 0.2.1 (origem corrigida e revisão de compatibilidade), necessidades reconstruídas mantêm 0.2.0 e artefatos Tiny Catalog/Board CRM mantêm 0.2.0. Pacotes Python demonstrativos mantêm 0.2.0a0.
