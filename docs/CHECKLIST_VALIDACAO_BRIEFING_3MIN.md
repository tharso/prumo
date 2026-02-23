# Checklist 3 Min - Validacao Cowork (Briefing v3.8.0)

Objetivo: validar rapidamente se o briefing progressivo esta funcionando em runtime real (Cowork), sem virar sessao de QA infinita.

## Preparacao (30s)

1. Confirmar que o core lido pelo agente esta em `3.8.0`.
2. Em `PAUTA.md`, garantir pelo menos dois itens em `Agendado` com semantica de cobranca:
   - um item com `| cobrar:` hoje;
   - um item com `| cobrar:` futuro.
3. Garantir que exista `Inbox4Mobile/_preview-index.json` (ou gerar preview antes).

Exemplo minimo em `Agendado`:

```md
- **25/02 (Qua)**: [Pai] Configurar Qustodio (...) | cobrar: 25/02
- **30/03 (Seg) 9h**: [Saúde] Eletroneuromiografia (...) | cobrar: 28/03
```

## Roteiro de validacao (2 min)

### Passo A - Bloco 1 (panorama automatico)

1. Rodar `/prumo:briefing`.
2. Verificar que o agente mostra:
   - agenda do dia,
   - link de `inbox-preview.html`,
   - contagem silenciosa de agendados.
3. Verificar que NAO despeja lista completa nem pede decisao item por item no comeco.

Resultado esperado: panorama curto e informativo, sem pressao.

### Passo B - Bloco 2 (interacao unica)

1. No mesmo briefing, verificar proposta do dia com opcoes:
   - `a) Aceitar e seguir`
   - `b) Ajustar`
   - `c) Ver lista completa`
   - `d) Tá bom por hoje`
2. Confirmar que existe uma unica interacao de decisao nesse ponto.

Resultado esperado: proposta objetiva com `a/b/c/d`.

### Passo C - Supressao temporal

1. No bloco de proposta (sem abrir detalhe), confirmar:
   - item com `cobrar` futuro NAO aparece como cobranca do dia;
   - item elegivel hoje aparece.
2. Confirmar que os suprimidos entram apenas na contagem silenciosa.

Resultado esperado: sem cobranca prematura de item futuro.

### Passo D - Escape hatch + retomada

1. Responder `d` (ou dizer "ta bom por hoje").
2. Verificar `_state/briefing-state.json` com:
   - `interrupted_at` preenchido;
   - `resume_point` preenchido.
3. Rodar `/prumo:briefing` novamente no mesmo dia.
4. Confirmar pergunta de retomada:
   - `a) retomar`
   - `b) recomecar`

Resultado esperado: briefing encerra sem cobranca e retoma corretamente no mesmo dia.

### Passo E - Contexto sob demanda

1. Na retomada, escolher `c` (ver lista completa) ou rodar `/prumo:briefing --detalhe`.
2. Confirmar que o detalhe abre sem quebrar o fluxo.

Resultado esperado: detalhe aparece so quando pedido.

## Criterio de aprovacao (30s)

Aprovado se TODOS passarem:

1. Bloco 1 automatico sem triagem forcada.
2. Bloco 2 com `a/b/c/d` em interacao unica.
3. Supressao temporal respeitada (`cobrar` futuro fora da proposta).
4. Escape grava estado e retomada funciona no mesmo dia.
5. Detalhe abre somente sob demanda.

Se falhar, registrar:

1. passo que falhou,
2. output exato do agente,
3. arquivo/estado impactado,
4. sugestao objetiva de ajuste.
