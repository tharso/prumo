**Tipo**: Refactor / Architecture  
**Labels sugeridas**: `architecture`, `canon`, `memory`, `governance`

## Contexto

Governanca de arquivo e politica de leitura estao hoje com a maior parte do miolo no plugin, um pouco nos templates e outro pouco em docs de apoio. Casa de regra assim fica parecendo cidade sem CEP.

## Objetivo

Extrair a governanca documental e a load policy para a area canonica compartilhada.

## Escopo

1. jurisdicao entre contexto estavel, pauta, inbox e registro
2. sinais de drift
3. limites de automacao e confirmacao
4. leitura base, leve e profunda
5. heuristicas de aprofundamento
6. higiene estrutural com delegacao otimista onde couber

## Fontes iniciais

1. `cowork-plugin/skills/prumo/references/modules/runtime-file-governance.md`
2. `cowork-plugin/skills/prumo/references/modules/load-policy.md`
3. `cowork-plugin/skills/prumo/references/modules/claude-hygiene.md`
4. `runtime/prumo_runtime/templates.py`
5. `runtime/prumo_runtime/workspace.py`

## Entregaveis

1. `canon/governance/file-governance.md`
2. `canon/governance/load-policy.md`
3. `canon/governance/memory-hygiene.md`

## Criterio de aceite

1. o plugin deixa de ser a casa principal da jurisdicao documental
2. o runtime passa a consumir uma regra compartilhada em vez de semear estrutura em varios lugares

## Dependencias

1. `#49`
2. `#50`
