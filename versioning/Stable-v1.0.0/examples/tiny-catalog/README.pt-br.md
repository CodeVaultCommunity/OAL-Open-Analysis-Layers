# Tiny Catalog · exemplo OAL Stable-v1.0.0

[English](README.md) · [Início](../../../../README.pt-br.md)

Tiny Catalog guarda itens por código. Seus quatro casos cadastram, consultam, listam e desativam itens. A desativação preserva o registro, e o SQLite impede que dois cadastros concorrentes usem o mesmo código.

> Este pacote apresenta artefatos de projeto associados às responsabilidades do OAL (L1–L4), adaptados do exemplo Alpha-v0.1.0-Alkimim. Os artefatos instanciam os quatro modelos reutilizáveis em `../models/` (versão 0.1.0); as declarações estão em [`model-instances.json`](model-instances.json). Os modelos foram aplicados manualmente, então os registros não demonstram a construção nem a execução de transformadores determinísticos. A base de necessidades continua reconstruída. Os [registros de derivação](derivations.json) são registros didáticos de derivação, não execuções de motor.

## UCS e permissões

A [UCS](OAL-P1/UCS.pt-br.md) dá ao mantenedor acesso aos quatro casos e ao leitor acesso às consultas e à listagem. Cada caso verifica a permissão antes de acessar os dados do catálogo, inclusive quando é chamado sem HTTP.

## Artefatos OAL

- [Base de necessidades reconstruída](needs-baseline.json) e [UCS](OAL-P1/UCS.pt-br.md) em OAL-P1.
- [Modelo de programa ADPM](OAL-P2/adpm/MODEL.pt-br.md), [contratos de ferramentas](OAL-P2/adpm/tool-contracts.pt-br.md) e [mapa dos casos](OAL-P2/adpm/traceability.json).
- [Cenários de verificação ADVS](OAL-P2/advs/SCENARIOS.pt-br.md) e [identidades dos testes comportamentais](OAL-P2/advs/behavioral-tests.json).
- [Decisões de implementação ADI](OAL-P3/IMPLEMENTATION.pt-br.md) e [testes dos casos](tests/p3).
- [Contrato HTTP ADIB](OAL-P4/HTTP.pt-br.md), [mapa da interface](OAL-P4/traceability.json) e [testes do canal](tests/p4).
- [Derivações identificadas](derivations.json) para as quatro transições (needs→L1, L1→L2, L2→L3, L3→L4).

No código, [`usecases`](src/tiny_catalog/usecases) toma as decisões do catálogo, [`entities`](src/tiny_catalog/entities) valida os dados dos itens, [`tools`](src/tiny_catalog/tools) define e implementa o armazenamento, e [`composition.py`](src/tiny_catalog/composition.py) liga essas partes. Autenticação HTTP, rotas, JSON e arquivos do navegador ficam em [`transport`](src/tiny_catalog/transport). O núcleo declarado não importa o adaptador de interação.

## Executar no navegador

Com Python 3.12 ou posterior, execute na raiz:

```bash
python run_examples.py tiny-catalog
```

O inicializador abre `http://127.0.0.1:8000/`. O navegador solicita credenciais HTTP Basic na primeira chamada à API. Use `maintainer` / `maintainer-demo` ou `reader` / `reader-demo`. Para trocar de conta, use outra sessão privada do navegador ou limpe as credenciais armazenadas. É possível alterar as senhas padrão por variáveis de ambiente `OAL_CATALOG_<ROLE>_PASSWORD`. A demonstração escuta em loopback; as senhas fixas são apenas para uso local.

Encerre com Ctrl+C. O [guia dos exemplos](../README.pt-br.md#executar-um-exemplo) explica as opções do lançador.

## Verificação

Instale a dependência opcional `test` do exemplo e execute `python -m pytest` neste diretório. A suíte cobre entidades, ferramentas SQLite, casos de uso, autorização e o adaptador HTTP local. Uma execução aprovada descreve os cenários e o ambiente exercitados. Com a demonstração em execução, `python scripts/demo_client.py --port 8000` percorre o fluxo HTTP de quatro passos com as credenciais de demonstração, confere o status esperado em cada etapa e interrompe diante de um resultado inesperado, sem imprimir segredos.

## Índice da documentação

[OAL Stable-v1.0.0](../../../Stable-v1.0.0/README.pt-br.md) · [Exemplos](../README.pt-br.md) · [UCS](OAL-P1/UCS.pt-br.md) · [ADPM](OAL-P2/adpm/MODEL.pt-br.md) · [ADVS](OAL-P2/advs/SCENARIOS.pt-br.md) · [ADI](OAL-P3/IMPLEMENTATION.pt-br.md) · [ADIB](OAL-P4/HTTP.pt-br.md)
