# ADR-003: Governanca documental, memoria local e limpeza com delegacao otimista

**Tipo**: Architecture  
**Labels sugeridas**: `adr`, `memory`, `documentation`, `product`

## Contexto

Persistencia e contexto nao sao perfumaria no Prumo. Sao o que separa um sistema util de um LLM simpatico com amnesia seletiva. O problema e nao cair no barroco cedo demais.

## Objetivo

Formalizar:

1. jurisdicao dos arquivos
2. tipos de memoria do sistema
3. nomes intuitivos
4. indices humanos e tecnicos proporcionais
5. limpeza automatica vs assistida
6. delegacao otimista quando o risco editorial for baixo
7. escalacao quando higiene for ignorada repetidamente

## Entregaveis

1. ADR-003 escrito e commitado
2. racional para escopo inicial minimo
3. exemplos de limpeza segura vs limpeza assistida

## Criterio de aceite

1. a memoria local deixa de ser intuicao espalhada
2. fica claro o que pode ser reorganizado sozinho e o que exige parceria com o usuario

## Dependencias

1. [issue-01-epic-reorientar-prumo.md](/Users/tharsovieira/Documents/DailyLife/Prumo/docs/issues/capability-backend/wave-1a/issue-01-epic-reorientar-prumo.md)
