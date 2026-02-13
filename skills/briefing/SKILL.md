---
name: briefing
description: >
  Morning briefing do Prumo. Executa a rotina completa: lê configuração pessoal,
  verifica pauta, processa inbox (todos os canais), checa calendário e emails,
  e apresenta o briefing do dia. Use com /briefing ou quando o usuário disser
  "bom dia", "briefing", "começar o dia".
---

# Briefing do Prumo

Você está executando o morning briefing do sistema Prumo. Esta é a rotina mais importante do sistema. Siga os passos abaixo **na ordem**, sem pular nenhum.

## Passo 1: Ler configuração

1. Leia o arquivo `CLAUDE.md` na pasta workspace do usuário. Ele contém: nome, áreas de vida, tom de comunicação, integrações configuradas, lembretes recorrentes.
2. Leia o arquivo `PRUMO-CORE.md` na mesma pasta. Ele contém as regras do sistema.

Se algum desses arquivos não existir, informe o usuário que o Prumo não está configurado e sugira rodar o setup.

## Passo 2: Verificar atualização

1. Leia o campo `prumo_version` no topo do `PRUMO-CORE.md` local.
2. Busque a versão remota em: `https://raw.githubusercontent.com/tharso/prumo/main/VERSION`
3. Se a versão remota for maior, informe: "Há uma atualização do Prumo (v[local] → v[remota]). Apenas o motor do sistema (PRUMO-CORE.md) será atualizado. Suas configurações pessoais, pauta, inbox e todos os seus arquivos permanecem intactos. Quer atualizar?"
4. Se aceitar: busque `https://raw.githubusercontent.com/tharso/prumo/main/skills/prumo/references/prumo-core.md` e substitua o `PRUMO-CORE.md` local.
5. Se recusar ou se já estiver atualizado: prossiga.

## Passo 3: Estado atual

1. Leia `PAUTA.md` — este é o arquivo mais importante.
2. Leia `INBOX.md` — se tiver itens, serão processados no passo 5.

## Passo 4: Canais de entrada

Verificar TODOS os canais, sem pular nenhum:

1. **Pasta `Inbox4Mobile/`**: Listar TODOS os arquivos. Abrir cada um, inclusive imagens (screenshots, fotos, prints de WhatsApp contêm informações críticas).
2. **Gmail** (se configurado no CLAUDE.md): Buscar emails com subject do agente e "INBOX:". Ler os não processados.
3. **Google Calendar** (se configurado): Listar eventos do dia.

## Passo 5: Processar inbox

Se houver itens novos (de qualquer canal):
- Numerar cada item
- Sugerir categoria e próxima ação
- Perguntar ao usuário se concorda ou quer ajustar
- Mover para PAUTA.md ou README da área
- Adicionar `(desde DD/MM)` em cada item
- Renomear arquivos com nomes descritivos
- Registrar no REGISTRO.md
- Deletar original do inbox

## Passo 6: Montar o briefing

Apresentar de forma direta (no tom configurado no CLAUDE.md):

1. **Compromissos do dia** (do calendário, se disponível)
2. **Itens quentes** que precisam de atenção hoje
3. **Lembretes do dia** (consultar lembretes recorrentes no CLAUDE.md — ex: "quarta = lanche da escola")
4. **Itens envelhecendo** — cobrar coisas paradas há muito tempo, com a data `(desde DD/MM)` visível
5. **Novidades do inbox** — se processou itens, mostrar resumo do que entrou

Se a PAUTA estiver vazia: não fazer o briefing padrão. Pedir um brain dump.

## Passo 7: Documentar

Atualizar PAUTA.md se algo mudou. Registrar itens processados no REGISTRO.md.

---

**Tom:** Seguir rigorosamente o tom definido no CLAUDE.md do usuário. Se for "direto", cobrar sem cerimônia. Se for "gentil", lembrar sem pressionar.

**Links:** Sempre usar `[Descrição](computer:///caminho)` ao referenciar arquivos. Nunca expor caminhos crus.
