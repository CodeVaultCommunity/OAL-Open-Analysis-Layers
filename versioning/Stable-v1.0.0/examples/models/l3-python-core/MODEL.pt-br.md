# OAL-EX-M3-PYTHON-CORE — Núcleo Python com Injeção (L3)

[English](MODEL.md) · [Modelos](../README.pt-br.md) · [Regras de referência](../../../../Stable-v1.0.0/README.pt-br.md#reference-rules)

**Identidade:** `OAL-EX-M3-PYTHON-CORE`
**Versão:** 0.1.0
**Camada:** L3 (ADI)
**Edição OAL declarada:** Stable-v1.0.0
**Estado:** exemplo de modelo reutilizável. Este documento especifica o modelo; não certifica artefato de projeto.

## 1. Objetivo e escopo

O modelo define uma organização reutilizável de código Python cujo núcleo de aplicação invocável realiza os casos de um artefato L2. Fixa os símbolos, convenções de chamada, injeção de dependências, ponto de autorização, contratos de ferramentas, composição e vínculos de verificação que um artefato L3 deve expor. Python é uma escolha deste modelo, não uma exigência de L3.

O modelo não escolhe framework web, mecanismo de persistência, organização de pacotes além do núcleo declarado nem executor de testes. Exige que o núcleo seja invocável sem a fronteira de interação.

## 2. Construções e relações

| Construção | Significado |
| --- | --- |
| `Core` | O conjunto declarado de módulos que contém casos, entidades, contratos de ferramenta e composição. Exclui o inicializador da aplicação e a fronteira de interação, e não importa o adaptador de interação. |
| `ApplicationInitializer` | Módulo que compõe a aplicação e/ou inicia um canal. Pode importar a fronteira e fica fora do escopo do núcleo. |
| `EntitySymbol` | O módulo/classe onde a validade canônica de uma entidade é estabelecida, pela própria entidade ou pelo caso consumidor. |
| `CaseSymbol` | A classe ou função que implementa um caso ADI, com sua convenção de chamada e ponto de autorização. |
| `ToolContractSymbol` | O protocolo ou contrato consumido pelos casos; implementações são selecionadas fora dos casos. |
| `ImplementationSymbol` | Implementação concreta de ferramenta ligada pela composição. |
| `CompositionSymbol` | O módulo ou fábrica que seleciona implementações e injeta colaboradores. |
| `VerificationLink` | O comando, referência de verificação ou registro de evidência que exercita o núcleo. |

Relações: cada caso ADPM mapeia para exatamente um caso ADI; cada caso ADI referencia seu caso UCS e seu caso de programa M2; cada caso consome contratos de ferramenta e recebe colaboradores da composição; o responsável declarado pela validade (entidade ou caso consumidor) estabelece a validade canônica; ferramentas recebem entidades prontas e não repetem verificações de coerência interna.

A separação entre o núcleo e o inicializador da aplicação é lógica. Um arquivo não precisa sair do pacote: o modelo exige que o artefato declare exatamente quais módulos pertencem ao núcleo e quais módulos compõem ou iniciam a fronteira.

## 3. Campos

O template legível por máquina é [`template.json`](template.json).

| Objeto | Campo | Tipo | Observações |
| --- | --- | --- | --- |
| Raiz | `model`, `model_version`, `layer`, `oal_edition`, `project`, `source_l2` | O | `source_l2` nomeia a instância M2 e sua versão. |
| Core | `package`, `modules`, `excluded`, `language`, `transport_imports` | O | `modules` é o escopo exato do núcleo. `excluded` nomeia arquivos dentro do contêiner que não são do núcleo. `transport_imports` deve ser vazio. |
| ApplicationInitializer | `symbol`, `role`, `imports_transport` | O | O módulo de composição/inicialização, fora do escopo do núcleo; pode importar a fronteira. |
| EntitySymbol | `ucs_entity_id`, `symbol`, `validity_owner` | O | `symbol` usa `caminho::nome.qualificado`; `validity_owner` é `entity` ou `consuming-case`. |
| CaseSymbol | `id`, `ucs_case_id`, `adpm_case_id`, `symbol`, `callable_convention`, `authorization` | O | `authorization` indica onde a recusa ocorre antes dos efeitos. |
| ToolContractSymbol | `id`, `symbol`, `ready_entity_assumption`, `contextual_conditions` | O | `contextual_conditions` não pode incluir cópia de $I_E$. |
| ImplementationSymbol | `contract_id`, `symbol`, `configuration` | O | Seleção concreta da ferramenta. |
| CompositionSymbol | `symbol`, `injected_collaborators`, `selection_point` | O | Sem busca global oculta. |
| VerificationLink | `bt_ids`, `checks`, `execution` | O | `execution.status` é `not_recorded`, `recorded` ou `not_applicable`. |
| Mapeamento | `cases`, `criteria`, `bt_links` | O | Preserva identidades de M1 e M2. |

`validity_owner` identifica quem estabelece a validade canônica antes de uma ferramenta receber uma entidade pronta:

- `entity`: a construção ou atribuição da entidade aplica $I_E$; uma instância pronta a satisfaz por construção.
- `consuming-case`: a entidade é uma forma de dados, e o caso que a cria ou aceita aplica a validação canônica, diretamente ou por um auxiliar canônico, antes de chamar uma ferramenta ou tratar a entidade como pronta.

`validity_location`, no modelo M1 selecionado, e os símbolos de caso deste modelo identificam o código que estabelece essa validade. Quando o responsável é um caso consumidor, o artefato deve identificar o caminho de construção/validação e a chamada de ferramenta que ele antecede. A ferramenta então assume $e \in V_E$ e verifica apenas suas próprias condições contextuais. Isso é distinto de outras precondições do caso, como permissão, versão esperada ou existência, verificadas separadamente pelo caso ou pela ferramenta conforme seus contratos.

## 4. Condições de validade

- **V-M3-01 — Identidade.** Identidade `OAL-EX-M3-PYTHON-CORE`, versão `0.1.0`, camada `L3` e edição OAL declarada presentes.
- **V-M3-02 — Bijeção de casos.** Todo caso da instância M2 selecionada tem exatamente um símbolo de caso ADI; não há identidades de caso ADI extras no escopo declarado.
- **V-M3-03 — Símbolos resolvem.** Todo símbolo declarado resolve no arquivo referenciado pelo AST do Python. Um nome em comentário ou string não é símbolo.
- **V-M3-04 — Independência do núcleo.** O escopo do núcleo é exatamente `core.modules`. Nenhum módulo do núcleo importa o adaptador de interação, um módulo de servidor web ou representação específica de transporte; `core.transport_imports` é vazio. `core.excluded` e `application_initializers` ficam fora do escopo do núcleo; um inicializador da aplicação pode importar a fronteira sem violar a independência do núcleo.
- **V-M3-05 — Autorização.** Cada caso recebe o contexto de ator explicitamente, por uma representação e um caminho confiável de invocação declarados pelo artefato, e aplica sua política antes dos efeitos de domínio. Contextos ausentes, não resolvidos, desconhecidos ou sem permissão são recusados; autenticação é exigida conforme o contrato do caso. Contexto anônimo explícito só é permitido quando admitido pelo caso selecionado. Chamadas entre casos propagam o contexto pertinente e preservam a política do caso chamado. A autorização não é delegada à interface.

Os exemplos atuais exigem chamadores autenticados. Sua string de papel, chamada `principal` ou ator, é a representação escolhida de um contexto já resolvido; chamadores diretos confiáveis a fornecem, e os adaptadores HTTP a resolvem pelas credenciais de demonstração. O núcleo verifica a permissão do papel, não as credenciais HTTP. Essa convenção não impõe uma classe universal de contexto de ator nem torna confiáveis strings arbitrárias recebidas externamente.
- **V-M3-06 — Coerência das ferramentas.** Os contratos declaram que uma entidade pronta satisfaz $I_E$. As implementações não reexecutam, duplicam nem geram verificação interna equivalente da entidade; suas verificações extras são condições contextuais distintas com objeto, finalidade e responsabilidade.
- **V-M3-07 — Composição.** Colaboradores são injetados por um símbolo de composição declarado. Casos não selecionam ferramentas concretas nem leem estado global.
- **V-M3-08 — Vínculos de verificação.** Toda verificação referenciada existe e é executável ou revisável. `execution.status` é verdadeiro; verificação não executada não é apresentada como aprovada.
- **V-M3-09 — Preservação de identidades.** Identidades de caso ADI e seus vínculos com UCS, ADPM e testes comportamentais são registrados e bidirecionais.

## 5. Mapeamento para as regras L3 do OAL (Stable-v1.0.0)

| Regra ADI do OAL | Construção ou condição do modelo |
| --- | --- |
| 1. Materialização dos papéis de L2 | `Core`, `CaseSymbol`, `EntitySymbol`, `ToolContractSymbol`, `CompositionSymbol`; V-M3-02, V-M3-03. |
| 2. Autorização | `CaseSymbol.authorization`; V-M3-05. |
| 3. Integração das verificações | `VerificationLink`; V-M3-08. |
| 4. Composição e colaboradores | `CompositionSymbol`, `ImplementationSymbol`; V-M3-07. |
| 5. Evolução, rastreabilidade e evidência | `source_l2`, mapeamentos, registros de execução; V-M3-08, V-M3-09. |

## 6. Template, exemplo e contraexemplo

- [`template.json`](template.json) é o template lógico.
- [`example.json`](example.json) é um **recorte parcial** do Tiny Catalog: dois símbolos de caso, o contrato de armazenamento, a composição e os vínculos de verificação. A instância completa é o núcleo do projeto e seus documentos.
- [`counterexample.json`](counterexample.json) delega autorização ao transporte, aponta um caso para símbolo inexistente e dá à implementação do armazenamento uma verificação redundante de campos da entidade. As violações esperadas estão listadas no arquivo.

## 7. Evidência e limites

O modelo foi revisado contra as regras ADI acima. É deliberadamente parcial: não prescreve organização de pacotes, hierarquia de classes, contêiner de injeção nem framework de teste. Também não prova que a implementação está correta; fixa as condições estruturais e de responsabilidade que uma revisão pode conferir.

A resolução de símbolos e as fronteiras de importação podem ser conferidas estruturalmente. Essa verificação não executa o núcleo nem prova correção comportamental.

## 8. Instanciar e verificar

1. Parta da instância M2 selecionada e liste seus casos.
2. Mapeie cada caso para um símbolo de caso ADI e registre a convenção de chamada.
3. Identifique entidades e seus símbolos canônicos de validade, contratos de ferramenta, implementações, o ponto de composição e o inicializador da aplicação separadamente do conjunto de módulos do núcleo.
4. Declare o ponto de autorização de cada caso.
5. Registre vínculos de verificação e o estado de execução.
6. Acrescente a entrada L3 a `model-instances.json` e execute os comandos de teste selecionados.

## Avaliação de compatibilidade estável

Origem: Alpha-v0.2.0-Alkimim, modelo 0.1.0. Para Stable-v1.0.0, as regras numeradas do OAL e os campos e condições de validade deste modelo foram comparados com essa baseline; permanecem iguais. O mapeamento acima continua aplicável ao mesmo escopo didático. Esta revisão de compatibilidade não é certificação externa nem execução de transformador. O [relatório de avaliação](../../../COMPATIBILITY.pt-br.md) registra escopo e limites; execuções dos projetos são registradas separadamente.
