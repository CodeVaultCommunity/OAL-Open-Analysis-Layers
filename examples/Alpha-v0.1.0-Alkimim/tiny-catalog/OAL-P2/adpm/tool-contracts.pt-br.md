# Contratos das ferramentas — documentação da implementação

[English](tool-contracts.md) · [Início](../../../../../README.pt-br.md)

Estes são contratos voltados ao código, **não seções nem nomes obrigatórios de
ferramentas em uma UCS**.

## ItemStore

`insert(item)` retorna um item retido independente após a confirmação do commit ou
gera `StoreConflict` para um código já alocado. Deve preservar a unicidade de forma
atômica; uma sequência “consultar e depois inserir” sem garantia atômica é
insuficiente. Nunca substitui um registro existente. O caso de uso atribui o
significado de negócio a `StoreConflict`.

`get(code)` retorna um `Item` destacado ou `None`. `list_all()` retorna registros
destacados, sem aplicar a política de disponibilidade nem a ordenação exigidas pelo
caso. Nenhuma das operações altera dados persistidos. `StoreUnavailable` não
significa registro ausente nem coleção vazia bem-sucedida.

`replace(item)` atualiza um código existente e confirma a escrita; `StoreMissing`
indica ausência. Não insere, autoriza, decide transições nem repete operações.

Todas as operações podem gerar `StoreUnavailable`. Uma falha durante uma escrita
não determina se houve commit. O substituto em memória implementa o formato das
operações e o comportamento dos registros durante o teste, **não o perfil de
persistência durável de produção**. Seu escopo limitado está explícito na
configuração de execução comportamental.

## RecordCodec

`encode(item)` produz dados destacados de código, nome e indicador inteiro.
`decode(record)` retorna uma entidade validada. Dados inválidos são rejeitados,
sem coerção silenciosa. O codec concreto consome apenas um construtor de entidade
injetado, não outra ferramenta ou serviço externo.

## ConnectionProvider

`open()` retorna uma conexão nova com o banco. A ferramenta consumidora é responsável
por fechá-la e gerencia a transação. A implementação selecionada recebe por injeção
a fábrica do driver, o caminho e o tempo limite. Não seleciona políticas de negócio.

## Composição de casos de uso

`ItemLookup` é o contrato chamável de UC-CAT-002 consumido por UC-CAT-004. **Não é
uma ferramenta nem um quinto caso de uso.** O valor concreto injetado é a instância
já construída de `GetItem`. Interfaces são declarações, não implementações adicionais.
