# Feedback loop

O Prumo tem um canal nativo de feedback para o time mantenedor. Isso é fundamental: o feedback mais valioso vem de quem usa o sistema no dia a dia, e essas pessoas nem sempre vão abrir issues no GitHub.

## Como funciona

O agente reconhece variações naturais de "feedback pro Prumo":
- "feedback: achei o briefing confuso"
- "quero dar um feedback pro prumo"
- "tem uma coisa que podia melhorar no sistema"
- "bug no prumo"

Quando detectar, o agente:

1. **Captura** o que o usuário disse (pode pedir pra elaborar se for vago)
2. **Formata** em estrutura limpa: o que aconteceu, o que esperava, sugestão (se houver)
3. **Monta o email** com link `mailto:` pronto:
   - To: email de suporte configurado no produto (`email-de-feedback@dominio-do-produto.com`)
   - Subject: `PRUMO-FEEDBACK: [resumo curto]`
   - Body: feedback formatado + metadados (nome do agente, data do setup, tom configurado)
4. **Apresenta** pro usuário: mostra o email montado e oferece o link clicável
5. O usuário **clica e envia** (um toque)

Exemplo de apresentação ao usuário:

```
Montei o feedback pra mandar para o time do Prumo:

---
**Assunto:** PRUMO-FEEDBACK: Briefing não mostra itens por prioridade
**Para:** email-de-feedback@dominio-do-produto.com

O briefing diário lista os itens na ordem que entraram, mas seria mais útil
ver os urgentes primeiro. Quando tem muita coisa, os itens quentes se perdem
no meio da lista.

Sugestão: agrupar por urgência (quente → andamento → agendado).

[Prumo v1.0 | Agente: "Atlas" | Tom: direto | Setup: 13/02/2026]
---

[Clica aqui pra enviar](mailto:...)

Só apertar "Enviar" no email que abre. Sem editar nada (mas pode, se quiser).
```

## Onde isso entra no CLAUDE.md gerado

Na seção de regras de ouro, adicionar como regra 13:

**REGRA 13: FEEDBACK PRO PRUMO**
Se o usuário mencionar feedback, bug, sugestão ou melhoria do sistema Prumo em si (não do conteúdo da pauta), montar email formatado com link mailto pronto para o canal de suporte configurado no produto (ex: `email-de-feedback@dominio-do-produto.com`) com subject "PRUMO-FEEDBACK: [resumo]". Incluir no body: descrição do feedback, metadados do sistema (nome do agente, tom, data do setup). Apresentar pro usuário com link clicável. Um clique pra enviar.

## Feedback proativo (o diferencial)

O agente tem algo que nenhum formulário de feedback tem: contexto. Ele sabe quando algo não funcionou bem. O agente deve observar sinais e, quando tiver insumo, sugerir o feedback pronto.

**Sinais que geram feedback proativo:**
- Usuário ignorou a revisão semanal 2+ vezes → "Parece que a revisão semanal não tá funcionando pra você. Quer que eu mande isso pro criador do Prumo?"
- Inbox mobile ficou vazio por 5+ dias → captura mobile pode não estar funcionando
- Briefing muito longo (10+ itens quentes) → sistema pode estar acumulando demais
- Usuário fez dump de algo que o sistema deveria ter lembrado → gap no briefing
- Usuário pediu algo que o sistema não suporta → feature request natural
- Qualquer "isso é chato", "podia ser melhor", "não gostei" durante interações

**Quando oferecer:**
- No final do morning briefing, se houver sinal acumulado: "Notei que [observação]. Quer mandar isso como feedback pro Prumo? Já escrevi o rascunho."
- Na revisão semanal: "Algum feedback sobre o Prumo em si? Bug, ideia, coisa que te irritou?"
- Imediatamente quando o usuário expressar frustração com o sistema

**Como oferecer:**
O agente apresenta o texto sugerido já pronto, com o link mailto. O usuário só precisa confirmar e clicar. Se quiser editar, edita. Se não, um clique.

Exemplo:
```
Notei que nas últimas 3 sessões o briefing listou mais de 12 itens quentes.
Isso pode significar que os critérios de "quente" estão frouxos demais.

Montei um feedback:

---
PRUMO-FEEDBACK: Critérios de prioridade "quente" podem ser mais restritivos

Nos últimos briefings, a seção "quente" teve 12-15 itens. Quando tudo é quente,
nada é quente. Sugiro critérios mais agressivos pra priorização ou um limite
visual (top 5 quentes, resto em "andamento").

[Prumo v1.0 | Agente: "Mia" | Tom: direto | Uso: 3 semanas]
---

[Enviar feedback](mailto:...) — um clique, sem editar nada.
```

**Frequência:** No máximo 1 sugestão de feedback por semana. Não ser chato. Se o usuário recusar, esperar pelo menos 2 semanas antes de sugerir de novo.
