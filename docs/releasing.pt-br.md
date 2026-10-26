# Preparar e publicar uma release OAL

[English](releasing.md) · [Início](../README.pt-br.md) · [Orientações para agentes](../AGENTS.md)

Este procedimento de manutenção não acrescenta requisitos de conformidade OAL. Selecione a edição pretendida antes de escolher seu manual, exemplos, skill ou verificações. VERSION identifica a edição padrão do repositório. Uma release fixa um commit verificado e seus bytes distribuídos; snapshots publicados por commit/tag permanecem imutáveis.

## Preparar as fontes

Confira primeiro a branch, o diretório de trabalho e as tags/releases publicadas. Preserve alterações do usuário e edições históricas. Finalize a documentação em inglês e português, referências de versões, proveniência e hashes de origem da skill selecionada antes das evidências finais. Preserve versões de modelos e aplicações quando seus contratos independentes não mudarem. As notas da release descrevem escopo e limites reais; datas de publicação e DOIs devem corresponder a publicação ou atribuição efetivas.

Preserve os bytes dos registros e logs anteriores, com seus comandos originais e a identidade do snapshot. Aponte as evidências correntes para a nova verificação. Um caminho removido ou hash anterior em uma execução arquivada descreve aquele snapshot; não é comando atual nem autorização para alterar conteúdo histórico. Não reescreva observações antigas para aparentar correspondência com a nova entrega.

Use checkout limpo ou exportação do índice Git conforme .gitattributes (text=auto eol=lf). Um diretório com diferenças CRLF preexistentes não serve como fonte de inventário de bytes reais ou ZIP. Mantenha os arquivos de trabalho protegidos intactos; não normalize apenas durante o cálculo de hashes nem regenere o manifesto para aceitar bytes mistos.

## Verificar a edição selecionada

Execute as verificações suportadas pela documentação da própria edição. Para Stable-v1.0.0, use Python 3.12+ com pytest 9.0.2 e, na raiz:

```bash
python scripts/test_edition_launchers.py
python versioning/Stable-v1.0.0/examples/board-crm/OAL-P1/render_ucs.py --check
python scripts/check_structure.py --edition Stable-v1.0.0
python scripts/test_release_checks.py
```

Execute `python -m pytest -q` separadamente em versioning/Stable-v1.0.0/examples/tiny-catalog, board-crm e work-board. A suíte dos lançadores verifica as três edições declaradas, incluindo nove servidores HTTP, cópias isoladas renomeadas e preservação de bancos existentes. O verificador estrutural confere declarações dos modelos Stable e links locais, inclusive guias operacionais Alpha; ele não reavalia conformidade Alpha.

Registre comandos, versões de Python/pytest/sistema, horários, resultados e hashes das entradas fixadas. Exclua relatórios/logs gerados e CONTENT-SHA256.json das entradas para evitar ciclos, declarando as exclusões. Atualize os ponteiros de evidência corrente com resultados observados e confira novamente as fontes e os metadados finais.

## Fixar e inspecionar o pacote

Inclua no índice as adições, alterações e exclusões pretendidas com caminhos explícitos antes de gerar o inventário; o script descobre arquivos pelo índice Git. No checkout canônico limpo, execute:

```bash
python scripts/content_inventory.py --write
python scripts/content_inventory.py --check
```

Inclua o inventário resultante no índice e faça commit da árvore final. Confira que a árvore comitada corresponde à árvore canônica usada nas verificações. Gere o ZIP desse commit com `git archive --format=zip --output=OAL-Stable-v1.0.0.zip HEAD`, substituindo a edição no nome quando necessário. O pacote deve conter os arquivos pretendidos daquele commit, sem .git, ambientes, caches, bancos ou saídas temporárias de compilação.

Execute `python scripts/check_archive.py CAMINHO_DO_ZIP`, extraia em diretório vazio e execute `python scripts/check_archive.py DIRETORIO_EXTRAIDO`. As duas verificações comparam cobertura completa, tamanhos e SHA-256 dos bytes reais com o inventário incluído, sem exigir Git. Já content_inventory.py, baseado no índice, exige checkout Git. Não existe contagem fixa permanente de arquivos.

Entregue o commit final e o hash do ZIP em recibo externo ou nos metadados da release. Incluir o identificador final ou hash do próprio ZIP naquele commit criaria referência circular. Quando os manuais normativos ou seus textos introdutórios mudarem, forneça a projetos dependentes, como Atlas, os novos bytes exatos, licença, commit e hashes; atualize seus snapshots fixados e inventários antes de afirmar sincronização.

## Publicar o commit verificado

Após a autorização para publicação, envie o commit pretendido e exija CI aprovada para essa revisão exata nos jobs suportados de Windows e Linux. A configuração da CI, isoladamente, não comprova execução aprovada. Crie a tag anotada e a release da edição a partir do commit verificado, anexe o ZIP conferido e seu SHA-256 e confirme que tag, release e arquivo publicado identificam a revisão pretendida. Nunca substitua um snapshot publicado para incorporar uma correção posterior.

O lançador de cada edição continua autossuficiente, com bancos padrão em seu próprio data/. Bancos antigos em `data/<edição>/` na raiz permanecem no lugar e podem ser selecionados por --database; a publicação não os migra nem exclui.

## Limites das evidências

Informe o ambiente efetivamente exercitado. Resposta HTTP e término do processo não comprovam comportamento JavaScript, acessibilidade visual, correção universal ou execução de transformador OAL. Controles simulados de Ctrl+C/navegador não comprovam integração com sinais do sistema ou interface. Preserve essas distinções nas notas da release e nas evidências.
