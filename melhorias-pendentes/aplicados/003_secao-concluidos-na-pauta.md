# Melhoria: seção de concluídos na PAUTA

## Contexto (dogfooding)
A PAUTA original só tinha itens pendentes. Adicionar uma seção "Semana atual — Concluídos" com itens riscados (~~item~~ ✓) mudou a dinâmica: dá visibilidade ao progresso, motiva nas revisões, e serve como mini-changelog semanal. Na revisão de domingo, os concluídos migram pra "Semana passada" e depois somem.

## O que mudar

### No `file-templates.md` (template da PAUTA):

Adicionar duas seções ao final da PAUTA, antes de "Notas do sistema":

```markdown
## Semana atual — Concluídos (DD/MM-DD/MM)

- ~~[Tag] Descrição do item concluído~~ ✓ Detalhes (data)

## Semana passada — Concluídos (DD/MM-DD/MM)

- ~~[Tag] Descrição~~ ✓ Detalhes
```

### No `claude-md-template.md` (Revisão semanal):

Adicionar ao ritual de revisão:

```
- Mover itens de "Semana atual — Concluídos" para "Semana passada"
- Limpar "Semana passada" anterior (já tem 2+ semanas, não precisa mais)
```

## Por que importa
Sistemas que só mostram o que falta fazer são deprimentes. A seção de concluídos é o contrapeso psicológico. "Olha quanta coisa saiu essa semana" é combustível pra continuar.
