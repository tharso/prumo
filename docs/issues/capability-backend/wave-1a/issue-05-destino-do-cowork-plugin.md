# Decidir o destino do cowork-plugin: legado suportado, adapter emagrecido ou combinacao

**Tipo**: Architecture / Legacy  
**Labels sugeridas**: `architecture`, `legacy`, `plugin`, `blocking`

## Contexto

O `cowork-plugin` ainda carrega muito valor, mas hoje faz papel de reliquia, adapter e deposito de sabedoria ao mesmo tempo. Isso e receita de novela ruim.

## Objetivo

Tomar a decisao bloqueante sobre o papel do `cowork-plugin` na transicao:

1. legado suportado
2. adapter Claude emagrecido
3. combinacao com fronteira explicita

## Perguntas que a issue precisa responder

1. o plugin continua recebendo inteligencia nova ou so manutencao?
2. o que fica nele por compatibilidade?
3. o que obrigatoriamente sobe para a area canonica?
4. que condicao encerraria o papel dele como linha principal?

## Entregaveis

1. decisao escrita
2. matriz do que fica, sai ou congela
3. impacto dessa decisao nas waves seguintes

## Criterio de aceite

1. nao existe mais ambiguidade sobre o papel do `cowork-plugin`
2. a Wave 1b pode ser executada sem pressuposto escondido

## Dependencias

1. [issue-02-adr-capability-backend.md](/Users/tharsovieira/Documents/DailyLife/Prumo/docs/issues/capability-backend/wave-1a/issue-02-adr-capability-backend.md)
