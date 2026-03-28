**Tipo**: Cleanup / Architecture  
**Labels sugeridas**: `architecture`, `adapter`, `cleanup`, `canon`

## Contexto

Parte do que hoje parece canon e, na verdade, workaround de Cowork vestido de regra eterna. Enquanto isso ficar embaralhado, toda extracao vira cirurgia com alicate.

## Objetivo

Separar explicitamente o que e adapter-specific do que e canon compartilhado.

## Escopo

1. bridge do Cowork
2. manutencao especifica do Cowork
3. runtime paths e detalhes de shell historicos
4. notes e playbooks de host
5. update/preflight: separar comportamento de produto de mecanismo de transporte

## Fontes iniciais

1. `cowork-plugin/skills/prumo/references/modules/cowork-runtime-bridge.md`
2. `cowork-plugin/skills/prumo/references/modules/cowork-runtime-maintenance.md`
3. `cowork-plugin/skills/prumo/references/modules/runtime-paths.md`
4. `cowork-plugin/skills/prumo/references/modules/version-update.md`
5. `ANTIGRAVITY-ADAPTER-PLAYBOOK.md`

## Entregaveis

1. lista clara do que fica no legado/adapters
2. lista do que sobe para `canon/`
3. lista do que deve ser rebaixado a doc operacional

## Criterio de aceite

1. fica claro o que e regra de produto e o que e gambiarra honesta de distribuicao

## Dependencias

1. `#49`
2. `#50`
