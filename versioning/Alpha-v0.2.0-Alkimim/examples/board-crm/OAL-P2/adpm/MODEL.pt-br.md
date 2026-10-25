# Board CRM — modelo de programa ADPM

[English](MODEL.md) · [Início](../../../../../../README.pt-br.md)

**Origem:** [UCS do projeto](../../OAL-P1/ucs.json), versão 0.2.0.
**Classificação:** artefato de projeto do componente de modelo do programa (ADPM) da L2 sob o OAL Alpha-v0.2.0-Alkimim; instanciando OAL-EX-M2-PROGRAM-SCENARIOS 0.1.0; consulte `model-instances.json` para a declaração da instância.
**Registro de derivação:** [derivations.json](../../derivations.json).

## Casos e autorização

O modelo preserva as identidades UC-CRM-001, UC-CRM-002, UC-CRM-003, UC-CRM-004, UC-CRM-005, UC-CRM-006. Cada caso recebe explicitamente um contexto de ator resolvido. O ator especificado é um papel; aqui, o contexto é representado por um identificador de papel estabelecido por um ponto de entrada confiável. Este exemplo exige autenticação em todos os casos. Cada caso verifica sua permissão antes de validação, leitura ou escrita. Atores ausentes ou desconhecidos são recusados. A matriz de permissões está na [UCS](../../OAL-P1/ucs.json); sua realização concreta está na [ADI](../../OAL-P3/IMPLEMENTATION.pt-br.md).

## Entidades, ferramentas e composição

Entidades contêm dados e validação durante atribuição. Casos decidem regras de domínio e chamam contratos de ferramentas. Os [contratos de ferramentas](tool-contracts.pt-br.md) especificam operações e garantias de persistência. A composição seleciona ferramentas concretas e fornece dependências aos casos. O provedor de identidade pertence ao limite de entrada; fornece o ator, mas não decide permissões dos casos.

## Algoritmos

A identidade autenticada é diferente do autor registrado no histórico. O limite de entrada autentica a identidade; o caso consulta a matriz de permissões. O autor do evento continua como entrada explícita do caso. A autorização ocorre antes mesmo da leitura do armazenamento.

| Caso UCS | Papéis permitidos | Dependências | Algoritmo do programa |
| --- | --- | --- | --- |
| UC-CRM-001 Criar | operador, gestor | Store, IdentifierProvider, Clock | Validar título (80), empresa (80) e responsável (40); obter ID e horário; criar oportunidade NEW na versão 1; persistir oportunidade e evento de criação atomicamente. |
| UC-CRM-002 Mover | operador, gestor | Store, Clock | Carregar cartão e comparar versão; aceitar somente movimento adjacente entre NEW, QUALIFIED e PROPOSAL; atualizar etapa, versão, horário e evento atomicamente. |
| UC-CRM-003 Anotar | operador, gestor | Store, IdentifierProvider, Clock | Validar nota (500); carregar e comparar versão; criar ID da nota; anexá-la e incrementar versão atomicamente. |
| UC-CRM-004 Consultar | leitor, operador, gestor | Store | Ler cartões, notas e eventos independentes; ordenar por atualização decrescente e depois ID; filtrar pelo responsável exato quando informado; retornar as cinco colunas. |
| UC-CRM-005 Ganhar | gestor | Store, IdentifierProvider, Clock | Validar motivo (200); carregar e comparar versão; exigir PROPOSAL; definir WON, registrar motivo, incrementar versão e acrescentar evento atomicamente. |
| UC-CRM-006 Perder | gestor | Store, IdentifierProvider, Clock | Validar motivo (200); carregar e comparar versão; exigir etapa ativa; definir LOST, registrar motivo, incrementar versão e acrescentar evento atomicamente. |

Construtores de entidades verificam validade local dos campos. Não decidem transições de etapa nem permissões. `Store` oferece criação e alteração atômicas, leituras independentes e resultados de ausência, conflito e indisponibilidade. O caso traduz esses resultados para a UCS. O [mapa de implementação](traceability.json) preserva uma identidade de implementação por caso da UCS.
