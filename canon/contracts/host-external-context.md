# Contrato de Contexto Externo via Host

Data de extracao: 2026-03-28

Este arquivo existe para evitar duas burrices simetricas:

1. o Prumo virar encanador de Gmail, Calendar e Drive quando o host ja faz isso direito;
2. o host despejar dado bruto no colo do Prumo como se isso ja fosse briefing.

## Principio

No MVP:

1. o host coleta;
2. o Prumo interpreta;
3. o runtime so entra como fallback, automacao futura ou suporte a host sem conector.

Em frase curta: aquisicao e do host; sentido e do Prumo.

## Escopo

Este contrato vale especialmente para:

1. Gmail
2. Google Calendar
3. Google Drive

Quando houver conector oficial, MCP ou app connector confiavel no host.

## Ordem de preferencia

Para contexto externo de Google no MVP, a ordem certa e:

1. conector oficial/MCP do host;
2. cache ou snapshot ja disponivel no workspace;
3. fallback tecnico do runtime, se houver e se realmente precisar.

O que nao faz sentido:

1. ignorar um conector bom para provar independência arquitetural;
2. chamar o runtime primeiro por reflexo;
3. abrir uma coleta artesanal em shell quando o host ja trouxe a informacao.

## O que o host deve entregar

O host nao precisa despejar o universo inteiro. Precisa trazer o suficiente para o Prumo operar.

### Gmail

Trazer, no minimo:

1. remetente
2. assunto
3. data/hora
4. snippet curto
5. sinal basico de unread / reply-needed / attachment quando existir

### Calendar

Trazer, no minimo:

1. titulo do evento
2. inicio e fim
3. timezone ou horario ja resolvido
4. local/link quando existir
5. janela relevante do dia

### Drive

Trazer, quando fizer sentido:

1. documento referenciado pela conversa atual;
2. artefato ligado ao briefing ou a uma acao do dia;
3. o minimo de texto util para decisao, nao a pasta inteira do usuario.

## O que o host nao deve fazer

1. colar thread de email inteira sem necessidade;
2. despejar agenda crua de 14 horas se o usuario so precisa do proximo bloco;
3. reformatar tudo como se estivesse escrevendo release note;
4. esconder a origem da informacao;
5. fingir que dado velho e dado fresco.

## O que o Prumo faz com isso

O Prumo continua responsavel por:

1. triagem
2. prioridade
3. briefing
4. proposta do dia
5. continuidade
6. registro no workspace

Se o host ja classificar demais, o produto fica terceirizado. Se nao classificar nada, o host vira cano sem torneira.

## Freshness e origem

Quando o host trouxer contexto externo, ele deve conseguir dizer, de forma curta:

1. de onde veio;
2. se e dado atual ou potencialmente defasado;
3. se faltou alguma parte relevante.

Exemplos bons:

1. `Agenda lida do Google Calendar connector do host.`
2. `Inbox resumida via Gmail connector; uma thread falhou e ficou de fora.`
3. `Documento veio do Google Drive connector; usei so o trecho relevante.`

## Falha parcial

Se uma fonte vier e outra nao:

1. o host preserva o que ainda presta;
2. o Prumo segue com o que houver;
3. a falta entra como nota curta, nao como funeral.

## Relação com o briefing

No briefing:

1. contexto externo entra para iluminar o dia;
2. nao entra para sequestrar a conversa;
3. a proposta do dia continua vindo da combinacao entre contexto externo e memoria local.

Sem memoria local, o Prumo vira leitor de caixa de entrada.
Sem contexto externo, o Prumo vira monge de clausura.

## Fronteira

Este contrato nao define:

1. API especifica de cada host;
2. nome de ferramenta MCP;
3. query exata de Gmail ou Calendar;
4. UI de renderizacao.

Isso e detalhe de adapter.
