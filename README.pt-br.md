<p align="center"><img src="assets/oal-banner-pt-br.png" alt="OAL — Open Analysis Layers" width="100%"></p>

<p align="center"><strong>OAL Alpha-v0.1.0-Alkimim</strong><br>Português brasileiro · <a href="README.md">English</a></p>

# OAL — Open Analysis Layers

OAL organiza o trabalho de um sistema em cinco responsabilidades ligadas: especificar casos de uso, modelar o programa, planejar verificações comportamentais, construir o núcleo invocável e expô-lo por interfaces. Cada derivação registra suas fontes, decisões e pessoa responsável. Equipes podem aplicar o modelo com linguagens, ferramentas, documentos e estruturas de pastas diferentes.

## Sumário

- [As cinco camadas](#as-cinco-camadas)
- [Correspondência e cardinalidade dos casos](#correspondência-e-cardinalidade-dos-casos)
- [Motores de derivação](#motores-de-derivação)
- [Traduções e implementações conjuntas](#traduções-e-implementações-conjuntas)
- [Versões](#versões)
- [Exemplos](#exemplos)
- [Perguntas frequentes](#perguntas-frequentes)
- [Autoria e créditos](#autoria-e-créditos)

## As cinco camadas

<p align="center"><img src="assets/oal-layers-pt-br.png" alt="Camadas de referência do OAL" width="750"></p>

| Camada | O que acrescenta |
| --- | --- |
| **L1 · UCS** | Define os casos de uso: objetivos, atores e permissões, comportamento, regras de domínio, resultados e critérios de aceite. Descreve o contrato observável sem escolher telas, rotas ou estrutura de código. |
| **L2.1 · ADPM** | Modela decisões e algoritmo de cada caso, entidades, ferramentas e seus contratos e composição de dependências. Distingue essas responsabilidades sem prescrever uma arquitetura concreta. |
| **L2.2 · ADVS** | Define exatamente um **teste comportamental** diretamente vinculado a cada caso UCS. Esse teste pode consumir subtestes de apoio para permissões, alternativas, falhas e critérios. Verificações de ferramentas e entidades são recomendadas, mas não precisam ser especificações ADVS separadas. |
| **L3 · ADI** | Implementa os casos modelados como núcleo invocável da aplicação. Preserva as distinções e mapeamentos do ADPM na arquitetura escolhida, aplica permissões nos casos e registra resultados observados. |
| **L4 · ADIB** | Constrói a fronteira externa de interação: páginas, endpoints, comandos, mensagens ou outros canais. Recebe pedidos, invoca casos da L3 e apresenta resultados, mantendo decisões do canal fora do núcleo. |

**L2.1 e L2.2 derivam da L1 em paralelo.** Em um escopo declarado, cada caso de uso tem um caso ADPM, um teste comportamental ADVS e um caso ADI correspondentes. Subtestes de apoio não são testes comportamentais porque não têm vínculo direto com um caso UCS. Um elemento de interface ADIB pode invocar vários casos, e um caso pode aparecer em vários elementos. Esses vínculos preservam a identidade dos casos sem exigir a mesma estrutura de arquivos ou classes em todo projeto. Consulte as [regras entre camadas](versioning/Alpha-v0.1.0-Alkimim.pt-br.md#oal-layers), as [regras do ADPM](versioning/Alpha-v0.1.0-Alkimim.pt-br.md#adpm) e as [regras da ADVS](versioning/Alpha-v0.1.0-Alkimim.pt-br.md#advs).

A separação do ADPM entre casos, ferramentas, entidades e domínios opcionais deve continuar identificável na ADI e através da ADIB. A ADIB deriva sua fronteira de interação dos casos invocáveis da ADI e também pode consultar a UCS. A ADIB não é cópia da ADI. As [regras da ADI](versioning/Alpha-v0.1.0-Alkimim.pt-br.md#adi) e da [ADIB](versioning/Alpha-v0.1.0-Alkimim.pt-br.md#adib) definem esses limites.

## Correspondência e cardinalidade dos casos

<p align="center"><img src="assets/oal-map-pt-br.png" alt="Vínculos um para um entre casos de L1, L2 e L3; relação muitos para muitos entre casos L3 e elementos de interface L4" width="750"></p>

Os vínculos um para um dizem respeito às **identidades dos casos**: um caso UCS, um caso ADPM, um teste comportamental ADVS e um caso ADI. As verificações de apoio podem ser numerosas. Entre os casos da ADI e os elementos de interface da ADIB, a relação é muitos para muitos.

## Motores de derivação

Um **motor OAL** produz uma camada a partir de material de origem. Pode ser um processo humano, software ou ambos. O motor LX-LY usa LX para produzir LY; não precisa traduzir a origem literalmente. Por exemplo, L4 acrescenta escolhas de interação que não existem em L3.

| Motor | Entradas → saída |
| --- | --- |
| **Motor Necessidades-L1** | Necessidades das partes interessadas → UCS (L1). |
| **Motor L1-L2.1** | UCS → ADPM (L2.1). |
| **Motor L1-L2.2** | UCS → ADVS (L2.2). |
| **Motor L2-L3** | ADPM **e** ADVS → ADI (L3); a UCS (L1) pode ser consultada como fonte adicional. L2 abrevia o par L2.1/L2.2; não é outra camada. |
| **Motor L3-L4** | ADI → ADIB (L4); a UCS (L1) pode ser consultada como fonte adicional. |

Uma derivação concreta registra versões de origem e destino, escopo, decisões acrescentadas e pessoa responsável. Uma implementação pode se apresentar como instância de uma camada ou motor OAL ao declarar edição, entradas e saídas quando pertinentes, escopo, vínculos preservados e evidências de apoio. Consulte a [regra dos motores](versioning/Alpha-v0.1.0-Alkimim.pt-br.md#oal-layers) e o [guia de versionamento](versioning/Alpha-v0.1.0-Alkimim.pt-br.md#versioning).

## Traduções e implementações conjuntas

Implementações da mesma camada compartilham os contratos que a definem. Por isso, uma pode ser traduzida em outra mesmo com linguagens ou formatos diferentes. A tradução registra quais características comuns foram preservadas e quais detalhes se perderam ou mudaram. O mesmo vale para implementações do mesmo motor nomeado.

Uma especialização pode reunir camadas vizinhas. Quando realiza a derivação entre elas, também implementa o motor correspondente. Origem, destino e passagem continuam exigindo evidências distinguíveis. Para L2-L3, a entrada L2 obrigatória inclui **ADPM e ADVS**. Consulte as [regras entre camadas](versioning/Alpha-v0.1.0-Alkimim.pt-br.md#oal-layers).

## Versões

| Edição | Situação | Regras de referência | Notas |
| --- | --- | --- | --- |
| Alpha-v0.1.0-Alkimim | Versão alfa finalizada | [Português](versioning/Alpha-v0.1.0-Alkimim.pt-br.md) · [English](versioning/Alpha-v0.1.0-Alkimim.md) | [Notas da edição](versioning/Alpha-v0.1.0-Alkimim.pt-br.md#notas-da-versao) |

Os guias de [verificação](versioning/Alpha-v0.1.0-Alkimim.pt-br.md#verification) e [conformidade](versioning/Alpha-v0.1.0-Alkimim.pt-br.md#conformance) explicam o alcance de cada resultado. O inglês é o texto de origem; o português é sua tradução.

## Exemplos

O repositório inclui Tiny Catalog, Board CRM e Work Board. Seus artefatos, funcionalidades, credenciais de demonstração e instruções de execução estão no [guia dos exemplos](examples/README.pt-br.md).

## Perguntas frequentes

<details><summary>OAL exige uma estrutura fixa de pastas?</summary>

Não. As camadas nomeiam responsabilidades. Um projeto pode reunir ou dividir arquivos e módulos mantendo contratos e derivações identificáveis.

</details>

<details><summary>O ADPM precisa usar pseudocódigo ou prescrever uma arquitetura?</summary>

Não. Texto semântico e pseudocódigo estruturado são válidos se especificarem casos, entidades, ferramentas, contratos, composição de dependências, permissões e algoritmos. O ADPM distingue e mapeia essas responsabilidades; a ADI escolhe uma arquitetura concreta que preserva o mapeamento.

</details>

<details><summary>Por que L2.1 e L2.2 são paralelas?</summary>

O ADPM modela o programa e a ADVS especifica a verificação. Ambos derivam da UCS. A numeração não determina uma ordem entre eles; ambos informam a ADI.

</details>

<details><summary>Um caso de uso pode ter vários testes comportamentais?</summary>

Não. Um caso UCS tem um teste comportamental ADVS diretamente vinculado. Esse teste pode consumir vários subtestes de apoio, que não são testes comportamentais. Verificações de ferramentas, entidades ou canais de interface também podem ser registradas sem criar outro teste comportamental para o caso.

</details>

<details><summary>O que caracteriza uma implementação de motor OAL?</summary>

Ela identifica transição nomeada e edição, entradas aceitas, saídas produzidas, vínculos preservados, decisões acrescentadas e escopo da validação. Cada derivação de projeto também identifica a pessoa responsável e as versões de origem e destino.

</details>

<details><summary>Quem é o ator?</summary>

Um ator de execução é pessoa ou sistema externo que solicita um caso de uso. A pessoa responsável pela derivação de um artefato é nomeada separadamente. Cada caso define atores permitidos; atores ausentes ou desconhecidos são recusados.

</details>

<details><summary>A ADIB se limita a uma API programática?</summary>

Não. Ela cobre páginas, endpoints programáticos, comandos, mensagens e outros canais de interação. OAL usa ADIB para essa fronteira mais ampla.

</details>

<details><summary>A ADIB precisa de um elemento de interface por caso de uso?</summary>

Não. Um elemento pode invocar vários casos especificados, e um caso pode aparecer em vários elementos. Registre os vínculos nos dois sentidos e identifique separadamente elementos exclusivos da interface.

</details>

<details><summary>Onde ficam autenticação e autorização?</summary>

A ADIB resolve ou autentica o chamador e passa a identidade do ator à ADI. O caso na ADI aplica sua permissão mesmo quando invocado diretamente. Rotas, páginas, formatação e sessões pertencem à ADIB.

</details>

<details><summary>Um teste aprovado comprova todo o modelo?</summary>

Não. Ele sustenta a verificação e a configuração observadas. A ADVS registra verificações planejadas; ADI e ADIB relatam execuções para os limites e ambientes declarados.

</details>

<details><summary>Os exemplos Python são implementações obrigatórias?</summary>

Não. Eles mostram escolhas possíveis de linguagem, armazenamento e navegador. As regras de referência admitem outras escolhas.

</details>

## Autoria e créditos

OAL foi idealizado e escrito por **Douglas de Oliveira Alkimim** e **Bruno Chevitarese**. Consulte os [metadados de citação](CITATION.cff) e a [licença MIT](LICENSE).

<table align="center" cellspacing="16" cellpadding="8">
  <tr>
    <td width="340" valign="top">
      <div>
        <img src="https://avatars.githubusercontent.com/u/65194413?v=4" alt="Douglas de Oliveira Alkimim" width="88" height="88" align="left" hspace="12">
        <strong>Douglas de Oliveira Alkimim</strong><br>
        <a href="https://github.com/douglas-alkimim"><img src="https://img.shields.io/badge/GitHub-181717?logo=github&amp;logoColor=white" alt="Douglas no GitHub"></a>&nbsp;<a href="https://www.linkedin.com/in/douglas-alkimim/"><img src="https://img.shields.io/badge/LinkedIn-0A66C2?logo=linkedin&amp;logoColor=white" alt="Douglas no LinkedIn"></a>
        <br clear="all">
      </div>
    </td>
    <td width="340" valign="top">
      <div>
        <img src="https://avatars.githubusercontent.com/u/150291749?v=4" alt="Bruno Chevitarese" width="88" height="88" align="left" hspace="12">
        <strong>Bruno Chevitarese</strong><br>
        <a href="https://github.com/chevitaresebruno"><img src="https://img.shields.io/badge/GitHub-181717?logo=github&amp;logoColor=white" alt="Bruno no GitHub"></a>&nbsp;<a href="https://www.linkedin.com/in/bruno-chevitarese/"><img src="https://img.shields.io/badge/LinkedIn-0A66C2?logo=linkedin&amp;logoColor=white" alt="Bruno no LinkedIn"></a>
        <br clear="all">
      </div>
    </td>
  </tr>
</table>
