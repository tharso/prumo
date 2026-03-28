# Apps Script setup para snapshots de email e calendar

Os templates rastreáveis para copiar no Apps Script ficam aqui:

1. [email-snapshot-personal-template.gs](/Users/tharsovieira/Documents/DailyLife/Prumo/bridges/google-apps-script/email-snapshot-personal-template.gs)
2. [email-snapshot-work-template.gs](/Users/tharsovieira/Documents/DailyLife/Prumo/bridges/google-apps-script/email-snapshot-work-template.gs)

Os dois arquivos têm a mesma estrutura. A única diferença real é `CONFIG.expectedAccount`. Isso é deliberado: se você colar o script da conta errada, ele falha cedo, em vez de gerar snapshot no lugar errado e te dar uma falsa sensação de controle.

Antes de colar no Apps Script, substitua:

1. `PERSONAL_ACCOUNT_EMAIL` pelo email da conta pessoal
2. `WORK_ACCOUNT_EMAIL` pelo email da conta de trabalho

## O que o script faz

1. Lê Gmail da conta onde está rodando e pega emails recebidos desde `since` (se não passar nada, usa 24h)
2. Lê eventos do Google Calendar de hoje e amanhã
3. Grava ou sobrescreve um Google Doc `Prumo/snapshots/email-snapshot` no Google Drive da mesma conta
4. Cria as pastas `Prumo/` e `Prumo/snapshots/` se não existirem
5. Grava JSON parcial se Gmail ou Calendar falharem, usando `emails_error` e `calendar_error`
6. Inclui `version: "1.0"` para migrações futuras
7. Tem helper para instalar trigger de 15 minutos sem web app público
8. Mantém o conteúdo como JSON texto dentro do Google Doc, para o leitor do Drive conseguir consumir sem truque

## Como o briefing deve consumir isso

O contrato esperado hoje é este:

1. procurar primeiro por um Google Doc `Prumo/snapshots/email-snapshot` nas contas conectadas;
2. ler o texto do Doc e parsear o JSON contido ali como fonte primária de email e agenda multi-conta;
3. avisar se `generated_at` estiver com mais de 30 minutos;
4. respeitar `emails_error` e `calendar_error` como falha parcial, sem fingir que deu tudo certo;
5. se o Doc faltar ou estiver inválido, cair para os fallbacks do runtime sem quebrar o briefing.

## Estrutura do snapshot

```json
{
  "version": "1.0",
  "account": "user@example.com",
  "generated_at": "2026-03-16T08:45:00-03:00",
  "since": "2026-03-15T09:00:00-03:00",
  "emails": [
    {
      "id": "18f2b4...",
      "from": "nome <email@dominio.com>",
      "subject": "assunto",
      "date": "2026-03-16T07:30:00-03:00",
      "snippet": "max 200 chars",
      "labels": ["INBOX", "UNREAD"],
      "has_attachments": false
    }
  ],
  "calendar": {
    "today": [
      {
        "title": "evento",
        "start": "2026-03-16T10:00:00-03:00",
        "end": "2026-03-16T11:00:00-03:00",
        "location": "link ou sala",
        "attendees_count": 3
      }
    ],
    "tomorrow": []
  },
  "emails_error": "opcional",
  "calendar_error": "opcional"
}
```

## Como subir o script da conta pessoal

1. Entre em [script.google.com](https://script.google.com/) logado na sua conta pessoal.
2. Crie um projeto novo. Pode chamar de `Prumo Email Snapshot (pessoal)`.
3. Em `Project Settings`, ajuste o timezone para `America/Sao_Paulo`.
4. Apague o conteúdo padrão de `Code.gs`.
5. Cole o conteúdo de [email-snapshot-personal-template.gs](/Users/tharsovieira/Documents/DailyLife/Prumo/bridges/google-apps-script/email-snapshot-personal-template.gs) em `Code.gs`.
6. Troque `PERSONAL_ACCOUNT_EMAIL` pelo email real dessa conta.
7. Salve.
8. Execute a função `runSnapshot` uma vez pelo editor.
9. Aceite as permissões pedidas.
10. Verifique no Drive dessa conta se o Google Doc `Prumo/snapshots/email-snapshot` apareceu.
11. Execute a função `installOrRefreshTrigger` uma vez.
12. Abra `Triggers` no menu lateral e confirme que existe um gatilho time-driven de 15 minutos para `runSnapshot`.

## Como subir o script da conta de trabalho

1. Saia da conta errada antes de começar.
2. Entre em [script.google.com](https://script.google.com/) logado na sua conta de trabalho.
3. Crie um projeto novo. Pode chamar de `Prumo Email Snapshot (trabalho)`.
4. Em `Project Settings`, ajuste o timezone para `America/Sao_Paulo`.
5. Apague o conteúdo padrão de `Code.gs`.
6. Cole o conteúdo de [email-snapshot-work-template.gs](/Users/tharsovieira/Documents/DailyLife/Prumo/bridges/google-apps-script/email-snapshot-work-template.gs) em `Code.gs`.
7. Troque `WORK_ACCOUNT_EMAIL` pelo email real dessa conta.
8. Salve.
9. Execute `runSnapshot` uma vez e autorize os acessos.
10. Verifique no Drive dessa conta se `Prumo/snapshots/email-snapshot` foi criado como Google Doc.
11. Execute `installOrRefreshTrigger`.
12. Confirme em `Triggers` o agendamento de 15 minutos para `runSnapshot`.

## Compartilhamento entre contas

Se o host/briefing roda autenticado só na conta pessoal do Google Drive, a snapshot da conta de trabalho não vai ficar visível sem compartilhamento:

1. Na conta de trabalho, compartilhe a pasta `Prumo/snapshots` com a conta pessoal leitora.
2. Permissão recomendada: `Leitor`.
3. Depois confirme na conta pessoal que o arquivo compartilhado aparece em `Compartilhados comigo` ou na busca.

Sem essa ponte, o Apps Script da conta de trabalho funciona, mas o briefing continua cego de um olho.

## Escopos e permissões

Os acessos esperados são:

1. Gmail leitura (`GmailApp`)
2. Calendar leitura (`CalendarApp`)
3. Drive escrita/leitura do documento (`DriveApp` + `DocumentApp`)
4. Gerenciamento de triggers (`ScriptApp`)
5. Identidade da conta para validação (`Session`)

## Funções disponíveis

1. `runSnapshot()` usa `since = agora - 24h`
2. `runSnapshot('2026-03-16T09:00:00-03:00')` roda com timestamp customizado
3. `installOrRefreshTrigger()` remove triggers antigos de `runSnapshot` e cria um novo de 15 min
4. `removeSnapshotTriggers()` limpa triggers desse projeto

## Comportamento de erro

1. Se Gmail falhar, o script ainda grava o JSON com `emails: []` e `emails_error`
2. Se Calendar falhar, o script ainda grava o JSON com `calendar.today = []`, `calendar.tomorrow = []` e `calendar_error`
3. Se o Drive ou o Google Docs falharem, a execução falha de verdade

## Notas práticas

1. O snippet do email é truncado para 200 caracteres e normalizado para uma linha só
2. O script filtra mensagens enviadas pela própria conta para focar em emails recebidos
3. O campo `location` usa `event.getLocation()` e, se estiver vazio, tenta achar a primeira URL na descrição do evento
4. O Google Doc é sobrescrito no mesmo path a cada execução
5. Se você já criou `email-snapshot.json` na versão anterior, pode ignorar ou apagar depois. O briefing novo deve passar a usar o Doc
6. Para esse caso, você não precisa usar `Deploy > New deployment`
