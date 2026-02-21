---
name: briefing
description: >
  Morning briefing do Prumo. Executa a rotina completa: lê configuração pessoal,
  verifica pauta, processa inbox (todos os canais), checa calendário e emails,
  e apresenta o briefing do dia. Use com /prumo:briefing (alias legado: /briefing) ou quando o usuário disser
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
3. Se a versão remota for **igual ou menor**: prossiga sem mencionar nada.
4. Se a versão remota for **maior**:
   a. Busque o PRUMO-CORE.md remoto em: `https://raw.githubusercontent.com/tharso/prumo/main/skills/prumo/references/prumo-core.md`
   b. Leia a seção "Changelog do Core" do arquivo remoto. Extraia as entradas entre a versão local e a remota.
   c. Apresente ao usuário: "Há uma atualização do Prumo (v[local] → v[remota]). O que mudou: [itens do changelog]. A atualização pode tocar SOMENTE `PRUMO-CORE.md`. Seus arquivos pessoais e operacionais não podem ser alterados. Atualizar?"
   d. Se aceitar:
      - criar backup de `PRUMO-CORE.md` em `_backup/PRUMO-CORE.md.YYYY-MM-DD-HHMMSS` (criando `_backup/` se necessário)
      - substituir apenas `PRUMO-CORE.md`
      - abortar se qualquer outra escrita for necessária
   e. Se recusar: prossiga sem insistir.

## Passo 3: Estado atual

1. Leia `PAUTA.md` — este é o arquivo mais importante.
2. Leia `INBOX.md` — se tiver itens, serão processados no passo 5.
3. Se existir `_state/HANDOVER.md`, identificar itens em `PENDING_VALIDATION` ou `REJECTED`.

## Passo 4: Canais de entrada

Verificar TODOS os canais, sem pular nenhum:

1. **Pasta `Inbox4Mobile/`**: Listar TODOS os arquivos. Abrir cada um, inclusive imagens (screenshots, fotos, prints de WhatsApp contêm informações críticas).
2. **Google dual via Gemini CLI (prioridade quando disponível)**:
   - Se existir `scripts/prumo_google_dual_snapshot.sh`, executar esse script.
   - Usar a saída do script como fonte principal para agenda (`AGENDA_HOJE` + `AGENDA_AMANHA`) e curadoria de emails (`TRIAGEM_RESPONDER`, `TRIAGEM_VER`, `TRIAGEM_SEM_ACAO`) das contas `pessoal` e `trabalho`.
   - Respeitar a janela "desde o último briefing" informada no próprio script.
   - Se uma conta falhar (auth/MCP), sinalizar no briefing e manter a outra conta.
3. **Fallback sem shell (paridade obrigatória de curadoria)**:
   - Se o script dual não existir ou não puder executar no runtime, usar integração nativa de Gmail/Calendar.
   - Definir janela de análise de email:
     - Se existir `_state/briefing-state.json` com `last_briefing_at`, usar esse timestamp.
     - Senão, usar fallback de 24h.
   - Buscar emails recebidos na janela e classificar com o mesmo padrão:
     - `Responder` (exige resposta ativa)
     - `Ver` (exige leitura/checagem, sem resposta imediata)
     - `Sem ação` (baixo valor imediato)
   - Atribuir prioridade `P1/P2/P3` e motivo objetivo em cada item.
4. **Google Calendar fallback** (se configurado): listar eventos de hoje e amanhã.

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
   - Quando usar o script dual, consolidar compromissos das duas contas e identificar a origem (`pessoal`/`trabalho`).
2. **Itens quentes** que precisam de atenção hoje
3. **Lembretes do dia** (consultar lembretes recorrentes no CLAUDE.md — ex: "quarta = lanche da escola")
4. **Itens envelhecendo** — cobrar coisas paradas há muito tempo, com a data `(desde DD/MM)` visível
5. **Novidades do inbox** — se processou itens, mostrar resumo do que entrou
   - Em qualquer modo (script dual ou fallback sem shell), incluir curadoria por conta quando disponível:
     - `Responder`: exige ação de resposta.
     - `Ver`: exige leitura/checagem, sem resposta imediata.
     - `Sem ação`: pode ignorar por ora.
6. **Pendências de handover** — se houver `_state/HANDOVER.md` com `PENDING_VALIDATION`/`REJECTED`, listar e propor ação

Se a PAUTA estiver vazia: não fazer o briefing padrão. Pedir um brain dump.

## Passo 7: Documentar

Atualizar PAUTA.md se algo mudou. Registrar itens processados no REGISTRO.md.
Se houve validação de handover, atualizar status no `_state/HANDOVER.md`.
Se o script dual foi usado e o briefing foi concluído, executar `scripts/prumo_google_dual_snapshot.sh --mark-briefing-complete` para atualizar a referência temporal do próximo briefing.
Se o script dual NÃO foi usado (fallback sem shell), atualizar `_state/briefing-state.json` manualmente com o timestamp atual em `last_briefing_at`.

---

**Tom:** Seguir rigorosamente o tom definido no CLAUDE.md do usuário. Se for "direto", cobrar sem cerimônia. Se for "gentil", lembrar sem pressionar.

**Links:** Sempre usar `[Descrição](computer:///caminho)` ao referenciar arquivos. Nunca expor caminhos crus.
