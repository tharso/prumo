# Prumo - Workflow de Produto (GitHub)

Este documento define o fluxo oficial para desenvolvimento do Prumo.

## 1) Fonte de verdade

- Backlog e estado de execução: Issues + Project no GitHub.
- Escopo técnico e entrega: Pull Requests.
- Versionamento público: `VERSION` + `CHANGELOG.md`.
- Regras de engenharia do produto: `docs/PRODUCT_DEVELOPMENT_GUIDELINES.md`.

## 2) Pipeline de trabalho

1. Triage da issue (`status/triage` -> `status/ready`).
2. Execução (`status/in-progress`) em branch `codex/<issue-id>-<slug>`.
3. PR com checklist completo, issue vinculada e matriz de compatibilidade (`Codex`, `Claude`, `Gemini`).
4. Abertura de issues `type/validation` para os agentes que não implementaram.
5. Merge em `main`.
6. Atualização de versão/changelog quando houver mudança pública.

## 2.1) Regra crítica de atualização segura

Update de versão nunca pode tocar arquivos personalizados do usuário.

Allowlist de escrita no update:

1. `PRUMO-CORE.md`
2. `_backup/PRUMO-CORE.md.*`

Para execução via shell, usar `scripts/safe_core_update.sh`.

## 2.2) Regra crítica de validação cruzada

Toda feature deve gerar validação por outros agentes.

Exemplo:

1. Implementado por `agent/codex` -> abrir validação para `agent/cowork` e `agent/gemini`.
2. Implementado por `agent/cowork` -> abrir validação para `agent/codex` e `agent/gemini`.
3. Implementado por `agent/gemini` -> abrir validação para `agent/codex` e `agent/cowork`.

As validações devem virar issues com label `type/validation` e serem linkadas no PR.

## 3) Taxonomia mínima de labels

- Tipo: `type/feature`, `type/bug`, `type/debt`, `type/spike`, `type/chore`.
- Tipo adicional: `type/validation`.
- Prioridade: `priority/p0`, `priority/p1`, `priority/p2`, `priority/p3`.
- Status: `status/triage`, `status/ready`, `status/in-progress`, `status/review`, `status/done`, `status/blocked`.
- Área: `area/core`, `area/briefing`, `area/setup`, `area/landing`, `area/docs`, `area/infra`.
- Agente: `agent/codex`, `agent/cowork`, `agent/gemini`.
- Compatibilidade: `compat/multi-agent`.

## 4) Regras de autonomia do Codex

Codex pode, sem pedir confirmação intermediária:

- pegar issue `status/ready` com `agent/codex`;
- implementar solução completa;
- abrir PR com checklist preenchido;
- abrir issues de validação cruzada para os agentes pares;
- atualizar `CHANGELOG.md` e `VERSION` (quando aplicável);
- mover issue para `status/review`.

Codex não pode:

- inventar escopo fora da issue;
- pular critérios de aceite;
- publicar release sem versão/changelog coerentes.

## 5) Ritmo operacional recomendado

- Diário: triagem curta (10 min) para manter `Next` limpo.
- Semanal: revisão de roadmap e corte de escopo (30 min).
- Release: sempre com changelog legível por humano.

## 6) Projeto GitHub (board)

Use o script `scripts/github/bootstrap_project.sh` para criar o board base.

Campos recomendados:

- Status
- Priority
- Area
- Size
- Target Version
- Agent
- Blocked By
