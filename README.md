# Prumo

Sistema de organização pessoal orientado à ação. O foco do Prumo não é listar pendência; é transformar entrada difusa em decisão clara.

Estado deste documento: **23/02/2026**.

## Estado atual

- Core de referência no produto: `prumo_version 3.8.3` (`references/prumo-core.md`).
- Skill principal de setup: `v3.4` (`SKILL.md`).
- Skill de briefing: `v2.2` (com curadoria por ação em runtime com e sem shell).
- Coexistência multiagente ativa e validada.
- Fluxo de handover operacional e auditável via `_state/HANDOVER.md`.

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
- `_state/HANDOVER.summary.md`: resumo leve de handover para briefing.
- `_state/briefing-state.json`: estado do briefing (`last_briefing_at`, `interrupted_at`, `resume_point`).
- `_state/auto-sanitize-state.json`: estado da última autosanitização.
- `_state/auto-sanitize-history.json`: histórico local para calibrar thresholds por usuário/workspace.

## Comandos ativos

- `/prumo:setup`: configuração inicial ou reconfiguração do sistema (áreas, tom, rituais e integrações).
- `/prumo:briefing` (canônico): rotina matinal completa com agenda, inbox, curadoria de email e prioridades.
- `/briefing` (alias legado): executa a mesma rotina do `/prumo:briefing` para compatibilidade.
- `/prumo:inbox`: processa inbox sob demanda (INBOX.md, Inbox4Mobile e canais conectados quando disponíveis).
- `/prumo:dump`: captura rápida de informações soltas para o sistema organizar em contexto e ação.
- `/prumo:revisao`: revisão semanal da pauta, limpeza de pendências e recalibração de prioridades.
- `/prumo:status`: visão rápida do estado atual (itens quentes, bloqueios e próximos focos).
- `/prumo:handover`: abre, responde e fecha handovers de validação entre agentes.
- `/prumo:sanitize`: compacta estado operacional (`HANDOVER`) e gera resumo leve para acelerar briefing.
- `/prumo:menu`: lista os comandos disponíveis no sistema.

## Workflow de produto (GitHub)

Este repositório agora usa um fluxo padrão de produto com Issues, Project e versionamento explícito.

1. Templates de issue: `.github/ISSUE_TEMPLATE/`
2. Template de PR: `.github/pull_request_template.md`
3. CI de higiene: `.github/workflows/ci.yml`
4. Workflow de release: `.github/workflows/release.yml`
5. Diretrizes obrigatórias de engenharia: `docs/PRODUCT_DEVELOPMENT_GUIDELINES.md`
6. Guia operacional: `docs/WORKFLOW.md`
7. Manual prático (Projects/Issues + Codex autônomo): `docs/MANUAL_GITHUB_CODEX_AUTONOMO.md`
8. Guia de autosanitização: `docs/AUTOSANITIZACAO.md`
9. Checklist de validação rápida do briefing (Cowork): `docs/CHECKLIST_VALIDACAO_BRIEFING_3MIN.md`
10. Versão pública: `VERSION`
11. Histórico de mudanças: `CHANGELOG.md`
12. Bootstrap de labels: `scripts/github/bootstrap_labels.sh`
13. Bootstrap de project: `scripts/github/bootstrap_project.sh`
14. Sync de schema de project existente: `scripts/github/sync_project_schema.sh`
15. Smoke test de briefing: `scripts/tests/briefing_smoke.sh`

## Briefing: lógica atual

### Fluxo progressivo

O briefing diário segue dois blocos:

1. Bloco 1 (automático): agenda + preview inbox + contagem silenciosa de agendados.
2. Bloco 2 (uma interação): proposta do dia com `a/b/c/d`.

`c` abre contexto completo sob demanda (`/prumo:briefing --detalhe`).
`d` aplica escape hatch (interrompe sem cobrança e salva ponto de retomada).
Guardrail: na primeira interação do briefing, não abrir arquivos brutos do inbox.

### Canais lidos

- `Inbox4Mobile/` (incluindo imagens)
- Gmail (quando disponível)
- Google Calendar (hoje e amanhã)
- `_state/HANDOVER.summary.md` (ou fallback `_state/HANDOVER.md`)

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

### Supressão temporal (agendados)

- Itens agendados podem registrar cobrança explícita com `| cobrar: DD/MM`.
- Se a data de cobrança estiver no futuro, o item fica fora do briefing diário (entra só na contagem silenciosa).
- Na revisão semanal, todos os itens aparecem, com ou sem cobrança futura.

### Garantia de não sobrescrita em updates

Durante atualização de versão do Prumo, a escrita permitida é restrita a:

1. `PRUMO-CORE.md`
2. `_backup/PRUMO-CORE.md.*` (backup pré-atualização)

Arquivos personalizados do usuário (`CLAUDE.md`, `PAUTA.md`, `INBOX.md`, `REGISTRO.md`, `IDEIAS.md`, `AGENTS.md` e pastas de áreas) não podem ser alterados no fluxo de update.

### Runtime com shell (modo avançado)

Quando disponível, pode usar script dual-profile:

- `scripts/prumo_google_dual_snapshot.sh`

Para triagem visual opcional do inbox multimídia:

- `scripts/generate_inbox_preview.py` (gera `Inbox4Mobile/inbox-preview.html` + `Inbox4Mobile/_preview-index.json`)
- `scripts/prumo_sanitize_state.py` (compacta handovers antigos e gera `_state/HANDOVER.summary.md`)
- `scripts/prumo_auto_sanitize.py` (autosanitização por gatilhos + cooldown; calibração adaptativa por workspace via `_state/auto-sanitize-history.json`)

Template do script no produto:

- `references/prumo-google-dual-snapshot.sh`

Esse modo permite consolidar duas contas (ex.: pessoal/trabalho) no mesmo briefing.

### Triagem de inbox em 2 estágios

1. Estágio A (leve): preview + índice (`inbox-preview.html` e `_preview-index.json`).
2. Estágio B (seletivo): abrir bruto só para `P1`, ambíguos ou risco legal/financeiro/documental.
3. No briefing diário, o preview é regenerado no início quando shell está disponível.

### Autosanitização (futuro operacional já habilitado)

Quando o runtime tem shell, o briefing pode executar manutenção preventiva automática:

1. roda `prumo_auto_sanitize.py` com cooldown (default: 6h),
2. dispara sanitização de handover quando `HANDOVER.md` cresce além do limite,
3. regenera preview/index do inbox quando volume ou defasagem exigirem,
4. calibra thresholds com base no histórico do próprio usuário/workspace,
5. grava trilha em `_state/auto-sanitize-state.json` e histórico em `_state/auto-sanitize-history.json`.

Regra de segurança: autosanitização não toca arquivos pessoais (`CLAUDE.md`, `PAUTA.md`, `INBOX.md`, `REGISTRO.md`, `IDEIAS.md`).

### Runtime sem shell (paridade obrigatória)

Sem shell/Gemini CLI, o briefing **mantém a mesma taxonomia de curadoria** via integrações nativas. O objetivo é evitar degradação de qualidade por limitação de runtime.

## Coexistência multiagente

Protocolo vigente:

1. lock de escopo em `_state/agent-lock.json` antes de alterações críticas.
2. handover em `_state/HANDOVER.md` para mudanças relevantes.
3. briefing checa `PENDING_VALIDATION` e `REJECTED` automaticamente.

Status de validação recente:

- Base de coexistência: aprovada.
- Checagem automática de handover no briefing: aprovada.
- Comando manual `/prumo:handover`: aprovado.
- Integração de curadoria Google dual: aprovada (com nota de limite de runtime por ambiente).
- Paridade sem shell + versionamento formal: aprovada.

## Estrutura do projeto (snapshot local)

```text
Prumo/
├── README.md
├── SKILL.md
├── skills/
│   ├── briefing/SKILL.md
│   ├── handover/SKILL.md
│   └── sanitize/SKILL.md
├── skills-briefing-SKILL.md
├── skills-handover-SKILL.md
├── skills-sanitize-SKILL.md
├── references/
│   ├── prumo-core.md
│   ├── claude-md-template.md
│   ├── agents-md-template.md
│   ├── file-templates.md
│   ├── mobile-shortcut-guide.md
│   ├── prumo-google-dual-snapshot.sh
│   └── modules/
│       ├── load-policy.md
│       ├── briefing-fast-path.md
│       └── sanitization.md
├── scripts/
│   ├── generate_inbox_preview.py
│   ├── prumo_auto_sanitize.py
│   ├── prumo_google_dual_snapshot.sh
│   ├── prumo_sanitize_state.py
│   ├── github/
│   │   ├── bootstrap_labels.sh
│   │   ├── bootstrap_project.sh
│   │   └── sync_project_schema.sh
│   └── tests/
│       └── briefing_smoke.sh
└── test-output/
```

## O que ainda não está redondo

1. Distribuição de plugin depende do pacote de release (manifesto e empacotamento) no repositório de distribuição.
2. Integração dual-profile depende de infraestrutura local (shell + Gemini CLI + MCP autenticado).
3. Ainda faltam cenários automatizados de reconfiguração completa (`/prumo:setup`) com fixtures de workspace.

## Roadmap curto

1. Consolidar pacote de release para publicação sem ajuste manual.
2. Adicionar suíte de regressão para setup/reconfiguração com fixtures.
3. Evoluir métricas de qualidade de curadoria (taxa de `Responder` resolvido por ciclo).

## Referências rápidas

- Motor local: `../PRUMO-CORE.md`
- Estado operacional: `../_state/`
- Registro de auditoria: `../REGISTRO.md`
- Pauta ativa: `../PAUTA.md`

---

Se o sistema parar de parecer útil, o problema não é falta de lista. É falta de decisão com contexto. O README acima existe para evitar exatamente esse tipo de autoengano elegante.
