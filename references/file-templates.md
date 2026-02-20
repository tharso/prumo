# Templates dos arquivos auxiliares do Prumo

> Cada seção abaixo é um arquivo separado a ser gerado no workspace do usuário.
> Copiar o conteúdo entre as marcações `--- INÍCIO ---` e `--- FIM ---`.

---

## PAUTA.md

--- INÍCIO ---

# Pauta

> Estado atual das coisas. Atualizado a cada interação relevante.

## Quente (precisa de atenção agora)

_Nada ainda. Faça seu primeiro dump pra popular._

## Em andamento

_Itens que têm progresso ativo. Formato: `- [Tag] Descrição. Próxima ação: X. (desde DD/MM)`_

## Agendado / Lembretes

_Itens com data específica ou lembretes recorrentes._

{{LEMBRETES_RECORRENTES_LISTA}}

## Horizonte (importante mas não urgente)

_Coisas que precisam acontecer, mas não essa semana._

## Hibernando (existe mas não está ativo)

_Projetos ou tarefas que existem mas não estão recebendo atenção agora._

## Semana atual — Concluídos (DD/MM-DD/MM)

_Itens concluídos nesta semana. Visibilidade do progresso._

## Semana passada — Concluídos (DD/MM-DD/MM)

_Concluídos da semana anterior. Limpo automaticamente na revisão semanal._

---

*Última atualização: {{DATA_SETUP}}*

--- FIM ---

---

## INBOX.md

--- INÍCIO ---

# Inbox

> Itens não processados. Tudo que entra passa por aqui antes de ir pro lugar certo.
> Objetivo: este arquivo deve estar VAZIO após cada sessão de processamento.

_Inbox limpo._

--- FIM ---

---

## REGISTRO.md

--- INÍCIO ---

# Registro

> Audit trail de todos os itens processados. Permite rastrear "aquele link que entrou semana passada, onde foi parar?"

| Data | Origem | Resumo | Ação | Destino |
|------|--------|--------|------|---------|

--- FIM ---

---

## IDEIAS.md

--- INÍCIO ---

# Ideias

> Ideias sem ação imediata. Revisado na revisão semanal.
> Se uma ideia amadureceu e tem próxima ação concreta, migrar para PAUTA.md.

_Nenhuma ideia registrada ainda._

--- FIM ---

---

## Pessoal/PESSOAS.md

--- INÍCIO ---

# Pessoas

> Tracking de pessoas-chave e pendências de relacionamento.
> Atualizado no briefing quando há novidade. Revisado sistematicamente na revisão semanal.

## Pessoas-chave

_Adicione pessoas conforme forem aparecendo nas interações._

| Pessoa | Contexto | Última interação | Pendência |
|--------|----------|------------------|-----------|

## Follow-ups pendentes

_Quem precisa de resposta, retorno, ou atenção._

--- FIM ---

---

## Referencias/INDICE.md

--- INÍCIO ---

# Índice de referências

> Material de referência salvo. Artigos, relatórios, links, PDFs.
> Atualizado sempre que novo material é adicionado.

| # | Título | Arquivo | Data | Descrição | Keywords |
|---|--------|---------|------|-----------|----------|

_Última atualização: {{DATA_SETUP}}_

--- FIM ---

---

## _state/briefing-state.json

--- INÍCIO ---

{
  "last_briefing_at": ""
}

--- FIM ---

---

## [Area]/README.md (template genérico por área)

--- INÍCIO ---

# {{AREA_NAME}}

> {{AREA_DESCRIPTION}}

## Status atual

_Sem informações ainda. Será atualizado conforme o uso._

## Pendências ativas

_Nenhuma pendência registrada._

## Notas e histórico

_Registros de decisões, conversas e contexto relevante._

--- FIM ---

---

## Valores de tom por nível

### Tom: Direto

```
TOM_COBRANCA = " gentilmente"  ← ironia: a cobrança não é gentil
TOM_BRIEFING = "Tom: direto, sem puxa-saquismo, pode provocar sobre coisas paradas."
TOM_REGRA_COBRANCA = "Se algo está parado há muito tempo, cobrar. {{USER_NAME}} quer um sparring partner, não um puxa-saco. Frases como 'faz 10 dias que isso tá aqui' são bem-vindas. Não precisa ser grosso, mas não passe a mão na cabeça."
TOM_COMUNICACAO = "- Direto, sem rodeios\n- Pode usar humor sutil e provocações\n- Evitar: emojis excessivos, listas infinitas, linguagem corporativa\n- Pode e deve desafiar premissas e apontar quando algo não faz sentido\n- Sparring partner, não cheerleader"
```

### Tom: Equilibrado

```
TOM_COBRANCA = ""
TOM_BRIEFING = "Tom: claro e objetivo, sem ser agressivo. Cobrar com contexto, não com provocação."
TOM_REGRA_COBRANCA = "Se algo está parado há muito tempo, lembrar com contexto. Explicar por que o item merece atenção, sugerir próximo passo. Firme mas não provocativo."
TOM_COMUNICACAO = "- Claro e objetivo\n- Firme quando necessário, mas sempre construtivo\n- Evitar linguagem corporativa ou excessivamente formal\n- Sugerir antes de pressionar"
```

### Tom: Gentil

```
TOM_COBRANCA = ""
TOM_BRIEFING = "Tom: parceiro e solidário. Lembrar sem pressionar, sugerir sem cobrar."
TOM_REGRA_COBRANCA = "Se algo está parado, lembrar de forma leve. O objetivo é ajudar, não pressionar. Oferecer ajuda para desbloquear em vez de cobrar por que parou."
TOM_COMUNICACAO = "- Amigável e parceiro\n- Lembrar sem pressionar\n- Focar em como ajudar a avançar\n- Comemorar progressos"
```
