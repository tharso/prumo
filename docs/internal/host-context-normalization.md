# Contrato de Normalizacao de Contexto Externo

Data de extracao: 2026-03-28

Este arquivo responde a uma pergunta chata e inevitavel:

"Se o host coleta Gmail, Calendar e Drive por conta propria, em que formato isso precisa chegar para o Prumo pensar sem virar peneira de JSON?"

## Principio

O host pode coletar contexto externo com a ferramenta que quiser.
O Prumo nao deveria precisar decifrar o dialeto bruto de cada conector.

O contrato de normalizacao existe para garantir:

1. previsibilidade;
2. pouco atrito entre hosts;
3. briefing consistente;
4. menos acoplamento a provider especifico.

## Regra-mãe

O host nao precisa entregar o payload cru do conector.
Tambem nao deve entregar uma narrativa pronta.

Ele deve entregar blocos normalizados o suficiente para o Prumo:

1. resumir;
2. priorizar;
3. propor proximo passo;
4. registrar no workspace.

## Envelope minimo

Quando houver contexto externo, o host deve conseguir produzir algo equivalente a:

```json
{
  "source": "host-connector",
  "provider": "google",
  "freshness": {
    "status": "fresh",
    "captured_at": "2026-03-28T09:10:00-03:00",
    "note": ""
  },
  "agenda_today": [],
  "agenda_tomorrow": [],
  "emails": {
    "reply": [],
    "view": [],
    "no_action": [],
    "note": ""
  },
  "documents": [],
  "errors": []
}
```

Nao precisa ser literalmente esse JSON.
Precisa respeitar essa ideia.

## Agenda

Cada item de agenda deve trazer, no minimo:

1. `label` curto para leitura humana;
2. `start` e `end` quando existirem;
3. `day_bucket` (`today` ou `tomorrow`);
4. `source_hint` curto quando isso importar.

Exemplo bom:

```json
{
  "label": "10:00-11:00 | Reuniao com Brise",
  "start": "2026-03-28T10:00:00-03:00",
  "end": "2026-03-28T11:00:00-03:00",
  "day_bucket": "today",
  "source_hint": "Google Calendar connector"
}
```

## Email

O host nao deve despejar a inbox inteira. Deve entregar triagem minima.

Cada item de email deve trazer:

1. `priority` (`P1`, `P2`, `P3` ou vazio);
2. `from`;
3. `subject`;
4. `snippet` curto;
5. `received_at`;
6. `reason` curto quando a classificacao nao for obvia.

Buckets:

1. `reply`
2. `view`
3. `no_action`

Exemplo bom:

```json
{
  "priority": "P1",
  "from": "Danilo",
  "subject": "Ajuste no contrato",
  "snippet": "Preciso da sua validacao hoje...",
  "received_at": "2026-03-28T08:40:00-03:00",
  "reason": "pedido com prazo curto"
}
```

## Documentos

Drive entra quando um documento realmente ajuda a decidir o dia.

Cada documento deve trazer:

1. `title`;
2. `kind` (`doc`, `sheet`, `slide`, `file`);
3. `why_relevant`;
4. `excerpt` curto ou `summary` curto;
5. `url` quando o host puder fornecer.

Se o host abrir 19 documentos para “garantir contexto”, ele nao esta ajudando. Esta montando entulho.

## Freshness

O host deve conseguir dizer se o contexto esta:

1. `fresh`
2. `stale`
3. `partial`
4. `unknown`

E, quando couber:

1. `captured_at`
2. `note`

Sem isso, o Prumo acaba tratando dado de ontem como se tivesse acabado de sair do forno.

## Erros e faltas

Quando algo falhar, o host deve registrar em `errors[]` com:

1. `area` (`agenda`, `email`, `documents`);
2. `summary` curto;
3. `recoverable` (`true` ou `false`).

Exemplo:

```json
{
  "area": "documents",
  "summary": "Drive connector nao conseguiu abrir o doc da reuniao",
  "recoverable": true
}
```

## O que nao normalizar demais

Nao vale a pena o host tentar normalizar:

1. tom de voz;
2. proposta do dia;
3. proximo movimento;
4. decisao final de prioridade do trabalho.

Isso ainda e do Prumo.

## Regra de bolso

Se o payload ainda exige conhecer o schema cru do conector, normalizou pouco.
Se o payload ja parece a resposta final ao usuario, normalizou demais.

O ponto bom e o meio: dados suficientes para decidir, magros o bastante para viajar entre hosts sem virar mudança de casa.
