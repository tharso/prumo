# Autosanitização do Prumo

Objetivo: manter o runtime leve sem perder histórico e sem tocar arquivos pessoais.

## O que é

Autosanitização é uma rotina de manutenção preventiva acionada por gatilhos objetivos.
Ela pode rodar no começo do briefing (quando há shell) ou manualmente.
Os thresholds podem ser calibrados automaticamente por usuário (workspace), com base no histórico local.

Script principal:

- `scripts/prumo_auto_sanitize.py`

Histórico por usuário:

- `_state/auto-sanitize-history.json`

## Como roda

### Modo dry-run (recomendado para diagnóstico)

```bash
python3 Prumo/scripts/prumo_auto_sanitize.py --workspace .
```

### Modo apply (executa ações)

```bash
python3 Prumo/scripts/prumo_auto_sanitize.py --workspace . --apply
```

### Forçar execução (ignora cooldown)

```bash
python3 Prumo/scripts/prumo_auto_sanitize.py --workspace . --apply --force
```

### Desligar calibração adaptativa (modo fixo)

```bash
python3 Prumo/scripts/prumo_auto_sanitize.py --workspace . --adaptive off
```

## Gatilhos padrão

1. `HANDOVER.md` >= `120000` bytes **e** há handovers `CLOSED` acima do limite de retenção
2. `HANDOVER.md` >= `350` linhas **e** há handovers `CLOSED` acima do limite de retenção
3. `Inbox4Mobile/` com >= `8` arquivos
4. `Inbox4Mobile/` com >= `4` itens multimídia
5. `inbox-preview.html` ou `_preview-index.json` ausentes/desatualizados

## Calibração adaptativa por usuário

Quando `--adaptive auto` (default), o script usa o histórico do próprio workspace para ajustar:

1. `handover_max_bytes`
2. `handover_max_lines`
3. `handover_keep_closed`
4. `inbox_min_total`
5. `inbox_min_media`

Sem histórico suficiente, ele usa os valores base com segurança.

## Cooldown

- padrão: `6h`
- configurável via `--cooldown-hours`

Exemplo:

```bash
python3 Prumo/scripts/prumo_auto_sanitize.py --workspace . --apply --cooldown-hours 4
```

## O que pode ser executado automaticamente

1. Sanitização de handover:
   - roda `scripts/prumo_sanitize_state.py --apply`
   - compacta handovers fechados antigos
   - gera/atualiza `_state/HANDOVER.summary.md`
2. Refresh do inbox preview:
   - roda `scripts/generate_inbox_preview.py`
   - regenera `Inbox4Mobile/inbox-preview.html`
   - regenera `Inbox4Mobile/_preview-index.json`

## Estado e auditoria

Arquivo de estado:

- `_state/auto-sanitize-state.json`

Campos principais:

1. `last_run_at`
2. `last_apply_at`
3. `metrics`
4. `thresholds`
5. `decision`
6. `actions`
7. `adaptive` (status, amostra, ajustes recomendados)

Esse arquivo permite depurar por que a autosanitização rodou (ou não rodou).

## Guardrails

Autosanitização **não pode** alterar:

1. `CLAUDE.md`
2. `PAUTA.md`
3. `INBOX.md`
4. `REGISTRO.md`
5. `IDEIAS.md`

Em handover, histórico é movido para archive; não é descartado.

## Integração com briefing

No fluxo atual, a skill de briefing pode chamar autosanitização em modo best-effort.
Se falhar, o briefing segue normalmente com aviso curto de manutenção.

## Ajuste fino recomendado

Comece com defaults por 1 semana e observe `auto-sanitize-state.json`.
Depois ajuste thresholds conforme seu volume real.
