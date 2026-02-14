---
name: status
description: >
  Dashboard rápido do Prumo. Visão geral do estado atual sem processar inbox
  nem rodar briefing completo. Use quando o usuário quiser uma foto rápida:
  "status", "como tá?", "qual a situação?", "resumo rápido", "dashboard".
---

# Status — Dashboard rápido

Visão rápida do estado do sistema. Sem processar inbox, sem briefing, sem calendário.
Só o essencial pra saber onde as coisas estão.

## Passo 1: Carregar

1. Leia `CLAUDE.md` (áreas, tom).
2. Leia `PAUTA.md` completa.

Se `CLAUDE.md` não existir, informe que o Prumo não está configurado e sugira `/prumo:setup`.

## Passo 2: Montar dashboard

Apresentar de forma compacta:

**Números:**
- Itens quentes: X
- Em andamento: X
- Agendados: X
- No horizonte: X
- Hibernando: X

**Alertas** (se houver):
- Itens parados há mais de 7 dias (com data)
- Deadlines nos próximos 3 dias
- Lembretes do dia (consultar CLAUDE.md)

**Inbox pendente** (checar sem processar):
- INBOX.md: X itens
- Inbox4Mobile/: X arquivos
- (Não abrir, não processar — só contar)

## Passo 3: Recomendação

Uma frase só. Ex:
- "Tudo sob controle. 2 itens quentes, nenhum alerta."
- "3 coisas paradas há mais de 10 dias. Recomendo `/prumo:revisao`."
- "Inbox com 5 itens pendentes. Quer um `/prumo:inbox`?"
- "Semana pesada: 4 deadlines nos próximos 3 dias."

---

**Tom:** Ultra-conciso. Máximo: uma tela. Se o usuário quer detalhes, roda briefing ou revisão.
**Links:** Sempre usar `[Descrição](computer:///caminho)` ao referenciar arquivos.
