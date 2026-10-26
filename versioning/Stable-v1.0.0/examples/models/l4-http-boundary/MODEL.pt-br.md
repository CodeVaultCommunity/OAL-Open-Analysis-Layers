# OAL-EX-M4-HTTP-BOUNDARY — Fronteira HTTP Local (L4)

[English](MODEL.md) · [Modelos](../README.pt-br.md) · [Regras de referência](../../../../Stable-v1.0.0/README.pt-br.md#reference-rules)

**Identidade:** `OAL-EX-M4-HTTP-BOUNDARY`
**Versão:** 0.1.0
**Camada:** L4 (ADIB)
**Edição OAL declarada:** Stable-v1.0.0
**Estado:** exemplo de modelo reutilizável. Este documento especifica o modelo; não certifica artefato de projeto.

## 1. Objetivo e escopo

O modelo define uma fronteira de interação HTTP local ao redor de um núcleo invocável. Fixa o contrato de canal, endpoints, resolução do contexto de ator, mapeamento de erros, elementos de interface, vínculos muitos para muitos e obrigações de canal que um artefato L4 deve expor. HTTP, JSON e execução local são escolhas deste modelo, não exigências de L4.

O modelo não escolhe framework web, desenho HTML, armazenamento de credenciais nem topologia de implantação. Exige que a fronteira invoque casos, não os absorva.

## 2. Construções e relações

| Construção | Significado |
| --- | --- |
| `Channel` | Canal declarado: tipo, configuração base, páginas, esquema de autenticação, resolução do contexto de ator. |
| `Endpoint` | Estímulo: método, caminho, caso ADI invocado, entradas, identidade, sucesso, falhas, representação. |
| `InterfaceElement` | Controle de página, rota ou elemento estático; pode invocar um ou mais casos ou ser exclusivo da interface. |
| `Obligation` | Requisito de canal com natureza, enunciado, origem (`external`, `ucs` ou `l4-decision`), escopo, condições verificáveis e referências de verificação. |
| `ChannelCheck` | Verificação planejada ou executada da fronteira. |
| `ExposureScope` | Conjunto de casos ADI expostos por este canal. |

Relações: $H$ é o conjunto de elementos de interface e $U_3$ o de casos ADI; a relação de invocação $R \subseteq H \times U_3$ é muitos para muitos e é registrada nos dois sentidos. Elementos sem vínculo de caso são classificados como exclusivos da interface. Todo endpoint invoca um caso ADI declarado e passa o contexto de ator resolvido explicitamente. O canal autentica quando o contrato do caso exige. Um papel anônimo expressamente admitido é resolvido como tal; contexto ausente ou autenticação falha não se converte em acesso anônimo.

## 3. Campos

O template legível por máquina é [`template.json`](template.json).

| Objeto | Campo | Tipo | Observações |
| --- | --- | --- | --- |
| Raiz | `model`, `model_version`, `layer`, `oal_edition`, `project`, `source_l3` | O | `source_l3` nomeia a instância M3 e sua versão. |
| Channel | `kind`, `configuration`, `pages`, `authentication`, `identity_resolution` | O | Configurações da demonstração local são declaradas; `identity_resolution` descreve como o contexto de ator é estabelecido. |
| Endpoint | `id`, `method`, `path`, `case_id`, `inputs`, `identity`, `success`, `failures`, `representation` | O | `case_id` deve ser um caso ADI exposto. |
| InterfaceElement | `id`, `description`, `invokes`, `interface_only` | O | `invokes` lista casos ADI; elementos exclusivos têm lista vazia e finalidade. |
| Obligation | `id`, `nature`, `statement`, `origin`, `origin_reference`, `scope`, `verifiable_conditions`, `check_refs` | O | `origin` distingue restrição externa/ucs de decisão de L4. |
| ChannelCheck | `id`, `obligation_ids`, `case_ids`, `criteria`, `scenario`, `boundary`, `status` | O | Estados planejado e executado são separados. |
| Armazenamento técnico | `technical_storage` | C | Se usado, declara estado exclusivo do canal, escopo, acesso, falhas e tempo de vida. Lista vazia significa ausência desse armazenamento. |
| Exposição | `exposure_scope`, `interface_only`, `persistence_access` | O | `persistence_access` declara que a persistência do domínio é acessada pelos casos; armazenamento estritamente técnico do canal tem contrato separado declarado. |

## 4. Condições de validade

- **V-M4-01 — Identidade.** Identidade `OAL-EX-M4-HTTP-BOUNDARY`, versão `0.1.0`, camada `L4` e edição OAL declarada presentes.
- **V-M4-02 — Canal declarado.** Tipo, configuração, exigências de autenticação e mecanismo de resolução do contexto de ator são declarados. Credenciais de demonstração são identificadas como tais.
- **V-M4-03 — Mapeamento de endpoint.** Todo endpoint invoca exatamente um caso ADI declarado e passa o contexto de ator resolvido explicitamente. Entradas, exigências de autenticação, sucesso, falhas e representação estão declarados.
- **V-M4-04 — Limite de autorização.** A fronteira resolve o contexto de ator e autentica quando o contrato do caso exige; não substitui a autorização do caso. Endpoints, páginas ou scripts não implementam decisões de permissão de domínio.
- **V-M4-05 — Persistência do domínio e estado técnico.** A fronteira acessa registros do domínio e suas ferramentas de persistência pelos casos. Estado estritamente técnico do canal, como uma sessão, pode usar armazenamento com contrato separado de escopo, acesso, falhas e tempo de vida. Esse armazenamento não pode conter decisões de domínio nem contornar a autorização dos casos. Os canais atuais de demonstração não usam armazenamento persistente de sessão.
- **V-M4-06 — Vínculos muitos para muitos.** $R \subseteq H \times U_3$ é registrada nos dois sentidos; todo elemento de interface está vinculado a casos ADI declarados ou classificado como exclusivo com finalidade. O escopo de exposição é explícito.
- **V-M4-07 — Origem das obrigações.** Cada obrigação declara sua origem. Restrições externas citam a fonte; requisitos herdados da UCS são marcados `ucs`; decisões introduzidas pela fronteira são marcadas `l4-decision` e não são apresentadas como requisitos externos.
- **V-M4-08 — Verificações de canal.** Cada obrigação declarada está vinculada a pelo menos uma verificação planejada. Verificações planejadas e resultados executados são separados; `execution.status` é verdadeiro.
- **V-M4-09 — Sem novas regras de domínio.** A fronteira não introduz nova transação, decisão ou objetivo de domínio em endpoint, página ou script. Se a interação revelar nova necessidade de domínio, a UCS e as derivações afetadas são revisadas.
- **V-M4-10 — Exposição parcial.** Se apenas parte dos casos ADI for exposta, `exposure_scope` nomeia o conjunto exposto.

## 5. Mapeamento para as regras L4 do OAL (Stable-v1.0.0)

| Regra ADIB do OAL | Construção ou condição do modelo |
| --- | --- |
| 1. Escopo de interação | `Channel`, `ExposureScope`. |
| 2. Estímulos e respostas | Campos de `Endpoint`. |
| 3. Contexto de ator na fronteira | `Channel.identity_resolution`, `Endpoint.identity`; V-M4-04. |
| 4. Mapeamento muitos para muitos | `InterfaceElement`, $R$, V-M4-06. |
| 5. Limite das decisões | V-M4-05, V-M4-09. |
| 6. Contrato do canal | `Obligation` com origem, escopo e condições; V-M4-07. |
| 7. Verificação da interação | `ChannelCheck`, V-M4-08. |

## 6. Template, exemplo e contraexemplo

- [`template.json`](template.json) é o template lógico.
- [`example.json`](example.json) é um **recorte parcial** do Tiny Catalog: dois endpoints, dois elementos de interface e as obrigações de canal. A instância completa é o contrato HTTP e o mapa de rastreabilidade do projeto.
- [`counterexample.json`](counterexample.json) deixa um endpoint ler SQLite diretamente, delega autorização à rota, introduz uma regra de negócio em JavaScript e deixa um vínculo inverso ausente. As violações esperadas estão listadas no arquivo.

## 7. Evidência e limites

O modelo foi revisado contra as regras ADIB acima. É deliberadamente parcial: não prescreve desenho de UI, produto de credenciais, mecanismo de sessão nem auditoria de acessibilidade. Também não prova que a interface funciona no navegador; as verificações declaradas e seu estado de execução delimitam a evidência.

Uma verificação estrutural pode conferir vínculos estruturais, mapeamento endpoint-caso, classificação de elementos exclusivos e o estado de evidência declarado. Ele não executa JavaScript nem prova comportamento visual.

## 8. Instanciar e verificar

1. Parta da instância M3 selecionada e liste seus casos ADI.
2. Declare o canal e os casos expostos.
3. Mapeie cada endpoint para um caso e declare identidade, entradas, sucesso, falhas e representação.
4. Registre elementos de interface e os vínculos muitos para muitos nos dois sentidos; classifique os exclusivos.
5. Registre obrigações com origem e vincule-as a verificações de canal.
6. Acrescente a entrada L4 a `model-instances.json` e execute os comandos de teste selecionados e os testes de canal selecionados.

## Avaliação de compatibilidade estável

Origem: Alpha-v0.2.0-Alkimim, modelo 0.1.0. Para Stable-v1.0.0, as regras numeradas do OAL e os campos e condições de validade deste modelo foram comparados com essa baseline; permanecem iguais. O mapeamento acima continua aplicável ao mesmo escopo didático. Esta revisão de compatibilidade não é certificação externa nem execução de transformador. O [relatório de avaliação](../../../COMPATIBILITY.pt-br.md) registra escopo e limites; execuções dos projetos são registradas separadamente.
