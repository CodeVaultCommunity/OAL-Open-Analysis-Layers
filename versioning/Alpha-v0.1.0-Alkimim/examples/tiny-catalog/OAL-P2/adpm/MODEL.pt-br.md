# Tiny Catalog — modelo de programa ADPM

[English](MODEL.md) · [Início](../../../../../../README.pt-br.md)

**Origem:** [UCS do projeto](../../OAL-P1/UCS.pt-br.md), versão 0.1.0.
**Registro de derivação:** [derivations.json](../../derivations.json).

## Casos e autorização

O modelo preserva as identidades UC-CAT-001, UC-CAT-002, UC-CAT-003, UC-CAT-004. Um ator autenticado entra como dado explícito em cada caso. Cada caso verifica sua permissão antes de validação, leitura ou escrita. Atores ausentes ou desconhecidos são recusados. A matriz de permissões está na [UCS](../../OAL-P1/UCS.pt-br.md); sua realização concreta está na [ADI](../../OAL-P3/IMPLEMENTATION.pt-br.md).

## Entidades, ferramentas e composição

Entidades contêm dados e validação durante atribuição. Casos decidem regras de domínio e chamam contratos de ferramentas. Os [contratos de ferramentas](tool-contracts.pt-br.md) especificam operações e garantias de persistência. A composição seleciona ferramentas concretas e fornece dependências aos casos. O provedor de identidade pertence ao limite de entrada; fornece o ator, mas não decide permissões dos casos.

## Algoritmos

O provedor de identidade autentica a pessoa no limite de entrada. A mesma identidade é enviada explicitamente a cada caso. O caso verifica a permissão antes de validar entradas ou ler o armazenamento. A desativação chama o caso de consulta já especificado com essa identidade.

| Caso UCS | Papéis permitidos | Dependências | Algoritmo do programa |
| --- | --- | --- | --- |
| UC-CAT-001 Cadastrar | mantenedor | Fábrica de Item, ItemStore | Construir item ativo válido; inserir com código único de modo atômico; traduzir conflito de armazenamento para item duplicado. |
| UC-CAT-002 Consultar | mantenedor, leitor | Fábrica de chave, ItemStore | Validar código; ler o registro preservado mesmo se inativo; distinguir ausência do registro de indisponibilidade do armazenamento. |
| UC-CAT-003 Listar | mantenedor, leitor | ItemStore | Ler registros independentes; manter os ativos; ordenar pelo código ASCII exato; retornar lista vazia quando não houver resultados. |
| UC-CAT-004 Desativar | mantenedor | Consulta UC-CAT-002, ItemStore | Obter item pela consulta; retorná-lo sem mudança se já inativo; caso contrário, marcá-lo inativo e substituir o registro preservado; traduzir desaparecimento concorrente para item ausente. |

`ItemKey` e `Item` validam campos atribuídos; os casos decidem unicidade, disponibilidade e preservação. `ItemStore` oferece inserção atômica, leituras independentes e substituição sem decidir essas regras. `RecordCodec` e `ConnectionProvider` apoiam o adaptador SQLite. O [mapa de implementação](traceability.json) preserva uma identidade de implementação por caso da UCS.
