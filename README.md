# Prumo

**Sistema de organização de vida pessoal com IA.**

Versão atual: **4.15.4**

Prumo é um plugin de IA que transforma o Claude, Codex ou Gemini em interface única para capturar, processar, lembrar e cobrar tudo que acontece na sua vida. Trabalho, filhos, contas, saúde, ideias — tudo entra pelo mesmo lugar.

O detalhe novo, e importante, é que o produto começou a sair da jaula `plugin-first`. Agora existe um trilho experimental de runtime local, para o Prumo parar de depender emocionalmente do humor do marketplace do host.

A direcao estrutural para Google no runtime agora esta formalizada em [ADR-001-GOOGLE-INTEGRATION.md](/Users/tharsovieira/Documents/DailyLife/Prumo/ADR-001-GOOGLE-INTEGRATION.md): Google APIs diretas como destino, snapshots como ponte.

O contrato de invocação do produto agora também está explícito em [INVOCATION-UX-CONTRACT.md](/Users/tharsovieira/Documents/DailyLife/Prumo/INVOCATION-UX-CONTRACT.md). Serve para impedir que cada host invente uma porta diferente e depois jure que isso era estratégia.

O próximo bloco operacional também já foi explicitado em [HOST-ADAPTER-IMPLEMENTATION-PLAN.md](/Users/tharsovieira/Documents/DailyLife/Prumo/HOST-ADAPTER-IMPLEMENTATION-PLAN.md). O ponto central ali é simples: mesma família de modelo não significa mesmo host. `Cowork` e `Claude Code` são adapters diferentes. `Gemini CLI` e `Antigravity` também.

Esse plano agora também inclui um mapa de documentação oficial por host, porque desenhar adapter sem saber onde a documentação é sólida e onde ela é rala é um jeito elegante de construir ponte em neblina.

O runtime também passou a carregar, em `prumo start --format json`, metadados explícitos para adapter (`adapter_contract_version`, `workspace_resolution`, `adapter_hints`). Traduzindo: o host já não precisa bancar médium para descobrir qual porta usar.

O primeiro playbook host-específico também já existe: [CODEX-ADAPTER-PLAYBOOK.md](/Users/tharsovieira/Documents/DailyLife/Prumo/CODEX-ADAPTER-PLAYBOOK.md). Não porque o Codex seja "mais importante", mas porque alguém precisa ser o primeiro trilho asfaltado.

O segundo playbook já deixa a taxonomia mais honesta: [CLAUDE-CODE-ADAPTER-PLAYBOOK.md](/Users/tharsovieira/Documents/DailyLife/Prumo/CLAUDE-CODE-ADAPTER-PLAYBOOK.md). Ele existe justamente para impedir que `Claude Code` seja confundido com `Cowork` só porque ambos andam pela mesma família de modelos.

E o próximo corte já está preparado em [GEMINI-CLI-ADAPTER-PLAYBOOK.md](/Users/tharsovieira/Documents/DailyLife/Prumo/GEMINI-CLI-ADAPTER-PLAYBOOK.md). A lógica é simples: depois do `Codex` e do shell explícito no `Claude Code`, o próximo host limpo para validar campo é `Gemini CLI`, não o velho drama do `Cowork`.

Para email e agenda multi-conta, o fluxo preferencial agora usa snapshots privados no Google Drive gerados por Google Apps Script e gravados como Google Docs com JSON texto. O motor do Prumo também saiu do formato armário de acumulador: o core agora é índice + guardrails, com procedimento detalhado em módulos canônicos. E a sanitização deixou de ser só “compactar handover”: o sistema agora já consegue arquivar frio seguro com índice global, sem brincar de sumiço.

Seus dados ficam em arquivos Markdown no seu computador. Sem cloud, sem conta, sem lock-in.
E, a partir de agora, com um pouco mais de governo: o Prumo começou a explicitar o que pertence a `CLAUDE.md`, `PAUTA.md`, `REGISTRO.md` e histórico, em vez de fingir que tudo cabe no mesmo armário.

## O problema

Você tem 47 coisas na cabeça: o email que precisa responder, a reunião que precisa preparar, o exame que depende do pedido médico que você ainda não pediu. Aí você baixa um app de produtividade — e duas semanas depois ele virou mais uma pendência na lista de pendências.

Prumo funciona diferente: você despeja o caos, ele organiza. Sem dashboard pra manter, sem card pra arrastar, sem disciplina sobre-humana.

## Como funciona

1. **Captura** — Despeje tudo que está na sua cabeça. Texto, áudio, foto, email. Do computador ou do celular.
2. **Processamento** — Prumo separa, categoriza e extrai próximas ações. "Renovar passaporte, o Fulano manda o contrato amanhã e tive uma ideia de app" vira três itens em três contextos diferentes.
3. **Briefing diário** — Todo dia, Prumo traz o que importa: pendências, prazos, emails sem resposta, compromissos. Você só reage.
4. **Revisão semanal** — Varredura periódica pra nada cair do radar.

## Instalação

Prumo funciona com **Claude Desktop (Cowork)**, **Codex CLI** e **Gemini CLI**.

### Opção 1: Marketplace Git no Cowork (recomendada)

No Cowork, o caminho mais confiável hoje é adicionar o marketplace pelo repositório Git:

```text
https://github.com/tharso/prumo.git
```

Isso reduz o risco de catálogo congelado e evita boa parte da pantomima que a UI consegue encenar quando o checkout local envelhece parado.

### Opção 2: CLI canônico (backend do Claude)

Se você usa o backend do `claude` no terminal, este é o caminho canônico.
Para Cowork, ele ajuda, mas não substitui o store local do app quando a UI decide envelhecer sentada.

```bash
claude plugin marketplace add https://github.com/tharso/prumo.git
claude plugin install prumo@prumo-marketplace
```

Para atualizar depois:

```bash
claude plugin marketplace update prumo-marketplace
claude plugin update prumo@prumo-marketplace
```

Se quiser um instalador sóbrio, sem copiar comando em duas etapas:

```bash
bash <(curl -fsSL https://raw.githubusercontent.com/tharso/prumo/main/scripts/prumo_plugin_install.sh)
```

### Runtime local experimental

O novo trilho do produto nasce aqui. Ainda não substitui o fluxo atual do plugin, mas já permite instalar o runtime local e rodar os primeiros comandos fora da barriga do host:

```bash
bash <(curl -fsSL https://raw.githubusercontent.com/tharso/prumo/main/scripts/prumo_runtime_install.sh)
```

Depois:

```bash
prumo setup --workspace /caminho/do/workspace
cd /caminho/do/workspace
prumo start
prumo migrate --workspace /caminho/do/workspace
prumo auth google --workspace /caminho/do/workspace --client-secrets /caminho/do/client_secret.json
prumo auth google --workspace /caminho/do/workspace --client-id SEU_CLIENT_ID --client-secret SEU_CLIENT_SECRET
prumo auth apple-reminders --workspace /caminho/do/workspace
prumo snapshot-refresh --workspace /caminho/do/workspace
prumo snapshot-refresh --workspace /caminho/do/workspace --profile pessoal
prumo context-dump --workspace /caminho/do/workspace --format json
prumo briefing --workspace /caminho/do/workspace
prumo repair --workspace /caminho/do/workspace
```

Importante, para não vender andaime como se já fosse varanda:

1. `prumo ...` é a porta técnica do runtime hoje;
2. a UX final desejada do produto não é obrigar o usuário a decorar subcomandos;
3. o destino é o usuário abrir Cowork, Claude Code, Codex, Gemini CLI, Antigravity ou host equivalente e chamar o Prumo por uma porta curta (`/prumo`, `@Prumo`, `bom dia, Prumo` ou affordance parecida);
4. o host então deve encaminhar isso para o runtime local.
5. se o host consumir `prumo start --format json`, deve tratar `shell_command` e `host_prompt` como coisas diferentes. Máquina que tenta executar conversa vira liquidificador sem tampa.

Em português simples: agora estamos construindo o motor. A ignição universal vem logo depois.

O primeiro passo concreto nessa direção já existe:

```bash
cd /caminho/do/workspace
prumo
prumo start
```

`prumo` sem subcomando já cai em `start`. Não é a ignição universal final, mas pelo menos o binário deixou de responder com parser ferido quando o usuário só quer chamar o produto pelo nome. O comportamento continua o mesmo: tenta inferir o workspace pelo diretório atual (ou por um pai reconhecível), olha o estado do sistema e oferece briefing, retomada, repair ou auth/config sem pedir que o usuário adivinhe qual subcomando merece ser invocado naquela manhã.

Esse trilho cria:

1. `AGENT.md` como índice canônico do workspace;
2. `CLAUDE.md` e `AGENTS.md` como wrappers regeneráveis;
3. `Agente/` como diretório modular do contexto do usuário.

Esses wrappers já não são só placa de "veja o balcão ao lado". Agora também carregam o contrato curto de invocação para hosts que leem arquivo antes de pensar:

1. se o usuário disser `Prumo`, o host deve rodar `prumo`;
2. se o pedido for briefing explícito, o host pode rodar `prumo briefing --workspace . --refresh-snapshot`;
3. se souber renderizar ações, melhor ainda: `prumo start --format json`.

E agora também deixa uma fundação decente para integrações:

1. `_state/google-integration.json` guarda estado e metadado da conexão;
2. `_state/apple-reminders-integration.json` faz o mesmo para Apple Reminders;
3. token sensível fica fora do workspace, em storage seguro local;
4. no macOS, o runtime usa o Keychain em vez de largar refresh token no chão.

Apple Reminders entrou como trilho experimental de laboratório:

```bash
prumo auth apple-reminders --workspace /caminho/do/workspace
prumo auth apple-reminders --workspace /caminho/do/workspace --list "A vida..."
prumo config apple-reminders --workspace /caminho/do/workspace
prumo config apple-reminders --workspace /caminho/do/workspace --list "A vida..."
prumo config apple-reminders --workspace /caminho/do/workspace --all
```

Hoje ele já consegue:

1. pedir permissão local no macOS;
2. registrar estado e listas visíveis no workspace;
3. limitar listas observadas quando você quiser parar de vasculhar o universo inteiro;
4. expor esse estado no `briefing` e no `context-dump`;
5. reaproveitar cache local de Apple Reminders.

Se quiser ajustar isso depois, sem reencenar autenticação:

```bash
prumo config apple-reminders --workspace /caminho/do/workspace
prumo config apple-reminders --workspace /caminho/do/workspace --list "A vida..."
prumo config apple-reminders --workspace /caminho/do/workspace --all
```

O que ainda não está pronto o bastante para posar de produto acabado:

1. a cobertura de Apple Reminders continua experimental;
2. o runtime agora prefere `EventKit` para o fetch e deixa AppleScript como fallback, mas isso ainda não significa cobertura total da fauna Apple;
3. então, por enquanto, trate isso como fonte experimental, não como cobertura definitiva do briefing.

E deixa uma coisa explícita, porque software adora esconder isso em rodapé: se você desinstalar o Prumo, seus arquivos continuam seus, legíveis e no mesmo lugar.

Se você já tem um workspace legado (com `CLAUDE.md` e `PRUMO-CORE.md` antigos), o caminho mais seguro agora é:

```bash
prumo migrate --workspace /caminho/do/workspace
```

Esse comando:

1. cria `AGENT.md` e o schema do workspace;
2. faz backup antes de sobrescrever wrappers e `PRUMO-CORE.md`;
3. preserva o `CLAUDE.md` legado em `Agente/LEGADO-CLAUDE.md`.

Se quiser abastecer agenda/email sem obrigar o briefing a esperar coleta ao vivo:

```bash
prumo snapshot-refresh --workspace /caminho/do/workspace
```

Esse comando tenta atualizar o cache local de snapshot dual. O briefing passa a preferir esse cache por padrão, em vez de bancar o herói toda vez que a integração externa decide atrasar.

Se houver conta Google conectada via `prumo auth google`, o `snapshot-refresh` passa a preferir Calendar API e Gmail API diretas antes de cair para snapshots antigos. Em outras palavras: o runtime finalmente parou de pedir ao Gemini para fazer papel de encanador.

Agora ele também sabe quando `Tasks API` ainda não entrou na festa. Se faltarem os escopos novos, o briefing avisa que alguns lembretes do Google podem ficar de fora, em vez de jurar completude com a serenidade de um impostor bem vestido.

Na Fase 1, o runtime assume um perfil Google principal (`pessoal`) por padrão. Multi-conta ficou para depois. Antes de querer dois fogões, convém fazer um acender sem drama.

Para conectar Google direto no runtime:

```bash
prumo auth google --workspace /caminho/do/workspace --client-secrets /caminho/do/client_secret.json
prumo auth google --workspace /caminho/do/workspace --client-id SEU_CLIENT_ID --client-secret SEU_CLIENT_SECRET
```

Esse fluxo abre o navegador, pede consentimento e grava só metadado no workspace. Credencial sensível vai para o Keychain. Não porque o Prumo seja dono do segredo, mas porque guardar refresh token em Markdown seria a forma mais criativa de chamar imprudência de transparência.

Se o Google Console resolver esconder o download do JSON como se fosse herança de família, o runtime também aceita `--client-id` e `--client-secret` diretamente. Produto bom não devia depender do humor de uma UI barroca.

Depois de conectado, o `briefing` mostra explicitamente:

1. status da integração Google;
2. conta ativa;
3. último refresh útil (com idade relativa);
4. caminho de reauth quando o token morrer;
5. aviso claro quando `Tasks API` ainda nao estiver coberta pelo perfil autenticado.

Descobertas tecnicas que mudam direcao agora ficam registradas em `EXECUTION-NOTES.md`. O objetivo e simples: nao repetir a mesma escavacao toda vez que um host resolver brincar de labirinto.

### Opção 3: Doctor e update do Cowork

Se o Cowork mostrar versão velha, deixar `Atualizar` morto ou jurar que está sincronizado enquanto lê jornal de ontem:

```bash
bash <(curl -fsSL https://raw.githubusercontent.com/tharso/prumo/main/scripts/prumo_cowork_doctor.sh)
```

Se o diagnóstico apontar checkout congelado do marketplace:

```bash
bash <(curl -fsSL https://raw.githubusercontent.com/tharso/prumo/main/scripts/prumo_cowork_update.sh)
```

Depois:
1. feche totalmente o Cowork;
2. abra o app de novo;
3. se ainda precisar, remova só o plugin `Prumo` e reinstale a partir do marketplace.

### Opção 4: Marketplace por URL raw na UI

Use a URL abaixo só como compatibilidade ou debug:

```text
https://raw.githubusercontent.com/tharso/prumo/main/marketplace.json
```

Observação importante:
o fluxo por `raw` pode parecer atualizado e continuar velho por baixo. Se o app disser "comando desconhecido", travar em versão antiga ou apagar o botão de update, trate isso como drift de catálogo. Não como azar metafísico.

### Opção 5: Upload local (.zip)

Baixe o repositório e instale manualmente como pacote local. Funciona, mas envelhece mal e cobra pedágio depois.

### Após instalar

1. Abra uma nova conversa na sua plataforma (Claude Desktop, Codex ou Gemini)
2. Selecione uma pasta no seu computador para o Prumo organizar seus arquivos
3. Digite `/setup`

O setup é um wizard conversacional — uma pergunta por vez, tudo reversível. Leva uns 15 minutos.

Se preferir ir direto ao ponto: `/start` — você despeja tudo que tem na cabeça e o sistema organiza na hora.

## Comandos

No Cowork, os slash commands do Prumo aparecem sem prefixo do plugin. Use `/setup`, `/briefing`, `/doctor`, `/handover`, `/sanitize`, `/higiene` e `/start`.

| Comando | O que faz |
|---------|-----------|
| `/setup` | Setup completo (wizard de 10 etapas) |
| `/start` | Onboarding rápido — despeje e o sistema organiza |
| `/briefing` | Briefing diário (pauta, inbox, calendário, emails) |
| `/doctor` | Diagnóstico do runtime do Prumo no Cowork (store, marketplace, drift de versão) |
| `/handover` | Handover entre agentes (abrir, responder, listar, fechar) |
| `/sanitize` | Sanitiza estado operacional e arquiva histórico frio com rastreabilidade |
| `/higiene` | Diagnostica e propõe limpeza assistida do `CLAUDE.md`, separando limpeza segura, confirmação factual, governança e avisando sobre core defasado |

## Princípios

- **Tudo local.** Arquivos Markdown em pastas do seu computador. Abra com qualquer editor.
- **Sem lock-in.** Deletou o plugin? Seus arquivos continuam lá — só que melhor organizados.
- **Uma entrada.** Sua vida não tem departamentos. Prumo também não.
- **Proativo.** Prumo não espera você checar. Traz o que importa na hora certa.

## Estrutura do repositório

```
├── plugin.json              # Manifest do plugin
├── marketplace.json         # Manifest do marketplace
├── runtime/                 # Runtime local experimental
├── commands/                # Slash commands (/setup, /briefing, etc.)
├── cowork-plugin/           # Pacote de runtime (skills, scripts, referências)
├── CHANGELOG.md             # Histórico de mudanças
└── VERSION                  # Versão atual
```

## Compatibilidade

- Claude Desktop (Cowork)
- Codex CLI
- Gemini CLI

## Diagnóstico rápido

Se aparecer "comando desconhecido" após instalar/atualizar, o suspeito principal é sessão velha, app sem restart, comando digitado com prefixo errado ou marketplace congelado num checkout velho.
Feche a conversa, abra uma nova, teste o autocomplete de `/setup`, `/briefing`, `/doctor`, `/handover`, `/sanitize`, `/higiene` e, se preciso, reinicie o Cowork antes de decretar bug no plugin.

Se o painel do app disser que atualizou, mas o plugin continuar em versão velha ou sumirem comandos novos, rode o `doctor` do Cowork. O painel às vezes sorri e não faz o serviço. Concierge de hotel ruim.

## Versão

Versão atual: `4.13.1`

## Licença

MIT

---

[prumo.me](https://prumo.me)
