# Epic: Reorientar o Prumo para UX host-native com runtime como backend de capacidades

**Tipo**: Epic  
**Labels sugeridas**: `epic`, `architecture`, `product`, `multi-host`

## Contexto

O Prumo ficou no pior lugar possivel: plugin demais para ser agnostico, runtime demais para continuar fluido. A proposta capability-backend existe para sair desse meio-termo sem matar a alma do produto.

## Objetivo

Consolidar a reorientacao arquitetural do Prumo para:

1. `Workspace` unico e canonicamente estruturado
2. runtime como backend de capacidades
3. orquestracao compartilhada entre host e runtime
4. experiencia principal nos hosts
5. governanca documental como subsistema central
6. transicao segura a partir do legado plugin-first

## Escopo do epico

1. ADRs estruturais
2. decisao sobre o destino do `cowork-plugin`
3. auditoria do estado atual
4. extracao do canon
5. definicao de orquestracao e persona
6. redesenho do runtime
7. adapters por host
8. onboarding e instalacao, depois da fundacao pronta

## Criterio de aceite

O epico so fecha quando o repositorio tiver:

1. canon explicito
2. runtime rebaixado para capacidades
3. orquestracao compartilhada definida
4. pelo menos Codex e Claude operando sobre a mesma base
5. governanca documental formalizada em nivel util

## Dependencias

Nenhuma. Esta issue e a arvore, o resto sao os galhos.
