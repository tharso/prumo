# Definir contrato de orquestracao compartilhada entre hosts e runtime

**Tipo**: Product architecture  
**Labels sugeridas**: `architecture`, `orchestration`, `hosts`, `runtime`

## Contexto

Sem orquestracao compartilhada, "host faz UX e runtime faz trabalho pesado" vira so um jeito elegante de espalhar a bagunca por mais de um endereco.

## Objetivo

Definir quem decide a sequencia do produto sem deixar cada host reinventar o fluxo.

## Escopo

1. ordem de acoes
2. quando priorizar repair vs briefing vs continuacao
3. quando documentar primeiro
4. quando inbox sobe
5. como o host consome a orquestracao sem virar marionete verborragica
6. o que o contrato decide e o que continua aberto a adaptacao do host

## Nao escopo

1. transformar o runtime de volta em narrador
2. engessar todos os hosts com uma conversa identica

## Entregaveis

1. contrato de orquestracao versionavel
2. exemplos de fluxo principal e de erro
3. relacao entre contrato e adapters

## Criterio de aceite

1. hosts deixam de improvisar o roteiro inteiro
2. runtime nao volta disfarçado de mestre de cerimonias

## Dependencias

1. [issue-08-extrair-canon-do-plugin.md](/Users/tharsovieira/Documents/DailyLife/Prumo/github-issues/capability-backend/wave-1b/issue-08-extrair-canon-do-plugin.md)
2. [issue-28-adapter-antigravity-e-validacao.md](/Users/tharsovieira/Documents/DailyLife/Prumo/github-issues/capability-backend/wave-1a/issue-28-adapter-antigravity-e-validacao.md)
