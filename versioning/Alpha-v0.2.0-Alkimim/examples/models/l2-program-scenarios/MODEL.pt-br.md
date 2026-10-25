# OAL-EX-M2-PROGRAM-SCENARIOS — Registros de Programa e Cenários (L2)

[English](MODEL.md) · [Modelos](../README.pt-br.md) · [Regras de referência](../../../../Alpha-v0.2.0-Alkimim/README.pt-br.md#reference-rules)

**Identidade:** `OAL-EX-M2-PROGRAM-SCENARIOS`
**Versão:** 0.1.0
**Camada:** L2 (ADMV: ADPM + ADVS)
**Edição OAL declarada:** Alpha-v0.2.0-Alkimim
**Estado:** exemplo de modelo reutilizável. Este documento especifica o modelo; não certifica artefato de projeto.

## 1. Objetivo e escopo

O modelo define o artefato L2 como um par $a_2 = (p, v)$, em que $p$ é o componente ADPM (modelo do programa) e $v$ é o componente ADVS (especificação da verificação). Ambos são obrigatórios. O modelo cobre as obrigações das regras L2 e a correspondência entre casos UCS, casos de programa, testes comportamentais e critérios de aceite.

O modelo não escolhe linguagem, arquitetura, framework de teste nem organização de arquivos. Fixa os registros lógicos que um artefato L2 deve conter e as condições que o tornam válido.

## 2. Construções e relações

**ADPM ($p$)**

| Construção | Significado |
| --- | --- |
| `ProgramCase` | Um caso de programa: caso UCS vinculado, colaboradores, sequência/decisões, resultados, efeitos, erros, entrada de permissão. |
| `ProgramEntity` | Registro de entidade: entidade UCS vinculada e localização canônica das condições de validade. |
| `ToolContract` | Operação, entradas, saídas, garantias, falhas, premissa de entidade pronta e condições contextuais. |
| `Dependency` / `Composition` | O que cada caso e ferramenta recebe, onde as implementações são selecionadas, como colaboradores são ligados. |
| `Authorization` | Contexto de ator resolvido explicitamente, autenticação exigida pelo contrato e decisão de recusa por padrão de cada caso. |
| `Lifetime` | Tempo de vida dos componentes quando pertinente. |

**ADVS ($v$)**

| Construção | Significado |
| --- | --- |
| `BehavioralTest` | Exatamente um por caso UCS: caso vinculado, critérios cobertos, limite, cenários planejados, verificações de apoio, estado. |
| `Scenario` | Preparação, contexto de ator, ação, limite observado, configuração, resultado e efeitos esperados, critérios verificados, aplicabilidade. |
| `SupportingCheck` | Verificação executável ou revisável que apoia um teste comportamental; não é outro teste diretamente vinculado. |
| `EvidenceRecord` | Evidência de execução observada, separada do plano. |

Relações: $p$ tem uma bijeção $f\colon U \to P$ entre casos UCS e casos de programa, e $v$ tem uma bijeção $g\colon U \to B$ entre casos UCS e testes comportamentais. Cada critério de um caso UCS deve ser verificado por pelo menos um cenário ou verificação de apoio do teste comportamental desse caso. Compartilhar uma verificação de apoio entre testes comportamentais é permitido quando o vínculo é explícito. Um critério transversal de integração declarado por M1 é coberto por cenário ou verificação de apoio compartilhado, com vínculos explícitos para todos os testes comportamentais pertinentes; não recebe vínculo direto próprio com caso UCS.

O registro do programa declara como o chamador fornece o contexto de ator e onde cada caso o autoriza. Uma chamada entre casos transmite o contexto pertinente; cada caso chamado aplica sua política. A autenticação é exigida conforme o contrato do caso selecionado. Contexto ausente é distinto de papel anônimo expressamente admitido.

## 3. Campos

O template legível por máquina é [`template.json`](template.json).

| Objeto | Campo | Tipo | Observações |
| --- | --- | --- | --- |
| Raiz | `model`, `model_version`, `layer`, `oal_edition`, `project`, `source_l1` | O | `source_l1` nomeia a instância M1 e sua versão. |
| Raiz | `adpm`, `advs` | O | Os dois componentes são obrigatórios e não vazios. |
| ProgramCase | `id`, `ucs_case_id`, `collaborators`, `sequence`, `results`, `effects`, `errors`, `permission` | O | `sequence` registra decisões e ordem. |
| ProgramCase | `domains`, `lifetime` | P | Obrigatórios quando o modelo usa domínios ou escolhe tempo de vida. |
| ProgramEntity | `id`, `ucs_entity_id`, `validity_location` | O | A localização é canônica para a entidade. |
| ToolContract | `id`, `operation`, `inputs`, `outputs`, `guarantees`, `failures`, `ready_entity_assumption`, `contextual_conditions` | O | `contextual_conditions` são verificações $Q_t(e,c)$ distintas da coerência da entidade. |
| ToolContract.contextual_condition | `condition`, `object`, `purpose`, `responsibility` | O | Os quatro campos tornam a condição identificável. |
| BehavioralTest | `id`, `ucs_case_id`, `criteria`, `boundary`, `scenarios`, `supporting_checks`, `status` | O | Exatamente um BT por caso UCS. |
| Scenario | `id`, `preparation`, `actor`, `action`, `observed_boundary`, `configuration`, `expected_result`, `expected_effects`, `criteria_verified`, `applicability` | O | `applicability` é `applicable` ou `not_applicable` com justificativa. |
| Verificação de apoio compartilhada | `id`, `criteria_verified`, `case_ids`, `obligation_ids`, `behavioral_test_ids`, `reference`, `scenario` | C | Obrigatório quando cobre critério transversal; vínculos resolvem para seus casos e respectivos BTs. |
| Evidência | `planned_checks`, `execution` | O | `execution.status` é `not_recorded`, `recorded` ou `not_applicable`. |
| Adições de canal | `l4_obligations` | P | Quando presentes, a ADVS deve referenciar os cenários de canal relacionados. |

## 4. Condições de validade

- **V-M2-01 — Identidade.** Identidade `OAL-EX-M2-PROGRAM-SCENARIOS`, versão `0.1.0`, camada `L2` e edição OAL declarada presentes.
- **V-M2-02 — Dois componentes.** `adpm` e `advs` presentes, não vazios e estruturalmente completos.
- **V-M2-03 — Bijeção de programa.** Todo caso UCS no escopo declarado tem exatamente um `ProgramCase` com `ucs_case_id` correspondente; não há casos de programa extras.
- **V-M2-04 — Bijeção de testes.** Todo caso UCS tem exatamente um `BehavioralTest` com `ucs_case_id` correspondente; identidades de teste são únicas; não há outros testes diretamente vinculados.
- **V-M2-05 — Referência de cobertura de critérios.** Todo critério próprio de um caso UCS aparece em `criteria_verified` de pelo menos um cenário ou verificação de apoio do teste comportamental desse caso. Um critério referenciado por cenário resolve para o caso vinculado ou para um critério transversal de integração declarado separadamente no artefato L1 selecionado. Neste último caso, o cenário identifica casos, obrigações e todos os testes comportamentais pertinentes; o critério transversal e seu contrato completo de verificação permanecem recuperáveis. Nenhum teste comportamental diretamente vinculado adicional é criado.
- **V-M2-06 — Verificações de apoio.** Toda referência de verificação de apoio resolve para arquivo e, quando há símbolo, para esse símbolo. Compartilhar verificações é permitido com vínculos explícitos.
- **V-M2-07 — Aplicabilidade.** Um cenário marcado `not_applicable` declara justificativa. Para o cenário de permissão de um caso $u$, sejam $A$ os atores conhecidos e $A_u$ os permitidos; o cenário é exigido quando $F_u = A \setminus A_u$ não é vazio, e só pode ser `not_applicable` com justificativa quando $F_u$ é vazio. Contextos de ator ausente e desconhecido continuam situações distintas e não são cobertas por essa isenção.
- **V-M2-08 — Ferramentas e coerência.** Todo contrato de ferramenta declara que uma entidade pronta satisfaz as condições de coerência interna da entidade, e suas condições contextuais são distintas dessas condições. Não pode conter cópia redundante de verificação interna da entidade.
- **V-M2-09 — Plano, código, execução.** Cenários planejados e referências de verificação de apoio são distintos de registros de execução. Referência a arquivo de teste não conta como resultado executado; `execution.status` é verdadeiro.
- **V-M2-10 — Adições de canal.** Se `l4_obligations` existe, os cenários de canal relacionados são referenciados e seu estado é registrado.

## 5. Mapeamento para as regras L2 do OAL (Alpha-v0.2.0-Alkimim)

| Regra OAL | Construção ou condição do modelo |
| --- | --- |
| ADPM 1. Responsabilidades | `ProgramCase`, `ProgramEntity`, `ToolContract`, `Dependency`, `Composition`. |
| ADPM 2. Casos de uso | `ProgramCase.sequence`, decisões, resultados, efeitos, erros; V-M2-03. |
| ADPM 3. Entidades | `ProgramEntity`; V-M2-08; a validade da entidade permanece canônica. |
| ADPM 4. Ferramentas e validação | `ToolContract.ready_entity_assumption`, `contextual_conditions` com objeto, finalidade e responsabilidade; V-M2-08. |
| ADPM 5. Dependências/composição | `Dependency`, `Composition`. |
| ADPM 6. Persistência | Garantias e falhas do contrato de ferramenta. |
| ADPM 7. Autorização | `ProgramCase.permission` e `Authorization`. |
| ADPM 8. Representação fiel | Os registros lógicos e este mapeamento. |
| ADPM 9. Domínios | Campo opcional `domains`. |
| ADPM 10. Tempo de vida | Campo opcional `lifetime`. |
| ADVS 1. Derivação e BT | `BehavioralTest`, V-M2-04. |
| ADVS 2. Contratos de teste/subteste | Campos de `Scenario`. |
| ADVS 3. Permissões | Cenários de permissão; V-M2-07. |
| ADVS 4. Falhas e limites | Falhas dos cenários e cenários de canal. |
| ADVS 5. Rastreabilidade e estado | `criteria_verified`, `supporting_checks`, `EvidenceRecord`; V-M2-05, V-M2-09. |

## 6. Template, exemplo e contraexemplo

- [`template.json`](template.json) é o template lógico.
- [`example.json`](example.json) é um **recorte parcial** do Tiny Catalog para dois casos. Está rotulado como parcial e não substitui o artefato L2 completo do projeto.
- [`counterexample.json`](counterexample.json) omite a ADVS de um caso, duplica uma identidade de teste comportamental, marca como `not_applicable` um cenário de permissão exigido, dá a um contrato de ferramenta uma verificação redundante da entidade e referencia um critério transversal não declarado. As violações esperadas estão listadas no arquivo.

## 7. Evidência e limites

O modelo foi revisado contra as regras ADPM e ADVS acima. A revisão está documentada aqui; não é certificada por máquina. O modelo é deliberadamente parcial: não define linguagem, notação de máquina de estados, executor de testes nem algoritmo para derivar cenários. Também não prova que os cenários são comportamentalmente suficientes; isso permanece uma obrigação de revisão.

As bijeções e referências de critérios são estruturais. Uma verificação estrutural pode conferir que identificadores resolvem e que todo critério aparece no apoio declarado; não pode conferir que um cenário realmente exercita a condição.

## 8. Instanciar e verificar

1. Parta da instância L1 do projeto e liste todos os casos UCS, conjuntos de atores e critérios.
2. Para cada caso, produza um `ProgramCase` e um `BehavioralTest`; não acrescente testes diretamente vinculados para funções ou subtestes.
3. Registre contratos de ferramenta com premissas de entidade pronta e condições contextuais.
4. Registre cenários com aplicabilidade; calcule $F_u = A \setminus A_u$ e só marque o cenário de permissão como `not_applicable` quando $F_u$ for vazio.
5. Registre verificações planejadas e execução separadamente.
6. Acrescente a entrada L2 a `model-instances.json` e execute os comandos de teste selecionados.
