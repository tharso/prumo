---
name: revisao
description: >
  Revisão semanal do Prumo. Análise completa de todas as áreas, pendências
  envelhecendo, prioridades da próxima semana, limpeza de itens obsoletos.
  Use com "revisão semanal", "review", "vamos revisar", "como tá tudo?",
  ou no dia configurado no CLAUDE.md (geralmente domingo à noite).
---

# Revisão semanal

Você está executando a revisão semanal do Prumo. Esta é a rotina de manutenção
que impede o sistema de acumular entropia. Seja rigoroso.

## Passo 1: Carregar tudo

1. Leia `CLAUDE.md` (configuração, áreas, tom).
2. Leia `PRUMO-CORE.md` (regras, especialmente a seção "Revisão semanal").
3. Leia `PAUTA.md` completa.
4. Leia `IDEIAS.md`.
5. Leia `REGISTRO.md` (últimas 50 linhas — pra entender o que movimentou na semana).
6. Liste os README.md de cada área de vida.

## Passo 2: Processar inbox residual

Antes da revisão, limpar qualquer inbox pendente:
- `INBOX.md`
- `Inbox4Mobile/`
- Gmail (se configurado)

Se houver itens, processar como no `/prumo:inbox` antes de continuar.

## Passo 3: Análise por área

Para CADA área de vida (listada no CLAUDE.md), avaliar:

1. **O que avançou esta semana?** (cruzar com REGISTRO.md)
2. **O que está parado?** Com data `(desde DD/MM)` e diagnóstico de por que parou
3. **O que deveria ser desprioritizado ou removido?**
4. **Alguma pendência com outra pessoa?** (follow-up necessário?)

Apresentar como lista numerada contínua com opções (a, b, c) por item.
Proatividade nível 4: já propor a decisão, não só a pergunta.

## Passo 4: Gestão da PAUTA

- Itens "Concluídos da semana" → mover pra "Semana passada"
- "Semana passada" antiga (2+ semanas) → deletar (já está em REGISTRO.md)
- Itens em "Horizonte" que amadureceram → propor mover pra "Quente" ou "Andamento"
- Itens em "Hibernando" → checar se ainda fazem sentido
- Itens "Quentes" há mais de 2 semanas sem movimento → cobrar ou rebaixar

## Passo 5: Revisão de IDEIAS.md

- Alguma ideia amadureceu? → propor migrar pra PAUTA
- Alguma ideia morreu? → propor remover
- Ideia que precisa de pesquisa? → oferecer pra pesquisar agora

## Passo 6: Pessoas

Se existir `Pessoal/PESSOAS.md`:
- Quem sumiu? (sem contato há muito tempo)
- Pendência com alguém? (resposta devida, follow-up)
- Propor ações concretas

## Passo 7: Prioridades da próxima semana

Com base em tudo que foi revisado, propor:
- Top 3 prioridades da semana que vem
- Alertas (deadlines, compromissos, coisas que vão vencer)
- Micro-passos pra itens parados (quebrar inércia)

## Passo 8: Registrar

- Salvar resumo da revisão em `_logs/YYYY-WXX.md`
- Atualizar PAUTA.md com todas as mudanças aprovadas
- Atualizar README.md das áreas que mudaram
- Registrar em REGISTRO.md

## Passo 9: Mini-dashboard

Fechar com números:
- Itens que entraram na semana: X
- Itens concluídos: X
- Itens pendentes total: X
- Item mais antigo parado: "X (desde DD/MM)"
- Saúde do sistema: 🟢/🟡/🔴

---

**Tom:** Revisão é o momento de ser mais duro. Se algo tá parado há semanas, cobrar sem cerimônia.
**Links:** Sempre usar `[Descrição](computer:///caminho)` ao referenciar arquivos.
