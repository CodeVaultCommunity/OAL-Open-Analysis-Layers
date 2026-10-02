# Autoavaliação do exemplo — OAL Alpha-v0.1.0-Alkimim

[English](CONFORMANCE.md) · [Início](../../../../README.pt-br.md)

Esta autoavaliação confere os quatro casos do Tiny Catalog com as características da UCS e do ADPM. As verificações executáveis estão em `tests/p3` e `tests/p4`. A [base de necessidades](../needs-baseline.json) foi reconstruída da UCS; ela não representa uma avaliação separada das partes interessadas.

## Características UCS

1. **Escopo:** UCS §1 identifica necessidades, participantes, limites, suposições e exclusões.
2. **Organização comportamental:** UCS §6 contém os quatro IDs estáveis dos casos.
3. **Contratos:** cada caso descreve acionamento, entradas, condições, resultados, efeitos e falhas.
4. **Entidades e regras:** UCS §§3–4 distinguem validade de campos e regras aplicadas pelos casos.
5. **Dependências:** cada caso identifica capacidades; a desativação declara a consulta como dependência.
6. **Obrigações complementares:** UCS §5 define persistência, resultados e limites.
7. **Aceitação e rastreabilidade:** critérios, o [mapa ADPM](../OAL-P2/adpm/traceability.json) e o [mapa de testes ADVS](../OAL-P2/advs/behavioral-tests.json) vinculam os quatro casos.
8. **Evolução:** baseline, autoridade de tradução, suposições e IDs estáveis estão explícitos; alterações posteriores de contrato exigem uma mudança de versão registrada.
9. **Domínios (opcional):** adotado como agrupamento lógico Catálogo, sem pastas de domínio.
10. **Cenários representativos:** cenários de aceite estão vinculados a `tests/p3`; verificações do canal ficam em `tests/p4`.

## Características ADPM

1. **Responsabilidades:** `entities`, `usecases` e `tools` são distinguíveis.
2. **Casos:** decisões permanecem nas quatro implementações; desativação compõe a consulta.
3. **Entidades:** somente atribuição, leitura e validação na atribuição; sem operações de domínio.
4. **Ferramentas:** contratos declarados, codec e implementações de conexão/armazenamento; testes de contrato incluídos.
5. **Injeção:** `composition.py` fornece colaboradores e construtores de dados; sem seleção oculta nos casos.
6. **Persistência:** acessada por `ItemStore`; responsabilidade pelos registros e condições de leitura/escrita documentadas.
7. **Correspondência biunívoca:** quatro IDs especificados mapeiam para quatro identidades distintas, e vice-versa.
8. **Domínios (opcional):** agrupamento lógico adotado; pastas mantidas por responsabilidade.
9. **Singletons (opcional):** uma instância de cada caso por `CatalogApplication`; entradas são locais à solicitação.
10. **Testes (opcional):** as três categorias são adotadas segundo as definições desta proposta.

## Limites desta revisão

O limite HTTP local autentica as credenciais de demonstração, e cada caso impõe
sua permissão de ator antes de produzir efeitos. O perfil em memória é um
substituto de teste, não uma implementação de armazenamento durável para
produção. Execute os testes no diretório do exemplo para obter resultados no
ambiente atual.
O [contrato P4](../OAL-P4/HTTP.pt-br.md) e o [mapa bidirecional da interface](../OAL-P4/traceability.json) documentam a fronteira ADIB.
