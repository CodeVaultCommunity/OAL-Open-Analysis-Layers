# Exemplos OAL — Alpha-v0.2.0-Alkimim

[English](README.md) · [Início](../../../README.pt-br.md) · [Regras de referência](../../Alpha-v0.2.0-Alkimim/README.pt-br.md#reference-rules)

Os exemplos executáveis desta edição estão neste diretório, adaptados dos [exemplos Alpha-v0.1.0-Alkimim](../../Alpha-v0.1.0-Alkimim/examples/README.pt-br.md), que permanecem preservados como histórico. Cada pacote apresenta artefatos de projeto associados às responsabilidades do OAL: UCS (L1), os componentes ADPM e ADVS da L2, ADI (L3), ADIB (L4) e registros de derivação. Os artefatos instanciam quatro modelos reutilizáveis, um por camada, definidos em [models/](models/README.pt-br.md). Os registros não demonstram a construção nem a execução de transformadores determinísticos entre modelos: os modelos foram aplicados manualmente. Suas bases de necessidades foram reconstruídas das UCS para fins didáticos; não são registros independentes das partes interessadas. Os READMEs de cada exemplo mostram onde terminam as regras dos casos e começam os adaptadores de navegador e HTTP.

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

Os exemplos atuais exigem Python 3.12 ou posterior. Na raiz do repositório, use [run_examples.py](../../../run_examples.py):

```bash
python run_examples.py tiny-catalog
python run_examples.py board-crm
python run_examples.py work-board
```

Use `python run_examples.py --list` para ver todos os exemplos de todas as edições. Um nome sem edição executa a edição atual; use `EDICAO/NOME` para uma edição histórica. Cada diretório de exemplo declara `runner.json` com executador, ponto de entrada, porta e banco. O lançador importa cada exemplo Python de seu diretório `src`, inicia um servidor vinculado a `127.0.0.1` e abre a página no navegador. Os arquivos SQLite padrão ficam em `data/` na raiz do repositório, em um subdiretório por edição, ignorado pelo Git. Encerre o servidor com Ctrl+C. O lançador apenas inicia aplicações; ele não é um motor de derivação do OAL.

As opções vêm **depois** do nome do exemplo:

| Opção | Efeito |
| --- | --- |
| `--port 8010` | Usa outra porta local em vez de 8000, 8001 ou 8002. |
| `--database CAMINHO` | Usa o arquivo SQLite indicado em vez do padrão em `data/`. |
| `--no-browser` | Inicia o servidor sem abrir o navegador. |
| `--help` | Mostra as opções do exemplo selecionado. |

Por exemplo, `python run_examples.py tiny-catalog --port 8010 --no-browser` inicia o Tiny Catalog na porta 8010. As senhas de demonstração são para uso local; o README de cada exemplo explica como alterá-las por variáveis de ambiente. Os exemplos históricos estão em `versioning/Alpha-v0.1.0-Alkimim/examples/`.



O lançador da raiz escolhe um executador do registro `EXECUTORS`. `ExampleExecutor` é a interface; `PythonWSGIExecutor` atende os exemplos atuais. Outra linguagem pode oferecer um novo executador e declará-lo no `runner.json` do exemplo, com seu próprio ponto de entrada e argumentos. O comando do lançador continua na raiz do repositório.

## Evidência de execução

O [registro estruturado de execução](verification/execution.json) preserva a execução dos testes de aplicação de **2026-10-24**, com seus horários, ambiente, comandos, resultados e logs originais. Essa execução registrou 90 testes aprovados no Tiny Catalog, 23 testes e 36 subtestes aprovados no Board CRM e 32 testes aprovados no Work Board: **145 testes e 36 subtestes aprovados**. O mesmo registro inclui a verificação das representações TeX do Board CRM.

As suítes exercitam os núcleos invocáveis e os adaptadores WSGI; o Tiny Catalog também exercita um servidor HTTP real em loopback. Elas não executam JavaScript no navegador nem avaliam acessibilidade visual. As verificações de falha de commit do Work Board usam falhas controladas do SQLite e não estabelecem garantias para quedas arbitrárias do processo ou de energia. Essas observações finitas não constituem uma prova geral de conformidade nem a construção ou execução de um transformador de derivação OAL.

O refinamento da notação matemática e a integração da skill foram atualizações de documentação e empacotamento. O código-fonte das aplicações e seus testes continuam iguais aos da execução registrada, e as suítes de aplicação não foram executadas novamente nessas atualizações. As [verificações estruturais](verification/structural-checks.json) foram atualizadas para o pacote final; o [inventário de conteúdo](../../../CONTENT-SHA256.json) identifica todos os bytes entregues, incluindo as evidências de execução preservadas e a skill informativa.
