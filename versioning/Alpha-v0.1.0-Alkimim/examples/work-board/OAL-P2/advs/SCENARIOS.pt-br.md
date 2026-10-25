# Work Board · verificação P2.2

[English](SCENARIOS.md) · [UCS](../../OAL-P1/UCS.pt-br.md) · [Exemplo](../../README.pt-br.md)

O [mapa de testes comportamentais](behavioral-tests.json) atribui uma identidade de teste diretamente vinculada a cada caso UCS. As funções executáveis em [`tests/p3`](../../tests/p3) são verificações de apoio, não outras identidades de teste comportamental diretamente vinculadas. Elas cobrem os doze critérios de aceite: resultados válidos, atores recusados, entradas inválidas, versões antigas, ordem do fluxo, filtros e itens ausentes.

[`tests/p4`](../../tests/p4) verifica autenticação HTTP, representação, despacho de rotas e códigos de resposta. Essas verificações sustentam o canal escolhido e não substituem as de P3. Uma suíte aprovada descreve apenas a configuração exercitada naquela execução.
