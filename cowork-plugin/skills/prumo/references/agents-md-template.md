# AGENTS.md template (adapter)

> Este template gera o arquivo `AGENTS.md` para ambientes que não leem
> `CLAUDE.md` nativamente (ex: Codex CLI).
>
> Princípio: **não duplicar conteúdo**. O AGENTS.md aponta para os arquivos
> fonte (`CLAUDE.md` + `PRUMO-CORE.md`) e adiciona só regras específicas
> de coexistência operacional.

---

INÍCIO DO TEMPLATE:

---

# Prumo Adapter — {{USER_NAME}}

## Instruções primárias

Antes de qualquer operação, leia nesta ordem:

1. `CLAUDE.md` (configuração pessoal: áreas, tom, tags, lembretes)
2. `PRUMO-CORE.md` (motor e regras operacionais)
3. `PAUTA.md` e `INBOX.md` (estado atual)
4. `_state/HANDOVER.md` (se existir)

## Comando canônico

- Briefing canônico: `/prumo:briefing`
- Alias legado aceito: `/briefing`
- Handover manual: `/prumo:handover`

## Regras específicas para agentes não-Cowork

1. Não editar `CLAUDE.md` nem `PRUMO-CORE.md` sem instrução explícita do usuário.
2. Em arquivos críticos (`PAUTA.md`, `INBOX.md`, `REGISTRO.md`), preferir append e preservar histórico.
3. Seguir lock por escopo em `_state/agent-lock.json` antes de escrever.
4. Para mudanças estruturais, abrir handover em `_state/HANDOVER.md` e pedir validação cruzada do Cowork.
5. Em handovers, manter tom respeitoso e cooperativo.
6. Em `/prumo:briefing`, checar handovers `PENDING_VALIDATION`/`REJECTED` e incluir no resumo.

## Escopo recomendado

- Primário: código, automação, validação técnica, manutenção de estrutura.
- Secundário: organização pessoal diária (briefing/inbox/revisão) quando o Cowork estiver operando esse fluxo.

## Limitações conhecidas

1. Você pode não ter integrações de Gmail/Calendar configuradas neste ambiente.
2. Você não executa comandos slash da plataforma Cowork.
3. Use os arquivos como fonte de verdade; nunca assuma estado só pela conversa.

---
