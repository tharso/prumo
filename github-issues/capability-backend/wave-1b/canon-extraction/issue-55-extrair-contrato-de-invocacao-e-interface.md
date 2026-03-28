**Tipo**: Refactor / Architecture  
**Labels sugeridas**: `architecture`, `canon`, `ux`, `invocation`

## Contexto

Invocacao e disciplina de interface hoje vivem espalhadas entre contrato, plugin, runtime, wrappers e README. E o tipo de duplicacao que parece governanca ate a hora em que um host le a versao errada e inventa outra terceira.

## Objetivo

Extrair para a area canonica compartilhada o contrato de invocacao e o contrato de interface do Prumo.

## Escopo

1. porta curta
2. briefing explicito
3. entrypoints estruturados
4. alternativas curtas e respondiveis
5. numeracao continua
6. preservacao de fluxo

## Fontes iniciais

1. `INVOCATION-UX-CONTRACT.md`
2. `cowork-plugin/skills/prumo/references/modules/interaction-format.md`
3. `runtime/prumo_runtime/commands/start.py`
4. `runtime/prumo_runtime/templates.py`

## Entregaveis

1. `canon/contracts/invocation.md`
2. `canon/contracts/interaction-format.md`
3. lista de pontos que devem passar a ser derivados nos wrappers e no runtime

## Criterio de aceite

1. ha uma fonte unica para invocacao
2. ha uma fonte unica para disciplina conversacional basica
3. wrappers e runtime deixam de ser cartorios concorrentes

## Dependencias

1. `#49`
2. `#50`
