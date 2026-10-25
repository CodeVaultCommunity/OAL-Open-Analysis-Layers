# Modelos de exemplo do OAL — Alpha-v0.2.0-Alkimim

[English](README.md) · [Exemplos](../README.pt-br.md) · [Regras de referência](../../../Alpha-v0.2.0-Alkimim/README.pt-br.md)

Este diretório contém quatro modelos reutilizáveis pequenos, um por camada do OAL. Eles são exemplos de modelos que declaram conformidade às regras numeradas de Alpha-v0.2.0-Alkimim. São deliberadamente estreitos: tomam decisões concretas suficientes para admitir ou rejeitar artefatos de projeto, com escopo didático declarado.

| Camada | Modelo | Identidade | Versão | Diretório |
| --- | --- | --- | --- | --- |
| L1 | Simple Case Contracts | `OAL-EX-M1-CASE-CONTRACTS` | 0.1.0 | [`l1-case-contracts/`](l1-case-contracts/MODEL.pt-br.md) |
| L2 | Program and Scenario Records | `OAL-EX-M2-PROGRAM-SCENARIOS` | 0.1.0 | [`l2-program-scenarios/`](l2-program-scenarios/MODEL.pt-br.md) |
| L3 | Injected Python Core | `OAL-EX-M3-PYTHON-CORE` | 0.1.0 | [`l3-python-core/`](l3-python-core/MODEL.pt-br.md) |
| L4 | Local HTTP Boundary | `OAL-EX-M4-HTTP-BOUNDARY` | 0.1.0 | [`l4-http-boundary/`](l4-http-boundary/MODEL.pt-br.md) |

A versão do modelo é independente da edição do OAL. Um modelo declara a edição contra a qual foi avaliado; uma edição posterior do OAL ou uma nova versão do modelo exige nova avaliação. Esta correção na edição existente mantém os identificadores de versão da edição e dos modelos. As notas da revisão descrevem as correções, e o [inventário de conteúdo](../../../../CONTENT-SHA256.json) identifica os bytes entregues; a versão mantida, sozinha, não identifica o conteúdo revisado. Os resultados observados dos testes de aplicação permanecem no [registro estruturado de execução](../verification/execution.json).

## O que estes modelos são e não são

- São **reutilizáveis**: Tiny Catalog, Board CRM e Work Board instanciam os mesmos quatro modelos.
- São **esquemas lógicos mais condições de validade**, não formatos de serialização. Cada modelo admite as representações que suas instâncias declaram e nomeia o conteúdo canônico.
- **Não** são novas aplicações e não substituem os projetos. As instâncias executáveis completas permanecem nos três diretórios de projeto.
- **Não** demonstram um transformador. Os projetos foram adaptados manualmente; `engine_status` permanece `not_demonstrated`.

## Formato do manifesto de instâncias

Cada projeto contém um manifesto `model-instances.json` com exatamente quatro entradas, uma por camada. O formato comum é:

```json
{
  "manifest_version": "1.0.0",
  "project": "Nome do projeto",
  "oal_edition": "Alpha-v0.2.0-Alkimim",
  "artifact_version": "0.2.0",
  "instances": [
    {
      "id": "projeto-m1",
      "layer": "L1",
      "model": {
        "identity": "OAL-EX-M1-CASE-CONTRACTS",
        "version": "0.1.0",
        "definition": "../models/l1-case-contracts/MODEL.md"
      },
      "artifact": {
        "scope": "escopo declarado desta instância",
        "canonical_content": ["OAL-P1/index.json"],
        "files": ["OAL-P1/index.json", "OAL-P1/UCS.md"],
        "symbols": []
      },
      "mapping": {
        "cases": {"UC-...": "identidade de caso declarada nesta camada"},
        "criteria": {"AC-...": "referência de critério declarada"}
      },
      "evidence": {
        "assessment": "reviewed",
        "planned_checks": ["o que está planejado"],
        "execution": {"status": "not_recorded", "reference": null}
      },
      "limits": "o que esta instância não declara"
    }
  ]
}
```

Regras dos campos:

- `instances` tem exatamente quatro entradas com as camadas `L1`, `L2`, `L3` e `L4`, nessa ordem.
- `model.identity`, `model.version` e `model.definition` devem corresponder à definição do diretório do modelo.
- `artifact.files` e `artifact.symbols` devem existir. Símbolos usam `caminho::nome.qualificado`.
- Para L2, `artifact.files` deve incluir os dois componentes ADPM e ADVS. `artifact.canonical_content` pode ser um objeto com arrays `adpm` e `advs` nomeando as fontes autoritativas de cada componente; `files` continua sendo a lista de arquivos integrantes, não a declaração de autoridade.
- Para L3, `artifact.canonical_content` lista os módulos do núcleo (não apenas um contêiner físico). `artifact.boundary_files` pode nomear o inicializador da aplicação e os caminhos da fronteira de interação que ficam fora do escopo do núcleo.
- Para L1, `canonical_content` pode identificar uma fonte completa ou atribuir uma fonte canônica a cada grupo de campos. Se uma representação for uma projeção parcial, a regra de consistência declara quais omissões são permitidas e exige que o conteúdo reproduzido concorde com sua fonte canônica. Critérios transversais de integração têm definição canônica completa, casos e obrigações associados e vínculos explícitos com as verificações de apoio.
- `mapping.cases` deve preservar as identidades de caso do projeto; identificadores de categorias diferentes não precisam ser a mesma string.
- `evidence.execution.status` é `not_recorded`, `recorded` ou `not_applicable`. Uma execução `recorded` nomeia o comando ou a referência; uma verificação planejada nunca é apresentada como executada.
- `limits` nomeia o que a instância não cobre. Um valor vazio ou genérico é recusado por um validador ou revisão.

## Como instanciar um modelo

1. Selecione um modelo por camada e registre sua identidade, versão e definição.
2. Produza os campos exigidos pelo modelo. Adapte arquivos existentes em vez de criar um projeto paralelo.
3. Declare o conteúdo canônico e o mapeamento entre representações.
4. Confira as condições de validade do modelo (`V-M1-…`, `V-M2-…`, `V-M3-…`, `V-M4-…`).
5. Registre a avaliação: o que foi revisado, o que foi executado e o que permanece não verificado.
6. Acrescente a instância a `model-instances.json`, revise-a contra as condições de validade do modelo e execute a suíte de testes do projeto.

Uma revisão estrutural pode conferir identidades, referências, arquivos, símbolos, correspondências de casos, presença dos componentes, mapeamentos e estados de evidência. Ela não substitui a avaliação semântica do modelo nem do artefato.

## Avaliação dos modelos

Cada `MODEL.md` contém seu mapeamento para as regras aplicáveis do OAL e uma seção de evidência e limites. Os modelos foram avaliados contra Alpha-v0.2.0-Alkimim lendo cada regra numerada e identificando a construção ou restrição que a atende. Essa avaliação está documentada no arquivo do modelo; é uma revisão, não um resultado de conformidade certificado por máquina.

As três instâncias de projeto foram revisadas contra os modelos selecionados. Os manifestos registram escopo, evidência e limites. Uma verificação estrutural não é uma aprovação semântica e não transforma uma verificação planejada em evidência executada.
