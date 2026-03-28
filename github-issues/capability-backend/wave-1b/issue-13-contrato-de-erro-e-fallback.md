# Definir contrato de erro, fallback e graceful degradation para hosts

**Tipo**: Architecture / Resilience  
**Labels sugeridas**: `architecture`, `resilience`, `errors`, `hosts`

## Contexto

Toda arquitetura parece elegante ate o primeiro erro real. Sem contrato de fallback, o primeiro stack trace vira o mordomo revelando o backstage no jantar.

## Objetivo

Impedir que jargao tecnico, stack trace e estados quebrados vazem para o usuario quando capacidades falham.

## Escopo

1. tipos de erro relevantes
2. degradacao aceitavel por fluxo
3. comportamento esperado do host diante de falha parcial
4. quando registrar em `_state/`
5. quando escalar para repair
6. como comunicar falha sem quebrar a UX

## Entregaveis

1. contrato de erro e fallback
2. exemplos para briefing, invocacao e documentacao
3. limites de retries e de silencios aceitaveis

## Criterio de aceite

1. cada host sabe tropeçar sem cair em cima do usuario

## Dependencias

1. [issue-11-contrato-de-orquestracao.md](/Users/tharsovieira/Documents/DailyLife/Prumo/github-issues/capability-backend/wave-1b/issue-11-contrato-de-orquestracao.md)
