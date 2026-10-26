# Contratos das ferramentas — documentação da implementação

[English](tool-contracts.md) · [Início](../../../../../../README.pt-br.md)

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


## Entidades prontas e verificações contextuais

`insert(item)` e `replace(item)` recebem um `Item` pronto. Por contrato, a entidade já satisfaz suas condições de coerência interna $I_E$; o armazenamento não pode chamar novamente a validação da entidade nem implementar uma cópia equivalente das verificações de campos. Para `ItemKey`, $I_{\mathrm{ItemKey}}(k)$ cobre o formato e as regras de normalização do próprio código; não inclui a presença de outros itens retidos. A condição contextual $Q_{\mathrm{insert}}(k, S) \iff \neg\exists x \in S:\, x.\mathrm{code} = k.\mathrm{code}$ depende do conjunto retido $S$; o armazenamento a garante atomicamente. $Q_{\mathrm{insert}}$ não faz parte de $I_{\mathrm{ItemKey}}$ e não autoriza revalidar campos da entidade. O armazenamento também avalia a existência do registro para `replace` e a disponibilidade do armazenamento — condições cujo objeto, finalidade e responsabilidade são distintos da coerência da entidade. `decode(record)` é a fronteira de representação: pode recusar dados brutos malformados, mas, ao construir um `Item`, usa a construção e a validação canônicas da entidade. A validação da entidade não substitui as garantias atômicas do armazenamento, e o armazenamento não substitui a validade da entidade.
