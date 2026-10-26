# Avaliação de compatibilidade estável

[English](COMPATIBILITY.md) · [Regras de referência](README.pt-br.md#reference-rules)

Origem: Alpha-v0.2.0-Alkimim no commit 5755a4e4a5b31a9614da5d409d03d1db9cf1e20c. Este registro apresenta revisão local de compatibilidade, sem revisão externa ou nova aprovação humana.

## Comparação normativa

A região completa das regras foi comparada nos dois idiomas, da âncora oal-layers até o fim da ADIB, antes de Interpretação. Os 46 itens numerados mantêm texto idêntico: OAL 9, UCS 10, ADPM 10, ADVS 5, ADI 5 e ADIB 7. A introdução explicativa da ADMV não mudou. Recomendações opcionais continuam opcionais.

| Região alterada | Motivo e efeito na compatibilidade |
| --- | --- |
| Notas e título da edição | Identificam a nova edição e sua origem Alpha; nenhuma nova obrigação numerada. |
| Guia de versionamento | Define releases imutáveis por commit/tag e evolução maior/menor/corretiva; correções ambíguas exigem análise de compatibilidade. |
| Navegação e empacotamento | Apontam à cópia estável e às novas evidências; acrescentam verificações reproduzíveis e mapas informativos para agentes. |
| Texto normativo | Nenhuma diferença em qualquer idioma. |

FAQ, skill, guias e mapas de agentes não acrescentam obrigações de conformidade.

## Avaliação dos quatro modelos

Os quatro contratos mantêm 0.1.0. Campos, construções, relações, condições de validade, tabelas de mapeamento e templates foram comparados com as definições Alpha. Só mudam metadados de edição/proveniência e a nota de avaliação. O contrato OAL numerado é idêntico; o mapeamento anterior continua aplicável no mesmo escopo didático.

| Modelo | Evidência e conclusão |
| --- | --- |
| OAL-EX-M1-CASE-CONTRACTS | Campos de casos/entidades/obrigações e condições V-M1 iguais. O vocabulário de origem continua external, domain, assumption, l4-decision. Corrige-se o valor inválido da instância Work Board. |
| OAL-EX-M2-PROGRAM-SCENARIOS | Contrato ADPM/ADVS e condições V-M2 iguais; ambos os componentes, casos, critérios e testes diretamente vinculados permanecem explícitos. |
| OAL-EX-M3-PYTHON-CORE | Organização reutilizável de código e condições V-M3 iguais; casos, entidades, ferramentas e composição mantêm os mapeamentos. |
| OAL-EX-M4-HTTP-BOUNDARY | Contrato de fronteira e condições V-M4 iguais; mapeamentos muitos para muitos e obrigações de canal permanecem explícitos. |

Os modelos surgiram na Alpha-v0.2.0-Alkimim. A avaliação original é histórica; esta avaliação de compatibilidade e as novas verificações estruturais e de aplicação constituem evidências separadas. São modelos de exemplo externos à definição do OAL.

## Revisão dos artefatos

Work Board 0.2.1 altera O-WB-AVAIL.origin de baseline-decision para domain, pois especifica resultados operacionais dos casos. origin_reference é preservado literalmente, inclusive a decisão de baseline e a ausência de evidência independente de stakeholders. Necessidades reconstruídas continuam 0.2.0. O registro Needs-to-L1 identifica o destino corrigido; referências seguintes usam 0.2.1.

Os derivados Work Board recebem revisão de compatibilidade, mantendo comportamento, identidades, critérios, implementação e testes. O rótulo 0.2.1 identifica o conjunto revisado, sem alegar nova geração. A responsabilidade histórica continua atribuída ao trabalho original; esta correção não afirma execução de transformador ou aprovação humana.

Tiny Catalog e Board CRM mantêm baseline 0.2.0, com metadados de edição e evidências atuais. O identificador de schema do Board CRM nomeia o formato histórico e permanece igual; o parágrafo de evolução registra a adaptação histórica. A linha de edição do TeX gerado identifica a edição avaliada atualmente. Pacotes Python demonstrativos mantêm 0.2.0a0; estabilidade do OAL não promete estabilidade comercial dessas aplicações.

## Evidências e limites

O [registro de execução](examples/verification/execution.json) traz comandos, horários, ambiente, logs, smoke dos lançadores e hashes das entradas fixadas. As [verificações estruturais](examples/verification/structural-checks.json) conferem referências explícitas. Logs originais permanecem em examples/verification/historical-alpha-v0.2.0/, com datas e resultados intactos.

O verificador estrutural não interpreta prosa ou código. Identificadores coerentes e testes finitos aprovados não provam suficiência dos cenários, adequação a stakeholders reais, semântica universal, comportamento JavaScript, acessibilidade ou construção/execução de transformadores. Não se introduz motor, aplicação, autenticação ou infraestrutura.
