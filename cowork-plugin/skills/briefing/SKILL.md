---
name: briefing
description: >
  Morning briefing do Prumo. Executa a rotina completa: lê configuração pessoal,
  verifica pauta, processa inbox (todos os canais), checa calendário e emails,
  e apresenta o briefing do dia. Use com /prumo:briefing (alias legado: /briefing) ou quando o usuário disser
  "bom dia", "briefing", "começar o dia".
---

# Briefing do Prumo

Você está executando o morning briefing do sistema Prumo.

O procedimento detalhado deixou de viver aqui. Agora a autoridade é modular, porque duplicar fluxo em `SKILL.md`, core e referência era uma maneira sofisticada de cultivar desobediência.

## Carregamento obrigatório

1. Leia `CLAUDE.md`.
2. Leia `PRUMO-CORE.md`.
3. Leia o módulo canônico:
   - `Prumo/cowork-plugin/skills/prumo/references/modules/briefing-procedure.md`
4. Quando disponível, leia também:
   - `Prumo/cowork-plugin/skills/prumo/references/modules/load-policy.md`
   - `Prumo/cowork-plugin/skills/prumo/references/modules/version-update.md`

Se o workspace não tiver o repo `Prumo/`, use a referência equivalente do bundle instalado. Não improvise um terceiro procedimento.

## Fonte de autoridade

Em caso de conflito:

1. `ASSERT:` do `PRUMO-CORE.md`
2. módulo canônico
3. resumo deste `SKILL.md`

## Módulos usados pelo briefing

- briefing detalhado:
  - `Prumo/cowork-plugin/skills/prumo/references/modules/briefing-procedure.md`
- inbox e preview:
  - `Prumo/cowork-plugin/skills/prumo/references/modules/inbox-processing.md`
- update seguro:
  - `Prumo/cowork-plugin/skills/prumo/references/modules/version-update.md`
- multiagente:
  - `Prumo/cowork-plugin/skills/prumo/references/modules/multiagent.md`

## Guardrails que não podem ser pulados

- Antes de Gmail MCP ou Calendar MCP, tentar snapshots no Google Drive.
- Se existir `_preview-index.json`, linkar `inbox-preview.html` antes de abrir bruto.
- Persistir `last_briefing_at` antes da primeira resposta.
- `interrupted_at` e `resume_point` só existem se o usuário acionou escape hatch.
- Update sem transporte seguro de aplicação não bloqueia briefing.

## Resultado esperado

O briefing continua entregando:

- `Bloco 1` de panorama;
- `Bloco 2` de proposta do dia;
- contexto completo apenas em `c` ou `/prumo:briefing --detalhe`;
- curadoria de email em `Responder`, `Ver`, `Sem ação`;
- prioridade `P1/P2/P3`;
- snapshots do Google Drive como fonte primária quando houver Google Docs `Prumo/snapshots/email-snapshot`;
- fallback com shell via script dual quando necessário;
- fallback sem shell com a mesma taxonomia.

## Observação

Se o runtime tentar “economizar leitura” e pular o módulo canônico, ele vai repetir o mesmo erro que motivou essa refatoração. A economia aí é de palito de fósforo.
```

**Expiração de estado interrompido:**

No início de novo dia, se `interrupted_at` for de dia anterior, limpar `interrupted_at` e `resume_point` silenciosamente (sem cobrar briefing antigo).

**Validação pós-escrita:**

Após cada escrita, ler `_state/briefing-state.json` e validar de forma condicional:

- briefing iniciado/concluído: confirmar que `last_briefing_at` contém a data do dia local atual e que `interrupted_at`/`resume_point` não existem;
- briefing interrompido: confirmar que `interrupted_at` contém a data do dia local atual, que `resume_point` foi gravado, e que `last_briefing_at` continua apontando para o início da sessão atual.

Se a validação correspondente falhar, repetir a escrita correta para esse caso.

---

**Tom:** Seguir rigorosamente o tom definido no CLAUDE.md do usuário. Se for "direto", cobrar sem cerimônia. Se for "gentil", lembrar sem pressionar.

**Links:** Sempre usar `[Descrição](computer:///caminho)` ao referenciar arquivos. Nunca expor caminhos crus.
