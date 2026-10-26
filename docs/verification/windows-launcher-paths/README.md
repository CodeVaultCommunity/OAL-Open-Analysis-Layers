# Windows launcher path maintenance / Manutenção de caminhos no Windows

This records repository maintenance after published OAL Stable-v1.0.0, commit
`ce225141686d4b6b3e46923866c97d84c031903f`. It does not revise the edition's
normative sources, examples, launchers, skill or previously recorded evidence.
The published tag remains fixed. / Este registro cobre manutenção do repositório
após a publicação. Fontes normativas, exemplos, lançadores, skill, evidências
anteriores e tag publicada permanecem preservados.

The Windows CI failure compared an abbreviated `RUNNER~1` temporary path with
the resolved `runneradmin` path passed by the launcher. The expected database
path is now resolved before the exact mock-call assertion. The three new
regressions load the real launcher through an existing `examples/../` alias;
they fail with the original assertion and exercise all existing control checks.
/ A falha comparava formas abreviada e completa do mesmo caminho. A correção
resolve o caminho esperado e mantém a comparação exata da chamada. As três
regressões novas exercitam os lançadores reais por um caminho equivalente.

See [execution.json](execution.json) for actual commands, environments, outcomes,
fixed input hashes, preservation checks and log paths. The before-fix failure
is intentional regression evidence, not a passing run. The local Windows 8.3
check is recorded only if an actual short-name alias is available.
/ Consulte o registro para comandos, ambientes, resultados, entradas fixadas,
preservação e logs. A falha anterior à correção é evidência negativa intencional.

Input hashes exclude CONTENT-SHA256.json, this generated maintenance report
directory and the earlier examples/verification/ report directories, avoiding
circular references. Earlier report bytes remain in the published snapshot
and are checked for preservation. / Hashes de entrada excluem o inventário,
este diretório de relatórios e relatórios anteriores, evitando circularidade;
os bytes históricos são preservados.

Local execution is not a successful GitHub Actions run. The new revision still
needs its Windows/Linux CI after an authorized push. HTTP tests do not assess
browser JavaScript or visual accessibility; Ctrl+C/browser controls are mocked.
/ Execução local não comprova CI remota aprovada. A nova revisão ainda precisa
da CI Windows/Linux após push autorizado. Não há avaliação de JavaScript ou
acessibilidade visual; controles de Ctrl+C/navegador são simulados.
