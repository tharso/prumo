# ADR-004 — Protocolo multi-host de desenvolvimento e handover interno

Status: aceito  
Data: 2026-03-28

Relacionado:

1. [#42](https://github.com/tharso/prumo/issues/42)
2. [#45](https://github.com/tharso/prumo/issues/45)
3. [REPO-WORKSPACE-JURISDICTION.md](/Users/tharsovieira/Documents/DailyLife/Prumo/REPO-WORKSPACE-JURISDICTION.md)

## Contexto

Codex, Claude e Antigravity participam do desenvolvimento do Prumo. Isso ajuda bastante. Tambem e um jeito eficiente de criar uma feira livre de contexto se o backstage nao tiver cerca.

O problema nao e o handover existir. O problema seria o handover virar feature do produto por osmose.

## Decisao

O projeto passa a assumir formalmente que:

1. `.workbench/HANDOVER.md` e ferramenta interna de oficina
2. `.workbench/` nao faz parte do produto
3. `.workbench/` tambem nao faz parte do Workspace vivo do usuario
4. handovers, revisoes cruzadas e notas internas servem para coordenacao entre hosts
5. toda decisao duravel deve subir para GitHub como issue, ADR, PR ou documento rastreavel

## Consequencias

### Positivas

1. backstage deixa de disputar identidade com o produto
2. o processo multi-host fica auditavel sem contaminar a experiencia final
3. agentes diferentes podem colaborar sem inventar memoria paralela do sistema

### Custos

1. exige disciplina para promover decisao boa da oficina para o GitHub
2. handover deixa de ser desculpa para backlog preguiçoso

## Rejeicoes explicitas

Esta ADR rejeita:

1. `HANDOVER.md` como artefato do usuario final
2. `.workbench/` como parte do runtime ou do workspace do usuario
3. manter decisao importante apenas em conversa, janela ou nota ignorada

## Implicacoes praticas

1. conversas de desenvolvimento devem abrir no repo do produto, nao no workspace do usuario
2. conversas de uso real do Prumo devem abrir no workspace vivo
3. quando uma tarefa misturar os dois papeis, isso deve ser declarado explicitamente
