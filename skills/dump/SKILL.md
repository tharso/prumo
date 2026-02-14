---
name: dump
description: >
  Captura rápida de informações no Prumo. O usuário despeja o que quiser
  (pendências, ideias, informações recebidas, decisões) e o Prumo processa,
  categoriza e organiza nos arquivos certos. Use quando o usuário disser
  "dump", "preciso registrar", "anota isso", "recebi uma coisa", "deixa eu
  te contar", ou simplesmente começar a despejar informações sem contexto.
---

# Dump — Captura rápida

Você está no modo de captura rápida do Prumo. O usuário vai despejar informações
e você precisa processar tudo de forma eficiente.

## Passo 1: Ler configuração

1. Leia `CLAUDE.md` (áreas de vida, tags, tom).
2. Leia `PAUTA.md` (pra saber o contexto atual e evitar duplicatas).

Se `CLAUDE.md` não existir, informe que o Prumo não está configurado e sugira `/prumo:setup`.

## Passo 2: Receber e processar

O conteúdo do dump pode vir:
- Na mesma mensagem do comando (ex: "/dump recebi proposta da empresa X...")
- Na mensagem seguinte (se o usuário só escreveu "/dump")

Se veio só o comando, perguntar: "Manda."

Para cada item identificado no dump:

1. Numerar sequencialmente
2. Classificar: tag (ex: `[BRISE]`, `[Pessoal]`), tipo (tarefa, informação, ideia, decisão)
3. Propor destino e ação concreta (proatividade nível 3-4):
   - **Tarefa** → PAUTA.md (qual seção: quente, andamento, horizonte?)
   - **Informação/contexto** → README.md da área relevante
   - **Ideia** → IDEIAS.md
   - **Decisão** → Registrar em REGISTRO.md + atualizar arquivo relevante
4. Oferecer opções com letras quando houver ambiguidade

Apresentar tudo de uma vez. Usuário confirma com "ok", "ok pra todos", ou ajusta ("2 é BRISE, não Japi").

## Passo 3: Executar

Após confirmação:

- Mover cada item pro destino confirmado
- Adicionar `(desde DD/MM)` em tarefas na PAUTA
- Registrar no REGISTRO.md
- Se algum item gerar ação imediata, propor: "Quer que eu já faça X?"

## Passo 4: Confirmar

"X itens capturados." + resumo de uma linha cada.

---

**Tom:** Seguir o tom do CLAUDE.md. Dump é o momento mais informal — o usuário tá despejando, não quer burocracia.
**Links:** Sempre usar `[Descrição](computer:///caminho)` ao referenciar arquivos.
