<a id="notas-da-versao"></a>
# Notas da versão — OAL Alpha-v0.1.0-Alkimim

Alpha-v0.1.0-Alkimim é uma versão finalizada dentro da fase alfa do OAL, que continua em desenvolvimento. A edição define UCS (L1), ADPM (L2.1), ADVS (L2.2), ADI (L3), ADIB (L4) e os motores entre elas. Também especifica como traduzir implementações da mesma camada ou motor com perda controlada e como implementar camadas vizinhas em conjunto. Os motores L2-L3 e L3-L4 podem consultar L1 como fonte adicional.

Os READMEs em inglês e português incluem o mapa de cardinalidade dos casos. Tiny Catalog, Board CRM e Work Board são exemplos Python executáveis com artefatos P1–P4. Suas bases de necessidades foram reconstruídas das UCS; não são registros independentes das partes interessadas.

Editor principal desta edição: Douglas de Oliveira Alkimim. Bruno Chevitarese é creditado como coautor do OAL.

---

<a id="reference-rules"></a>

# OAL Alpha-v0.1.0-Alkimim — regras de referência

[English](README.md#reference-rules) · [Início](../../README.pt-br.md)

OAL significa Open Analysis Layers. Suas cinco camadas tratam do comportamento dos casos de uso (UCS), da modelagem do programa (ADPM), do planejamento da verificação (ADVS), do núcleo invocável (ADI) e da interação externa (ADIB). O modelo é público e deixa equipes livres para escolher formatos, linguagens, ferramentas e organização do projeto. Cada camada nomeia uma responsabilidade; um projeto pode reuni-las em arquivos desde que seus limites continuem rastreáveis. A pessoa responsável por uma derivação é distinta do ator que executa um caso.

<a id="oal-layers"></a>
## OAL — regras entre camadas

1. **Camadas de referência.** Distinguir UCS, ADPM, ADVS, ADI e ADIB por responsabilidade. ADPM e ADVS derivam em paralelo da UCS; a ADIB é a fronteira de interação ao redor dos casos implementados. Artefatos físicos podem reunir ou dividir responsabilidades se cada uma permanecer identificável e rastreável.

2. **Derivações com responsável.** Para as derivações necessidades→UCS, UCS→ADPM, UCS→ADVS, ADPM+ADVS→ADI e ADI→ADIB, registrar versões de origem e destino, uma pessoa responsável identificada, escopo e decisões acrescentadas. A UCS pode ser consultada como fonte adicional ao derivar a ADI ou a ADIB; quando utilizada, registrar sua versão e as decisões que orientou. Uma pessoa pode responder por várias derivações; cargo ou ferramenta, isoladamente, não identifica o responsável.

3. **Identidade dos casos e teste comportamental.** No escopo declarado, cada caso da UCS possui exatamente uma identidade correspondente no ADPM, um teste comportamental diretamente vinculado na ADVS e uma identidade na ADI, sem casos extras no ADPM ou na ADI nem outros testes comportamentais ADVS diretamente vinculados. O teste comportamental é único para seu caso UCS. Ele pode consumir subtestes de apoio para critérios, alternativas, permissões ou outras verificações; os subtestes não têm vínculo direto com um caso UCS e não são testes comportamentais por esta definição. Verificações exclusivas do canal podem ser registradas separadamente sem se tornarem novos casos de uso. Elementos da interface ADIB e casos da ADI podem ter relação muitos para muitos; esse mapeamento não cria outra identidade de caso.

4. **Mudanças e declarações.** A alteração de contrato, permissão ou decisão de interface exige revisar os artefatos derivados e os cenários de verificação afetados. Declarações de versão e conformidade identificam as bases, o escopo das interfaces e a evidência efetivamente comparada.

5. **Pessoas e atores distintos.** Um ator de execução é pessoa ou sistema externo que solicita um caso de uso. O responsável pela derivação é a pessoa identificada que produz ou aprova a passagem entre artefatos. Especificador, modelador do programa, projetista de verificação, implementador e projetista de interação são papéis de trabalho, não cargos obrigatórios; nenhum se torna automaticamente ator de execução.

6. **Nomes das camadas e declarações de implementação.** UCS é L1; ADPM é L2.1; ADVS é L2.2; ADI é L3; ADIB é L4. L2.1 e L2.2 derivam em paralelo de L1. Uma declaração de implementação de uma camada OAL identifica esta edição, a camada, a responsabilidade implementada, seu escopo e os artefatos ou evidências que sustentam a declaração. A declaração de uma camada, isoladamente, não afirma conformidade do modelo completo.

7. **Motores de derivação.** Um Motor LX-LY produz um artefato LY a partir de uma base LX, com as entradas adicionais exigidas pela derivação nomeada. Produzir não significa traduzir literalmente nem manter equivalência estrutural: L4 define uma fronteira de interação ao redor dos casos invocáveis de L3, em vez de ser uma cópia traduzida de L3. Os nomes canônicos são Motor Necessidades-L1, Motor L1-L2.1, Motor L1-L2.2, Motor L2-L3 e Motor L3-L4. L2 é uma forma curta para o par L2.1 e L2.2, não outra camada: o Motor L2-L3 exige ambas e também pode consultar L1. O Motor L3-L4 exige L3 e também pode consultar L1. Consultar L1 não muda o nome de nenhum dos dois motores. Uma implementação de um motor OAL identifica sua edição, a transição nomeada, entradas aceitas, saídas produzidas, vínculos preservados, decisões acrescentadas e escopo da validação. Um motor pode ser realizado por processo humano, software ou ambos; seu uso em um projeto ainda registra a pessoa responsável e as versões exigidas pela regra 2.

8. **Tradução dentro de uma camada ou motor.** Implementações da mesma camada compartilham as responsabilidades e os contratos que a definem. Uma implementação pode, portanto, ser traduzida em outra implementação dessa camada, inclusive com outra linguagem, formato ou arquitetura. A tradução identifica as características comuns preservadas e as informações ou comportamentos perdidos ou alterados; a perda só é controlada quando é explícita, delimitada pelo escopo declarado e não descarta silenciosamente uma característica definidora ou um contrato exigido. A mesma regra vale para implementações do mesmo motor nomeado: preservar suas entradas obrigatórias, a responsabilidade de destino, os vínculos entre casos e as obrigações da derivação, registrando perdas e decisões próprias da implementação. O nome comum, sozinho, não demonstra equivalência.

9. **Implementações conjuntas de camadas vizinhas.** Uma especialização pode implementar responsabilidades de camadas vizinhas ligadas por uma derivação nomeada. Quando ela realiza a passagem da responsabilidade de origem para a de destino, também implementa o motor correspondente; não é necessário um componente separado para o motor. Origem, destino e passagem continuam identificáveis e verificáveis. Isso vale, por exemplo, para L1 com L2.1 e para L3 com L4. Para o Motor L2-L3, a origem L2 obrigatória reúne L2.1 e L2.2, mesmo quando uma delas está empacotada com L3. L2.1 e L2.2 são ramos paralelos, sem derivação nomeada entre si.

<a id="ucs"></a>
## UCS — especificação de casos de uso

1. **Escopo.** Definir objetivos, limites do sistema, atores relevantes e participantes externos sem prescrever a organização do código.

2. **Casos de uso.** Dar a cada caso identificador estável, objetivo principal, ator iniciador e conjunto de atores permitidos. Um ator ausente do conjunto não pode executar o caso.

3. **Contratos comportamentais.** Explicitar acionamentos, entradas, contexto, premissas, condições verificadas, resultados, efeitos, garantias, alternativas e falhas, inclusive o resultado observável da recusa de acesso. Declarar restrições externas relevantes sem prescrever rotas, telas, codificações de payload ou outros mecanismos da ADIB.

4. **Entidades e regras.** Definir o significado, os dados, as relações e as condições de validade das entidades. Explicitar as demais regras de domínio e vinculá-las aos casos de uso responsáveis por aplicá-las.

5. **Composição e dependências.** Identificar as dependências entre casos de uso e as capacidades exigidas de recursos e sistemas externos. Explicitar as condições, informações e resultados envolvidos sem determinar mecanismos de chamada, acesso ou integração.

6. **Obrigações complementares.** Explicitar, quando aplicáveis, requisitos de persistência, segurança e isolamento, observabilidade, desempenho, acessibilidade e outras restrições pertinentes. Cada obrigação tem escopo definido e condições verificáveis; escolhas específicas do canal pertencem à ADIB.

7. **Aceite e vínculos.** Dar a cada caso critérios de aceite e vínculos com necessidades, atores, entidades, regras e dependências pertinentes. Preservar sua identidade no ADPM e na ADI; a ADVS vincula critérios a cenários; a ADIB vincula interações expostas aos casos que invocam.

8. **Consistência e evolução.** Informações compartilhadas possuem definição única e referências explícitas. Alterações preservam identidade e histórico; suposições, pendências e definições aprovadas permanecem distinguíveis.

9. **Domínios — recomendação.** A organização por domínios com responsabilidades delimitadas é opcional, mas fortemente recomendada. Quando adotada, identifica os casos de uso e as entidades associados a cada domínio.

10. **Exemplos representativos.** Exemplos podem esclarecer contratos, mas não substituem regras explícitas nem cenários da ADVS.

<a id="adpm"></a>
## ADPM — modelo de programa orientado pela análise

1. **Separação e preservação das responsabilidades.** O ADPM distingue casos de uso, ferramentas e entidades e exige que suas responsabilidades e relações sejam identificáveis e mapeadas na arquitetura adotada. Ele não escolhe uma arquitetura concreta nem uma estrutura de arquivos. A distinção e o mapeamento permanecem identificáveis na ADI e, por consequência, na ADIB. Domínios são opcionais; quando modelados, seus limites e mapeamento também devem ser preservados.

2. **Casos de uso.** Cada caso de uso realiza um objetivo identificável e concentra as decisões e regras de domínio necessárias, excetuadas as validações permitidas nas entidades. Não determina mecanismos tecnológicos. Pode utilizar outros casos de uso, respeitando seus contratos.

3. **Entidades.** Entidades representam dados e relações e podem ser manipuladas por casos de uso e ferramentas. Suas operações limitam-se à leitura, à atribuição de valores e à validação dos dados durante a atribuição. Não executam outros comportamentos nem dependem de casos de uso ou ferramentas.

4. **Ferramentas e contratos.** Modelar operações, resultados, efeitos e garantias das ferramentas separadamente dos mecanismos. Casos dependem de contratos; ferramentas não inventam regras de domínio.

5. **Dependências e composição.** Mostrar o que cada caso e ferramenta recebe, onde as implementações são selecionadas e como colaboradores são compostos. Não ocultar dependências necessárias em buscas globais.

6. **Persistência.** O acesso à persistência ocorre por ferramentas. As responsabilidades pelos dados e as condições de leitura e alteração devem ser explícitas, independentemente de haver armazenamento compartilhado.

7. **Limite de autorização.** Modelar a entrada do ator autenticado e a decisão de permissão com recusa por padrão para cada caso. A decisão antecede efeitos de domínio e continua efetiva além de controles da interface.

8. **Representação fiel.** Texto semântico ou pseudocódigo estruturado pode expressar ADPM. Ambas as formas devem permitir recuperar responsabilidades, contratos, composição de dependências, autorização e algoritmos.

9. **Domínios.** Recomenda-se agrupar responsabilidades do modelo por domínio quando isso esclarece os limites.

10. **Tempo de vida.** Declarar o tempo de vida dos componentes quando pertinente. Pode-se escolher uma instância por caso no escopo da aplicação, sem tornar a escolha obrigatória.

<a id="advs"></a>
## ADVS — especificação de verificação orientada pela análise

1. **Derivação da UCS e teste comportamental.** Definir exatamente um teste comportamental diretamente vinculado a cada caso de uso UCS no escopo declarado, preservando sua identidade. Identificar a versão da UCS, os contratos e os critérios de aceite cobertos. Um teste comportamental pode consumir subtestes de apoio, inclusive vários cenários, sem criar outros testes comportamentais para esse caso. Arquivos físicos podem reunir vários testes se o mapeamento de um para um entre casos continuar explícito.

2. **Contratos do teste e dos subtestes.** Declarar para o teste comportamental e cada cenário ou subteste de apoio precondições, ator quando pertinente, ação, resultado e efeitos esperados e limite ou configuração observada. O teste comportamental pode exercitar o caso diretamente ou por um canal ADIB; seus subtestes apoiam esse teste sem vínculo direto com um caso UCS.

3. **Permissões.** Cobrir acesso permitido e negado para cada permissão distinta de caso; verificar a recusa antes de efeitos de domínio ou persistência.

4. **Falhas e limites.** Cobrir alternativas, falhas e limites relevantes especificados. Quando a ADIB selecionar um canal, acrescentar cenários para seu contrato de interação, como interpretação, representação, autenticação e acessibilidade quando aplicável; nomear riscos fora dos cenários escolhidos.

5. **Rastreabilidade e estado.** Vincular cada critério de aceite da UCS ao teste comportamental de seu caso e às verificações de apoio que o cobrem; vincular obrigações específicas da ADIB declaradas às verificações planejadas. Recomenda-se verificar ferramentas e entidades, mas a ADVS não precisa ter especificações separadas para elas; as garantias contratuais e regras de validade ainda exigem as verificações necessárias para sustentar uma declaração de conformidade. Distinguir planos de evidência executada; resultados aprovados sustentam apenas configurações observadas. Decisões da ADIB podem, portanto, exigir revisão da ADVS.

<a id="adi"></a>
## ADI — implementação orientada pela análise

1. **Realização do programa.** Implementar identidades dos casos, entidades, contratos de ferramentas, composição, algoritmos e falhas modelados como núcleo de aplicação invocável. Preservar na arquitetura escolhida a distinção e o mapeamento do ADPM entre casos, ferramentas, entidades e domínios modelados; a organização física pode ser diferente. Registrar desvios e artefatos de origem afetados. Mecanismos dos canais externos são especificados na ADIB.

2. **Aplicação da autorização.** Receber a identidade do ator de um chamador e aplicar a permissão do caso antes de efeitos de domínio. Atores ausentes, desconhecidos ou sem permissão são recusados tanto na chamada direta quanto pela ADIB. A fronteira de interação fornece a identidade, mas não substitui a autorização do caso.

3. **Execução da verificação.** Implementar e executar os testes comportamentais e verificações de apoio derivados da ADVS para o núcleo da aplicação, preservando vínculos com casos, critérios e subtestes. Relatar verificações falhas e não executadas; verificações específicas da ADIB também são executadas no canal escolhido.

4. **Garantias das ferramentas.** Ferramentas concretas cumprem contratos ADPM na configuração declarada, incluindo garantias pertinentes de persistência, isolamento e falha.

5. **Evidência.** Declarar versão da implementação, ambiente, cenários executados, resultados e limites. Não apresentar verificações planejadas ou configuradas como execuções concluídas.

<a id="adib"></a>
## ADIB — fronteira de interação orientada pela análise

1. **Escopo de interação.** Declarar os canais de interação oferecidos e os atores ou sistemas externos atendidos. Um canal pode ser página, endpoint programático, linha de comando, consumidor de mensagens ou outra forma de entrada e saída. Indicar quais casos são expostos no escopo declarado.

2. **Estímulos e respostas.** Especificar como cada canal recebe e interpreta um estímulo, verifica sua representação, invoca casos da ADI e apresenta resultados e falhas. A resposta pode ser imediata, posterior ou emitida como evento; o contrato observável deve ser explícito.

3. **Identidade na fronteira.** Quando um caso exigir ator, autenticar ou resolver o chamador pelo mecanismo declarado do canal e passar a identidade à ADI. A ADI ainda aplica a permissão do caso. Ocultar um controle de interface ou verificar apenas a rota não autoriza o caso.

4. **Mapeamento muitos para muitos.** Registrar nos dois sentidos o mapeamento entre elementos da interface e identidades dos casos ADI que invocam; cada lado pode ter vários vínculos. Identificar separadamente elementos exclusivos da interface e sua finalidade. Uma interação que introduza novo objetivo ou regra de negócio exige revisar a UCS e suas derivações.

5. **Limite das decisões.** Manter na ADIB decisões de transporte, apresentação, sessão e representação. Preservar nessa fronteira a distinção entre casos, ferramentas, entidades e domínios modelados no ADPM e realizados na ADI: a ADIB invoca casos em vez de absorver suas responsabilidades. A ADIB pode coordenar casos já especificados, mas não toma novas decisões de domínio nem acessa ferramentas de persistência diretamente. Algoritmos dos casos e autorização permanecem na ADI.

6. **Contrato do canal.** Documentar rotas ou telas, comandos ou eventos, representações, erros e obrigações pertinentes de acessibilidade, localização e operação do canal escolhido. Quando a UCS for consultada, distinguir os requisitos herdados dela das decisões introduzidas na ADIB; caso contrário, identificar as fontes das obrigações do canal. Tornar verificável cada obrigação declarada.

7. **Verificação da interação.** Revisar a ADVS quando decisões da ADIB acrescentarem obrigações observáveis; vincular essas obrigações e os critérios UCS expostos a cenários de interface. Registrar resultados executados e limites de cada canal declarado sem tratar um núcleo funcional ou um cenário planejado como prova da interface.

## Interpretação

O inglês é a origem desta edição; o português é sua tradução. Apenas requisitos numerados definem conformidade. Recomendações estão assinaladas.

## Guia desta edição

Este guia explica as regras numeradas sem acrescentar requisitos.

### Conceitos

No OAL, analisar é registrar necessidades, regras, decisões, premissas e consequências de modo que outra pessoa possa conferi-las. As regras admitem diferentes documentos, linguagens, frameworks e ferramentas. Um repositório pode reunir artefatos desde que o leitor ainda consiga localizar a responsabilidade de cada camada.

A UCS descreve comportamento, atores, permissões, significado dos dados, resultados e critérios de aceite sem escolher canais. O ADPM define o modelo do programa: responsabilidades dos casos, entidades, ferramentas e seus contratos, composição de dependências, permissões e algoritmos. A ADVS define um teste comportamental para cada caso UCS. A ADI realiza o núcleo invocável da aplicação e registra resultados observados do núcleo. A ADIB define e realiza canais que recebem estímulos, chamam casos da ADI e apresentam respostas imediatas, posteriores ou emitidas como eventos. Essas responsabilidades não impõem uma ordem de construção. Uma decisão de canal pode exigir atualização da ADVS ou revelar requisito comportamental que pertence à UCS.

Um ator de execução é pessoa ou sistema externo que solicita um caso de uso. O responsável pela derivação é a pessoa identificada que responde pela produção ou aprovação de um artefato a partir da base de origem. Os papéis de trabalho são especificador (necessidades para UCS), modelador do programa (UCS para ADPM), projetista de verificação (UCS para ADVS e depois cenários de canal), implementador (ADPM e ADVS para ADI) e projetista de interação (ADI para ADIB, com consulta opcional à UCS). Uma pessoa pode acumular papéis. O registro da derivação identifica a pessoa, versões de origem e destino, escopo e decisões acrescentadas.

Os nomes das camadas são L1 para UCS, L2.1 para ADPM, L2.2 para ADVS, L3 para ADI e L4 para ADIB. L2.1 e L2.2 derivam em paralelo. Cada caso UCS tem um modelo de caso, um teste comportamental diretamente vinculado e um caso implementado correspondentes. Um teste comportamental pode consumir vários subtestes de apoio; esses subtestes não são, por si, testes comportamentais. Elementos de interface e casos implementados têm mapeamento muitos para muitos. Navegação, conteúdo estático e outros elementos exclusivos da interface são identificados separadamente. As distinções do ADPM entre casos, ferramentas, entidades e eventuais domínios modelados continuam rastreáveis na ADI e através da fronteira ADIB, mesmo que a organização física seja diferente.

Um motor produz a responsabilidade de destino a partir de artefatos de origem, sem necessariamente traduzi-los. O Motor L2-L3 usa ADPM e ADVS e pode consultar a UCS; o Motor L3-L4 usa casos invocáveis ADI para produzir canais de interação e também pode consultar a UCS. L4 introduz decisões próprias de apresentação e transporte. Uma implementação de motor declara edição, transição nomeada, entradas aceitas, saídas, vínculos preservados, decisões acrescentadas e escopo da validação. Seu uso em um projeto continua identificando a pessoa responsável.

Duas implementações de uma camada podem usar meios diferentes e ainda preservar os contratos que definem essa camada. A tradução entre elas pode omitir detalhes próprios de um meio; as omissões e suas consequências integram o registro da tradução. O mesmo raciocínio vale para duas implementações de um motor nomeado. Uma implementação conjunta pode conter responsabilidades vizinhas e a derivação entre elas sem dividi-las em arquivos ou serviços; a rastreabilidade e as verificações ainda distinguem cada responsabilidade.

<a id="versioning"></a>
### Versionamento e derivação

**Alpha-v0.1.0-Alkimim** identifica o estágio alfa, o número da versão e o editor principal desta edição. Autoria e créditos são registrados separadamente; outra edição pode ter outro editor. O inglês é o texto de origem e o português é sua tradução. Esta versão está fechada para mudanças normativas; tais mudanças exigem uma nova versão.

Artefatos de projeto podem ter versões próprias. O nome da versão, isoladamente, não demonstra conformidade nem comprova execução de verificações. Mudanças em contratos, permissões ou decisões de interação exigem revisão das derivações e cenários afetados. Uma declaração de implementação de uma camada ou um motor identifica sua edição, escopo e evidências de apoio; ela não abrange automaticamente o modelo completo.

<a id="verification"></a>
### Verificação

A ADVS registra o que verificar antes de declarar um resultado. Para cada caso UCS, seu teste comportamental único mantém o vínculo direto com o caso e identifica critérios cobertos, ator, precondições, ação, resultado e efeitos esperados e limite ou configuração relevante. Ele pode consumir subtestes de apoio para atores permitidos e negados, alternativas e falhas; esses não têm vínculo direto com o caso UCS. A ADVS não precisa prescrever verificações separadas para toda ferramenta ou entidade, embora isso seja recomendado. Garantias contratuais e validade das entidades ainda precisam de evidência suficiente para o escopo declarado.

A ADI executa verificações do núcleo da aplicação. Quando a ADIB escolhe um canal, a ADVS também registra cenários para interpretação, representação, autenticação, acessibilidade e outras obrigações declaradas do canal, quando aplicáveis. A evidência de execução da ADIB informa quais canais e configurações foram exercitados. Verificações de permissão cobrem a recusa antes de efeitos de domínio ou persistência. Cenários planejados e resultados executados permanecem distintos.

Os exemplos contêm verificações unitárias para entidades e ferramentas puras, de integração para ferramentas que usam outros recursos e verificações voltadas aos casos. O uso de substituto, SQLite ou HTTP não define, por si, se uma verificação é comportamental: o vínculo direto e único com um caso UCS é que define. No diretório de cada exemplo, `python -m pytest` executa sua suíte; qualquer resultado informado descreve aquela execução e seu ambiente.

<a id="conformance"></a>
### Conformidade e escopo

As regras numeradas acima definem conformidade. Uma declaração informa edição, versões dos artefatos do projeto, casos e canais de interação no escopo, responsáveis identificados pelas derivações e evidência efetivamente examinada. Uma declaração para o modelo completo inclui a ADIB; uma declaração mais restrita nomeia as responsabilidades cobertas.

Revisar a UCS para comportamento e atores permitidos; o ADPM para algoritmos dos casos, contratos, composição de dependências e decisões de permissão; a ADVS para um teste comportamental por caso UCS, seus subtestes de apoio e cobertura; a ADI para casos invocáveis, aplicação das permissões e resultados observados do núcleo; e a ADIB para contratos dos canais, identidade na fronteira, decisões de interação e resultados observados nos canais.

Comparar nos dois sentidos as identidades dos casos entre UCS, ADPM, testes comportamentais ADVS e ADI. Vincular cada critério de aceite da UCS ao teste comportamental de seu caso e às verificações de apoio. Para cada canal ADIB declarado, examinar nos dois sentidos o mapa muitos para muitos entre elementos de interface e casos implementados, identificar elementos exclusivos da interface e vincular obrigações do canal a verificações. A contagem isolada não demonstra preservação de contratos. Verificação planejada não é resultado executado. A [revisão do Tiny Catalog](examples/tiny-catalog/OAL-P3/CONFORMANCE.pt-br.md) registra uma avaliação mais restrita desse exemplo.

### Trabalhos relacionados

OAL dialoga com especificação de casos de uso, rastreabilidade, limites de dependência e derivação de testes. Os links aqui oferecem contexto, sem acrescentar requisitos. [Use-Case 2.0](https://www.ivarjacobson.com/publications/white-papers/use-case-20-e-book) descreve o trabalho incremental com casos de uso do projeto até os testes. [Couto, Ribeiro e Campos](https://arxiv.org/abs/1603.08632) discutem formalização de casos e consistência. [Hajri e colegas](https://arxiv.org/abs/1905.11699) estudam classificação e priorização de testes de sistema a partir de casos de uso.

A [documentação Python sqlite3](https://docs.python.org/3.13/library/sqlite3.html) apoia a implementação de armazenamento dos exemplos. O [guia de workflow Python do GitHub](https://docs.github.com/en/actions/tutorials/build-and-test-code/python) orienta a automação do repositório. Nenhuma dessas tecnologias é exigida pelo OAL.
