# Sanitization

> **module_version: 4.3.1**
>
> Fonte canônica de sanitização manual e automática do estado operacional.

## Sanitização manual

Quando houver shell, usar `prumo_sanitize_state.py` resolvendo os caminhos pela ordem definida em `runtime-paths.md`.

O processo deve:

1. compactar handovers `CLOSED` antigos;
2. mover histórico para `_state/archive/HANDOVER-ARCHIVE.md`;
3. regenerar `_state/HANDOVER.summary.md`;
4. nunca tocar arquivos pessoais.

## Autosanitização

Pode rodar no briefing como manutenção preventiva, não como ritual destrutivo.

Regras:

1. respeitar cooldown;
2. registrar estado em `_state/auto-sanitize-state.json`;
3. usar `_state/auto-sanitize-history.json` para calibrar thresholds quando houver amostra;
4. sem histórico suficiente, usar defaults seguros;
5. nunca apagar histórico sem archive.
