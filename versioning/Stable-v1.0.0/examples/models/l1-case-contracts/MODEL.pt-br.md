# OAL-EX-M1-CASE-CONTRACTS — Simple Case Contracts (L1)

[English](MODEL.md) · [Modelos](../README.pt-br.md) · [Regras de referência](../../../../Stable-v1.0.0/README.pt-br.md#reference-rules)

**Identidade:** `OAL-EX-M1-CASE-CONTRACTS`
**Versão:** 0.1.0
**Camada:** L1 (UCS)
**Edição OAL declarada:** Stable-v1.0.0
**Estado:** exemplo de modelo reutilizável. Este documento especifica o modelo; não certifica artefato de projeto.

## 1. Objetivo e escopo

O modelo define uma especificação de casos que um projeto pode reutilizar. Fixa os campos lógicos, seus significados e as condições que tornam um artefato uma instância válida. É intencionalmente mais simples que uma linguagem geral de requisitos: cobre os assuntos exigidos pelas regras L1 e nada além deles.

O modelo cobre um escopo de projeto com conjunto fechado de atores, entidades, regras, casos de uso, obrigações complementares e critérios de aceite. Não prescreve organização de arquivos, linguagem, formato de serialização, interface de usuário ou decomposição de domínio. Não define um modelo externo de necessidades: necessidades entram como fontes declaradas com sua proveniência.

## 2. Construções e relações

| Construção | Significado |
| --- | --- |
| `ProjectSpecification` | Objeto raiz: identidade, versão, edição, escopo, fontes, estado, conteúdo canônico. |
| `Actor` | Papel de interação declarado na especificação, desempenhado por pessoa ou sistema que solicita um caso. O chamador concreto e o contexto de ator da execução são distintos do papel; o responsável pela derivação tem outra responsabilidade. |
| `Entity` | Significado dos dados, campos, relações, invariantes e localização canônica das condições de validade. |
| `Rule` | Condição de domínio compartilhada, com os casos que a aplicam. |
| `CaseContract` | Um caso de uso: identidade, objetivo, atores, acionamento, entradas, contexto, precondições, resultados, efeitos, alternativas, falhas, construções referenciadas, obrigações, critérios. |
| `Obligation` | Requisito complementar com natureza, enunciado, origem, escopo, condições verificáveis e responsabilidade. |
| `Criterion` | Critério de aceite pertencente a exatamente um caso. |
| `SharedCriterion` | Critério de integração declarado separadamente, abrangendo casos e obrigações complementares identificados, com uma definição canônica. |
| `TraceLink` | Referência resolvida de um caso ou critério para necessidades, entidades, regras, obrigações, capacidades ou outros casos. |

Relações: `specification` possui `actors`, `entities`, `rules`, `obligations` e `cases`; cada `case` referencia atores, entidades, regras, obrigações, capacidades e dependências, e possui seus `criteria`; cada `criterion` próprio de caso pertence a um caso; `shared_criteria` opcionais pertencem à especificação e referenciam os casos e obrigações envolvidos; cada `rule` nomeia os casos que a aplicam; cada `obligation` nomeia escopo e origem. Um critério transversal não cria novo caso de uso nem outro teste comportamental diretamente vinculado.

O contexto e as precondições dos casos declaram como o contexto de ator é estabelecido, se autenticação é exigida e quais são as condições de autorização. Contexto ausente ou não resolvido é recusado. Acesso anônimo só é válido para um papel anônimo declarado e permitido expressamente; nunca é inferido de contexto ausente. Chamadores sistêmicos seguem as mesmas regras. Um caso que chama outro transmite o contexto pertinente, e o caso chamado aplica sua própria política. Delegação deve ser declarada.

## 3. Campos

O template legível por máquina é [`template.json`](template.json). Campos obrigatórios (O), opcionais (P) e condicionais (C):

| Objeto | Campo | Tipo | Observações |
| --- | --- | --- | --- |
| ProjectSpecification | `identity`, `version`, `oal_edition`, `scope`, `status` | O | O estado distingue baseline, rascunho e revisado. |
| ProjectSpecification | `sources` | O | Cada fonte tem `id`, `description`, `provenance`; necessidades reconstruídas são marcadas `reconstructed`. |
| ProjectSpecification | `canonical_content` | O | Nomeia a representação canônica de cada grupo de campos. |
| ProjectSpecification | `facts` | C | Obrigatório quando aparecem fatos observados, requisitos, inferências, premissas ou pendências. Cada entrada tem `kind`. |
| Actor | `id`, `name`, `description` | O | Papéis são atores de execução. |
| Entity | `id`, `meaning`, `fields`, `relations`, `invariants`, `validity_owner`, `validity_location` | O | `validity_owner` é a entidade ou o caso consumidor; nunca uma ferramenta. |
| Rule | `id`, `statement`, `applied_by` | O | `applied_by` lista IDs de caso. |
| CaseContract | `id`, `title`, `objective`, `initiating_actor`, `permitted_actors` | O | O ator iniciador deve ser permitido. |
| CaseContract | `trigger`, `inputs`, `context`, `preconditions`, `results`, `effects`, `alternatives`, `failures` | O | Resultados incluem a recusa observável de acesso. |
| CaseContract | `entities`, `rules`, `capabilities`, `dependencies`, `obligations` | P | Referências precisam resolver. |
| CaseContract | `criteria` | O | Pelo menos um critério. |
| Obligation | `id`, `nature`, `statement`, `origin`, `scope`, `verifiable_conditions`, `responsibility` | O | `origin` é `external`, `domain`, `assumption` ou `l4-decision`; origem externa cita a fonte. |
| Criterion | `id`, `statement` | O | Globalmente único; pertence ao caso que o contém ou ao `case_id` explícito. |
| SharedCriterion | `id`, `statement`, `case_ids`, `obligation_ids`, `verifiable_conditions` | C | Obrigatório em cada critério de integração declarado. Os conjuntos de casos e obrigações são não vazios e resolvem. |

O artefato declara suas representações; JSON estruturado, narrativa Markdown e TeX são exemplos, não uma lista fechada. Pode combiná-las quando todo o conteúdo obrigatório permanece recuperável. O modelo exige uma fonte canônica por grupo de campos e um mapeamento e regra de consistência explícitos entre representações. Uma revisão ou uma verificação de representação existente detecta divergência; alterações de formatação não criam outro modelo.

## 4. Condições de validade

Um artefato é instância válida de `OAL-EX-M1-CASE-CONTRACTS` 0.1.0 quando todas as condições valem:

- **V-M1-01 — Identidade.** `identity`, `version` e `oal_edition` estão presentes. A versão de modelo declarada pela instância é exatamente `0.1.0`.
- **V-M1-02 — Identificadores únicos.** Identificadores de ator, entidade, regra, obrigação, caso e critério são únicos no artefato.
- **V-M1-03 — Referências resolvidas.** Toda referência a ator, entidade, regra, obrigação, capacidade, dependência e caso resolve para um objeto declarado.
- **V-M1-04 — Conjuntos e contexto de atores.** Cada caso tem ator iniciador e conjunto de atores permitidos; o iniciador pertence ao conjunto; todo ator permitido existe. Seu contrato declara o contexto de ator necessário, a autenticação quando exigida e as condições de autorização. Contextos ausentes, não resolvidos, desconhecidos ou sem permissão são recusados. Papéis anônimos ou sistêmicos são explícitos; chamada interna não concede permissão adicional.
- **V-M1-05 — Critérios.** Cada caso tem pelo menos um critério próprio; cada um desses critérios pertence a exatamente um caso e é referenciado por ele. Um critério transversal de integração é declarado separadamente com identificador único, enunciado completo, IDs dos casos e obrigações envolvidos e condições verificáveis. Possui uma definição canônica e não substitui os critérios dos casos envolvidos.
- **V-M1-06 — Regras compartilhadas.** Toda regra nomeia os casos que a aplicam; uma regra compartilhada tem uma única definição canônica.
- **V-M1-07 — Obrigações.** Toda obrigação tem natureza, enunciado, origem, escopo, condições verificáveis e responsabilidade. Origem externa cita a fonte; decisão introduzida pela solução é marcada `l4-decision` e não é apresentada como requisito externo.
- **V-M1-08 — Fatos.** Fatos observados, requisitos desejados, inferências, premissas e pendências são distinguíveis. Necessidades reconstruídas são marcadas `reconstructed`.
- **V-M1-09 — Validade das entidades.** Toda entidade declara significado, campos, relações, invariantes e a localização canônica das condições de validade. A validade é atribuída à entidade ou ao caso consumidor, nunca a uma ferramenta.
- **V-M1-10 — Sem decisões de canal embutidas.** Um caso não enuncia rota, codificação de payload, tela, protocolo ou representação como requisito de domínio. Quando tal referência aparece, sua origem é declarada.
- **V-M1-11 — Conteúdo canônico.** O artefato nomeia seu conteúdo canônico e, quando há várias representações, o mapeamento e a regra de consistência entre elas.

O modelo não exige convenção de nomes, organização de pastas, quantidade de arquivos ou esquema de serialização além do conteúdo canônico declarado.

## 5. Mapeamento para as regras L1 do OAL (Stable-v1.0.0)

| Regra L1 do OAL | Construção ou condição do modelo |
| --- | --- |
| 1. Escopo | `ProjectSpecification.scope`, fontes e `facts`. |
| 2. Casos de uso | Identidade, objetivo, ator iniciador e conjunto permitido do `CaseContract`; V-M1-04. |
| 3. Contratos comportamentais | Acionamento, entradas, contexto, precondições, resultados, efeitos, alternativas e falhas do caso; recusa; V-M1-10. |
| 4. Entidades e regras | `Entity`, `Rule`, V-M1-06, V-M1-09. |
| 5. Composição e dependências | `capabilities`, `dependencies` e `TraceLink` do caso. |
| 6. Obrigações complementares | `Obligation` com natureza, origem, escopo e condições verificáveis; V-M1-07. |
| 7. Aceite e vínculos | `Criterion`, critérios do caso, `SharedCriterion` com escopo declarado e vínculos de rastreabilidade; V-M1-05. |
| 8. Consistência e evolução | Identificadores únicos, referências resolvidas, conteúdo canônico e `facts`; V-M1-02, V-M1-08, V-M1-11. |
| 9. Domínios (recomendação) | Não exigido; um campo de domínio pode ser acrescentado sem mudar a identidade do modelo. |
| 10. Exemplos representativos | O exemplo do modelo é explicitamente parcial; não substitui os contratos dos casos. |

## 6. Template, exemplo e contraexemplo

- [`template.json`](template.json) é o template lógico com campos obrigatórios e opcionais.
- [`example.json`](example.json) é um **recorte parcial** do Tiny Catalog, assim rotulado. Ilustra as construções e não substitui a UCS completa.
- [`counterexample.json`](counterexample.json) é uma instância inválida. Contém um caso cujo ator permitido não foi declarado, uma obrigação sem origem, uma regra aplicada por um caso não declarado e um caso sem critérios; a entidade também atribui sua validade a uma ferramenta, e um critério transversal de integração tem escopo não resolvido e nenhuma condição verificável. As violações esperadas estão listadas no arquivo; um validador ou revisão deve recusá-la.

## 7. Evidência e limites

O modelo foi revisado contra as regras L1 acima. A revisão está documentada neste arquivo; não é certificada por máquina. O modelo é deliberadamente parcial: não define um modelo de necessidades, uma taxonomia de domínios, uma lógica temporal formal nem um algoritmo para gerar casos. Seus exemplos são recortes ilustrativos, não especificações completas de projeto.

As condições de validade do modelo são estruturais. Passar por elas significa que os campos e referências declarados são coerentes; não prova que os contratos descrevem o sistema real nem que os critérios são suficientes. Esse julgamento permanece uma revisão do artefato contra suas fontes, como exigem as regras de conformidade do OAL.

## 8. Instanciar e verificar

1. Copie o template e preencha escopo, fontes, atores, entidades, regras, casos, obrigações e critérios do projeto.
2. Atribua uma fonte canônica por grupo de campos.
3. Confira V-M1-01 a V-M1-11. Um projeto pode acrescentar restrições, mas não pode remover estas.
4. Registre a versão do artefato e a versão do modelo em `model-instances.json` (entrada L1).
5. Uma revisão estrutural confere identidades, referências, arquivos e mapeamentos declarados. A revisão semântica confere se contratos e critérios são adequados ao projeto.

## Avaliação de compatibilidade estável

Origem: Alpha-v0.2.0-Alkimim, modelo 0.1.0. Para Stable-v1.0.0, as regras numeradas do OAL e os campos e condições de validade deste modelo foram comparados com essa baseline; permanecem iguais. O mapeamento acima continua aplicável ao mesmo escopo didático. Esta revisão de compatibilidade não é certificação externa nem execução de transformador. O [relatório de avaliação](../../../COMPATIBILITY.pt-br.md) registra escopo e limites; execuções dos projetos são registradas separadamente.
