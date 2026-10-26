# Exemplos OAL — Alpha-v0.1.0-Alkimim

[English](README.md) · [Início](../../../README.pt-br.md) · [Regras históricas de referência](../README.pt-br.md#reference-rules)

Estes são os exemplos históricos da edição Alpha-v0.1.0-Alkimim, preservados como referência histórica. Não são a edição atual. Cada pacote contém UCS (P1), ADPM e ADVS (P2), ADI (P3), ADIB (P4) e um registro de derivações. Suas bases de necessidades foram reconstruídas das UCS para fins didáticos; não são registros independentes das partes interessadas.

## Tiny Catalog

O [Tiny Catalog](tiny-catalog/README.pt-br.md) gerencia um pequeno catálogo de itens. Seus quatro casos cadastram, consultam, listam e desativam itens. Um **mantenedor** pode usar os quatro casos; um **leitor** pode consultar e listar. Inicie em `http://127.0.0.1:8000/` com as contas de demonstração `maintainer` / `maintainer-demo` ou `reader` / `reader-demo`. Consulte a [UCS](tiny-catalog/OAL-P1/UCS.pt-br.md), o [ADPM](tiny-catalog/OAL-P2/adpm/MODEL.pt-br.md), a [ADVS](tiny-catalog/OAL-P2/advs/SCENARIOS.pt-br.md), a [ADI](tiny-catalog/OAL-P3/IMPLEMENTATION.pt-br.md), a [ADIB](tiny-catalog/OAL-P4/HTTP.pt-br.md) e o [registro de derivações](tiny-catalog/derivations.json).

## Board CRM

O [Board CRM](board-crm/README.pt-br.md) apresenta oportunidades em um quadro comercial de arrastar e soltar. Seus seis casos criam, movem, anotam, consultam, encerram como ganha e encerram como perdida. Um **gestor** pode usar os seis casos; um **operador** pode criar, mover, anotar e consultar; um **leitor** pode somente consultar. Inicie em `http://127.0.0.1:8001/` com `manager` / `manager-demo`, `operator` / `operator-demo` ou `viewer` / `viewer-demo`. Consulte a [UCS JSON](board-crm/OAL-P1/ucs.json), o [ADPM](board-crm/OAL-P2/adpm/MODEL.pt-br.md), a [ADVS](board-crm/OAL-P2/advs/SCENARIOS.pt-br.md), a [ADI](board-crm/OAL-P3/IMPLEMENTATION.pt-br.md), a [ADIB](board-crm/OAL-P4/HTTP.pt-br.md) e o [registro de derivações](board-crm/derivations.json).

## Work Board

O [Work Board](work-board/README.pt-br.md) é um pequeno gerenciador de itens de trabalho. Seus seis casos criam, atribuem e avançam itens, registram comentários e consultam o quadro e a discussão. Inicie em `http://127.0.0.1:8002/` com `manager` / `manager-demo`, `contributor` / `contributor-demo` ou `viewer` / `viewer-demo`. Consulte a [UCS](work-board/OAL-P1/UCS.pt-br.md), o [ADPM](work-board/OAL-P2/adpm/MODEL.pt-br.md), a [ADVS](work-board/OAL-P2/advs/SCENARIOS.pt-br.md), a [ADI](work-board/OAL-P3/IMPLEMENTATION.pt-br.md) e a [ADIB](work-board/OAL-P4/HTTP.pt-br.md).

## Executar um exemplo

Use Python 3.12 ou posterior e o [lançador desta edição](../run_examples.py). Na raiz do repositório:

```bash
python versioning/Alpha-v0.1.0-Alkimim/run_examples.py --list
python versioning/Alpha-v0.1.0-Alkimim/run_examples.py tiny-catalog
python versioning/Alpha-v0.1.0-Alkimim/run_examples.py board-crm
python versioning/Alpha-v0.1.0-Alkimim/run_examples.py work-board
```

Dentro de `versioning/Alpha-v0.1.0-Alkimim/`, use `python run_examples.py NOME` ou `python run_examples.py --list`. A lista contém somente os três exemplos desta edição; a seleção aceita somente o nome, sem `EDICAO/`. Para outra edição, escolha seu próprio caminho de lançador. Uma cópia isolada da pasta da edição, mesmo renomeada, mantém essa identidade e funciona sem arquivos da raiz. Em outro diretório de trabalho, informe o caminho absoluto do lançador.

O lançador lê somente `examples/*/runner.json` ao lado dele, importa o `src` do exemplo selecionado, escuta em `127.0.0.1` e abre o navegador por padrão. Encerre com Ctrl+C. Ele apenas inicia aplicações; não é um motor de derivação do OAL.

As opções vêm **depois** do nome do exemplo:

| Opção | Efeito |
| --- | --- |
| `--port 8011` | Substitui a porta declarada em `runner.json` (8000, 8001 ou 8002). |
| `--database CAMINHO` | Usa o SQLite indicado; caminhos relativos partem do diretório de trabalho atual, e caminhos absolutos são aceitos. |
| `--no-browser` | Inicia sem abrir o navegador. |
| `--help` | Mostra as opções do exemplo selecionado. |

Por exemplo, na raiz: `python versioning/Alpha-v0.1.0-Alkimim/run_examples.py board-crm --port 8011 --no-browser`.

O banco padrão fica em `versioning/Alpha-v0.1.0-Alkimim/data/<database_name>`, ao lado de `examples/`, independentemente do diretório de trabalho. Os bancos antigos em `data/Alpha-v0.1.0-Alkimim/` na raiz continuam onde estavam: não há migração nem exclusão automática. Para reutilizá-los, na raiz execute `python versioning/Alpha-v0.1.0-Alkimim/run_examples.py work-board --database data/Alpha-v0.1.0-Alkimim/work-board.sqlite3`; em outro diretório, informe o caminho absoluto do banco antigo.

As senhas de demonstração são para uso local; cada README explica as variáveis de ambiente. `PythonWSGIExecutor` interpreta as declarações locais `runner.json`; o lançador não depende de módulo compartilhado em outra edição ou na raiz.
