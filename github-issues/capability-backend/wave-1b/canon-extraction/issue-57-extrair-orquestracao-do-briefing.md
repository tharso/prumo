**Tipo**: Refactor / Architecture  
**Labels sugeridas**: `architecture`, `canon`, `briefing`, `orchestration`

## Contexto

O briefing ainda guarda a maior concentracao de sabedoria operacional do produto. Se a extracao for mal feita, sobra um runtime que coleta dados e um host que tenta fazer stand-up improvisado.

## Objetivo

Extrair o procedimento compartilhado de orquestracao do briefing para a area canonica.

## Escopo

1. pre-carga e load policy
2. preflight de versao
3. estado operacional e janela temporal
4. canais de entrada
5. persistencia de `last_briefing_at`
6. panorama
7. proposta
8. detalhe sob demanda
9. escape hatch
10. escrita e fechamento

## Fontes iniciais

1. `cowork-plugin/skills/prumo/references/modules/briefing-procedure.md`
2. `cowork-plugin/skills/prumo/references/prumo-core.md`
3. `runtime/prumo_runtime/commands/briefing.py`

## Entregaveis

1. `canon/orchestration/briefing.md`
2. lista de guardrails do briefing que deixam de morar em `prumo-core.md`
3. mapeamento do que permanece adapter-specific

## Criterio de aceite

1. existe um procedimento compartilhado de briefing fora do plugin
2. o runtime e os adapters podem obedecer a mesma partitura

## Dependencias

1. `#49`
2. `#50`
3. `#51`
4. `#56` (ou equivalente)
