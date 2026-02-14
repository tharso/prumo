---
name: inbox
description: >
  Reprocessa o inbox do Prumo sob demanda. Verifica todos os canais de entrada
  (Inbox4Mobile/, Gmail, INBOX.md), processa itens pendentes, categoriza e move
  pra PAUTA.md. Use quando quiser limpar o inbox fora do briefing, após enviar
  notas pelo celular, ou quando disser "processar inbox", "checar inbox",
  "o que entrou?", "tem coisa nova?".
---

# Inbox — Processamento sob demanda

Você está executando o processamento de inbox do Prumo fora do briefing regular.
O objetivo é: capturar tudo que entrou, processar, e deixar o inbox zerado.

## Passo 1: Ler configuração

1. Leia `CLAUDE.md` na pasta workspace do usuário (nome, áreas, tom, integrações).
2. Leia `PRUMO-CORE.md` (regras do sistema).

Se algum não existir, informe que o Prumo não está configurado e sugira `/prumo:setup`.

## Passo 2: Verificar todos os canais

Checar TODOS os canais, sem pular nenhum:

1. **`INBOX.md`**: Ler itens pendentes.
2. **Pasta `Inbox4Mobile/`**: Listar TODOS os arquivos. Abrir cada um, inclusive imagens (screenshots, fotos, prints de WhatsApp contêm informações críticas).
3. **Gmail** (se configurado no CLAUDE.md): Buscar emails com subject do agente e "INBOX:". Ler os não processados.

Se TODOS os canais estiverem vazios: informar "Inbox limpo, nada novo." e encerrar.

## Passo 3: Processar itens

Para cada item encontrado:

1. Numerar sequencialmente (lista contínua, sem resetar)
2. Mostrar o conteúdo resumido
3. Sugerir: categoria (tag), próxima ação concreta, destino (PAUTA.md ou README da área)
4. Oferecer opções com letras (a, b, c) quando houver decisão

Apresentar TODOS os itens de uma vez, com propostas de ação (proatividade nível 3-4).
O usuário responde no formato rápido: "1a, 2b, 3a" ou "ok pra todos" ou ajusta individualmente.

## Passo 4: Executar

Após confirmação do usuário:

- Mover cada item para o destino (PAUTA.md, README da área, IDEIAS.md)
- Adicionar `(desde DD/MM)` em cada item movido pra PAUTA
- Renomear arquivos do Inbox4Mobile/ com nomes descritivos
- Registrar no REGISTRO.md
- Limpar: deletar originais do inbox, remover de INBOX.md

## Passo 5: Confirmar

Resumo rápido: "X itens processados. Inbox zerado." com lista do que foi pra onde.

---

**Tom:** Seguir rigorosamente o tom definido no CLAUDE.md do usuário.
**Links:** Sempre usar `[Descrição](computer:///caminho)` ao referenciar arquivos.
