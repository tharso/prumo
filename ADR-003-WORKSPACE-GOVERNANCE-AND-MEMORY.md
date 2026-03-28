# ADR-003 — Governanca documental, memoria local e limpeza com delegacao otimista

Status: aceito  
Data: 2026-03-28

Relacionado:

1. [#42](https://github.com/tharso/prumo/issues/42)
2. [#44](https://github.com/tharso/prumo/issues/44)
3. [PRUMO-CAPABILITY-BACKEND-ARCHITECTURE.md](/Users/tharsovieira/Documents/DailyLife/Prumo/PRUMO-CAPABILITY-BACKEND-ARCHITECTURE.md)
4. [REPO-WORKSPACE-JURISDICTION.md](/Users/tharsovieira/Documents/DailyLife/Prumo/REPO-WORKSPACE-JURISDICTION.md)

## Contexto

No Prumo, memoria local nao e adereco. E o que impede o produto de virar conversa esperta com amnesia bem penteada.

O risco oposto tambem e real:

1. overengineering cedo demais
2. catalogacao barroca para problema pequeno
3. limpeza tagarela que faz o usuario odiar o proprio sistema

## Decisao

O produto passa a assumir formalmente que:

1. o Workspace do usuario tem **jurisdicao documental explicita**
2. `_state/` e reservado ao **estado vivo do usuario**
3. nomes de arquivos devem ser humanos primeiro e tecnicos depois
4. indices humanos e tecnicos existem, mas a primeira fase deve ser proporcional
5. limpeza se divide em:
   - automatica segura
   - assistida
   - delegacao otimista quando o risco editorial for baixo
6. higiene ignorada repetidamente pode escalar de forma mais assertiva

## Consequencias

### Positivas

1. contexto vira sistema, nao pilha de markdown
2. a memoria do usuario continua local e legivel
3. o produto ganha criterio claro sobre onde cada tipo de informacao mora

### Custos

1. o runtime precisa sustentar alguma governanca estrutural
2. os hosts precisam documentar com mais disciplina
3. fica proibido tratar qualquer arquivo como gaveta universal

## Rejeicoes explicitas

Esta ADR rejeita:

1. depender so de memoria difusa do modelo
2. deixar todo cleanup para a boa vontade do usuario
3. construir um sistema de catalogacao pesado antes de resolver jurisdicao e naming

## Implicacoes praticas

1. `PAUTA.md`, `INBOX.md`, `REGISTRO.md`, `Referencias/` e `_state/` precisam ter contratos claros
2. artefatos da oficina nao pertencem ao `_state/` do usuario
3. o repo do produto deve guardar templates, schemas e exemplos sanitizados, nao dados vivos
