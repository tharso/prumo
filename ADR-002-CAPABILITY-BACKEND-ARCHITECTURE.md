# ADR-002 — Prumo como backend de capacidades com experiencia multi-host

Status: aceito  
Data: 2026-03-28

Relacionado:

1. [#42](https://github.com/tharso/prumo/issues/42)
2. [#43](https://github.com/tharso/prumo/issues/43)
3. [PRUMO-CAPABILITY-BACKEND-ARCHITECTURE.md](/Users/tharsovieira/Documents/DailyLife/Prumo/PRUMO-CAPABILITY-BACKEND-ARCHITECTURE.md)
4. [REPO-WORKSPACE-JURISDICTION.md](/Users/tharsovieira/Documents/DailyLife/Prumo/REPO-WORKSPACE-JURISDICTION.md)

## Contexto

O Prumo ficou tempo demais no pior tipo de entrelugar:

1. plugin demais para ser produto agnostico
2. runtime demais para continuar fluido
3. host demais para ter governanca propria

O resultado foi previsivel: o runtime comecou a cheirar a prefeitura e o plugin continuou carregando sabedoria de produto demais.

## Decisao

O Prumo passa a adotar formalmente a seguinte arquitetura:

1. a **experiencia** mora no host
2. o **runtime** fornece capacidades e operacoes confiaveis
3. o **Workspace** raiz do usuario e a memoria viva do sistema
4. existe uma camada de **orquestracao compartilhada** entre host e runtime
5. `AGENT.md` segue como direcao canonica pragmatica, sem virar dogma de curto prazo

Em portugues simples: o host conversa, o runtime faz trabalho pesado, e nenhum dos dois ganha licenca para virar o produto inteiro.

## Consequencias

### Positivas

1. o produto deixa de depender de um host especifico para existir
2. adapters por host passam a ser cascas de experiencia, nao centros de regra
3. o runtime ganha funcao clara como motor tecnico reutilizavel
4. o workspace do usuario continua local, auditavel e legivel

### Custos

1. a fronteira entre canon e capability precisa ser extraida com mais disciplina
2. hosts precisam respeitar contrato de orquestracao, erro e persona
3. a qualidade de UX deixa de ser milagre do host e vira problema nosso

## Rejeicoes explicitas

Esta ADR rejeita tres modelos:

1. plugin-first como linha principal de produto
2. runtime-first como narrador da experiencia
3. cada host improvisando sua propria versao do Prumo

## Implicacoes praticas

1. regra host-agnostica nova nao deve nascer em adapter
2. o runtime nao deve encapsular operacoes locais simples que o host ja executa melhor
3. orquestracao, persona e fallback passam a ser contratos formais do produto
4. o repo do produto, o workspace do usuario e a oficina de desenvolvimento devem permanecer separados
