# Plano de Extracao do Canon

Data: 2026-03-28

Este documento continua a auditoria e a matriz de duplicacoes. A pergunta aqui nao e mais "de onde tirar". E "para onde levar sem criar outro cemiterio elegante".

## Decisao de estrutura

A inteligencia compartilhada do produto nao deve morar:

1. dentro do `cowork-plugin/`, porque isso faz o legado parecer centro;
2. dentro de `runtime/prumo_runtime/`, porque isso faz o runtime parecer dono do produto;
3. em `README.md`, porque manifesto nao e cartorio;
4. em wrappers, porque bilhete de elevador nao deve virar constituicao.

### Casa recomendada

Criar uma area nova, na raiz do repo:

```text
canon/
  README.md
  contracts/
  orchestration/
  governance/
  operations/
  adapters/
```

## O que vai em cada lugar

### `canon/contracts/`

Regras que valem em qualquer host ou runtime, sem depender de um app especifico.

Arquivos candidatos:

1. `invocation.md`
2. `interaction-format.md`
3. `selection-and-continuation.md`

Fontes iniciais:

1. [INVOCATION-UX-CONTRACT.md](/Users/tharsovieira/Documents/DailyLife/Prumo/INVOCATION-UX-CONTRACT.md)
2. [cowork-plugin/skills/prumo/references/modules/interaction-format.md](/Users/tharsovieira/Documents/DailyLife/Prumo/cowork-plugin/skills/prumo/references/modules/interaction-format.md)
3. `adapter_hints` de [runtime/prumo_runtime/commands/start.py](/Users/tharsovieira/Documents/DailyLife/Prumo/runtime/prumo_runtime/commands/start.py)

### `canon/orchestration/`

Fluxos do produto que combinam regra de sequencia, persistencia e criterio de parada.

Arquivos candidatos:

1. `briefing.md`
2. `start.md`
3. `weekly-review.md`

Fontes iniciais:

1. [cowork-plugin/skills/prumo/references/modules/briefing-procedure.md](/Users/tharsovieira/Documents/DailyLife/Prumo/cowork-plugin/skills/prumo/references/modules/briefing-procedure.md)
2. [cowork-plugin/skills/prumo/references/modules/weekly-review.md](/Users/tharsovieira/Documents/DailyLife/Prumo/cowork-plugin/skills/prumo/references/modules/weekly-review.md)
3. [runtime/prumo_runtime/commands/briefing.py](/Users/tharsovieira/Documents/DailyLife/Prumo/runtime/prumo_runtime/commands/briefing.py)
4. [runtime/prumo_runtime/commands/start.py](/Users/tharsovieira/Documents/DailyLife/Prumo/runtime/prumo_runtime/commands/start.py)

### `canon/governance/`

Regras de memoria viva, jurisdicao e higiene estrutural.

Arquivos candidatos:

1. `file-governance.md`
2. `load-policy.md`
3. `memory-hygiene.md`

Fontes iniciais:

1. [cowork-plugin/skills/prumo/references/modules/runtime-file-governance.md](/Users/tharsovieira/Documents/DailyLife/Prumo/cowork-plugin/skills/prumo/references/modules/runtime-file-governance.md)
2. [cowork-plugin/skills/prumo/references/modules/load-policy.md](/Users/tharsovieira/Documents/DailyLife/Prumo/cowork-plugin/skills/prumo/references/modules/load-policy.md)
3. [cowork-plugin/skills/prumo/references/modules/claude-hygiene.md](/Users/tharsovieira/Documents/DailyLife/Prumo/cowork-plugin/skills/prumo/references/modules/claude-hygiene.md)

### `canon/operations/`

Procedimentos concretos que ainda sao regra de produto, mas ja tangenciam capacidade.

Arquivos candidatos:

1. `inbox-processing.md`
2. `version-preflight.md`

Fontes iniciais:

1. [cowork-plugin/skills/prumo/references/modules/inbox-processing.md](/Users/tharsovieira/Documents/DailyLife/Prumo/cowork-plugin/skills/prumo/references/modules/inbox-processing.md)
2. [cowork-plugin/skills/prumo/references/modules/version-update.md](/Users/tharsovieira/Documents/DailyLife/Prumo/cowork-plugin/skills/prumo/references/modules/version-update.md)

Observacao:

`version-preflight.md` pode ficar no canon apenas na parte de comportamento de produto. Transporte seguro, shell path e bridge continuam fora disso.

### `canon/adapters/`

Aqui entra o que e conscientemente especifico de host, para parar de fingir universalidade.

Arquivos candidatos:

1. `cowork-bridge.md`
2. `cowork-maintenance.md`
3. `claude-wrapper-notes.md`
4. `antigravity-notes.md`

Fontes iniciais:

1. [cowork-plugin/skills/prumo/references/modules/cowork-runtime-bridge.md](/Users/tharsovieira/Documents/DailyLife/Prumo/cowork-plugin/skills/prumo/references/modules/cowork-runtime-bridge.md)
2. [cowork-plugin/skills/prumo/references/modules/cowork-runtime-maintenance.md](/Users/tharsovieira/Documents/DailyLife/Prumo/cowork-plugin/skills/prumo/references/modules/cowork-runtime-maintenance.md)
3. [ANTIGRAVITY-ADAPTER-PLAYBOOK.md](/Users/tharsovieira/Documents/DailyLife/Prumo/ANTIGRAVITY-ADAPTER-PLAYBOOK.md)

## Fatias de extracao

Nao vale tentar mover tudo de uma vez. Isso seria mudar a biblioteca de lugar carregando os livros nos bracos, sem caixa, na chuva.

### Fatia 1. Contratos de interface e invocacao

Escopo:

1. porta curta;
2. briefing explicito;
3. structured entrypoints;
4. numeração contínua;
5. alternativas curtas;
6. disciplina de "uma resposta que continua a outra".

Saidas:

1. `canon/contracts/invocation.md`
2. `canon/contracts/interaction-format.md`
3. wrappers passam a apontar para esses arquivos

### Fatia 2. Politica de leitura e governanca

Escopo:

1. `PAUTA.md` vs `REGISTRO.md` vs contexto estavel;
2. politica de leitura incremental;
3. limites de automacao vs confirmacao;
4. higienizacao geral com delegacao otimista onde fizer sentido.

Saidas:

1. `canon/governance/file-governance.md`
2. `canon/governance/load-policy.md`
3. `canon/governance/memory-hygiene.md`

### Fatia 3. Orquestracao do briefing

Escopo:

1. preflight de versao;
2. estado operacional;
3. canais de entrada;
4. persistencia de `last_briefing_at`;
5. panorama;
6. proposta;
7. detalhe sob demanda;
8. escape hatch;
9. escrita e fechamento.

Saidas:

1. `canon/orchestration/briefing.md`
2. runtime e adapters passam a obedecer o mesmo roteiro

### Fatia 4. Inbox e operacoes correlatas

Escopo:

1. preview;
2. taxonomia `Responder`, `Ver`, `Sem ação`;
3. `P1/P2/P3`;
4. commit, delecao e `_processed.json`.

Saidas:

1. `canon/operations/inbox-processing.md`
2. `runtime/prumo_runtime/commands/briefing.py` deixa de manter regra paralela

### Fatia 5. Adapter boundaries

Escopo:

1. bridge Cowork;
2. manutencao Cowork;
3. restricoes especificas de host;
4. playbooks de host que apontam para canon em vez de competir com ele.

Saidas:

1. `canon/adapters/*`
2. `cowork-plugin/` emagrece

## O que nao deve entrar no canon compartilhado

Para nao transformar canon em porao reformado com nome novo:

1. shell paths especificos;
2. comandos de transporte seguro de update;
3. detalhes de marketplace;
4. notas de validacao de host;
5. qualquer workaround que exista so por causa do Cowork;
6. detalhes de permissao do Antigravity, Claude Code ou app especifico.

## Proposta de decomposicao da issue 50

Issue 50 deve deixar de ser um saco de cimento unico e virar pelo menos estas fatias:

1. extrair contratos de invocacao e interface;
2. extrair governanca documental e load policy;
3. extrair orquestracao do briefing;
4. extrair inbox processing;
5. separar adapter-specific docs do canon compartilhado;
6. alinhar templates e runtime com a nova area canonica.

## Ordem recomendada

1. contratos de interface e invocacao;
2. governanca e load policy;
3. briefing;
4. inbox;
5. adapter boundaries;
6. alinhamento de runtime/templates.

Se a ordem for invertida e o briefing for extraido primeiro, ele vai puxar junto metade das decisoes de interface, memoria e host-boundary. A extracao vira caravana sem mapa.

## Criterio de pronto para a issue 50

1. existe uma area canonica proposta e aceita;
2. as fatias de extracao estao decompostas em issues menores;
3. esta claro o que sai do plugin, o que fica no plugin e o que nunca deveria ter morado ali;
4. runtime, wrappers e docs deixam de disputar autoridade com a nova casa do canon.
