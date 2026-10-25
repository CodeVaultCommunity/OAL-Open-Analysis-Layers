# Exemplos OAL — Alpha-v0.1.0-Alkimim

[English](README.md) · [Início](../../../README.pt-br.md) · [Regras históricas de referência](../README.pt-br.md)

Estes são os exemplos históricos da edição Alpha-v0.1.0-Alkimim, preservados como referência histórica. Não são a edição atual. Cada pacote contém UCS (P1), ADPM e ADVS (P2), ADI (P3), ADIB (P4) e um registro de derivações. Suas bases de necessidades foram reconstruídas das UCS para fins didáticos; não são registros independentes das partes interessadas.

## Tiny Catalog

O [Tiny Catalog](tiny-catalog/README.pt-br.md) gerencia um pequeno catálogo de itens. Seus quatro casos cadastram, consultam, listam e desativam itens. Um **mantenedor** pode usar os quatro casos; um **leitor** pode consultar e listar. Inicie em `http://127.0.0.1:8000/` com as contas de demonstração `maintainer` / `maintainer-demo` ou `reader` / `reader-demo`. Consulte a [UCS](tiny-catalog/OAL-P1/UCS.pt-br.md), o [ADPM](tiny-catalog/OAL-P2/adpm/MODEL.pt-br.md), a [ADVS](tiny-catalog/OAL-P2/advs/SCENARIOS.pt-br.md), a [ADI](tiny-catalog/OAL-P3/IMPLEMENTATION.pt-br.md), a [ADIB](tiny-catalog/OAL-P4/HTTP.pt-br.md) e o [registro de derivações](tiny-catalog/derivations.json).

## Board CRM

O [Board CRM](board-crm/README.pt-br.md) apresenta oportunidades em um quadro comercial de arrastar e soltar. Seus seis casos criam, movem, anotam, consultam, encerram como ganha e encerram como perdida. Um **gestor** pode usar os seis casos; um **operador** pode criar, mover, anotar e consultar; um **leitor** pode somente consultar. Inicie em `http://127.0.0.1:8001/` com `manager` / `manager-demo`, `operator` / `operator-demo` ou `viewer` / `viewer-demo`. Consulte a [UCS JSON](board-crm/OAL-P1/ucs.json), o [ADPM](board-crm/OAL-P2/adpm/MODEL.pt-br.md), a [ADVS](board-crm/OAL-P2/advs/SCENARIOS.pt-br.md), a [ADI](board-crm/OAL-P3/IMPLEMENTATION.pt-br.md), a [ADIB](board-crm/OAL-P4/HTTP.pt-br.md) e o [registro de derivações](board-crm/derivations.json).

## Work Board

O [Work Board](work-board/README.pt-br.md) é um pequeno gerenciador de itens de trabalho. Seus seis casos criam, atribuem e avançam itens, registram comentários e consultam o quadro e a discussão. Inicie em `http://127.0.0.1:8002/` com `manager` / `manager-demo`, `contributor` / `contributor-demo` ou `viewer` / `viewer-demo`. Consulte a [UCS](work-board/OAL-P1/UCS.pt-br.md), o [ADPM](work-board/OAL-P2/adpm/MODEL.pt-br.md), a [ADVS](work-board/OAL-P2/advs/SCENARIOS.pt-br.md), a [ADI](work-board/OAL-P3/IMPLEMENTATION.pt-br.md) e a [ADIB](work-board/OAL-P4/HTTP.pt-br.md).

## Executar um exemplo

Na raiz do repositório, use o [lançador compartilhado](../../../run_examples.py). Como esta é uma edição histórica, nomeie a edição explicitamente:

```bash
python run_examples.py Alpha-v0.1.0-Alkimim/tiny-catalog
python run_examples.py Alpha-v0.1.0-Alkimim/board-crm
python run_examples.py Alpha-v0.1.0-Alkimim/work-board
```

`python run_examples.py --list` lista todos os exemplos de todas as edições. Um nome de exemplo sem edição resolve para a edição atual; use `EDICAO/NOME` para edições históricas.

Cada diretório de exemplo contém um `runner.json` com seu executador, ponto de entrada, porta padrão e nome do banco. O lançador cria os arquivos SQLite padrão em `data/` na raiz do repositório, em um subdiretório por edição. As opções vêm depois da seleção, por exemplo:

```bash
python run_examples.py Alpha-v0.1.0-Alkimim/tiny-catalog --port 8010 --no-browser
```

As senhas de demonstração são para uso local; o README de cada exemplo explica como alterá-las por variáveis de ambiente. O lançador apenas inicia aplicações; ele não é um motor de derivação do OAL.
