# Relatório de Validação: Consumo Estruturado por Host

**Data:** 2026-03-28  
**Host:** Claude Code (Opus 4.6)  
**Adapter:** Claude Code Adapter (implícito, sem adapter separado)  
**Runtime:** prumo v4.16.6  
**Protocolo de referência:** `HOST-CONSUMPTION-VALIDATION.md`  
**Workspace:** `/Users/tharsovieira/Documents/DailyLife`

---

## 1. Contexto de execução

O workspace precisou de `prumo migrate` antes do `start`, porque não tinha identidade canônica do runtime. Isso é esperado para workspaces legados. Após migrate, `prumo start --format json` retornou payload estruturado completo.

**Pré-requisito atendido:** workspace foi adotado sem perda de dados (backup em `_backup/runtime-migrate/20260328-192805`).

---

## 2. Cenário identificado

**Cenário 2: Início do dia sem briefing.**

Evidências do payload:

| Campo | Valor | Alinhamento com cenário |
|-------|-------|------------------------|
| `state_flags.has_briefed_today` | `false` | Confirma: sem briefing hoje |
| `next_move.id` | `"briefing"` | Correto para cenário 2 |
| `next_move.recommended` | `true` | Runtime recomenda briefing |
| `next_move.priority` | `90` | Maior prioridade entre ações |
| `degradation.status` | `"ok"` | Sem degradação, descarta cenários 1 e 4 |
| `state_flags.has_continue_item` | `true` | Há frente quente, mas briefing tem precedência |

---

## 3. Validação: ordem de leitura do payload

O protocolo exige esta ordem de consumo:

| # | Campo esperado | Lido pelo host? | Posição na resposta | Veredicto |
|---|----------------|-----------------|---------------------|-----------|
| 1 | `degradation` | Sim | 1o item citado | PASS |
| 2 | `next_move` | Sim | 2o item citado | PASS |
| 3 | `selection_contract` | Sim | 3o item citado | PASS |
| 4 | `state_flags` | Sim | 4o item citado | PASS |
| 5 | `actions[]` | Sim | 5o item citado | PASS |
| 6 | `google_status` / `apple_reminders_status` | Sim | 6o item citado | PASS |
| 7 | `message` / `sections` | Não citado na resposta | Correto: não usado para decisão | PASS |

**Veredicto da ordem:** PASS. A resposta seguiu a ordem canônica e não inverteu prosa antes de payload operacional.

---

## 4. Validação: critérios do cenário 2

| Critério | Esperado | Observado | Veredicto |
|----------|----------|-----------|-----------|
| `next_move.id = briefing` | Sim | `"briefing"` | PASS |
| `selection_contract` claro | Aceite curto executa briefing | Tokens `1`, `a`, `ok` -> executa direto | PASS |
| Host não abre menu novo antes de oferecer next_move | Sem menu, foi direto à oferta | Resposta terminou com "Rodo?" sem menu intermediário | PASS |

---

## 5. Validação: sinais de consumo ruim

| Sinal de consumo ruim | Ocorreu? | Veredicto |
|------------------------|----------|-----------|
| 1. Leu `message` antes do payload operacional | Não | PASS |
| 2. Rerodou `start` depois de aceite curto | N/A (não houve aceite curto neste turno) | N/A |
| 3. Ignorou `degradation` | Não, foi o 1o campo citado | PASS |
| 4. Concatenou liturgia com prosa do runtime | Não, resposta enxuta, sem duplicar `message` | PASS |
| 5. Executou comando extra por ansiedade | Não, apenas apresentou o payload e ofereceu ação | PASS |
| 6. Usou `google_status`/`apple_reminders_status` para decisão de fluxo | Não, tratou como estado operacional informativo | PASS |

---

## 6. Validação: resultado mínimo aceitável

| Critério | Atendido? | Evidência |
|----------|-----------|-----------|
| Usa `next_move` de forma disciplinada | Sim | Citou briefing como próximo movimento, não inventou alternativas | PASS |
| Trata `selection_contract` como regra | Sim | Mencionou que aceite curto executa direto | PASS |
| Responde à degradação sem melodrama nem negação | Sim | `ok` -> seguiu em frente sem drama | PASS |
| Não exige parsing textual | Sim | Decisão veio de campos estruturados | PASS |
| Não introduz passos extras | Sim | Nenhum tool-call extra, nenhum menu inventado | PASS |

---

## 7. Regra de bolso

> Se a revisão do host precisar citar o `message` antes de citar `degradation`, `next_move` ou `selection_contract`, provavelmente o adapter ainda está dirigindo olhando pelo retrovisor.

**Resultado:** O host citou `degradation` primeiro, `next_move` segundo, `selection_contract` terceiro. `message` não foi citado em nenhum momento da resposta operacional.

**Veredicto:** PASS.

---

## 8. Observações adicionais

### 8.1 Migrate como pré-requisito

O runtime detectou workspace legado e exigiu `migrate` antes de aceitar `start`. O host respondeu a isso de forma correta: rodou `migrate` com os parâmetros certos sem inventar fluxo alternativo. Isso expôs um pré-cenário real de campo.

### 8.2 Integrações desconectadas

Google e Apple Reminders estavam ambos `disconnected`. O host tratou isso corretamente como estado operacional e não elevou a drama central. A ação `auth-google` apareceu na lista de `actions[]` com prioridade 50, abaixo de briefing (90), continue (80) e process-inbox (70).

### 8.3 Frente quente disponível mas não priorizada

`state_flags.has_continue_item = true` e `actions[1]` continham a frente quente. O runtime decidiu corretamente que briefing tem precedência sobre continuação quando `has_briefed_today = false`. O host respeitou essa decisão sem tentar inverter.

### 8.4 Payload `message`

O campo `message` contém texto bem estruturado com menu (`a/b/c/d`), mas o host não o usou para decisão nem o reproduziu. Isso está alinhado com o protocolo: `message` serve apenas para acabamento humano.

---

## 9. Resumo

| Dimensão | Resultado |
|----------|-----------|
| Ordem de leitura | PASS |
| Cenário correto identificado | PASS (Cenário 2) |
| Critérios do cenário | 3/3 PASS |
| Sinais de consumo ruim | 0/6 detectados |
| Resultado mínimo aceitável | 5/5 PASS |
| Regra de bolso | PASS |

**Resultado geral: PASS.**

O host consumiu o contrato estruturado como contrato. Não pescou prosa, não inventou menu, não dramatizou estado operacional e ofereceu execução do `next_move` sem cerimônia.

---

*Relatório gerado em 2026-03-28 contra `HOST-CONSUMPTION-VALIDATION.md` (commit `e472b4f`).*
