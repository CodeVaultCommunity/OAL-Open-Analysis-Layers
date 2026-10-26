# Autoavaliação do exemplo — OAL Stable-v1.0.0

[English](CONFORMANCE.md) · [Início](../../../../../README.pt-br.md)

Esta autoavaliação confere os quatro casos do Tiny Catalog com as regras numeradas da UCS (L1) e do ADPM (dentro de L2) da [edição Stable-v1.0.0](../../../../Stable-v1.0.0/README.pt-br.md). As verificações executáveis estão em `tests/p3` e `tests/p4`. A [base de necessidades](../needs-baseline.json) foi reconstruída da UCS; ela não representa uma avaliação separada das partes interessadas. O pacote instancia OAL-EX-M1-CASE-CONTRACTS e OAL-EX-M2-PROGRAM-SCENARIOS 0.1.0 (consulte `model-instances.json`). Esta revisão avalia os artefatos em relação às regras da edição e aos modelos selecionados; ela não certifica conformidade semântica nem demonstra um transformador de motor.

## Regras da UCS (L1)

1. **Escopo:** UCS §1 identifica objetivos, limites, atores, suposições e exclusões.
2. **Casos de uso:** UCS §6 contém os quatro IDs estáveis dos casos, cada um com objetivo, ator iniciador e conjunto de atores permitidos.
3. **Contratos comportamentais:** cada caso descreve acionamento, entradas, condições, resultados, efeitos e falhas, inclusive o resultado observável da recusa de acesso; escolhas de canal são referidas como decisões de L4 com sua origem declarada.
4. **Entidades e regras:** UCS §§3–4 distinguem validade de campos e regras aplicadas pelos casos.
5. **Composição e dependências:** cada caso identifica as capacidades exigidas; a desativação declara a consulta como dependência.
6. **Obrigações complementares:** UCS §5 define persistência, resultados e limites.
7. **Aceite e vínculos:** critérios, o [mapa ADPM](../OAL-P2/adpm/traceability.json) e o [mapa de testes ADVS](../OAL-P2/advs/behavioral-tests.json) vinculam os quatro casos.
8. **Consistência e evolução:** baseline, autoridade de tradução, suposições e IDs estáveis estão explícitos; fatos, suposições e exclusões permanecem distinguíveis; alterações posteriores de contrato exigem uma mudança de versão registrada.
9. **Domínios (recomendação):** adotado como agrupamento lógico Catálogo, sem pastas de domínio.
10. **Exemplos representativos:** cenários de aceite estão vinculados a `tests/p3`; verificações do canal ficam em `tests/p4`.

## Regras do ADPM (L2)

1. **Separação e preservação das responsabilidades:** `entities`, `usecases` e `tools` são distinguíveis e mapeados na implementação.
2. **Casos de uso:** as decisões de domínio permanecem nas quatro implementações; a desativação compõe o caso de consulta; cada caso decide sua permissão antes dos efeitos.
3. **Entidades:** o modelo deste exemplo escolhe entidades predominantemente de dados — leitura, atribuição e validação dos dados durante a atribuição —, sem outro comportamento e sem dependência de casos ou ferramentas; seus contratos e invariantes estão declarados na UCS §3 e no MODEL.md.
4. **Ferramentas, contratos e localização da validação:** contratos declarados, codec e implementações de conexão/armazenamento; a validade de domínio permanece nas entidades e nos casos, enquanto as ferramentas mantêm apenas garantias técnicas (unicidade atômica, verificações de representação, tradução de corrupção); testes de contrato incluídos.
5. **Dependências e composição:** `composition.py` fornece colaboradores e construtores de dados; sem seleção oculta nos casos.
6. **Persistência:** acessada por `ItemStore`; responsabilidade pelos registros e condições de leitura/escrita documentadas.
7. **Limite de autorização:** cada caso modela contexto de ator resolvido explicitamente e decisão de permissão com recusa por padrão antes dos efeitos de domínio. Autenticação é exigida pelo contrato deste projeto e estabelecida pelo chamador confiável; a string de papel é a representação de contexto escolhida pelo modelo.
8. **Representação fiel:** o texto do MODEL.md mantém recuperáveis responsabilidades, contratos, composição de dependências, autorização, localizações de validação e algoritmos.
9. **Domínios (recomendação):** agrupamento lógico adotado; pastas mantidas por responsabilidade.
10. **Tempo de vida:** uma instância de cada caso por `CatalogApplication`; entradas locais à solicitação.

A identidade dos casos e a correspondência um-para-um entre os quatro IDs especificados e as quatro identidades implementadas são avaliadas pela regra 3 entre camadas da edição, por meio do [mapa ADPM](../OAL-P2/adpm/traceability.json) e do [mapa de testes ADVS](../OAL-P2/advs/behavioral-tests.json).

## Limites desta revisão

O limite HTTP local autentica as credenciais de demonstração por um mecanismo
especificado no [contrato P4](../OAL-P4/HTTP.pt-br.md); cada caso impõe sua permissão
de ator antes de produzir efeitos. O perfil em memória é um substituto de teste, não
uma implementação de armazenamento durável para produção. O [mapa bidirecional da interface](../OAL-P4/traceability.json) documenta a fronteira ADIB.
Esta é uma autoavaliação de artefatos com foco declarado em UCS+ADPM; as regras de
ADVS, ADI e ADIB são apenas parcialmente revisadas aqui. Execute os testes no
diretório do exemplo para obter resultados no ambiente atual; uma suíte aprovada
sustenta apenas as verificações e a configuração observadas.
