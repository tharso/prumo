**Tipo**: Refactor  
**Labels sugeridas**: `refactor`, `runtime`, `templates`, `canon`

## Contexto

Extrair o canon sem depois religar runtime e templates a essa nova casa seria trocar o nome do armario e deixar as roupas no chao.

## Objetivo

Alinhar runtime, templates e wrappers com a nova area canonica compartilhada.

## Escopo

1. `runtime/prumo_runtime/templates.py`
2. `runtime/prumo_runtime/workspace.py`
3. `runtime/prumo_runtime/commands/start.py`
4. `runtime/prumo_runtime/commands/briefing.py`
5. wrappers e templates de host
6. docs de topo que hoje repetem regra ja extraida

## Entregaveis

1. mapa de referencias que devem deixar de ser locais/duplicadas
2. lista de patches necessarios
3. criterio de derivacao para wrappers e `adapter_hints`

## Criterio de aceite

1. runtime e templates passam a apontar para a casa canonica
2. docs de topo deixam de repetir regra que ja foi consolidada

## Dependencias

1. `#55`
2. `#56`
3. `#57`
4. `#58`
5. `#59`
