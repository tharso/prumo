# Melhoria: datas de entrada em itens pendentes

## Contexto (dogfooding)
Itens na PAUTA sem data de entrada envelhecem em silêncio. Você não sabe se aquilo tá ali há 3 dias ou 3 semanas. Na prática, adicionar `(desde DD/MM)` em cada item pendente tornou a cobrança muito mais eficaz ("faz 12 dias que isso tá aqui" vs "isso tá pendente").

## O que mudar

### No `claude-md-template.md`:

**Regra 3 (PROCESSAR O INBOX)**, adicionar ao final:

```
Ao mover itens para PAUTA.md ou README de área, sempre incluir a data de entrada no formato `(desde DD/MM)`. Isso torna visível o envelhecimento de cada item e facilita cobranças na revisão semanal.
```

### No `file-templates.md` (template da PAUTA):

Adicionar exemplos com datas nos itens de "Em andamento":

```
- [Área] Descrição do item pendente. Próxima ação: X. (desde 05/02)
```

## Por que importa
Sem data, tudo parece recente. Com data, a inércia fica constrangedora. É o mecanismo mais simples de accountability do sistema.
