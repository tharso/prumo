# ADR-002: Prumo como backend de capacidades com experiencia multi-host

**Tipo**: Architecture  
**Labels sugeridas**: `adr`, `architecture`, `runtime`, `hosts`

## Contexto

A direcao capability-backend foi aprovada por Codex, Claude e Antigravity. Falta cristalizar isso como decisao oficial, para o repositorio parar de discutir a cada esquina se o runtime ainda e o narrador do produto.

## Objetivo

Registrar oficialmente que:

1. a experiencia mora no host
2. o runtime fornece capacidades
3. o `Workspace` raiz e a memoria viva do sistema
4. `AGENT.md` e direcao arquitetural pragmatica, nao dogma de curto prazo
5. o produto nao deve mais tratar runtime como narrador principal

## Entregaveis

1. ADR-002 escrito e commitado
2. ligacoes claras para docs existentes impactados
3. resumo da decisao no backlog e no README-DEV, se necessario

## Criterio de aceite

1. qualquer pessoa consegue explicar a arquitetura sem falar duas frases contraditorias
2. fica explicito o que e produto, o que e host e o que e runtime

## Dependencias

1. [issue-01-epic-reorientar-prumo.md](/Users/tharsovieira/Documents/DailyLife/Prumo/docs/issues/capability-backend/wave-1a/issue-01-epic-reorientar-prumo.md)
