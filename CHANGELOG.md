# Changelog

Este arquivo registra mudanças públicas do produto Prumo.

O formato segue, de forma pragmática, a ideia de Keep a Changelog e versionamento semântico.

## [3.6.3] - 2026-02-22

### Changed
- Regra de processamento do inbox reforçada com commit explícito (confirmar, executar em lote e verificar).
- Skills de briefing (`skills/briefing/SKILL.md` e `skills-briefing-SKILL.md`) agora exigem:
  - confirmação de commit antes da execução;
  - deleção real do original no inbox;
  - tratamento explícito de falha por permissão (incluindo `allow_cowork_file_delete` quando aplicável);
  - relatório final de sucesso/falha por item.
- Fallback oficial para runtimes sem deleção física: marcação em `Inbox4Mobile/_processed.json` e filtro no briefing para não reapresentar itens já processados.

## [3.6.2] - 2026-02-21

### Added
- Guardrails explícitos de atualização segura para impedir sobrescrita de arquivos personalizados.
- Script `scripts/safe_core_update.sh` para atualizar apenas `PRUMO-CORE.md` com backup automático.
- Regra de validação no CI para presença do guardrail de update.

### Changed
- Instruções de update em `skills/briefing/SKILL.md`, `skills-briefing-SKILL.md` e `references/prumo-core.md` reforçam allowlist de escrita.
- Setup/reconfiguração em `SKILL.md` passa a exigir confirmação explícita para sobrescritas de arquivos sensíveis.
- Conteúdo público sanitizado para remover referências pessoais diretas em canais e exemplos.

## [3.6.1] - 2026-02-21

### Added
- Estrutura de governança de produto no GitHub (`issues`, `PR template`, `CI`, scripts de bootstrap).
- Documentação operacional para fluxo de trabalho com Codex/Cowork (`docs/WORKFLOW.md`).
- Script para bootstrap de labels (`scripts/github/bootstrap_labels.sh`).
- Script para criação de project de produto (`scripts/github/bootstrap_project.sh`).

### Changed
- Reintroduzido `VERSION` como fonte de verdade de versão pública do produto.

## [3.6.0] - 2026-02-19

### Added
- Curadoria de emails orientada à ação (`Responder`, `Ver`, `Sem ação`) com prioridade (`P1/P2/P3`).
- Janela temporal de briefing via `_state/briefing-state.json`.
- Paridade de briefing entre runtime com shell e sem shell.
