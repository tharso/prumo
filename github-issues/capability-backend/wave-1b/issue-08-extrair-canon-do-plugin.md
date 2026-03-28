# Extrair modulos canonicos do produto a partir do legado do plugin com inventario de sabedoria operacional

**Tipo**: Refactor / Architecture  
**Labels sugeridas**: `refactor`, `architecture`, `canon`, `plugin`

## Contexto

O plugin guarda mais do que codigo antigo. Guarda ritmo, thresholds, leis pequenas e feias que impedem o produto de virar uma reparticao com autocomplete. Se a extracao for generica, a inteligencia evapora e sobra o esqueleto.

## Objetivo

Mover para uma area canonica compartilhada os modulos que hoje vivem enterrados em `cowork-plugin`, com inventario explicito da sabedoria operacional herdada.

## Escopo inicial

1. invocacao
2. briefing
3. persistencia
4. governanca documental
5. workflows
6. higiene / limpeza
7. disciplina conversacional herdada do plugin
8. heuristicas temporais e thresholds relevantes

## Entregaveis

1. parent issue com decomposicao em sub-issues, se necessario
2. inventario dos modulos canonicos herdados
3. primeira proposta de area canonica compartilhada

## Criterio de aceite

1. o repositorio passa a ter uma casa clara para a inteligencia do produto
2. o plugin deixa de ser o porao onde mora a sabedoria por acidente

## Dependencias

1. [issue-05-destino-do-cowork-plugin.md](/Users/tharsovieira/Documents/DailyLife/Prumo/github-issues/capability-backend/wave-1a/issue-05-destino-do-cowork-plugin.md)
2. [issue-06-auditoria-do-estado-atual.md](/Users/tharsovieira/Documents/DailyLife/Prumo/github-issues/capability-backend/wave-1a/issue-06-auditoria-do-estado-atual.md)
3. [issue-07-duplicacoes-de-regra.md](/Users/tharsovieira/Documents/DailyLife/Prumo/github-issues/capability-backend/wave-1b/issue-07-duplicacoes-de-regra.md)
