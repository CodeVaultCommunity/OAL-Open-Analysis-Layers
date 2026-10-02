# Exemplos OAL — Alpha-v0.1.0-Alkimim

[English](README.md) · [Início](../README.pt-br.md) · [Regras de referência](../versioning/Alpha-v0.1.0-Alkimim.pt-br.md)

Os três exemplos usam Python e SQLite, mas resolvem problemas diferentes: um catálogo pequeno, um quadro comercial e um quadro de itens de trabalho. Cada um inclui UCS (P1), ADPM e ADVS (P2), ADI (P3), ADIB (P4) e um registro de derivações. As bases de necessidades foram reconstruídas das UCS para fins didáticos; não são registros independentes das partes interessadas. Os READMEs de cada exemplo mostram onde terminam as regras dos casos e começam os adaptadores de navegador e HTTP.

## Tiny Catalog

O [Tiny Catalog](Alpha-v0.1.0-Alkimim/tiny-catalog/README.pt-br.md) gerencia um pequeno catálogo de itens. Seus quatro casos cadastram um item, consultam um item, listam os disponíveis e desativam um item. A desativação preserva o registro; a unicidade dos códigos é verificada atomicamente no SQLite. Um **mantenedor** pode usar os quatro casos; um **leitor** pode consultar e listar. As permissões dos casos são aplicadas mesmo quando um caso é chamado fora do navegador.

Inicie em `http://127.0.0.1:8000/`. As contas locais de demonstração HTTP Basic são `maintainer` / `maintainer-demo` e `reader` / `reader-demo`. Consulte a [UCS](Alpha-v0.1.0-Alkimim/tiny-catalog/OAL-P1/UCS.pt-br.md), o [ADPM](Alpha-v0.1.0-Alkimim/tiny-catalog/OAL-P2/adpm/MODEL.pt-br.md), a [ADVS](Alpha-v0.1.0-Alkimim/tiny-catalog/OAL-P2/advs/SCENARIOS.pt-br.md), as [notas da ADI](Alpha-v0.1.0-Alkimim/tiny-catalog/OAL-P3/IMPLEMENTATION.pt-br.md), o [contrato ADIB](Alpha-v0.1.0-Alkimim/tiny-catalog/OAL-P4/HTTP.pt-br.md) e o [registro de derivações](Alpha-v0.1.0-Alkimim/tiny-catalog/derivations.json).

## Board CRM

O [Board CRM](Alpha-v0.1.0-Alkimim/board-crm/README.pt-br.md) apresenta oportunidades em um quadro comercial de arrastar e soltar. Seus seis casos criam uma oportunidade, movem-na entre etapas, registram uma interação, consultam o quadro, encerram uma oportunidade como ganha e encerram outra como perdida. Ele mantém notas e histórico das etapas no SQLite e confere versões ao alterar um cartão. Um **gestor** pode usar os seis casos; um **operador** pode criar, mover, anotar e consultar; um **leitor** pode somente consultar.

Inicie em `http://127.0.0.1:8001/`. As contas locais de demonstração HTTP Basic são `manager` / `manager-demo`, `operator` / `operator-demo` e `viewer` / `viewer-demo`. A [UCS em JSON](Alpha-v0.1.0-Alkimim/board-crm/OAL-P1/ucs.json) também tem representações LaTeX em [português](Alpha-v0.1.0-Alkimim/board-crm/OAL-P1/UCS.pt-br.tex) e [inglês](Alpha-v0.1.0-Alkimim/board-crm/OAL-P1/UCS.tex). Consulte o [ADPM](Alpha-v0.1.0-Alkimim/board-crm/OAL-P2/adpm/MODEL.pt-br.md), a [ADVS](Alpha-v0.1.0-Alkimim/board-crm/OAL-P2/advs/SCENARIOS.pt-br.md), as [notas da ADI](Alpha-v0.1.0-Alkimim/board-crm/OAL-P3/IMPLEMENTATION.pt-br.md), o [contrato ADIB](Alpha-v0.1.0-Alkimim/board-crm/OAL-P4/HTTP.pt-br.md) e o [registro de derivações](Alpha-v0.1.0-Alkimim/board-crm/derivations.json).

## Work Board

O [Work Board](Alpha-v0.1.0-Alkimim/work-board/README.pt-br.md) é um pequeno gerenciador de itens de trabalho por projeto. Seus seis casos criam, atribuem e avançam itens, registram comentários e consultam o quadro e a discussão. Usa um fluxo de três estados e confere versões ao atribuir ou avançar. Inicie em `http://127.0.0.1:8002/` com as contas locais `manager` / `manager-demo`, `contributor` / `contributor-demo` ou `viewer` / `viewer-demo`. A [UCS](Alpha-v0.1.0-Alkimim/work-board/OAL-P1/UCS.pt-br.md), o [ADPM](Alpha-v0.1.0-Alkimim/work-board/OAL-P2/adpm/MODEL.pt-br.md), a [ADVS](Alpha-v0.1.0-Alkimim/work-board/OAL-P2/advs/SCENARIOS.pt-br.md), a [ADI](Alpha-v0.1.0-Alkimim/work-board/OAL-P3/IMPLEMENTATION.pt-br.md) e a [ADIB](Alpha-v0.1.0-Alkimim/work-board/OAL-P4/HTTP.pt-br.md) explicam as fronteiras.

## Executar um exemplo

Os exemplos atuais exigem Python 3.12 ou posterior. Na raiz do repositório, use [run_examples.py](run_examples.py):

```bash
python examples/run_examples.py tiny-catalog
python examples/run_examples.py board-crm
python examples/run_examples.py work-board
```

Dentro da pasta `examples`, use `python run_examples.py NOME`, com `NOME` igual a `tiny-catalog`, `board-crm` ou `work-board`. O lançador importa cada exemplo Python de seu diretório `src`, inicia um servidor vinculado a `127.0.0.1` e abre a página no navegador. Os arquivos SQLite padrão ficam em `data/` na raiz do repositório, pasta ignorada pelo Git. Encerre o servidor com Ctrl+C.

As opções vêm **depois** do nome do exemplo:

| Opção | Efeito |
| --- | --- |
| `--port 8010` | Usa outra porta local em vez de 8000, 8001 ou 8002. |
| `--database CAMINHO` | Usa o arquivo SQLite indicado em vez do padrão em `data/`. |
| `--no-browser` | Inicia o servidor sem abrir o navegador. |
| `--help` | Mostra as opções do exemplo selecionado. |

Por exemplo, `python examples/run_examples.py tiny-catalog --port 8010 --no-browser` inicia o Tiny Catalog na porta 8010. As senhas de demonstração são para uso local; o README de cada exemplo explica como alterá-las por variáveis de ambiente.

## Acrescentar outra linguagem de execução

O lançador escolhe um executador do registro `EXECUTORS`. `ExampleExecutor` é a interface; `PythonWSGIExecutor` atende os exemplos atuais. Outra linguagem pode oferecer um novo executador e registrar seus exemplos em `EXAMPLES`, com seu próprio ponto de entrada e argumentos. O comando principal continua nesta pasta.
