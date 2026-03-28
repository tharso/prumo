**Tipo**: Refactor / Architecture  
**Labels sugeridas**: `architecture`, `canon`, `inbox`

## Contexto

Inbox processing ja funciona como modulo de produto, mas ainda mora dentro do plugin. O runtime ja toca partes disso, so que sem uma casa compartilhada a taxonomia corre o risco de derreter em variacao de implementacao.

## Objetivo

Extrair o procedimento de inbox processing para a area canonica compartilhada.

## Escopo

1. preview
2. `Responder`, `Ver`, `Sem acao`
3. `P1/P2/P3`
4. commit, delecao e `_processed.json`
5. relacao com briefing e preview mobile

## Fontes iniciais

1. `cowork-plugin/skills/prumo/references/modules/inbox-processing.md`
2. `cowork-plugin/skills/prumo/references/modules/briefing-procedure.md`
3. `runtime/prumo_runtime/commands/briefing.py`

## Entregaveis

1. `canon/operations/inbox-processing.md`
2. lista de pontos de runtime que passam a obedecer esse canon

## Criterio de aceite

1. a taxonomia de inbox deixa de depender do plugin
2. o runtime nao precisa mais carregar regra paralela sem sobrenome

## Dependencias

1. `#49`
2. `#50`
3. `#57`
