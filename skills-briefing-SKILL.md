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
3. Extraia o fuso do usuário do `CLAUDE.md` (default: `America/Sao_Paulo`) e use esse fuso para qualquer referência de data relativa (`hoje`, `amanhã`, dia da semana).
4. Determine a data local por fonte verificável (ordem de preferência): ferramenta de tempo com timezone, relógio do sistema com TZ explícito, APIs de calendário no mesmo fuso.
5. Se não houver fonte confiável, NÃO anunciar dia/data textual no cabeçalho do briefing.

Se algum desses arquivos não existir, informe o usuário que o Prumo não está configurado e sugira rodar o setup.

## Passo 2: Verificar atualização

1. Leia o campo `prumo_version` no topo do `PRUMO-CORE.md` local.
2. Tente fonte remota:
   - versão: `https://raw.githubusercontent.com/tharso/prumo/main/VERSION`
   - core: `https://raw.githubusercontent.com/tharso/prumo/main/references/prumo-core.md`
3. Se a fonte remota falhar (404/auth/rede), tente fonte local (se existir no workspace):
   - versão: `Prumo/VERSION`
   - core: `Prumo/references/prumo-core.md`
4. Se nenhuma fonte estiver acessível:
   - informe: "Não consegui verificar atualização do Prumo agora (falha de acesso à fonte de versão)."
   - prossiga sem afirmar que está atualizado.
5. Se a versão encontrada for **igual ou menor**: prossiga sem mencionar nada.
6. Se a versão encontrada for **maior**:
   a. Leia a seção "Changelog do Core" do core da fonte válida. Extraia as entradas entre a versão local e a remota.
   b. Apresente ao usuário: "Há uma atualização do Prumo (v[local] → v[remota]). O que mudou: [itens do changelog]. A atualização pode tocar SOMENTE `PRUMO-CORE.md`. Seus arquivos pessoais e operacionais não podem ser alterados. Atualizar?"
   c. Se aceitar:
      - criar backup de `PRUMO-CORE.md` em `_backup/PRUMO-CORE.md.YYYY-MM-DD-HHMMSS` (criando `_backup/` se necessário)
      - substituir apenas `PRUMO-CORE.md` com o core da fonte válida
      - abortar se qualquer outra escrita for necessária
   d. Se recusar: prossiga sem insistir.

## Passo 3: Estado atual

1. Leia `PAUTA.md` — este é o arquivo mais importante.
2. Leia `INBOX.md` — se tiver itens, serão processados no passo 5.
3. Verifique handovers em modo leve:
   - se existir `_state/HANDOVER.summary.md`, use como fonte principal;
   - se não existir ou estiver desatualizado, leia `_state/HANDOVER.md`;
   - identifique itens em `PENDING_VALIDATION` ou `REJECTED`.
4. Se existir `_state/auto-sanitize-state.json`, leia para telemetria de manutenção (última execução/último apply).

## Passo 4: Canais de entrada

Verificar TODOS os canais, sem pular nenhum:

0. **Autosanitização preventiva (quando shell disponível)**:
   - Rodar `if [ -f scripts/prumo_auto_sanitize.py ]; then python3 scripts/prumo_auto_sanitize.py --workspace . --apply; else python3 Prumo/scripts/prumo_auto_sanitize.py --workspace . --apply; fi`.
   - Se falhar, reportar em 1 linha e seguir briefing (não bloquear rotina).

1. **Pasta `Inbox4Mobile/`**: Listar TODOS os arquivos e iniciar por triagem leve (não abrir bruto de todos por padrão).
   - Se existir `Inbox4Mobile/_processed.json`, usar como filtro para não reapresentar como "novos" os itens já processados em sessão anterior sem deleção física.
   - Rodar em **2 estágios obrigatórios**:
     - Estágio A (triagem leve): gerar `Inbox4Mobile/inbox-preview.html` + `Inbox4Mobile/_preview-index.json`.
     - com shell: `if [ -f scripts/generate_inbox_preview.py ]; then python3 scripts/generate_inbox_preview.py --output Inbox4Mobile/inbox-preview.html --index-output _preview-index.json; else python3 Prumo/scripts/generate_inbox_preview.py --output Inbox4Mobile/inbox-preview.html --index-output _preview-index.json; fi`.
     - sem shell: gerar HTML equivalente inline + índice textual equivalente (tipo, tamanho, data, link).
     - Estágio B (aprofundamento): abrir conteúdo bruto completo apenas para itens `P1`, ambíguos, risco legal/financeiro/documental, ou solicitação explícita do usuário.
   - Se a geração falhar, seguir com lista numerada no chat (fallback universal), mantendo a regra de aprofundamento seletivo.
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
- Sugerir categoria e próxima ação com `Responder`/`Ver`/`Sem ação` e `P1`/`P2`/`P3`
- Perguntar ao usuário se concorda ou quer ajustar
- Montar plano único de commit com todas as operações pendentes
- Pedir confirmação explícita antes de executar: "Vou executar estas N operações. Confirma?"
- Executar em lote:
  - mover para PAUTA.md ou README da área
  - adicionar `(desde DD/MM)` em cada item
  - renomear arquivos com nomes descritivos
  - registrar no REGISTRO.md
  - deletar original do inbox com ação real de filesystem
- Tratar permissão de deleção por runtime:
  - quando necessário, solicitar proativamente permissão (ex.: `allow_cowork_file_delete`) antes de deletar
  - se falhar por permissão, solicitar e tentar novamente
  - se continuar falhando, registrar `DELECAO_FALHOU` no REGISTRO.md (com motivo) e marcar item em `Inbox4Mobile/_processed.json`
- Verificar pós-commit: listar `Inbox4Mobile/` e confirmar que itens processados não ficaram para trás
- Reportar fechamento: quantos processados, quantos deletados, quantos falharam e por quê

## Passo 6: Montar o briefing

Apresentar de forma direta (no tom configurado no CLAUDE.md):

1. **Abertura com data correta** (obrigatório)
   - Mostrar data e dia da semana no fuso do usuário (não usar UTC para anunciar "hoje").
   - Use formato absoluto: `Sábado, 21 de fevereiro de 2026 (America/Sao_Paulo)`.
   - Se data não for verificável com confiança, omitir a linha de dia/data.
2. **Compromissos do dia** (do calendário, se disponível)
   - Quando usar o script dual, consolidar compromissos das duas contas e identificar a origem (`pessoal`/`trabalho`).
3. **Itens quentes** que precisam de atenção hoje
4. **Lembretes do dia** (consultar lembretes recorrentes no CLAUDE.md — ex: "quarta = lanche da escola")
5. **Itens envelhecendo** — cobrar coisas paradas há muito tempo, com a data `(desde DD/MM)` visível
6. **Novidades do inbox** — se processou itens, mostrar resumo do que entrou
   - Em qualquer modo (script dual ou fallback sem shell), incluir curadoria por conta quando disponível:
     - `Responder`: exige ação de resposta.
     - `Ver`: exige leitura/checagem, sem resposta imediata.
     - `Sem ação`: pode ignorar por ora.
   - Informar quais itens ficaram só na triagem leve e quais exigiram abertura completa.
7. **Pendências de handover** — se houver `_state/HANDOVER.md` com `PENDING_VALIDATION`/`REJECTED`, listar e propor ação

Se a PAUTA estiver vazia: não fazer o briefing padrão. Pedir um brain dump.

## Passo 7: Documentar

Atualizar PAUTA.md se algo mudou. Registrar itens processados no REGISTRO.md.
Se houve validação de handover, atualizar status no `_state/HANDOVER.md`.
Se o script dual foi usado e o briefing foi concluído, executar `scripts/prumo_google_dual_snapshot.sh --mark-briefing-complete` para atualizar a referência temporal do próximo briefing.
Se existir `_state/HANDOVER.summary.md`, atualizar via sanitização quando houver grande volume de handovers fechados.
Se o script dual NÃO foi usado (fallback sem shell), atualizar `_state/briefing-state.json` manualmente com o timestamp atual em `last_briefing_at`.
Se houve fallback sem deleção física, manter `Inbox4Mobile/_processed.json` atualizado para evitar reapresentação de itens já processados.

---

**Tom:** Seguir rigorosamente o tom definido no CLAUDE.md do usuário. Se for "direto", cobrar sem cerimônia. Se for "gentil", lembrar sem pressionar.

**Links:** Sempre usar `[Descrição](computer:///caminho)` ao referenciar arquivos. Nunca expor caminhos crus.
