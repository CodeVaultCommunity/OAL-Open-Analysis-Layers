# Distribuição canônica da candidata

[English](DISTRIBUTION.md) · [Início](README.pt-br.md)

Stable-v1.0.0 está em preparação local como candidata. Este trabalho não publica tag, release ou commit remoto. Snapshots publicados continuam imutáveis. A [lista de exceções operacionais Alpha](ALPHA-OPERATIONAL-ALLOWLIST.json) registra as únicas mudanças autorizadas nos dois diretórios históricos: lançadores independentes e trechos operacionais de oito READMEs por edição. Manuais normativos, modelos, instâncias, fontes das aplicações, testes, skills e evidências históricas permanecem iguais à base registrada. A exceção não altera requisito OAL.

O lançador da raiz foi removido. Cada `run_examples.py` depende apenas dos `examples/` de sua edição e grava os bancos padrão em seu próprio `data/`. Os bancos antigos em `data/<edição>/` na raiz são preservados; informe `--database` para reutilizá-los. Consulte o [guia operacional Stable](versioning/Stable-v1.0.0/examples/README.pt-br.md#executar-um-exemplo).

## Preparar e verificar

1. Inclua no índice as adições, alterações e exclusões pretendidas com caminhos explícitos. Finalize os textos e hashes de origem da skill. Exporte a candidata do índice para um checkout Git separado e limpo, com bytes canônicos conforme `.gitattributes` (`text=auto eol=lf`). Preserve arquivos Alpha locais protegidos; não normalize apenas durante o cálculo de hashes.
2. Execute `python scripts/test_edition_launchers.py`, as três suítes pytest Stable separadamente, o renderizador Board CRM com `--check`, `python scripts/check_structure.py --edition Stable-v1.0.0` e `python scripts/test_release_checks.py`. A suíte dos lançadores verifica as três edições e nove servidores HTTP, incluindo cópias isoladas renomeadas e bancos existentes.
3. Preserve os bytes das evidências anteriores. O [índice histórico](versioning/Stable-v1.0.0/examples/verification/history.json) distingue observações de snapshots anteriores da [execução atual](versioning/Stable-v1.0.0/examples/verification/execution.json). Registre entradas e resultados reais; exclua saídas de verificação e inventário dos hashes de entrada para evitar ciclos.
4. Inclua as evidências finais no índice do checkout limpo; execute `python scripts/content_inventory.py --write` e `python scripts/content_inventory.py --check`. A ferramenta usa os bytes reais de todos os arquivos indexados, exceto o próprio inventário. Copie os arquivos finais pretendidos de volta ao repositório de origem, inclua-os explicitamente no índice e faça commit. Verifique que a árvore Git comitada corresponde à candidata canônica validada.
5. Gere a distribuição desse commit com `git archive --format=zip --output=OAL-Stable-v1.0.0.zip HEAD`. Não compacte um diretório de trabalho potencialmente misto. `.git`, ambientes, caches, bancos e saídas temporárias não pertencem ao ZIP.
6. Execute `python scripts/check_archive.py CAMINHO_DO_ZIP`, extraia em um diretório vazio e execute `python scripts/check_archive.py DIRETORIO_EXTRAIDO`. As duas verificações comparam cobertura completa, tamanhos e SHA-256 dos bytes reais com o inventário incluído, sem exigir Git. Já `content_inventory.py`, baseado no índice, exige checkout Git e não serve como verificador isolado de arquivo ZIP.

Entregue o commit final e o hash do ZIP fora dos arquivos comitados; incluir o identificador ou hash da própria entrega criaria referência circular. Isso não implica publicação. Atualize os snapshots de origem e hashes da base Atlas quando mudarem os textos ou bytes de origem.

## Limites da verificação

A execução local informa Python, pytest, sistema, horários e comandos reais. Configurar CI não comprova execução local em Linux. Resposta HTTP e término do processo não comprovam comportamento JavaScript, acessibilidade visual, correção universal ou execução de transformador. Controles de Ctrl+C e navegador simulados não comprovam sinais do sistema ou comportamento da interface. Diferenças CRLF locais preexistentes podem fazer falhar a verificação de bytes reais desse checkout; a evidência de distribuição é a árvore canônica e o ZIP verificados.
