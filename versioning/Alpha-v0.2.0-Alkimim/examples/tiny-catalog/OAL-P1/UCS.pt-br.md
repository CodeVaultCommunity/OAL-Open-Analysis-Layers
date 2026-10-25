# Tiny Catalog — UCS

[English](UCS.md) · [Início](../../../../../README.pt-br.md)

[Executar o exemplo](../README.pt-br.md) · [Classificação UCS](../../../../Alpha-v0.2.0-Alkimim/README.pt-br.md)

**Versão da especificação do projeto:** 0.2.0. **Classificação:** artefato UCS da edição Alpha-v0.2.0-Alkimim, adaptado da baseline 0.1.0.
**Estado:** baseline de exemplo didático, não um sistema de produção contratado.
**Idioma de referência:** inglês para este exemplo; este arquivo é sua tradução.

Este é **um documento pertencente à classificação UCS**, não um modelo obrigatório.
Escolhas tecnológicas e contratos do código ficam fora deste documento.

**Conteúdo canônico:** o [índice](index.json) é autoritativo para identificadores, conjuntos, relações, a política comum de ator e os critérios transversais de integração completos. A narrativa em inglês é autoritativa para contratos detalhados de casos, entidades, regras e obrigações; resumos estruturados não substituem detalhes omitidos. Enunciados reproduzidos e referências devem concordar. Esta narrativa em português é uma tradução. A autoridade por grupo de campos e a regra de consistência estão registradas em `index.json`.

## 1. Objetivo, escopo e suposições

Tiny Catalog permite ao mantenedor cadastrar e desativar itens, e ao mantenedor
ou leitor consultar e listar itens sem excluir seu registro retido.
O escopo completo consiste nos quatro casos de uso abaixo. Passos internos não
constituem casos de uso adicionais.

**N-01:** reter um item de catálogo sob um código inequívoco.
**N-02:** consultar itens conhecidos e identificar os atualmente disponíveis.
**N-03:** retirar um item da disponibilidade sem perder seu registro atual.

**Atores:** ACT-CAT-M é o mantenedor e pode executar os quatro casos. ACT-CAT-R é o leitor e pode executar somente UC-CAT-002 e UC-CAT-003. Ator ausente, desconhecido ou sem permissão é recusado antes de leitura ou escrita. O modo como um canal autentica o chamador e o resolve em um desses papéis é uma decisão da fronteira de interação (L4), registrada no [contrato ADIB](../OAL-P4/HTTP.pt-br.md); esta especificação exige apenas que toda solicitação porte uma identidade de ator autenticado do conjunto permitido.

Os nomes dos atores acima denotam papéis. Um chamador desempenha um papel por meio de contexto resolvido explicitamente. Este projeto exige autenticação nos quatro casos e não admite papel anônimo. Uma invocação confiável fornece o contexto resolvido; cada caso avalia sua própria permissão de papel, inclusive quando outro caso o invoca.

**A-01 — verificada:** a solicitação possui ator autenticado no conjunto permitido para o caso. Uma solicitação negada não produz efeito de domínio ou persistência.
**A-02:** o ambiente fornece persistência funcional e recursos suficientes;
a indisponibilidade continua sendo uma falha explicitamente possível.

Há um único catálogo. Excluem-se exclusão, reativação, alteração de nome, preços,
estoque, usuários, pagamentos, histórico de eventos, paginação e múltiplas empresas.
Registro retido significa seus dados atuais, **não um histórico de auditoria/eventos**.

## 2. Organização opcional por domínio

**D-CAT — Catálogo.** Responsável por identidade, disponibilidade e retenção dos itens.
Todos os quatro casos de uso e as duas entidades estão associados a esse domínio.
É um agrupamento semântico, sem prescrever diretórios ou API entre domínios.

## 3. Entidades e condições de validade

**E-01 — Chave do item.** Identifica um registro por `code`: texto de 1 a 24 caracteres
exclusivamente de `A–Z`, `0–9`, `_` e `-`. Códigos são exatos e sensíveis a maiúsculas:
não se promete normalização; entrada em minúsculas é inválida.

**E-02 — Item.** Contém um código E-01, `name` e o indicador `active`. O nome tem
1 a 80 caracteres Unicode e pelo menos um caractere que não seja espaço em branco.
Espaços são preservados. O indicador de atividade é booleano, não um substituto
numérico ou textual. Cada item tem um código E-01; a unicidade entre itens retidos é a regra funcional R-01, não uma condição de campo da entidade.

A validade dos campos é verificada durante a atribuição. Uma atribuição inválida
preserva o valor anterior do campo. Essa validação não consulta a persistência,
não autoriza uma operação e não decide uma transição de disponibilidade.

## 4. Regras compartilhadas

**R-01 — Unicidade do código retido.** O cadastro não pode reutilizar um código já
atribuído a um item retido, inclusive inativo. Aplicada por UC-CAT-001.

**R-02 — Disponibilidade inicial.** Um cadastro bem-sucedido cria um item ativo.
O solicitante não escolhe sua disponibilidade inicial. Aplicada por UC-CAT-001.

**R-03 — Retenção.** Desativar altera a disponibilidade, não identidade ou nome,
e não exclui o registro. A consulta pode retornar registros ativos ou inativos.
Aplicada por UC-CAT-002 e UC-CAT-004.

**R-04 — Listagem disponível.** Retorna apenas itens ativos, em ordem crescente
de código ASCII. Uma coleção vazia é um resultado de sucesso. Aplicada por UC-CAT-003.

**R-05 — Repetição da desativação.** Desativar um item já inativo tem sucesso
sem alterar seus dados. Aplicada por UC-CAT-004.

**R-06 — Ausência de persistência implícita dos dados retornados.** A leitura
retorna dados independentes do estado persistido. Atribuir valores à entidade
retornada não persiste alterações. Aplicada por UC-CAT-002, com suporte da
capacidade de persistência.

## 5. Obrigações e resultados compartilhados

**P-01 — Persistência.** O cadastro deve preservar a unicidade atomicamente,
mesmo diante de duas solicitações simultâneas para o mesmo código. Sucesso na
escrita significa confirmação pelo mecanismo de armazenamento. Registros
confirmados permanecem consultáveis após reconstrução normal da aplicação com
o mesmo armazenamento retido. Não se promete resistência a queda abrupta,
falta de energia, replicação remota ou recuperação de backup.

**P-02 — Responsabilidade e alteração.** Catálogo responde por esses registros.
Escritas são solicitadas pelos casos especificados; leituras não alteram dados
implicitamente. Código desconhecido e persistência indisponível permanecem
distinguíveis. Nenhuma operação pública exclui ou reativa itens nesta versão.

**S-01 — Segurança e isolamento.** Cada caso verifica A-01: a solicitação porta uma identidade de ator autenticado no conjunto permitido, e a recusa antecede qualquer efeito de domínio ou persistência. O mecanismo de autenticação e a exposição de rede — como a demonstração HTTP Basic em loopback usada pelo canal deste exemplo — são decisões de L4 documentadas no [contrato ADIB](../OAL-P4/HTTP.pt-br.md), não requisitos desta especificação. Operação multi-tenant e exposição à internet ficam fora desta versão.

**O-01 — Resultados observáveis.** Sucesso, dados inválidos, código duplicado,
item inexistente e persistência indisponível são distinguíveis quando aplicáveis.
Falhas não podem ser representadas como listagens vazias bem-sucedidas ou escritas confirmadas.

**O-02 — Escrita sem confirmação.** Se a persistência falhar após uma tentativa
de escrita, seu resultado final pode ser desconhecido. Não se promete reversão
somente porque houve falha. Após o restabelecimento, uma consulta pode verificar
o registro antes de decidir repetir a solicitação. Não se exige repetição automática.

**Q-01 — Recursos e desempenho.** Entradas obedecem aos limites finitos dos campos.
A listagem retorna o conjunto completo de disponíveis; pressupõe-se um catálogo
pequeno. Não são especificadas nem afirmadas metas de latência, vazão,
disponibilidade ou capacidade de recursos. Uma adoção em produção deve definir
as metas de que realmente necessita.

**Vocabulário de resultados:** `registered`, `found`, `listed`, `deactivated`,
`invalid_data`, `duplicate_item`, `item_not_found`, `persistence_unavailable`.
Identificam significados, não protocolo HTTP, representação de exceções ou esquema.

## 6. Casos de uso

### UC-CAT-001 — Cadastrar item

**Atores permitidos:** maintainer. Os demais são recusados antes dos efeitos.


**Objetivo / necessidade:** reter um novo item disponível; N-01.
**Acionamento / contexto:** um mantenedor solicita cadastro no catálogo único.
**Entradas:** código e nome. **Saída:** item cadastrado.
**Entidades / regras:** E-01, E-02; R-01, R-02.
**Condições assumidas:** A-01 e as suposições de escopo.
**Condições verificadas:** validade dos campos e código já atribuído.
**Capacidade exigida:** registrar atomicamente um novo item preservando unicidade.
**Dependências de casos de uso:** nenhuma.

Com dados válidos e código livre, cadastra o item como ativo e confirma seu registro.
Código duplicado rejeita o cadastro sem sobrescrever o item existente. Campos
inválidos rejeitam o cadastro antes da solicitação de escrita. Falha de recurso
produz `persistence_unavailable`, sob O-02, e não um resultado de sucesso.

**Efeitos e garantias:** um registro novo no sucesso; registros existentes
inalterados na rejeição por duplicidade. Aplicam-se P-01, P-02, S-01, O-01, O-02 e Q-01.

**Critérios de aceitação:**

- **AC-CAT-001-01:** cadastro válido retorna código/nome informados e active=true;
  consulta posterior retorna o registro.
- **AC-CAT-001-02:** entrada inválida é rejeitada e não cria registro.
- **AC-CAT-001-03:** código já atribuído é rejeitado mesmo que o item esteja inativo;
  seus dados permanecem inalterados.
- **AC-CAT-001-04:** dois cadastros válidos simultâneos para um código livre resultam
  em exatamente um sucesso e uma rejeição por duplicidade, com persistência disponível.
- **AC-CAT-001-05:** indisponibilidade é distinguível de cadastro confirmado.
- **AC-CAT-001-06:** Ator ausente ou sem permissão é recusado antes de qualquer efeito de domínio ou persistência.

### UC-CAT-002 — Consultar item

**Atores permitidos:** maintainer, reader. Os demais são recusados antes dos efeitos.


**Objetivo / necessidade:** inspecionar um registro retido; N-02.
**Acionamento / contexto:** um ator permitido solicita item pelo código.
**Entrada:** código. **Saída:** item, independentemente da disponibilidade.
**Entidades / regras:** E-01, E-02; R-03, R-06.
**Condição assumida:** A-01. **Condições verificadas:** validade do código e existência.
**Capacidade exigida:** recuperar registro retido por seu código.
**Dependências de casos de uso:** nenhuma.

Retorna registro encontrado independentemente de estar ativo. Código inválido
produz `invalid_data`; código válido ausente, `item_not_found`; persistência
indisponível produz `persistence_unavailable`, não ausência.

**Efeitos e garantias:** nenhuma alteração persistida. Aplicam-se P-02, S-01, O-01 e Q-01.

**Critérios de aceitação:**

- **AC-CAT-002-01:** registros ativos e inativos são consultáveis com seus dados.
- **AC-CAT-002-02:** código válido ausente produz resultado de item inexistente.
- **AC-CAT-002-03:** código inválido é rejeitado como dado inválido.
- **AC-CAT-002-04:** indisponibilidade da consulta não é informada como ausência.
- **AC-CAT-002-05:** alterar dados retornados não altera o registro persistido.
- **AC-CAT-002-06:** Ator ausente ou sem permissão é recusado antes de qualquer efeito de domínio ou persistência.

### UC-CAT-003 — Listar itens disponíveis

**Atores permitidos:** maintainer, reader. Os demais são recusados antes dos efeitos.


**Objetivo / necessidade:** identificar registros atualmente disponíveis; N-02.
**Acionamento / contexto:** um ator permitido solicita catálogo disponível.
**Entradas:** nenhuma além do contexto. **Saída:** coleção ordenada de itens.
**Entidades / regras:** E-02; R-04.
**Condição assumida:** A-01. **Condição verificada:** disponibilidade de cada item retornado.
**Capacidade exigida:** recuperar dados dos itens retidos.
**Dependências de casos de uso:** nenhuma.

Retorna registros ativos em ordem crescente de código. Retorna coleção vazia
se não houver disponíveis. Persistência indisponível é falha, não catálogo vazio.

**Efeitos e garantias:** nenhuma alteração persistida. Aplicam-se P-02, S-01, O-01 e Q-01.

**Critérios de aceitação:**

- **AC-CAT-003-01:** resultado contém exatamente os ativos na ordem exigida.
- **AC-CAT-003-02:** catálogo vazio ou apenas com inativos resulta em coleção vazia.
- **AC-CAT-003-03:** falha de persistência não se transforma em coleção vazia de sucesso.
- **AC-CAT-003-04:** Ator ausente ou sem permissão é recusado antes de qualquer efeito de domínio ou persistência.

### UC-CAT-004 — Desativar item

**Atores permitidos:** maintainer. Os demais são recusados antes dos efeitos.


**Objetivo / necessidade:** deixar de oferecer um item preservando seu registro; N-03.
**Acionamento / contexto:** um mantenedor solicita desativação por código.
**Entrada:** código. **Saída:** item retido inativo.
**Entidades / regras:** E-01, E-02; R-03, R-05.
**Condição assumida:** A-01. **Condições verificadas:** código válido, existência e disponibilidade.
**Capacidade exigida:** registrar dados alterados de item existente, sem inserir ausente.
**Dependência de caso de uso:** UC-CAT-002 obtém o item e fornece seus resultados de consulta.

Item ativo torna-se inativo sem perder código/nome. Item já inativo é retornado
com sucesso sem nova mudança de estado. Código inválido e item inexistente
preservam suas rejeições. Falhas de consulta ou persistência são distinguíveis;
escritas sem confirmação seguem O-02.

**Efeitos e garantias:** apenas active muda na transição bem-sucedida. Repetir
não apaga dados. Aplicam-se P-01, P-02, S-01, O-01, O-02 e Q-01.

**Critérios de aceitação:**

- **AC-CAT-004-01:** item torna-se inativo, sai da listagem e continua consultável.
- **AC-CAT-004-02:** repetir tem sucesso com os mesmos dados retidos.
- **AC-CAT-004-03:** registro ausente é rejeitado, sem criação implícita.
- **AC-CAT-004-04:** código inválido é rejeitado como dado inválido.
- **AC-CAT-004-05:** indisponibilidade da consulta ou persistência não gera falsa confirmação.
- **AC-CAT-004-06:** Ator ausente ou sem permissão é recusado antes de qualquer efeito de domínio ou persistência.

## 7. Cenários de aceite centralizados

As verificações executáveis dos casos são incluídas **por referência** em
[tests/p3](../tests/p3). O [mapa ADVS](../OAL-P2/advs/behavioral-tests.json) identifica o teste comportamental de cada caso. Cada verificação identifica os critérios de
aceitação. Os contratos legíveis acima permanecem a fonte do comportamento
exigido; preparação da execução não integra esses contratos.

**AC-SHARED-01 — critério transversal de integração da retenção:** cadastrar um item, confirmar sua desativação, encerrar aquela instância da aplicação e reconstruí-la com o mesmo armazenamento retido. A consulta retorna o mesmo código e nome com `active=false`; a listagem de disponíveis exclui esse item. Avalia reconstrução normal, não queda abrupta ou falta de energia.

Sua definição canônica completa é a entrada `shared_criteria` do [index.json](index.json). Abrange UC-CAT-001 a UC-CAT-004 e as obrigações P-01/P-02. É distinto dos critérios próprios de caso e é coberto por uma verificação compartilhada vinculada a BT-CAT-001 a BT-CAT-004; não cria novo caso nem teste comportamental diretamente vinculado adicional.

O [índice](index.json) identifica os quatro casos e todos os critérios.
A suíte central é recomendada, não condição para classificar um documento como UCS.
Testes unitários e de integração não integram esta especificação.

## 8. Rastreabilidade, estado e evolução

A baseline completa contém exatamente UC-CAT-001 a UC-CAT-004. Cada um deve
corresponder a exatamente uma implementação, sem caso arquitetural não documentado.
A [correspondência da implementação](../OAL-P2/adpm/traceability.json) registra o vínculo
separadamente, sem prescrever um formato de armazenamento de UCS.

As exigências acima são decisões da baseline didática. A-01/A-02 são suposições;
hospedagem de produção, gestão de contas, recuperação após falha abrupta, metas de
desempenho e isolamento de implantação são excluídos ou explicitamente não
especificados, não promessas implementadas implicitamente. A-01 exige uma identidade
de ator autenticado em toda solicitação; o mecanismo de canal que fornece essa
identidade é especificado na fronteira de interação, e suas credenciais de
demonstração não são um sistema de contas de produção. Não há requisitos pendentes
para o escopo didático dos quatro casos.

A versão 0.1.0 introduziu o escopo. A versão 0.2.0 adapta a especificação à edição
Alpha-v0.2.0-Alkimim: as escolhas de canal (mecanismo de autenticação, exposição em
loopback) foram separadas em referências de L4, e a redação de autenticação de
A-01/S-01 foi harmonizada com as exclusões acima. Uma versão posterior registra
mudanças de objetivos, resultados, dependências e garantias, preservando IDs quando o
significado é preservado. IDs não são reutilizados para objetivos diferentes.
Textos em inglês e português são traduções sincronizadas.
