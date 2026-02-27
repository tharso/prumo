# Briefing Fast Path

Fluxo recomendado para `Inbox4Mobile/` durante `/prumo:briefing`.

## Pré-passo opcional (manutenção)

Quando houver shell, rodar antes da triagem:

- `if [ -f scripts/prumo_auto_sanitize.py ]; then python3 scripts/prumo_auto_sanitize.py --workspace . --apply; elif [ -f Prumo/cowork-plugin/scripts/prumo_auto_sanitize.py ]; then python3 Prumo/cowork-plugin/scripts/prumo_auto_sanitize.py --workspace . --apply; else python3 Prumo/scripts/prumo_auto_sanitize.py --workspace . --apply; fi`

## Estágio A — Triagem leve (obrigatório)

1. Gerar preview local:
   - `if [ -f scripts/generate_inbox_preview.py ]; then python3 scripts/generate_inbox_preview.py --output Inbox4Mobile/inbox-preview.html --index-output Inbox4Mobile/_preview-index.json; elif [ -f Prumo/cowork-plugin/scripts/generate_inbox_preview.py ]; then python3 Prumo/cowork-plugin/scripts/generate_inbox_preview.py --output Inbox4Mobile/inbox-preview.html --index-output Inbox4Mobile/_preview-index.json; else python3 Prumo/scripts/generate_inbox_preview.py --output Inbox4Mobile/inbox-preview.html --index-output Inbox4Mobile/_preview-index.json; fi`
2. Ler o índice leve: `Inbox4Mobile/_preview-index.json`.
3. Classificar cada item em:
   - ação (`Responder`, `Ver`, `Sem ação`)
   - prioridade (`P1`, `P2`, `P3`)
   - motivo objetivo.

## Estágio B — Aprofundamento seletivo (condicional)

Abrir conteúdo bruto completo (imagem/PDF/arquivo longo) apenas para:

1. itens `P1`,
2. itens ambíguos sem próxima ação segura,
3. itens com risco legal/financeiro/documental,
4. itens explicitamente solicitados pelo usuário.

## Saída esperada

1. Lista curta de ações com prioridade.
2. Link para preview local (`Inbox4Mobile/inbox-preview.html`) quando houver multimídia.
3. Registro explícito de quais itens foram aprofundados e quais ficaram só em triagem leve.
