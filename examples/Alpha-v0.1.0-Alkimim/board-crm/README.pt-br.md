# Board CRM · exemplo OAL Alpha-v0.1.0-Alkimim

[English](README.md) · [Início](../../../README.pt-br.md)

Board CRM acompanha oportunidades comerciais em cinco etapas. Seus seis casos criam e movem oportunidades, registram notas, mostram o quadro e encerram negócios como ganhos ou perdidos. O SQLite preserva o histórico, e a conferência de versão recusa alterações baseadas em um cartão antigo.

## UCS e permissões

A [UCS](OAL-P1/ucs.json) dá ao gestor os seis casos, ao operador os casos de criação, movimentação, anotação e consulta, e ao leitor apenas a consulta. Cada caso verifica a permissão antes de acessar dados, inclusive quando é chamado sem HTTP.

O mesmo conteúdo da UCS está em [JSON](OAL-P1/ucs.json) e [LaTeX](OAL-P1/UCS.pt-br.tex). O [LaTeX em inglês](OAL-P1/UCS.tex) vem dos campos de origem no JSON. O JSON é a fonte do conteúdo; o formato não define UCS.

## Artefatos OAL

- [Base de necessidades reconstruída](needs-baseline.json) e [UCS](OAL-P1/ucs.json) em OAL-P1.
- [Modelo de programa ADPM](OAL-P2/adpm/MODEL.pt-br.md), [contratos de ferramentas](OAL-P2/adpm/tool-contracts.pt-br.md) e [mapa dos casos](OAL-P2/adpm/traceability.json).
- [Cenários de verificação ADVS](OAL-P2/advs/SCENARIOS.pt-br.md) e [identidades dos testes comportamentais](OAL-P2/advs/behavioral-tests.json).
- [Decisões de implementação ADI](OAL-P3/IMPLEMENTATION.pt-br.md) e [testes dos casos](tests/p3).
- [Contrato HTTP ADIB](OAL-P4/HTTP.pt-br.md), [mapa da interface](OAL-P4/traceability.json) e [testes do canal](tests/p4).
- [Derivações identificadas](derivations.json) para as cinco transições.

No código, [`usecases`](src/board_crm/usecases) toma as decisões dos casos e das etapas, [`entities.py`](src/board_crm/entities.py) define os dados, [`tools`](src/board_crm/tools) define e implementa o armazenamento, e [`composition.py`](src/board_crm/composition.py) liga essas partes. Autenticação HTTP, rotas, JSON e arquivos do navegador ficam em [`transport`](src/board_crm/transport). O [validador](../../validate_oal.py) do repositório confere que o núcleo não importa P4.

## Executar no navegador

Com Python 3.12 ou posterior, execute na raiz:

```bash
python examples/run_examples.py board-crm
```

O inicializador abre `http://127.0.0.1:8001/`. O navegador solicita credenciais HTTP Basic na primeira chamada à API. Use `manager` / `manager-demo`, `operator` / `operator-demo` ou `viewer` / `viewer-demo`. Para trocar de conta, use outra sessão privada do navegador ou limpe as credenciais armazenadas. É possível alterar as senhas padrão por variáveis de ambiente `OAL_CRM_<ROLE>_PASSWORD`. A demonstração escuta em loopback; as senhas fixas são apenas para uso local.

Encerre com Ctrl+C. O [guia dos exemplos](../../README.pt-br.md#executar-um-exemplo) explica as opções do lançador.

## Verificação

Instale `pytest==9.0.2` e execute `python -m pytest` neste diretório. A suíte cobre entidades, armazenamento SQLite, casos de uso, autorização e o adaptador HTTP local. Uma execução aprovada descreve os cenários e o ambiente exercitados.

## Índice da documentação

[OAL Alpha-v0.1.0-Alkimim](../../../versioning/Alpha-v0.1.0-Alkimim.pt-br.md) · [Exemplos](../../README.pt-br.md) · [UCS](OAL-P1/ucs.json) · [ADPM](OAL-P2/adpm/MODEL.pt-br.md) · [ADVS](OAL-P2/advs/SCENARIOS.pt-br.md) · [ADI](OAL-P3/IMPLEMENTATION.pt-br.md) · [ADIB](OAL-P4/HTTP.pt-br.md)
