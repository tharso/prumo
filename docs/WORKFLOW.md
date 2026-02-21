# Prumo - Workflow de Produto (GitHub)

Este documento define o fluxo oficial para desenvolvimento do Prumo.

## 1) Fonte de verdade

- Backlog e estado de execução: Issues + Project no GitHub.
- Escopo técnico e entrega: Pull Requests.
- Versionamento público: `VERSION` + `CHANGELOG.md`.

## 2) Pipeline de trabalho

1. Triage da issue (`status/triage` -> `status/ready`).
2. Execução (`status/in-progress`) em branch `codex/<issue-id>-<slug>`.
3. PR com checklist completo e issue vinculada.
4. Merge em `main`.
5. Atualização de versão/changelog quando houver mudança pública.

## 3) Taxonomia mínima de labels

- Tipo: `type/feature`, `type/bug`, `type/debt`, `type/spike`, `type/chore`.
- Prioridade: `priority/p0`, `priority/p1`, `priority/p2`, `priority/p3`.
- Status: `status/triage`, `status/ready`, `status/in-progress`, `status/review`, `status/done`, `status/blocked`.
- Área: `area/core`, `area/briefing`, `area/setup`, `area/landing`, `area/docs`, `area/infra`.
- Agente: `agent/codex`, `agent/cowork`.

## 4) Regras de autonomia do Codex

Codex pode, sem pedir confirmação intermediária:

- pegar issue `status/ready` com `agent/codex`;
- implementar solução completa;
- abrir PR com checklist preenchido;
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
