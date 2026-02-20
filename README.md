# Prumo

Sistema de organizacao pessoal orientado a acao. O foco do Prumo nao e listar pendencia; e transformar entrada difusa em decisao clara.

Estado deste documento: **19/02/2026**.

## Estado atual

- Core local: `prumo_version 3.6` (`PRUMO-CORE.md`).
- Skill principal de setup: `v3.4` (`SKILL.md`).
- Skill de briefing: `v2.2` (com curadoria por acao em runtime com e sem shell).
- Coexistencia multiagente Codex/Cowork ativa e validada.
- Handovers `HO-2026-02-19-001` ate `HO-2026-02-19-005`: **CLOSED** em `_state/HANDOVER.md`.

## O que o sistema entrega hoje

1. Setup guiado para gerar estrutura de operacao (arquivos, areas, rituais, tom).
2. Briefing diario com consolidacao de agenda e triagem de email por prioridade.
3. Processamento de inbox multi-canal (`INBOX.md`, `Inbox4Mobile/`, email quando disponivel).
4. Revisao semanal com higienizacao de pauta e historico.
5. Protocolo de coexistencia entre agentes (lock por escopo + handover rastreavel).

## Arquitetura

O sistema opera em tres arquivos principais:

- `CLAUDE.md`: configuracao pessoal (identidade, areas, tom, lembretes, integracoes).
- `PRUMO-CORE.md`: regras operacionais do sistema (rituais, fluxo, governanca).
- `AGENTS.md`: adaptador para runtimes que nao usam `CLAUDE.md` nativamente.

Arquivos de estado e operacao:

- `_state/agent-lock.json`: lock cooperativo por escopo entre agentes.
- `_state/HANDOVER.md`: validacoes cruzadas e status de handovers.
- `_state/briefing-state.json`: referencia temporal de briefing (`last_briefing_at`).

## Comandos ativos

- `/prumo:setup`
- `/prumo:briefing` (canonico)
- `/briefing` (alias legado)
- `/prumo:inbox`
- `/prumo:dump`
- `/prumo:revisao`
- `/prumo:status`
- `/prumo:handover`
- `/prumo:menu`

## Briefing: logica atual

### Canais lidos

- `Inbox4Mobile/` (incluindo imagens)
- Gmail (quando disponivel)
- Google Calendar (hoje e amanha)
- `_state/HANDOVER.md` (pendencias de validacao)

### Curadoria de email (modelo unico)

A triagem usa tres buckets:

- `Responder`: exige resposta ativa.
- `Ver`: exige leitura/checagem, sem resposta imediata.
- `Sem acao`: baixo valor imediato.

Cada item deve vir com:

- prioridade (`P1`, `P2`, `P3`)
- motivo objetivo

### Janela temporal

- Se `_state/briefing-state.json` tiver `last_briefing_at`, essa e a ancora.
- Se nao tiver, fallback de 24h.
- Ao concluir o briefing, atualizar `last_briefing_at`.

### Runtime com shell (modo avancado)

Quando disponivel, pode usar script dual-profile:

- `scripts/prumo_google_dual_snapshot.sh`

Template do script no produto:

- `references/prumo-google-dual-snapshot.sh`

Esse modo permite consolidar duas contas (ex.: pessoal/trabalho) no mesmo briefing.

### Runtime sem shell (paridade obrigatoria)

Sem shell/Gemini CLI, o briefing **mantem a mesma taxonomia de curadoria** via integracoes nativas. O objetivo e evitar degradacao de qualidade por limitacao de runtime.

## Coexistencia Codex x Cowork

Protocolo vigente:

1. lock de escopo em `_state/agent-lock.json` antes de alteracoes criticas.
2. handover em `_state/HANDOVER.md` para mudancas relevantes.
3. briefing checa `PENDING_VALIDATION` e `REJECTED` automaticamente.

Status de validacao recente:

- Base de coexistencia: aprovada.
- Checagem automatica de handover no briefing: aprovada.
- Comando manual `/prumo:handover`: aprovado.
- Integracao de curadoria Google dual: aprovada (com nota de limite de runtime Cowork).
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

## O que ainda nao esta redondo

1. Distribuicao de plugin depende do pacote de release (manifesto e empacotamento) no repositorio de distribuicao.
2. Integracao dual-profile depende de infraestrutura local (shell + Gemini CLI + MCP autenticado).
3. Ainda faltam testes de regressao automatizados para cenarios de briefing e reconfiguracao.

## Roadmap curto

1. Consolidar pacote de release para publicacao sem ajuste manual.
2. Adicionar testes de smoke para briefing (com e sem shell).
3. Evoluir metricas de qualidade de curadoria (taxa de `Responder` resolvido por ciclo).

## Referencias rapidas

- Motor local: `../PRUMO-CORE.md`
- Estado operacional: `../_state/`
- Registro de auditoria: `../REGISTRO.md`
- Pauta ativa: `../PAUTA.md`

---

Se o sistema parar de parecer util, o problema nao e falta de lista. E falta de decisao com contexto. O README acima existe para evitar exatamente esse tipo de autoengano elegante.
