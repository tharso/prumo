# Prumo

Sistema de organização pessoal orientado à ação. O foco do Prumo não é listar pendência; é transformar entrada difusa em decisão clara.

Estado deste documento: **19/02/2026**.

## Estado atual

- Core local: `prumo_version 3.6` (`PRUMO-CORE.md`).
- Skill principal de setup: `v3.4` (`SKILL.md`).
- Skill de briefing: `v2.2` (com curadoria por ação em runtime com e sem shell).
- Coexistência multiagente Codex/Cowork ativa e validada.
- Handovers `HO-2026-02-19-001` até `HO-2026-02-19-005`: **CLOSED** em `_state/HANDOVER.md`.

## O que o sistema entrega hoje

1. Setup guiado para gerar estrutura de operação (arquivos, áreas, rituais, tom).
2. Briefing diário com consolidação de agenda e triagem de email por prioridade.
3. Processamento de inbox multi-canal (`INBOX.md`, `Inbox4Mobile/`, email quando disponível).
4. Revisão semanal com higienização de pauta e histórico.
5. Protocolo de coexistência entre agentes (lock por escopo + handover rastreável).

## Arquitetura

O sistema opera em três arquivos principais:

- `CLAUDE.md`: configuração pessoal (identidade, áreas, tom, lembretes, integrações).
- `PRUMO-CORE.md`: regras operacionais do sistema (rituais, fluxo, governança).
- `AGENTS.md`: adaptador para runtimes que não usam `CLAUDE.md` nativamente.

Arquivos de estado e operação:

- `_state/agent-lock.json`: lock cooperativo por escopo entre agentes.
- `_state/HANDOVER.md`: validações cruzadas e status de handovers.
- `_state/briefing-state.json`: referência temporal de briefing (`last_briefing_at`).

## Comandos ativos

- `/prumo:setup`: configuração inicial ou reconfiguração do sistema (áreas, tom, rituais e integrações).
- `/prumo:briefing` (canônico): rotina matinal completa com agenda, inbox, curadoria de email e prioridades.
- `/briefing` (alias legado): executa a mesma rotina do `/prumo:briefing` para compatibilidade.
- `/prumo:inbox`: processa inbox sob demanda (INBOX.md, Inbox4Mobile e canais conectados quando disponíveis).
- `/prumo:dump`: captura rápida de informações soltas para o sistema organizar em contexto e ação.
- `/prumo:revisao`: revisão semanal da pauta, limpeza de pendências e recalibração de prioridades.
- `/prumo:status`: visão rápida do estado atual (itens quentes, bloqueios e próximos focos).
- `/prumo:handover`: abre, responde e fecha handovers de validação entre agentes.
- `/prumo:menu`: lista os comandos disponíveis no sistema.

## Workflow de produto (GitHub)

Este repositório agora usa um fluxo padrão de produto com Issues, Project e versionamento explícito.

1. Templates de issue: `.github/ISSUE_TEMPLATE/`
2. Template de PR: `.github/pull_request_template.md`
3. CI de higiene: `.github/workflows/ci.yml`
4. Guia operacional: `docs/WORKFLOW.md`
5. Versão pública: `VERSION`
6. Histórico de mudanças: `CHANGELOG.md`
7. Bootstrap de labels: `scripts/github/bootstrap_labels.sh`
8. Bootstrap de project: `scripts/github/bootstrap_project.sh`

## Briefing: lógica atual

### Canais lidos

- `Inbox4Mobile/` (incluindo imagens)
- Gmail (quando disponível)
- Google Calendar (hoje e amanhã)
- `_state/HANDOVER.md` (pendências de validação)

### Curadoria de email (modelo único)

A triagem usa três buckets:

- `Responder`: exige resposta ativa.
- `Ver`: exige leitura/checagem, sem resposta imediata.
- `Sem ação`: baixo valor imediato.

Cada item deve vir com:

- prioridade (`P1`, `P2`, `P3`)
- motivo objetivo

### Janela temporal

- Se `_state/briefing-state.json` tiver `last_briefing_at`, essa é a âncora.
- Se não tiver, fallback de 24h.
- Ao concluir o briefing, atualizar `last_briefing_at`.

### Runtime com shell (modo avançado)

Quando disponível, pode usar script dual-profile:

- `scripts/prumo_google_dual_snapshot.sh`

Template do script no produto:

- `references/prumo-google-dual-snapshot.sh`

Esse modo permite consolidar duas contas (ex.: pessoal/trabalho) no mesmo briefing.

### Runtime sem shell (paridade obrigatória)

Sem shell/Gemini CLI, o briefing **mantém a mesma taxonomia de curadoria** via integrações nativas. O objetivo é evitar degradação de qualidade por limitação de runtime.

## Coexistência Codex x Cowork

Protocolo vigente:

1. lock de escopo em `_state/agent-lock.json` antes de alterações críticas.
2. handover em `_state/HANDOVER.md` para mudanças relevantes.
3. briefing checa `PENDING_VALIDATION` e `REJECTED` automaticamente.

Status de validação recente:

- Base de coexistência: aprovada.
- Checagem automática de handover no briefing: aprovada.
- Comando manual `/prumo:handover`: aprovado.
- Integração de curadoria Google dual: aprovada (com nota de limite de runtime Cowork).
- Paridade sem shell + versionamento formal: aprovada.

## Estrutura do projeto (snapshot local)

```text
Prumo/
├── README.md
├── SKILL.md
├── skills/
│   ├── briefing/SKILL.md
│   └── handover/SKILL.md
├── skills-briefing-SKILL.md
├── skills-handover-SKILL.md
├── references/
│   ├── prumo-core.md
│   ├── claude-md-template.md
│   ├── agents-md-template.md
│   ├── file-templates.md
│   ├── mobile-shortcut-guide.md
│   └── prumo-google-dual-snapshot.sh
└── test-output/
```

## O que ainda não está redondo

1. Distribuição de plugin depende do pacote de release (manifesto e empacotamento) no repositório de distribuição.
2. Integração dual-profile depende de infraestrutura local (shell + Gemini CLI + MCP autenticado).
3. Ainda faltam testes de regressão automatizados para cenários de briefing e reconfiguração.

## Roadmap curto

1. Consolidar pacote de release para publicação sem ajuste manual.
2. Adicionar testes de smoke para briefing (com e sem shell).
3. Evoluir métricas de qualidade de curadoria (taxa de `Responder` resolvido por ciclo).

## Referências rápidas

- Motor local: `../PRUMO-CORE.md`
- Estado operacional: `../_state/`
- Registro de auditoria: `../REGISTRO.md`
- Pauta ativa: `../PAUTA.md`

---

Se o sistema parar de parecer útil, o problema não é falta de lista. É falta de decisão com contexto. O README acima existe para evitar exatamente esse tipo de autoengano elegante.
