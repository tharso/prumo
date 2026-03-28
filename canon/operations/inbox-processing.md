# Inbox Processing

Data de extracao: 2026-03-28

Este arquivo define a triagem e o commit de inbox do Prumo. Inbox bom e aquele que vira rota. Nao aquele que acumula como garagem onde ja nem o carro entra.

## Escopo

Vale para:

1. `INBOX.md`;
2. `Inbox4Mobile/`;
3. itens detectados durante briefing ou fluxo de inbox.

## Triagem em dois estagios

### Estagio A. Triagem leve

1. preferir preview e indice quando existirem;
2. se houver preview, linkar antes de abrir bruto;
3. classificar cada item por:
   - acao: `Responder`, `Ver`, `Sem acao`
   - prioridade: `P1`, `P2`, `P3`
   - motivo objetivo

### Estagio B. Aprofundamento seletivo

Abrir conteudo bruto apenas quando houver:

1. item `P1`;
2. ambiguidade que impeca acao segura;
3. risco legal, financeiro ou documental;
4. pedido explicito do usuario.

## Preview multimidia

1. se a geracao falhar e houver preview anterior, usar o preview e avisar defasagem;
2. se nao houver preview, seguir com fallback textual equivalente;
3. no panorama do briefing, mostrar link e contagem, nao despejar o porao inteiro no hall.

## Commit do inbox

Depois da triagem:

1. montar um plano unico de operacoes;
2. pedir confirmacao explicita quando o commit alterar material do usuario;
3. executar em lote;
4. verificar cada operacao;
5. reportar fechamento do commit.

## Operacoes validas

1. mover item para `PAUTA.md`;
2. mover item para contexto modular ou referencia;
3. adicionar marca temporal quando nascer nova pendencia;
4. registrar o que foi feito em `REGISTRO.md`;
5. renomear arquivo para nome descritivo;
6. deletar o original apenas com acao real e verificavel.

## Fallback de delecao

Se a delecao falhar:

1. tentar de novo com permissao ou caminho correto;
2. se ainda falhar, registrar a falha;
3. marcar o item como processado para nao reaparecer como recem-nascido zumbi.

## Contrato minimo de item processado

Quando houver rastreio de fallback:

1. preservar o nome do arquivo original;
2. registrar timestamp ISO;
3. indicar status de processamento;
4. guardar motivo objetivo.

## Regras de apresentacao

1. numerar os itens ao apresentar;
2. oferecer alternativas curtas quando houver ambiguidade;
3. se sobrar item no inbox depois do commit, listar remanescentes e dizer por que ficaram.
