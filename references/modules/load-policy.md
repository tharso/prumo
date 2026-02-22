# Load Policy (Prumo)

Objetivo: reduzir overhead de contexto sem perder capacidade operacional.

## Princípios

1. Ler primeiro o mínimo necessário para decidir.
2. Abrir conteúdo pesado (PDF/imagem longa/transcrição extensa) apenas quando houver necessidade objetiva de ação.
3. Preferir resumo incremental (índices e arquivos `.summary`) quando disponíveis.

## Matriz de leitura por comando

- `/prumo:briefing`
  - obrigatório: `CLAUDE.md`, `PRUMO-CORE.md`, `PAUTA.md`, `INBOX.md`
  - preferencial leve: `_state/HANDOVER.summary.md` (se existir)
  - estado operacional: `_state/auto-sanitize-state.json` (se existir)
  - detalhado sob demanda: `_state/HANDOVER.md`, arquivos de `Inbox4Mobile/`
  - módulo específico: `Prumo/references/modules/briefing-fast-path.md`

- `/prumo:handover`
  - obrigatório: `_state/HANDOVER.md`
  - módulo específico: `Prumo/skills/handover/SKILL.md`

- `/prumo:sanitize`
  - obrigatório: `_state/HANDOVER.md`
  - módulo específico: `Prumo/references/modules/sanitization.md`

## Heurística de aprofundamento

Abrir arquivo bruto imediatamente se qualquer condição for verdadeira:

1. risco legal/financeiro/documental,
2. vencimento em até 72h,
3. item classificado como `P1`,
4. ambiguidade que impede ação segura.

Se nenhuma condição ocorrer, manter no nível de triagem leve e pedir decisão do usuário.
