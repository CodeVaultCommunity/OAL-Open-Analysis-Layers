<a id="notas-da-versao"></a>
# Notas da versão — OAL Stable-v1.0.0

Stable-v1.0.0 mantém os 46 requisitos numerados de Alpha-v0.2.0-Alkimim no commit-base 5755a4e4a5b31a9614da5d409d03d1db9cf1e20c, sem mudar sua redação nem suas recomendações opcionais. Os snapshots publicados das edições Alpha permanecem imutáveis. Nesta árvore candidata, a única exceção à preservação dos diretórios Alpha é a [lista explícita de ajustes operacionais](../../ALPHA-OPERATIONAL-ALLOWLIST.json): lançadores locais e instruções de execução; os demais arquivos históricos continuam preservados.

Estabilidade significa contrato definido, exemplos verificados e limites publicados. Não certifica todas as implementações, estabelece correção universal nem transforma aplicações demonstrativas em produtos de produção. Esta preparação local não afirma data de publicação, DOI ou revisão externa.

A baseline UCS do Work Board passa a 0.2.1: O-WB-AVAIL é classificada como obrigação de domínio, mantendo sua proveniência original. Os derivados recebem revisão de compatibilidade sem mudança comportamental. Necessidades reconstruídas permanecem em 0.2.0. Tiny Catalog e Board CRM mantêm 0.2.0; os quatro modelos didáticos mantêm 0.1.0 e os pacotes Python mantêm 0.2.0a0. Essas versões são independentes do número 1.0.0 do OAL.

A [comparação e avaliação](COMPATIBILITY.pt-br.md) registra a comparação normativa e nova revisão dos modelos. As [evidências de execução](examples/verification/execution.json), [verificações estruturais](examples/verification/structural-checks.json), o [inventário](../../CONTENT-SHA256.json) e a [skill informativa](skill/SKILL.md) identificam o escopo entregue. Resultados históricos de testes ficam separados das novas execuções.

Os autores creditados do OAL continuam sendo Douglas de Oliveira Alkimim e Bruno Chevitarese. Autoria e responsabilidade histórica pelas derivações são preservadas; esta revisão não afirma nova aprovação humana.

---

<a id="reference-rules"></a>

# OAL Stable-v1.0.0 — regras de referência

[English](README.md#reference-rules) · [Início](../../README.pt-br.md)

OAL significa Open Analysis Layers. O modelo organiza as responsabilidades de desenvolvimento em quatro camadas: L1 especifica casos de uso (UCS); L2 reúne modelagem do programa (ADPM) e especificação da verificação (ADVS) como ADMV; L3 implementa o núcleo invocável (ADI); e L4 oferece a fronteira de interação externa (ADIB). Cada camada define um metamodelo; um modelo reutilizável que satisfaz esse metamodelo é instanciado por artefatos concretos de projeto. O OAL atua como modelo de referência: como outros modelos de referência, separa responsabilidades e nomeia a conformidade sem importar a tecnologia de um domínio particular, e deixa equipes livres para escolher formatos, linguagens, ferramentas e organização do projeto. A pessoa responsável por uma derivação é distinta do ator que executa um caso.

<a id="oal-layers"></a>
## OAL — regras entre camadas

1. **Camadas, metamodelos, modelos e artefatos.** As camadas do OAL são UCS (L1), ADMV (L2), ADI (L3) e ADIB (L4). Cada camada $L_i$ define um metamodelo: os requisitos que um modelo reutilizável $M_i$ dessa camada deve satisfazer. Um artefato concreto de projeto $a$ instancia um modelo selecionado: $M_i \models L_i$, e $a \models M_i$ (equivalentemente, $a \in A(M_i)$). O número da camada nomeia uma responsabilidade de desenvolvimento; a cadeia metamodelo-modelo-artefato nomeia instanciação. São eixos diferentes: L1 não é o metanível acima de L2, e L1–L4 não se equiparam automaticamente a metaníveis como M0–M3 de outro formalismo.

   Um artefato pode ser um conjunto de arquivos e pode ter várias representações do mesmo conteúdo, como JSON, Markdown e TeX; número de arquivos, formato de serialização e número de modelos não são a mesma coisa. Artefatos físicos podem reunir ou dividir responsabilidades se a responsabilidade de cada camada, seu modelo e seus vínculos entre casos permanecerem identificáveis e rastreáveis. Uma expressão abreviada como “artefato L3” significa artefato de um modelo associado a L3; ela não torna o artefato uma instância direta do metamodelo da camada e só pode ser usada depois que essa distinção estiver clara no contexto.

   A ADMV contém dois componentes obrigatórios e distintos: ADPM para a modelagem do programa e ADVS para a especificação da verificação. Podem ser preparados em paralelo a partir da UCS, mas não constituem camadas separadas; pastas ou seções `adpm` e `advs` são organização interna da única L2.

   Para uma edição e versões fixadas, $A(M) = \{a \mid a \models M\}$ denota os artefatos que satisfazem o modelo $M$, e $\mathcal{M}_i = \{M \mid M \models L_i\}$ denota os modelos que satisfazem a camada $L_i$. O [guia de notação](#mathematical-notation) explica esses símbolos. As necessidades do cliente não são uma camada do OAL; quando usadas como origem de derivação, pertencem a um modelo externo de necessidades declarado.

2. **Derivações com responsável.** Uma derivação consome fontes versionadas e produz um destino versionado. Três registros são distintos e não se substituem: a proveniência dos modelos envolvidos (edição, identidade, versão), a construção de um transformador entre modelos selecionados e a execução desse transformador sobre artefatos concretos. Para as derivações Needs-to-L1, L1→L2, L2→L3 e L3→L4, registrar versões de origem e destino, uma pessoa responsável identificada, escopo e decisões acrescentadas. O destino de L1→L2 é uma única ADMV contendo ADPM e ADVS, mesmo que pessoas diferentes os preparem em paralelo; não há duas derivações L2 canônicas paralelas. Uma derivação Needs-to-L1 nomeia o modelo externo de necessidades consumido ($M_{\mathrm{Needs}}$) e o modelo L1 de destino ($M_1$); necessidades reconstruídas a partir de uma UCS existente continuam identificadas como reconstruídas e não são apresentadas como evidência independente de partes interessadas. A UCS pode ser consultada como fonte adicional ao derivar a ADI ou a ADIB; quando utilizada, registrar sua versão e as decisões que orientou por meio de referências explícitas e versionadas, integrantes das entradas fixadas ou do contrato. Uma pessoa pode responder por várias derivações; cargo ou ferramenta, isoladamente, não identifica o responsável. Uma derivação manual registra a mesma proveniência, escopo, decisões acrescentadas e obrigações de preservação aplicáveis. Registrá-la não significa, por si só, declarar que um transformador foi construído ou executado; uma declaração sobre transformador também satisfaz a regra 7.

3. **Identidade dos casos e teste comportamental.** No escopo declarado, cada caso da UCS possui exatamente uma identidade de caso ADPM e um teste comportamental ADVS diretamente vinculado dentro da L2, além de uma identidade de caso na ADI. Não há casos extras no ADPM ou na ADI nem outros testes comportamentais ADVS diretamente vinculados. O teste comportamental é único para seu caso UCS. Ele pode compreender vários cenários e consumir subtestes de apoio para critérios, alternativas, permissões ou outras verificações; os subtestes não têm vínculo direto com um caso UCS e não são testes comportamentais por esta definição. A cardinalidade de um teste por caso não se converte em um teste comportamental por função, nem exige uma única função física de teste por caso. Verificações exclusivas do canal podem ser registradas separadamente sem se tornarem novos casos de uso. Elementos da interface ADIB e casos da ADI podem ter relação muitos para muitos; esse mapeamento não cria outra identidade de caso.

4. **Mudanças e declarações.** A alteração de contrato, permissão ou decisão de interface exige analisar o impacto sobre os modelos afetados, os transformadores construídos e os artefatos derivados e cenários de verificação: qual modelo mudou, quais transformadores precisam ser reconstruídos ou revalidados e quais artefatos precisam ser rederivados ou reverificados. Declarações de versão e conformidade identificam as bases, o escopo das interfaces e a evidência efetivamente comparada.

5. **Pessoas e atores distintos.** Ator é um papel de interação declarado na especificação, desempenhado por uma pessoa ou sistema ao solicitar a execução de um caso de uso. Chamador é a pessoa ou sistema concreto em cujo nome a solicitação ocorre. Cada solicitação está associada a um contexto de ator resolvido conforme o contrato aplicável. Esse contexto representa os papéis pertinentes e, quando exigidas, a identidade do chamador e as informações de autenticação. O modelo define como o contexto é representado e resolvido, incluindo sua origem e premissas de confiança; o OAL não prescreve classe, campos fixos ou mecanismo tecnológico. Autenticação verifica uma identidade alegada quando exigida pelo contrato; autorização determina se um caso pode executar nas condições apresentadas. Atores anônimos e sistêmicos são escolhas explícitas de modelagem. Contexto ausente ou não resolvido e falha de resolução não estabelecem participação anônima.

   O responsável pela derivação é a pessoa identificada que produz ou aprova a passagem entre artefatos. As responsabilidades de definir um modelo, construir um transformador e executar uma derivação são distinguíveis e podem pertencer a pessoas diferentes ou à mesma pessoa. Especificador, modelador do programa, projetista de verificação, implementador e projetista de interação são papéis de trabalho, não cargos obrigatórios; nenhum se torna automaticamente ator de execução. Esta edição não cria cargos obrigatórios.

6. **Nomes das camadas e declarações de conformidade.** UCS é L1; ADMV é L2; ADI é L3; ADIB é L4. ADPM e ADVS são componentes obrigatórios da ADMV, não nomes de camadas. As declarações de conformidade distinguem quatro coisas:

   - **(a)** **Conformidade do modelo:** um modelo $M$ satisfaz o metamodelo de uma camada determinada $L_i$ para um escopo declarado. Isso não diz nada sobre outras camadas.
   - **(b)** **Conformidade do artefato:** um artefato $a$ satisfaz seu modelo selecionado $M$ para um escopo declarado.
   - **(c)** **Cobertura de camadas:** um conjunto declarado de modelos e artefatos cobre um conjunto nomeado de camadas. A cobertura de uma camada não autoriza inferir a cobertura de outra.
   - **(d)** **Cobertura completa das camadas:** cobertura de todas as quatro camadas do OAL — L1, L2, L3 e L4. Quando L2 está no escopo, ADPM e ADVS continuam obrigatórios.

   Toda declaração identifica esta edição, a camada ou camadas, o objeto declarado (modelo, artefato, construção de transformador, execução de transformador ou composição de transformadores), seu escopo e os artefatos ou evidências que a sustentam. Uma declaração de cobertura de L2 inclui ADPM e ADVS e mantém suas responsabilidades identificáveis; declarar apenas um componente não é uma declaração de cobertura de L2. A expressão “modelo completo” é usada apenas quando o modelo, sua versão e o significado de completude são inequívocos; caso contrário, a declaração nomeia seu escopo. “Não especificado”, “não avaliado”, “não demonstrado” e “inconclusivo” distinguem-se entre si e de “não conforme”; nenhum deles é uma aprovação.

7. **Motores de derivação.** Um Motor LX-LY é um metamodelo que especifica a construção de uma lógica determinística a partir de um modelo de origem selecionado para um modelo de destino selecionado e a execução dessa lógica sobre artefatos.

   **Construção e execução.** Para um modelo de origem $M_n \models L_n$ e um modelo de destino $M_{n+1} \models L_{n+1}$: a construção $\mathrm{Build}_E(M_n, M_{n+1})$ produz um transformador $T[M_n, M_{n+1}]$ ou uma falha de construção; a execução $T[M_n, M_{n+1}]\,(a)$ produz $b$, em que $a \in A(M_n)$ e $b \in A(M_{n+1})$; $a$ e $b$ instanciam, respectivamente, os modelos selecionados de origem e destino. $\mathrm{Build}$ é uma notação explicativa da operação prevista pelo metamodelo do motor; não exige uma fábrica executável, outro metanível obrigatório ou um serviço separado. Os nomes canônicos são Motor Needs-L1, Motor L1-L2, Motor L2-L3 e Motor L3-L4.

   **Contrato declarado.** Uma implementação declarada de motor deve definir, de forma verificável:

   - **(a)** identidade, versão e edição dos modelos de origem e destino;
   - **(b)** compatibilidade e capacidades exigidas do par de modelos;
   - **(c)** a separação entre a construção de $T$ e sua execução;
   - **(d)** as decisões de mapeamento, representação, tecnologia e política resolvidas e congeladas na construção, ou incorporadas aos modelos;
   - **(e)** o domínio suportado $D_T$, as precondições de entrada e os critérios de validade dos artefatos;
   - **(f)** a garantia de que uma saída bem-sucedida satisfaz o modelo de destino selecionado, e não apenas algum modelo da mesma camada;
   - **(g)** as obrigações de preservação — identidades, contratos, critérios, permissões e outras relações aplicáveis — expressas como uma relação $P_T \subseteq A(M_n) \times A(M_{n+1})$ tal que $(a, T(a)) \in P_T$ para todo $a$ em $D_T$;
   - **(h)** o significado de determinismo e o critério de igualdade da saída (bytes, estrutura canônica ou equivalência semântica rigorosamente delimitada), de modo que, para os mesmos modelos e versões, transformador e versão, configuração fixa e entrada válida, tempo, aleatoriedade, ambiente e consultas externas não alterem silenciosamente o resultado, e os metadados operacionais fora do artefato comparado sejam explicitamente separados; quando o determinismo é definido por uma relação de equivalência $\equiv$ no destino, diferenças ignoradas por $\equiv$ não podem alterar silenciosamente a aceitação ou o resultado de um transformador seguinte — o transformador seguinte deve ser compatível com $\equiv$ no domínio relevante, ou consumir uma forma canônica que ele fixe explicitamente;
   - **(i)** falhas, limitações de cobertura, término e resultado das verificações;
   - **(j)** a rastreabilidade da construção e das execuções efetivamente registradas.

   **Domínio suportado e cobertura.** Para toda entrada em $D_T$ que satisfaça as precondições e condições operacionais declaradas, $T$ deve terminar com um artefato válido do modelo de destino e preservar as obrigações anunciadas; $D_T$ não pode ser reduzido retrospectivamente para excluir uma entrada porque sua execução falhou. Um transformador com cobertura parcial declara $D_T$ como subconjunto dos artefatos válidos de origem; um que se declara completo cobre todo o conjunto anunciado.

   **Escolhas de construção.** O determinismo de $T$ não implica uma única construção possível a partir do par de modelos: construções com escolhas congeladas diferentes produzem transformadores distintos, e nem todo par arbitrário de modelos admite transformação completa ou automática. Uma função que sempre retorna o mesmo erro é determinística, mas não cumpre a obrigação de produzir destino válido no domínio suportado.

   **Categorias de falha.** As falhas distinguem entrada inválida, entrada válida não suportada, incompatibilidade do par de modelos, falha operacional e saída inválida; um estado inconclusivo não é apresentado como aprovação.

   **Preservação e evidência.** Validade da saída e preservação são obrigações distintas: um artefato pode satisfazer o esquema do destino e ainda perder uma relação que devia ser preservada. Testes finitos sustentam os casos executados; não provam correção universal de $T$. Humanos e IA podem participar da construção de regras determinísticas; interpretação livre ou serviço variável consultado a cada execução não é, por si, transformação determinística.

   **Transições nomeadas e fontes adicionais.** O Motor Needs-L1 consome artefatos de um modelo externo de necessidades declarado; o Motor L1-L2 produz uma ADMV completa a partir de um único modelo L1, e o trabalho em seus componentes pode ocorrer em paralelo sem criar motores de camada separados; os Motores L2-L3 e L3-L4 podem consultar a UCS como fonte versionada adicional, o que não muda o nome de nenhum dos dois, e qualquer consulta adicional a L1 durante a execução usa referências explícitas e versionadas, integrantes das entradas ou do contrato fixado, nunca uma consulta livre a uma UCS mutável como dependência oculta de $T(a)$.

   **Decisões de interação.** As escolhas de canal e representação em L3→L4 pertencem ao modelo de destino ou às decisões congeladas na construção; o motor não inventa preferências nem novos requisitos de domínio. Produzir não significa traduzir literalmente nem manter equivalência estrutural: L4 define uma fronteira de interação ao redor dos casos invocáveis de L3, em vez de ser uma cópia traduzida de L3.

   **Declarações e realização.** Uma implementação declarada de um motor OAL identifica sua edição, a transição nomeada, entradas aceitas, saídas produzidas, vínculos preservados, decisões acrescentadas e escopo da validação; seu uso em um projeto ainda registra a pessoa responsável e as versões exigidas pela regra 2. Um motor pode ser realizado por processo humano, software ou ambos. O determinismo de um motor não exige determinismo de toda execução das aplicações que ele ajuda a produzir.

8. **Conversão, tradução, derivação e substituição de realizações.** Quatro operações são distintas e têm obrigações diferentes:

   - **(a)** **Conversão entre representações de um modelo.** Documentos válidos de um modelo podem usar várias representações, como JSON, Markdown ou TeX. Uma conversão $C_{rs}$ mapeia documentos válidos na representação $r$ para documentos na representação $s$ do mesmo modelo $M$. Para todo documento $x$ em seu domínio declarado, $\mathrm{decode}_s(C_{rs}(x)) \equiv_M \mathrm{decode}_r(x)$, em que $\mathrm{decode}$ recupera o conteúdo do modelo e $\equiv_M$ é a equivalência declarada desse conteúdo. Uma alegação de ida e volta também declara o critério de equivalência do retorno. Identidade de bytes e convenções editoriais fora do modelo não são exigidas nem são evidência de preservação do conteúdo.
   - **(b)** **Tradução entre modelos distintos da mesma camada.** Modelos $M, N \in \mathcal{M}_i$ compartilham as responsabilidades definidoras da camada, mas pertencer à mesma camada não implica tradução total, invertível ou sem perdas. A tradução exige mapeamento explícito, domínio declarado e as obrigações que preserva. Informação ou comportamento fora do mapeamento é perdido ou alterado e é registrado. Um rótulo de camada compartilhado não presume um tradutor universal.
   - **(c)** **Derivação entre camadas.** A derivação produz artefatos do modelo de destino selecionado, preserva as identidades, contratos, critérios e permissões aplicáveis da origem e pode acrescentar decisões próprias da responsabilidade de destino. Registra proveniência e decisões conforme a regra 2. Uma derivação manual pode ser documentada sem declarar um transformador construído ou executado. Uma declaração de realização de motor, construção de transformador ou execução de transformador também satisfaz a regra 7. A correção da derivação não exige cópia estrutural da origem.
   - **(d)** **Tradução ou substituição entre realizações do mesmo motor nomeado.** Está sujeita aos modelos de origem e destino selecionados, aos domínios declarados e às garantias dessas realizações. Preserva as entradas obrigatórias, a responsabilidade de destino, os vínculos entre casos e as obrigações da derivação, registrando perdas e decisões próprias da implementação.

   Documentar uma perda com honestidade não satisfaz um contrato que exige preservar a informação perdida. Uma transformação com perdas pode ser descrita com precisão e ainda ser insuficiente para uma declaração mais forte de preservação ou conformidade.

9. **Modelos combinados, motores, transformadores e composições.** Uma especialização pode implementar responsabilidades de camadas vizinhas ligadas por uma derivação nomeada. Três objetos são distintos: um modelo ou pacote combinado, que reúne artefatos de várias camadas; um transformador construído segundo um metamodelo de motor para um par selecionado de modelos; e uma composição de transformadores. Um modelo combinado ou a coexistência de artefatos não demonstra, por si, um motor, um transformador nem uma transformação.

   Cobrir as duas camadas não constrói automaticamente o transformador da transição entre elas; se a especialização precisar realizar internamente essa passagem, poderá construir um transformador segundo o metamodelo do motor correspondente, que então mantém origem, destino e passagem identificáveis e verificáveis. Isso é opcional, inclusive quando ambas as camadas são informacionais, como L1 e L2. Uma especialização também pode reunir L3 e L4 e, quando necessário, construir e executar internamente o transformador do Motor L3-L4. Toda implementação conjunta que declare cobertura de L2 inclui ADPM e ADVS, inclusive quando L2 está reunida com L1 ou L3.

   Uma composição de transformadores, como um transformador L1→L3 definido por $T_{13}(a) = T_{23}(T_{12}(a))$, é um novo objeto declarado. Seu domínio declarado deve satisfazer $D_{13} \subseteq \{a \in D_{12} \mid T_{12}(a) \in D_{23}\}$, e a igualdade vale nesse domínio.

   Compartilhar o mesmo modelo intermediário, inclusive sua versão, não é suficiente para garantir a composição em todo o domínio de origem: $T_{12}$ pode produzir artefatos em $A(M_2)$ fora de $D_{23}$, e duas saídas equivalentes segundo o critério de determinismo de $T_{12}$ podem levar $T_{23}$ a aceitação ou resultado diferente. Uma composição exige, portanto, modelo intermediário e versão compatíveis, domínios declarados, compatibilidade entre a equivalência usada por $T_{12}$ e as expectativas de entrada de $T_{23}$ (ou uma forma canônica consumida por $T_{23}$), tratamento de falhas e preservação dos rastros. Esta edição não estabelece nenhum motor canônico não adjacente.

<a id="ucs"></a>
## UCS (L1) — especificação de casos de uso

Um modelo conforme a L1 deve estabelecer os assuntos a seguir para seus artefatos; os artefatos que instanciam tal modelo devem satisfazê-los no escopo declarado. L1 não exige JSON, uma notação ou um esquema único universal: prosa semântica e representações estruturadas são igualmente válidas quando os assuntos permanecem recuperáveis.

1. **Escopo.** O modelo deve definir como seus artefatos declaram objetivos, limites do sistema, atores relevantes e participantes externos sem prescrever a organização do código.

2. **Casos de uso.** O modelo deve dar a cada caso identificador estável, objetivo principal, ator iniciador, conjunto de atores permitidos e condições de autorização aplicáveis. Declara quais informações do contexto de ator são necessárias e quando a autenticação é exigida. Participação pública ou sistêmica é declarada explicitamente. Atores fora do conjunto permitido e contextos ausentes, não resolvidos ou insuficientes para o contrato não podem executar o caso; contexto ausente não deve ser interpretado como acesso anônimo.

3. **Contratos comportamentais.** O modelo deve explicitar acionamentos, entradas, contexto, premissas, condições verificadas, resultados, efeitos, garantias, alternativas e falhas, inclusive o resultado observável da recusa de acesso. A L1 pode registrar restrições de interação impostas de fora da solução, com sua origem identificada. Decisões de interação introduzidas pela solução — rotas, telas, codificações de payload, protocolos, representações — pertencem à L4; uma referência feita na L1 a tal decisão não a transforma em requisito externo. Uma restrição externa não muda de responsabilidade apenas por mencionar protocolo, representação, rota ou interface. Quando uma decisão de interação revelar nova necessidade de domínio, revisar a UCS e as derivações afetadas.

4. **Entidades e regras.** O modelo deve definir o significado, os dados, as relações e as condições de validade das entidades, explicitar as demais regras de domínio e vinculá-las aos casos de uso responsáveis por aplicá-las.

5. **Composição e dependências.** O modelo deve identificar as dependências entre casos de uso e as capacidades exigidas de recursos e sistemas externos, explicitando as condições, informações e resultados envolvidos sem determinar mecanismos de chamada, acesso ou integração.

6. **Obrigações complementares.** O modelo deve explicitar, quando aplicáveis, requisitos de persistência, segurança e isolamento, observabilidade, desempenho, acessibilidade e outras restrições pertinentes. Cada obrigação tem escopo definido, origem identificada e condições verificáveis; escolhas específicas do canal pertencem à ADIB.

7. **Aceite e vínculos.** O modelo deve dar a cada caso critérios de aceite e vínculos com necessidades, atores, entidades, regras e dependências pertinentes. A identidade do caso é preservada no ADPM e na ADI; a ADVS vincula critérios a cenários; a ADIB vincula interações expostas aos casos que invocam. Quando um modelo declara critérios compartilhados de integração, identifica seu escopo, os casos afetados e sua definição autoritativa única por referências explícitas.

8. **Consistência e evolução.** Informações compartilhadas possuem definição única e referências explícitas. Alterações preservam identidade e histórico. O modelo deve manter distinguíveis, em seus artefatos, fatos observados, requisitos desejados, inferências, premissas e pendências; nem toda afirmação de uma especificação é um fato comprovado.

9. **Domínios — recomendação.** A organização por domínios com responsabilidades delimitadas é opcional, mas fortemente recomendada. Quando adotada, identifica os casos de uso e as entidades associados a cada domínio.

10. **Exemplos representativos.** Exemplos podem esclarecer contratos, mas não substituem regras explícitas nem cenários da ADVS.

<a id="admv"></a>
## ADMV (L2) — Modelagem e Verificação Orientadas pela Análise

A ADMV é a única camada L2. Ela reúne o modelo do programa (ADPM) e a especificação da verificação (ADVS): um modelo integrado de programa e verificação para um projeto. Os componentes continuam distinguíveis e podem ser preparados em paralelo, mas nenhum deles, isoladamente, completa L2, e existe uma única derivação L1→L2. Pastas ou seções chamadas `adpm` e `advs` são organização interna da L2 unificada. Um modelo conforme a L2 deve estabelecer os assuntos dos dois componentes; seus artefatos devem satisfazê-los.

<a id="adpm"></a>
### ADPM — modelo de programa orientado pela análise

Dentro do modelo L2, o componente ADPM deve estabelecer os assuntos a seguir; os artefatos que instanciam o modelo devem satisfazê-los no escopo declarado.

1. **Separação e preservação das responsabilidades.** O modelo deve distinguir casos de uso, ferramentas e entidades e exigir que suas responsabilidades e relações sejam identificáveis e mapeadas na organização de código L3 selecionada. Ele não escolhe uma organização concreta de código nem uma estrutura de arquivos. A distinção e o mapeamento permanecem identificáveis na ADI e, por consequência, na ADIB. Domínios são opcionais; quando modelados, seus limites e mapeamento também devem ser preservados.

2. **Casos de uso.** Cada caso de uso realiza um objetivo identificável e concentra as decisões e regras de domínio necessárias para ele, excetuadas a validação e o comportamento que o modelo delega explicitamente às entidades. A forma de distribuir comportamento entre casos e entidades é uma escolha do modelo, não uma prescrição universal. Um caso não determina mecanismos tecnológicos. Pode utilizar outros casos de uso, respeitando seus contratos e fornecendo o contexto de ator pertinente pela dependência declarada. O caso chamado aplica sua própria política de autorização. Delegação ou atuação em nome de outro participante exige regra explícita; uma chamada interna, por si só, não concede permissão adicional. A permissão para executar o caso é decidida pelo próprio caso, antes de qualquer efeito proibido.

3. **Entidades.** Entidades representam dados e relações e não dependem de casos de uso nem de ferramentas. O modelo pode definir entidades predominantemente de dados — cujas operações são leitura, atribuição de valores e validação dos dados durante a atribuição — ou entidades com comportamento de domínio, distribuindo comportamento entre entidades e casos de uso. Em qualquer dos casos, o modelo deve explicitar os contratos, invariantes e dependências de cada entidade, e as regras que uma entidade aplica devem ser identificáveis regra a regra. Entidades não absorvem responsabilidades de caso que o modelo atribuiu aos casos.

4. **Ferramentas, contratos e localização da validação.** O modelo deve declarar operações, resultados, efeitos e garantias das ferramentas separadamente dos mecanismos. Casos dependem de contratos; ferramentas não inventam regras de domínio. A validade de domínio exigida por uma entidade ou por um caso é implementada nessa entidade ou no caso consumidor, e a responsabilidade por cada regra é identificável.

   Cada entidade $e$ define suas condições de coerência interna $I_E$, e $V_E = \{e \mid I_E(e)\}$. Uma operação de ferramenta que recebe uma entidade pronta recebe $e \in V_E$ por contrato e não pode reexecutar $I_E$, chamar uma validação redundante nem implementar uma cópia semanticamente equivalente dessa verificação. Gerar a mesma condição automaticamente em outro lugar não torna sua duplicação permitida; renomear a operação ou chamá-la de “garantia técnica” não autoriza repetir a validação interna da entidade.

   A ferramenta pode avaliar condições distintas $Q_t(e, c)$ que dependem de seu próprio contrato e contexto — por exemplo versão esperada, conflito de concorrência, unicidade global atômica, existência de recurso persistido ou disponibilidade de serviço externo —, desde que a condição, seu objeto, sua finalidade e sua responsabilidade sejam identificáveis. Avaliar uma condição distinta não transfere a autorização do caso nem as decisões de domínio para a ferramenta.

   Registros brutos usados na hidratação ainda não são entidades prontas; a construção de uma entidade a partir deles continua usando a construção e a validação canônicas da entidade.

   Codecs e adaptadores podem verificar aspectos da representação de dados brutos, mas não ganham uma implementação paralela da validade da entidade.

   A validação na entidade não substitui as garantias atômicas exigidas pelo contrato de persistência por consultas prévias sujeitas a concorrência.

   JSON, codificação, formato de corpo e parâmetros do canal pertencem à fronteira L4; a forma técnica de um registro, sua serialização e desserialização, pertence a um codec ou adaptador segundo um contrato de representação.

   Auxiliares de validação usados por entidades e casos podem centralizar regras; não são transferidos para ferramentas nem evoluem como condições duplicadas. Uma interface de usuário pode oferecer prevenção de erros, mas a validação autoritativa também funciona por chamada direta ao núcleo. Ferramentas colaboradoras do programa distinguem-se de instrumentos de verificação de schemas, modelos e rastreabilidade do próprio OAL, que esta regra não restringe.

5. **Dependências e composição.** O modelo deve mostrar o que cada caso e ferramenta recebe, onde as implementações são selecionadas e como colaboradores são compostos. Não oculta dependências necessárias em buscas globais.

6. **Persistência.** O acesso à persistência ocorre por ferramentas. As responsabilidades pelos dados e as condições de leitura e alteração devem ser explícitas, independentemente de haver armazenamento compartilhado.

7. **Limite de autorização.** O modelo deve declarar uma entrada explícita para o contexto de ator resolvido conforme o contrato e uma decisão de autorização com recusa por padrão para cada caso. O caso recusa contextos ausentes, não resolvidos, desconhecidos ou insuficientes. Exige identidade autenticada quando o contrato a exige e admite contexto anônimo somente quando expressamente permitido. A decisão antecede efeitos de domínio e continua efetiva tanto em chamadas diretas quanto além dos controles da interface.

8. **Representação fiel.** Texto semântico ou pseudocódigo estruturado pode expressar ADPM. Ambas as formas devem permitir recuperar responsabilidades, contratos, composição de dependências, autorização, localizações de validação e algoritmos.

9. **Domínios — recomendação.** Recomenda-se agrupar responsabilidades do modelo por domínio quando isso esclarece os limites.

10. **Tempo de vida.** O modelo deve declarar o tempo de vida dos componentes quando pertinente. Pode-se escolher uma instância por caso no escopo da aplicação, sem tornar a escolha obrigatória.

<a id="advs"></a>
### ADVS — especificação de verificação orientada pela análise

Dentro do modelo L2, o componente ADVS deve estabelecer os assuntos a seguir; os artefatos que instanciam o modelo devem satisfazê-los no escopo declarado. A ADVS não precisa estar em arquivo ou pacote separado do ADPM.

1. **Derivação da UCS e teste comportamental.** Definir exatamente um teste comportamental diretamente vinculado a cada caso de uso UCS no escopo declarado, preservando sua identidade. Identificar a versão da UCS, os contratos e os critérios de aceite cobertos. Um teste comportamental pode compreender vários cenários e consumir subtestes de apoio — para permissões, alternativas, falhas e critérios — sem criar outros testes comportamentais para esse caso. Arquivos físicos podem reunir vários testes se o mapeamento de um para um entre casos continuar explícito.

2. **Contratos do teste e dos subtestes.** Declarar para o teste comportamental e cada cenário ou subteste de apoio preparação e precondições, contexto de ator nos cenários de caso, ação, oráculo (resultado e efeitos esperados) e limite ou configuração observada. Um cenário de caso pode fornecer deliberadamente um contexto ausente ou não resolvido para verificar a recusa. Verificações de apoio de entidades ou ferramentas podem declarar que o contexto de ator não se aplica. O teste comportamental pode exercitar o caso diretamente ou por um canal ADIB; seus subtestes apoiam esse teste sem vínculo direto com um caso UCS.

3. **Permissões.** Cobrir acesso permitido e negado para cada permissão distinta de caso, incluindo contextos ausentes, desconhecidos e insuficientes e participação explicitamente anônima quando aplicável ao contrato. Verificar a recusa antes de efeitos de domínio ou persistência.

4. **Falhas e limites.** Cobrir alternativas, falhas e limites relevantes especificados. Quando a ADIB selecionar um canal, acrescentar cenários para seu contrato de interação, como interpretação, representação, autenticação e acessibilidade quando aplicável; nomear riscos fora dos cenários escolhidos.

5. **Rastreabilidade e estado.** Vincular cada critério de aceite específico de caso da UCS ao teste comportamental de seu caso e às verificações de apoio que o cobrem. Vincular critérios compartilhados de integração explicitamente declarados aos testes comportamentais dos casos afetados e às verificações de apoio compartilhadas, sem criar testes comportamentais diretamente vinculados adicionais. Vincular obrigações específicas da ADIB declaradas às verificações planejadas.

   Recomenda-se verificar ferramentas e entidades, mas a ADVS não precisa ter especificações separadas para elas; as garantias contratuais e regras de validade ainda exigem as verificações necessárias para sustentar uma declaração de conformidade.

   Manter três objetos distintos: a verificação planejada, o código de teste e o resultado observado de uma execução. A presença de um arquivo de teste não demonstra que ele foi executado, e resultados aprovados sustentam apenas configurações observadas. Decisões da ADIB podem, portanto, exigir revisão da ADVS.

<a id="adi"></a>
## ADI (L3) — implementação orientada pela análise

Um modelo L3 é uma organização reutilizável de código. Define como responsabilidades, dependências, casos invocáveis e verificação são organizados em código e os critérios pelos quais seus artefatos concretos são reconhecidos. Uma arquitetura pode ser uma escolha dentro desse modelo. O modelo não precisa ter executado os testes de todos os projetos futuros que o instanciarão. Seus artefatos são códigos concretos organizados segundo esse modelo.

1. **Materialização dos papéis de L2 e dependências.** O modelo de organização de código deve definir como os papéis do ADPM — casos, entidades, ferramentas e domínios modelados — e suas dependências são materializados em código, e como identidades de caso, algoritmos e caminhos de erro se tornam um núcleo de aplicação invocável. Os artefatos devem preservar na organização de código selecionada a distinção e o mapeamento do ADPM; a organização física pode ser diferente. Desvios e artefatos de origem afetados são registrados. Mecanismos dos canais externos são especificados na ADIB.

2. **Autorização.** O modelo de organização de código deve definir como um contexto de ator é recebido por um caminho de invocação explícito e declarado e como o caso aplica sua política de autorização antes de efeitos de domínio. A origem do contexto e suas premissas de confiança permanecem identificáveis. Contextos ausentes, não resolvidos, desconhecidos, sem permissão ou de outra forma insuficientes são recusados em chamadas diretas e pela ADIB. Um contexto anônimo expressamente permitido é distinto de contexto ausente. A ADIB ou o mecanismo declarado de chamada direta fornece o contexto; o caso avalia sua própria política.

3. **Integração das verificações.** O modelo de organização de código deve definir como os testes comportamentais e verificações de apoio derivados da ADVS são integrados e executados contra o núcleo, preservando vínculos com casos, critérios e subtestes. Os artefatos relatam verificações falhas e não executadas; verificações específicas da ADIB também são executadas no canal escolhido.

4. **Composição e seleção de colaboradores.** O modelo de organização de código deve definir onde as implementações são selecionadas e como os colaboradores são compostos e fornecidos por dependências explícitas. Ferramentas concretas cumprem contratos ADPM na configuração declarada, incluindo garantias pertinentes de persistência, isolamento e falha.

5. **Evolução, rastreabilidade e evidência.** O modelo de organização de código deve definir como mudanças se propagam e permanecem rastreáveis até suas fontes de L2. Os artefatos declaram versão da implementação, ambiente, cenários executados, resultados e limites, e não apresentam verificações planejadas ou configuradas como execuções concluídas.

<a id="adib"></a>
## ADIB (L4) — fronteira de interação orientada pela análise

Um modelo conforme a L4 deve estabelecer os assuntos de interação a seguir; os artefatos que o instanciam devem satisfazê-los no escopo declarado.

1. **Escopo de interação.** Declarar os canais de interação oferecidos, os atores ou sistemas externos atendidos e suas capacidades. Um canal pode ser página, endpoint programático, linha de comando, consumidor de mensagens ou outra forma de entrada e saída. Indicar quais casos são expostos no escopo declarado.

2. **Estímulos e respostas.** Especificar como cada canal recebe e interpreta um estímulo, verifica sua representação, invoca casos da ADI e apresenta resultados e falhas. A resposta pode ser imediata, posterior ou emitida como evento; o contrato observável deve ser explícito.

3. **Contexto de ator na fronteira.** Resolver o contexto de ator pelo mecanismo declarado do canal e passá-lo à ADI. Autenticar o chamador quando exigido pelos contratos do caso e do canal. O modelo declara a origem do contexto e suas premissas de confiança; um rótulo de papel fornecido pelo chamador, isoladamente, não estabelece um contexto confiável. O acesso público pode resolver um contexto anônimo expressamente permitido. Resolução ausente ou falha não deve se tornar silenciosamente acesso anônimo. A ADI ainda aplica a política de autorização do caso. Ocultar um controle de interface ou verificar apenas a rota não autoriza o caso.

4. **Mapeamento muitos para muitos.** Registrar nos dois sentidos o mapeamento entre elementos da interface e identidades dos casos ADI que invocam; cada lado pode ter vários vínculos. Identificar separadamente elementos exclusivos da interface e sua finalidade.

5. **Limite das decisões.** Manter na ADIB decisões de transporte, apresentação, sessão e representação. Preservar nessa fronteira a distinção entre casos, ferramentas, entidades e domínios modelados no ADPM e realizados na ADI: a ADIB invoca casos em vez de absorver suas responsabilidades. A ADIB pode coordenar casos já especificados, mas não toma novas decisões de domínio nem acessa ferramentas de persistência do domínio diretamente.

   Pode usar armazenamento exclusivamente para estado técnico do canal, como sessões ou correlação de solicitações, sob contrato explícito que identifica os dados, condições de acesso, tempo de vida e comportamento em falhas. Esse armazenamento não deve introduzir regras de dados de negócio, contornar casos para ler ou alterar estado de domínio nem substituir a autorização do caso.

   Coordenação de interface que introduza nova transação, decisão ou objetivo de domínio exige especificá-lo como responsabilidade de caso, revisando a UCS e suas derivações; uma nova regra de negócio não é colocada em um endpoint ou script de interface apenas para evitar revisar L1 ou L2. Algoritmos dos casos e autorização permanecem na ADI.

6. **Contrato do canal.** Documentar rotas ou telas, comandos ou eventos, representações, erros e obrigações pertinentes de acessibilidade, localização e operação do canal escolhido. Requisitos impostos externamente são herdados com sua origem identificada; decisões introduzidas pela fronteira são registradas como decisões de L4. Quando a UCS for consultada, distinguir os requisitos herdados dela das decisões introduzidas na ADIB; caso contrário, identificar as fontes das obrigações do canal. Tornar verificável cada obrigação declarada.

7. **Verificação da interação.** Revisar a ADVS quando decisões da ADIB acrescentarem obrigações observáveis; vincular essas obrigações e os critérios UCS expostos a cenários de interface. Registrar resultados executados e limites de cada canal declarado sem tratar um núcleo funcional ou um cenário planejado como prova da interface.

## Interpretação

O inglês é a origem desta edição; o português é sua tradução. Apenas requisitos numerados definem conformidade. Recomendações estão assinaladas. O guia a seguir é informativo e não acrescenta requisitos; o conteúdo normativo sobre motores e conformidade está nas regras numeradas acima.

## Guia desta edição

Este guia explica as regras numeradas sem acrescentar requisitos.

### Conceitos

<a id="mathematical-notation"></a>

No OAL, analisar é registrar necessidades, regras, decisões, premissas e consequências de modo que outra pessoa possa conferi-las. As regras admitem diferentes documentos, linguagens, frameworks e ferramentas. Um repositório pode reunir artefatos desde que o leitor ainda consiga localizar a responsabilidade de cada camada.

Cada camada define um metamodelo; um modelo reutilizável é conforme à camada; artefatos concretos de projeto instanciam o modelo:

| Símbolo | Significado |
| --- | --- |
| $L_i$ | Metamodelo definido pela camada $i$. |
| $M_i$ | Modelo reutilizável selecionado, associado a $L_i$. |
| $a$, $b$ | Artefatos concretos de projeto, que podem reunir vários arquivos. |
| $\models$ | “Satisfaz os requisitos de”, conforme as regras de conformidade do OAL. |
| $\mathcal{M}_i$ | Classe de modelos reutilizáveis que satisfazem $L_i$. |
| $A(M)$ | Classe de artefatos que satisfazem o modelo selecionado $M$. |
| $\in$ | Pertencimento à classe ou ao conjunto indicado. |
| $\iff$ | “Se e somente se”: as duas afirmações são equivalentes. |

As relações do modelo e do artefato são:

$$
M_i \models L_i,
\qquad
a \models M_i.
$$

O pertencimento do artefato à classe de artefatos conformes é escrito como:

$$
a \in A(M_i) \iff a \models M_i.
$$

Leia assim: “$a$ é um artefato conforme a $M_i$ se e somente se satisfaz os requisitos desse modelo.” O pertencimento é a $A(M_i)$, a classe de artefatos; conformidade do modelo e conformidade do artefato continuam sendo declarações separadas.

A tabela a seguir ilustra as categorias; ela não atribui modelos genéricos aos exemplos deste repositório:

| Camada | Instância da camada (modelo reutilizável) | Instância desse modelo (artefato de projeto) |
| --- | --- | --- |
| L1 | Modelo genérico de especificação de projetos | Especificação de um projeto concreto |
| L2 | Modelo genérico integrado de programa e verificação | Modelagem do programa e plano de verificação de um projeto |
| L3 | Organização reutilizável de código | Código concreto organizado segundo esse modelo |
| L4 | Modelo reutilizável de interação e adaptação de canais | Interfaces e adaptadores concretos de um projeto |

Para uma edição, versões dos modelos e escopo declarado fixados, as classes são definidas por:

$$
\mathcal{M}_i = \{M \mid M \models L_i\},
\qquad
A(M) = \{a \mid a \models M\}.
$$

O símbolo $\mid$ é lido como “tal que”. O símbolo $\models$ denota a relação de conformidade do OAL definida pelas regras numeradas. A notação registra a relação pretendida entre camada, modelo e artefato; ela não prova, por si, uma declaração de conformidade. Toda declaração informa também seu escopo e a evidência examinada.

O Markdown usa LaTeX em linha com `$...$` e fórmulas destacadas com `$$...$$`, conforme o [suporte do GitHub a expressões matemáticas](https://docs.github.com/pt/get-started/writing-on-github/working-with-advanced-formatting/writing-mathematical-expressions). As fórmulas resumem os requisitos existentes; a prosa fornece seu significado e suas condições.

A UCS descreve comportamento, atores, permissões, significado dos dados, resultados e critérios de aceite. Pode registrar restrições de interação impostas externamente com sua origem; escolhas de interação introduzidas pela solução pertencem à ADIB. A ADMV é L2: seu componente ADPM define o modelo do programa — responsabilidades dos casos, entidades, ferramentas e seus contratos, composição de dependências, permissões, localizações de validação e algoritmos —, enquanto a ADVS define um teste comportamental para cada caso UCS. A ADI realiza o núcleo invocável da aplicação e registra resultados observados do núcleo. A ADIB define e realiza canais que recebem estímulos, chamam casos da ADI e apresentam respostas imediatas, posteriores ou emitidas como eventos. Essas responsabilidades não impõem uma ordem de construção. Uma decisão de canal pode exigir atualização da ADVS ou revelar requisito comportamental que pertence à UCS.

A localização da validação segue a mesma divisão de responsabilidades:

| Situação | Responsável |
| --- | --- |
| Campo obrigatório, limite de domínio, transição admissível | Entidade ou caso consumidor |
| Permissão para executar o caso | Caso, antes dos efeitos proibidos |
| JSON, codificação, formato de corpo e parâmetros do canal | Fronteira L4 |
| Forma técnica de um registro, serialização e desserialização | Codec ou adaptador, segundo contrato de representação |
| Construção de entidade durante hidratação | A entidade continua executando sua validação canônica |
| Unicidade atômica, transações, referências persistentes e escrita condicionada à versão | Garantia técnica da persistência, com significado e resposta de domínio definidos no núcleo |

Uma garantia técnica de armazenamento não transfere a definição de validade do domínio para a ferramenta ou para o SQL, e a validação no núcleo não substitui as garantias atômicas por consultas prévias que criam corrida de concorrência.

A tabela separa três perguntas que é fácil confundir. A coerência interna $I_E$ pertence à entidade: $V_E = \{e \mid I_E(e)\}$, e uma ferramenta que recebe uma entidade pronta recebe $e \in V_E$ por contrato. Uma repetição proibida é a ferramenta chamar a validação da entidade ou reimplementar a mesma condição de tamanho, formato ou transição sob outro nome, inclusive quando a condição é gerada automaticamente ou apresentada como garantia técnica. Uma verificação distinta permitida é uma condição contextual $Q_t(e, c)$ do próprio contrato da ferramenta — versão esperada, conflito de concorrência, unicidade global atômica ou disponibilidade de recurso externo, por exemplo. Essa condição tem objeto, finalidade e responsabilidade próprios e não decide a validade do domínio nem a autorização do caso. Uma terceira pergunta é a forma técnica de um registro bruto: um codec pode recusar dados serializados malformados, mas, ao construir uma entidade, usa a construção e a validação canônicas da entidade. A validação na entidade não substitui as garantias atômicas da persistência por consultas prévias que criam corrida de concorrência.

Um contrato L1 pode herdar uma restrição de interação imposta de fora, por exemplo “o gateway do cliente aceita apenas JSON sobre HTTPS”, citando o contrato externo como origem. Uma rota inventada pela implementação, como `POST /api/board`, é uma decisão de L4 mesmo quando a L1 registra o resultado subjacente. Nomear um protocolo ou uma rota na L1 não transfere a titularidade da decisão; registrar uma decisão de L4 na L1 não a transforma em requisito externo. Se uma decisão de canal revelar nova necessidade de domínio, a UCS e as derivações afetadas são revisadas.

As necessidades do cliente não são uma camada. Uma derivação Needs-to-L1 consome artefatos de um modelo externo de necessidades declarado ($M_{\mathrm{Needs}}$) e produz artefatos de um modelo L1 ($M_1$). Necessidades reconstruídas a partir de uma UCS existente mantêm essa proveniência visível.

Ator é um papel de interação especificado; o chamador é a pessoa ou sistema que desempenha esse papel. O contexto de ator contém as informações exigidas pelo contrato e possui um caminho de resolução declarado. A autenticação é exigida quando o contrato a exige, enquanto o caso sempre avalia sua política de autorização. Por exemplo, um modelo pode admitir um papel humano autenticado, um papel sistêmico resolvido para um processo agendado ou um papel explicitamente anônimo para uma operação pública. Contexto ausente não é contexto anônimo, e uma chamada por outro caso não concede permissão por si só. Um modelo simples pode representar o contexto por um identificador de papel quando declara a origem, o significado e as premissas de confiança desse identificador.

O responsável pela derivação é a pessoa identificada que responde pela produção ou aprovação de um artefato a partir da base de origem. Os papéis de trabalho são especificador (necessidades para UCS), modelador do programa (ADPM dentro de L2), projetista de verificação (ADVS dentro de L2 e depois cenários de canal), implementador (L2 completa para ADI) e projetista de interação (ADI para ADIB, com consulta opcional à UCS). Uma pessoa pode acumular papéis. O registro da derivação identifica a pessoa, versões de origem e destino, escopo e decisões acrescentadas.

Os nomes das camadas são L1 para UCS, L2 para ADMV, L3 para ADI e L4 para ADIB. Dentro de L2, ADPM e ADVS podem ser preparados em paralelo a partir de L1; continuam componentes distintos de uma única camada. Cada caso UCS tem um modelo de caso ADPM, um teste comportamental ADVS diretamente vinculado e um caso ADI implementado correspondentes. Um teste comportamental pode consumir vários subtestes de apoio; esses subtestes não são, por si, testes comportamentais. Elementos de interface e casos implementados têm mapeamento muitos para muitos. Navegação, conteúdo estático e outros elementos exclusivos da interface são identificados separadamente. As distinções do ADPM entre casos, ferramentas, entidades e eventuais domínios modelados continuam rastreáveis na ADI e através da fronteira ADIB, mesmo que a organização física seja diferente.

Um motor é um metamodelo, não meramente um processo que recebe um documento e gera outro. Construção e execução são momentos diferentes:

Para uma transição entre camadas vizinhas do OAL, os modelos selecionados satisfazem os metamodelos das respectivas camadas:

$$
M_n \models L_n,
\qquad
M_{n+1} \models L_{n+1}.
$$

**Construção.** Uma construção bem-sucedida segundo o motor $E$ é escrita como:

$$
\mathrm{Build}_E(M_n, M_{n+1})
\longrightarrow T[M_n, M_{n+1}].
$$

A seta registra uma construção com suas escolhas fixadas. Outras escolhas podem produzir outro transformador, e a construção pode falhar. $\mathrm{Build}$ nomeia a operação de construção especificada pelo motor; não prescreve uma fábrica executável.

**Execução.** Seja $T = T[M_n, M_{n+1}]$ esse transformador construído. Sob suas precondições e condições operacionais declaradas:

$$
T(a) = b,
\qquad
a \in D_T \subseteq A(M_n),
\qquad
b \in A(M_{n+1}).
$$

Aqui, $D_T$ é o domínio de entrada suportado, $a$ é o artefato de origem e $b$ é o artefato produzido. A saída satisfaz o modelo de destino selecionado: $b \models M_{n+1}$. Artefatos válidos de origem fora de $D_T$ permanecem fora da declaração de cobertura. A notação descreve a execução bem-sucedida; as categorias de falha declaradas continuam aplicáveis.

O transformador $T$ é especializado para aquele par de modelos e deve satisfazer o contrato do motor assim especializado. A construção congela decisões de mapeamento, representação, tecnologia e política; a execução aplica $T$ a uma entrada válida do domínio suportado e deve terminar com um artefato que satisfaz o modelo de destino selecionado e preserva as obrigações anunciadas. O Motor Needs-L1 consome um modelo externo de necessidades declarado; o Motor L1-L2 produz ADMV com ADPM e ADVS; o Motor L2-L3 usa ambos os componentes de L2 e pode consultar a UCS; o Motor L3-L4 usa casos invocáveis ADI para produzir canais de interação e também pode consultar a UCS. L4 introduz decisões próprias de apresentação e transporte. Uma implementação de motor declara edição, transição nomeada, entradas aceitas, saídas, vínculos preservados, decisões acrescentadas e escopo da validação. Seu uso em um projeto continua identificando a pessoa responsável.

Para modelos selecionados $M_1$, $M_2$ e $M_3$, o comportamento bem-sucedido pode ser escrito como:

$$
\begin{aligned}
T_{12}&\colon D_{12} \to A(M_2),
& D_{12} &\subseteq A(M_1),\\
T_{23}&\colon D_{23} \to A(M_3),
& D_{23} &\subseteq A(M_2).
\end{aligned}
$$

Essas assinaturas descrevem o que é garantido dentro do domínio suportado, sob as precondições e condições operacionais declaradas; as categorias de falha permanecem separadas. A preservação é uma relação $P_T \subseteq A(M) \times A(N)$ com $(a, T(a)) \in P_T$ para todo $a$ em $D_T$. Validade da saída e preservação são obrigações diferentes: um artefato pode satisfazer o modelo de destino e ainda perder uma identidade, contrato, critério, permissão ou relação que devia ser preservada.

Uma composição $T_{13}(a) = T_{23}(T_{12}(a))$ é definida apenas em $D_{13} \subseteq \{a \in D_{12} \mid T_{12}(a) \in D_{23}\}$. Compartilhar o mesmo modelo e a mesma versão intermediários não é suficiente: $T_{12}$ pode produzir um artefato válido de $M_2$ fora de $D_{23}$, e duas saídas equivalentes segundo o critério de determinismo de $T_{12}$ podem levar $T_{23}$ a aceitação ou resultado diferente. A composição exige, portanto, compatibilidade entre essa equivalência e as expectativas de entrada de $T_{23}$, ou uma forma canônica explicitamente consumida por $T_{23}$. As garantias anunciadas para uma composição são sustentadas pelas garantias dos componentes apenas em seu domínio declarado: $T_{12}$ deve preservar o que $T_{23}$ exige como entrada, e $T_{23}$ deve preservar as obrigações anunciadas de destino; nenhuma garantia de componente vale fora de seu próprio domínio. Exemplo: $M_2$ admite operações síncronas e assíncronas, mas $T_{23}$ suporta apenas síncronas. A saída $T_{12}(a)$ pode satisfazer $M_2$ e ainda conter uma operação assíncrona fora do domínio suportado por $T_{23}$, portanto $T_{12}(a) \notin D_{23}$; $D_{13}$ precisa excluir essas entradas, ou $T_{12}$ precisa ser restringido ou reconstruído para que suas saídas permaneçam em $D_{23}$. Contraexemplo: supor que toda saída conforme a $M_2$ é aceitável para $T_{23}$ porque ambos os componentes são chamados determinísticos ou porque o par declara a mesma versão de $M_2$.

Dois modelos conformes à mesma camada podem admitir representações diferentes preservando os contratos que definem essa camada. Quatro operações permanecem distintas: converter representações do mesmo modelo, traduzir entre modelos distintos da mesma camada, derivar entre camadas e substituir realizações do mesmo motor nomeado.

Para representações $r$ e $s$ de um modelo $M$, uma conversão sem perda do conteúdo do modelo pode ser escrita como $\mathrm{decode}_s(C_{rs}(x)) \equiv_M \mathrm{decode}_r(x)$, com domínio declarado para $C_{rs}$, definição das funções de decodificação e uma equivalência declarada $\equiv_M$; alegações de ida e volta também declaram o critério de equivalência do retorno. Uma conversão não é uma derivação, uma camada compartilhada não é um tradutor universal, e uma perda documentada não satisfaz um contrato que exige preservar a informação perdida.

Exemplos: converter a UCS JSON do Board CRM em suas representações LaTeX é uma conversão de representação de um modelo; traduzir dois modelos L1 com nomes de campos diferentes exige um mapeamento; derivar a ADMV da UCS acrescenta decisões de ADPM e ADVS e não é uma cópia da UCS.

Para substituição entre realizações de motor, considere dois transformadores hipotéticos $T_{12}^{A}\colon D_A \to A(M_2)$ e $T_{12}^{B}\colon D_B \to A(M_2)$, com $D_A, D_B \subseteq A(M_1)$, para as mesmas versões selecionadas de $M_1$ e $M_2$. A declaração de substituição fica limitada a um domínio de uso declarado: nesse domínio, ambos os transformadores devem preservar identidades, contratos, critérios e permissões anunciados e produzir saídas equivalentes segundo o critério declarado. A igualdade dos modelos de origem e destino, isoladamente, não é suficiente; se os domínios diferirem, a declaração vale apenas no domínio compartilhado. Esses transformadores são exemplos conceituais; não foram implementados nem executados.

Dois armazenamentos que implementam o mesmo contrato de ferramenta são uma substituição de implementações de ferramenta em L3, não uma realização de motor do OAL.

Uma implementação conjunta pode cobrir responsabilidades vizinhas sem construir o transformador entre elas; quando necessário, pode construir esse transformador internamente e fazer uma declaração separada quando a passagem tiver evidência. Um modelo combinado ou um pacote que apenas reúne artefatos demonstra coexistência, não transformação.

### Os exemplos deste repositório

O repositório especifica quatro modelos reutilizáveis didáticos, um por camada, em `examples/models/`: OAL-EX-M1-CASE-CONTRACTS (L1), OAL-EX-M2-PROGRAM-SCENARIOS (L2), OAL-EX-M3-PYTHON-CORE (L3) e OAL-EX-M4-HTTP-BOUNDARY (L4). Cada modelo tem identidade, versão 0.1.0, escopo, construções, condições de validade, template, exemplo preenchido, contraexemplo e limites declarados. São exemplos de modelos que declaram conformidade a esta edição; especificar um modelo e avaliar sua conformidade não são a mesma operação, e nenhuma delas prova que todo artefato futuro está correto.

Os pacotes de projeto declaram quatro instâncias cada — uma por modelo — em `model-instances.json`: Tiny Catalog, Board CRM e Work Board, doze declarações no total. A declaração de instância identifica o modelo, sua versão, a edição, os arquivos e símbolos que compõem o artefato, o escopo, os mapeamentos, a evidência e os limites. As declarações registram escopo, mapeamentos, estado da evidência e limites. Uma revisão estrutural pode conferir identidades, referências e arquivos declarados; ela não certifica conformidade semântica.

As bases de necessidades foram reconstruídas das UCS e continuam identificadas como reconstruídas; nenhum modelo externo de necessidades está especificado. Os registros não demonstram a construção nem a execução de transformadores determinísticos entre modelos: os modelos foram aplicados para adaptar manualmente os projetos existentes, não produzidos por uma cadeia de motores. Quatro objetos são avaliados separadamente: um modelo em relação ao metamodelo da camada; um artefato em relação ao modelo selecionado; um transformador especializado em relação ao metamodelo do motor; e uma execução concreta em relação às suas entradas, saídas e garantias declaradas.

<a id="versioning"></a>
### Versionamento e derivação

**Stable-v1.0.0** é o nome da edição; **1.0.0** é seu número de versão. Releases identificadas por commit/tag são imutáveis. Uma mudança que invalida conformidades anteriormente válidas exige revisão maior; uma extensão compatível exige revisão menor; uma correção editorial sem efeito normativo exige revisão corretiva. Uma correção ambígua exige análise de compatibilidade, sem classificação automática como editorial. Ambas as pastas Alpha permanecem históricas. O inglês é o texto de origem e o português é sua tradução.

Modelos, baselines de artefatos e pacotes de implementação têm versões independentes. O rótulo da versão não estabelece conformidade nem comprova execução de verificações. Mudanças em contratos, permissões ou decisões de interação exigem a análise de impacto da regra 4, incluindo modelos, transformadores, artefatos derivados e cenários afetados. Uma declaração identifica objeto, edição, escopo, baselines fixadas e evidências reais; não implica aprovação de outros objetos ou camadas.

<a id="verification"></a>
### Verificação

A ADVS registra o que verificar antes de declarar um resultado. Para cada caso UCS, seu teste comportamental único mantém o vínculo direto com o caso e identifica critérios cobertos, contexto de ator, preparação e precondições, ação, oráculo (resultado e efeitos esperados) e limite ou configuração relevante. Ele pode consumir subtestes de apoio para atores permitidos e negados, alternativas e falhas; esses não têm vínculo direto com o caso UCS. A ADVS não precisa prescrever verificações separadas para toda ferramenta ou entidade, embora isso seja recomendado. Garantias contratuais e validade das entidades ainda precisam de evidência suficiente para o escopo declarado. Verificação planejada, código de teste e resultado observado de execução são três objetos distintos; um arquivo de teste em disco não prova que ele foi executado.

A ADI executa verificações do núcleo da aplicação. Quando a ADIB escolhe um canal, a ADVS também registra cenários para interpretação, representação, autenticação, acessibilidade e outras obrigações declaradas do canal, quando aplicáveis. A evidência de execução da ADIB informa quais canais e configurações foram exercitados. Verificações de permissão cobrem a recusa antes de efeitos de domínio ou persistência. Cenários planejados e resultados executados permanecem distintos.

Os exemplos contêm verificações unitárias para entidades e ferramentas puras, de integração para ferramentas que usam outros recursos e verificações voltadas aos casos. O uso de substituto, SQLite ou HTTP não define, por si, se uma verificação é comportamental: o vínculo direto e único com um caso UCS é que define. No diretório de cada exemplo, `python -m pytest` executa sua suíte; qualquer resultado informado descreve aquela execução e seu ambiente.

<a id="conformance"></a>
### Conformidade e escopo

As regras numeradas acima definem conformidade. Quatro declarações são distintas: conformidade do modelo a uma camada determinada; conformidade do artefato ao seu modelo selecionado; cobertura de um conjunto declarado de camadas; e cobertura completa das camadas L1, L2, L3 e L4. Um modelo $M_1$ pode ser plenamente conforme a L1 sem cobrir L4. Quando L2 está no escopo, ADPM e ADVS continuam obrigatórios. A expressão “modelo completo” é usada apenas quando o modelo, a versão e o significado de completude são inequívocos; caso contrário, a declaração nomeia seu escopo.

Uma declaração informa edição, versões dos artefatos do projeto, o objeto declarado (modelo, artefato, construção de transformador, execução de transformador ou composição de transformadores), as camadas e casos no escopo, responsáveis identificados pelas derivações e evidência efetivamente examinada. A conformidade do modelo e a do artefato são declarações separadas, com limites separados. Uma declaração de cobertura de todas as camadas inclui L1, L2, L3 e L4; uma declaração mais restrita nomeia as responsabilidades cobertas.

Revisar a UCS para comportamento e atores permitidos; a ADMV (L2) tanto para os algoritmos dos casos, contratos, composição de dependências, localizações de validação e decisões de permissão do ADPM quanto para o teste comportamental por caso UCS, subtestes de apoio e cobertura da ADVS; a ADI para casos invocáveis, aplicação das permissões e resultados observados do núcleo; e a ADIB para contratos dos canais, resolução do contexto de ator, decisões de interação e resultados observados nos canais.

Comparar nos dois sentidos as identidades dos casos entre UCS, ADPM, testes comportamentais ADVS e ADI. Vincular cada critério de aceite específico de caso da UCS ao teste comportamental de seu caso e às verificações de apoio; vincular critérios compartilhados de integração declarados aos testes comportamentais dos casos afetados e às verificações compartilhadas. Para cada canal ADIB declarado, examinar nos dois sentidos o mapa muitos para muitos entre elementos de interface e casos implementados, identificar elementos exclusivos da interface e vincular obrigações do canal a verificações. A contagem isolada não demonstra preservação de contratos. Verificação planejada não é resultado executado. A [revisão do Tiny Catalog](examples/tiny-catalog/OAL-P3/CONFORMANCE.pt-br.md) registra uma avaliação mais restrita dos artefatos desse exemplo.

### Trabalhos relacionados

OAL dialoga com especificação de casos de uso, rastreabilidade, limites de dependência e derivação de testes. Os links aqui oferecem contexto, sem acrescentar requisitos. [Use-Case 2.0](https://www.ivarjacobson.com/publications/white-papers/use-case-20-e-book) descreve o trabalho incremental com casos de uso do projeto até os testes. [Couto, Ribeiro e Campos](https://arxiv.org/abs/1603.08632) discutem formalização de casos e consistência. [Hajri e colegas](https://arxiv.org/abs/1905.11699) estudam classificação e priorização de testes de sistema a partir de casos de uso.

A [documentação Python sqlite3](https://docs.python.org/3.13/library/sqlite3.html) apoia a implementação de armazenamento dos exemplos. O [guia de workflow Python do GitHub](https://docs.github.com/en/actions/tutorials/build-and-test-code/python) orienta a automação do repositório. Nenhuma dessas tecnologias é exigida pelo OAL.
