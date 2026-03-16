# Inbox Processing

> **module_version: 4.3.0**
>
> Fonte canônica da triagem e do commit de inbox do Prumo.

## Escopo

Vale para:

- `INBOX.md`
- `Inbox4Mobile/`
- itens de inbox detectados durante `/prumo:briefing` ou `/prumo:inbox`

## Triagem em dois estágios

### Estágio A: triagem leve

1. Se houver shell, regenerar:
   - `Inbox4Mobile/inbox-preview.html`
   - `Inbox4Mobile/_preview-index.json`
2. Se não houver shell, produzir fallback textual equivalente.
3. Se `_preview-index.json` existir, o agente DEVE linkar `inbox-preview.html` antes de abrir qualquer arquivo bruto.
4. Classificar cada item por:
   - ação: `Responder`, `Ver`, `Sem ação`
   - prioridade: `P1`, `P2`, `P3`
   - motivo objetivo

### Estágio B: aprofundamento seletivo

Abrir conteúdo bruto completo apenas quando houver:

1. item `P1`;
2. ambiguidade que impeça ação segura;
3. risco legal, financeiro ou documental;
4. solicitação explícita do usuário.

## Preview multimídia

1. Se a geração falhar mas houver preview anterior, ainda assim linkar o preview e avisar que pode estar defasado.
2. Se não houver preview utilizável, seguir com lista numerada no chat e registrar a falha.
3. No panorama do briefing, mostrar apenas o link e a contagem de itens. Não despejar arquivos individuais ali.

## Commit do inbox

Depois da triagem:

1. montar um plano único de operações pendentes;
2. pedir confirmação explícita do usuário;
3. executar em lote;
4. verificar cada operação;
5. reportar fechamento do commit.

## Operações válidas

1. mover item para `PAUTA.md` ou README da área/projeto;
2. adicionar `(desde DD/MM)` ao criar item novo;
3. se for agendado futuro, registrar `| cobrar: DD/MM`;
4. renomear arquivos com nomes descritivos;
5. registrar no `REGISTRO.md`;
6. deletar o original do inbox com ação real de filesystem.

## Deleção e fallback

1. Antes de deletar, confirmar o plano com o usuário.
2. Se a deleção falhar por permissão:
   - solicitar a permissão do runtime;
   - tentar novamente.
3. Se continuar falhando:
   - registrar `DELECAO_FALHOU` no `REGISTRO.md`;
   - marcar o item em `Inbox4Mobile/_processed.json`.
4. No próximo briefing, usar `_processed.json` para não reapresentar como novo o que já foi processado.

## Material de referência

Quando o item for referência:

1. mover para `Referencias/`;
2. renomear com padrão descritivo;
3. registrar no `Referencias/INDICE.md`;
4. remover o original do inbox.

## Regras de apresentação

1. Numerar os itens ao apresentar.
2. Oferecer alternativas de categorização quando houver ambiguidade.
3. Se sobrar item no inbox depois do commit, listar os remanescentes e dizer por quê.
