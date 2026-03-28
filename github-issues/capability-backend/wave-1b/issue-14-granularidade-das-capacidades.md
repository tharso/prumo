# Definir granularidade ideal das capacidades para evitar micro-tool-chaining excessivo

**Tipo**: Runtime / Host performance  
**Labels sugeridas**: `runtime`, `performance`, `hosts`, `ux`

## Contexto

Capability demais e como talher de restaurante metido a besta: bonito no guardanapo, inutil quando o usuario so quer jantar sem cerimonia. Se cada resposta exigir uma procissao de tool calls, a fluidez morre na fila.

## Objetivo

Evitar que o runtime fique granular demais e obrigue hosts a encadear dezenas de chamadas para montar uma resposta simples.

## Escopo

1. criterio para capacidade "atomica demais"
2. criterio para capacidade "gorda demais"
3. latencia aceitavel por fluxo
4. composicoes predefinidas quando fizer sentido
5. compatibilidade com hosts fortes que ja operam bem em arquivos locais

## Entregaveis

1. diretriz de granularidade
2. exemplos concretos de corte bom vs ruim
3. implicacoes para o catalogo inicial de capacidades

## Criterio de aceite

1. o runtime nao vira nem uma API obesa nem um saco de pecinhas Lego despejado no chao

## Dependencias

1. [issue-11-contrato-de-orquestracao.md](/Users/tharsovieira/Documents/DailyLife/Prumo/github-issues/capability-backend/wave-1b/issue-11-contrato-de-orquestracao.md)
2. [issue-28-adapter-antigravity-e-validacao.md](/Users/tharsovieira/Documents/DailyLife/Prumo/github-issues/capability-backend/wave-1a/issue-28-adapter-antigravity-e-validacao.md)
