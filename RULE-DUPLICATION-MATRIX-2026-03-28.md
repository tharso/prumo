# Matriz de Duplicacao de Regras

Data: 2026-03-28

Este documento fecha a issue de duplicacoes sem perfumar o problema. O repo nao tem "muitos jeitos de dizer a mesma coisa". Ele tem, em alguns pontos centrais, a mesma lei morando em tres delegacias diferentes.

O criterio aqui e simples:

1. separar regra de produto de detalhe de host;
2. decidir qual fonte sobrevive;
3. parar de usar README e playbook como esconderijo de canon.

## Resumo executivo

Hoje, a duplicacao relevante se concentra em seis familias:

1. invocacao e porta curta;
2. briefing e lifecycle diario;
3. disciplina conversacional e persona operacional;
4. politica de leitura e hidratacao de contexto;
5. governanca documental;
6. higiene / limpeza e inbox processing.

O diagnostico seco e este:

1. o plugin ainda guarda a maior parte do canon fino;
2. o runtime ja implementa parte do comportamento executavel;
3. os docs de topo fazem papel de contrato, mas repetem regra demais;
4. wrappers e templates do runtime ja reproduzem trechos que ainda nao foram extraidos para uma casa neutra.

## Matriz

| Familia de regra | Onde vive hoje | Natureza real | Fonte que deve sobreviver | Destino recomendado |
|---|---|---|---|---|
| Invocacao / porta curta | `INVOCATION-UX-CONTRACT.md`; `runtime/prumo_runtime/commands/start.py`; templates `AGENT.md`/wrappers; `README.md`; `cowork-plugin/.../agents-md-template.md`; `cowork-plugin/.../cowork-runtime-bridge.md` | Contrato de produto + hints executaveis + detalhe de host | Contrato explicito de invocacao + runtime como implementacao | Canon compartilhado de invocacao; wrappers e `adapter_hints` viram derivados |
| Briefing / lifecycle diario | `cowork-plugin/.../modules/briefing-procedure.md`; `cowork-plugin/.../prumo-core.md`; `runtime/prumo_runtime/commands/briefing.py`; `LOCAL-RUNTIME-PHASE1-PLAN.md`; `README.md` | Orquestracao de produto + fallback de host + execucao tecnica | Procedimento compartilhado de orquestracao + runtime como executor | Canon compartilhado de briefing; bridge Cowork fica separado |
| Disciplina conversacional / persona | `cowork-plugin/.../modules/interaction-format.md`; `cowork-plugin/.../prumo-core.md`; `runtime/prumo_runtime/commands/start.py`; `ANTIGRAVITY-ADAPTER-PLAYBOOK.md`; `PRUMO-PLUGIN-VS-RUNTIME-COMPARISON.md` | Regra de UX do produto | `interaction-format.md` e guardrails correlatos | Canon compartilhado de interface/persona; playbooks passam a referenciar |
| Politica de leitura / load policy | `cowork-plugin/.../modules/load-policy.md`; `cowork-plugin/.../prumo-core.md`; `briefing-procedure.md`; templates `AGENT.md` | Regra de hidratacao de contexto | `load-policy.md` | Canon compartilhado de load policy; templates derivam hints minimos |
| Governanca documental | `cowork-plugin/.../modules/runtime-file-governance.md`; `cowork-plugin/.../claude-hygiene.md`; `runtime/prumo_runtime/templates.py`; `runtime/prumo_runtime/workspace.py`; `REPO-WORKSPACE-JURISDICTION.md`; `README.md` | Regra de produto + estrutura de workspace + higiene assistida | `runtime-file-governance.md` como base; jurisdicao repo/workspace como regra de dev | Canon compartilhado de governanca; templates/workspace viram implementacao; higiene host-specific vira adaptador |
| Inbox processing | `cowork-plugin/.../modules/inbox-processing.md`; `briefing-procedure.md`; `runtime/prumo_runtime/commands/briefing.py` | Procedimento de triagem e commit | `inbox-processing.md` | Canon compartilhado de inbox; runtime passa a obedecer esse contrato |
| Higiene / sanitizacao | `cowork-plugin/.../modules/claude-hygiene.md`; `cowork-plugin/.../modules/sanitization.md`; scripts legados; docs de backlog | Mistura de regra geral com detalhe do `CLAUDE.md` e automacao historica | Separar regra geral de higiene de detalhe do `CLAUDE.md` | Canon de higiene + adapters especificos por arquivo/host |
| Update / bridge / runtime paths | `cowork-plugin/.../modules/version-update.md`; `cowork-plugin/.../modules/cowork-runtime-bridge.md`; `runtime-paths.md`; `README.md` | Detalhe de distribuicao e compatibilidade | Nao devem virar canon puro | Permanecem em adapter/distribuicao e docs operacionais |

## Leituras por familia

### 1. Invocacao

Duplicacao real:

1. [INVOCATION-UX-CONTRACT.md](/Users/tharsovieira/Documents/DailyLife/Prumo/INVOCATION-UX-CONTRACT.md) ja descreve o contrato de produto;
2. [runtime/prumo_runtime/commands/start.py](/Users/tharsovieira/Documents/DailyLife/Prumo/runtime/prumo_runtime/commands/start.py) implementa `adapter_hints` e a logica de descoberta;
3. [runtime/prumo_runtime/templates.py](/Users/tharsovieira/Documents/DailyLife/Prumo/runtime/prumo_runtime/templates.py) replica parte do mesmo contrato nos wrappers;
4. [cowork-plugin/skills/prumo/references/agents-md-template.md](/Users/tharsovieira/Documents/DailyLife/Prumo/cowork-plugin/skills/prumo/references/agents-md-template.md) ainda carrega a variante legacy;
5. [cowork-plugin/skills/prumo/references/modules/cowork-runtime-bridge.md](/Users/tharsovieira/Documents/DailyLife/Prumo/cowork-plugin/skills/prumo/references/modules/cowork-runtime-bridge.md) mistura regra geral com excecao do Cowork.

Decisao:

1. o contrato sobrevive fora do plugin;
2. `start.py` continua sendo implementacao e JSON oficial;
3. wrappers passam a ser material derivado, nao lugar de invencao.

### 2. Briefing

Duplicacao real:

1. [cowork-plugin/skills/prumo/references/modules/briefing-procedure.md](/Users/tharsovieira/Documents/DailyLife/Prumo/cowork-plugin/skills/prumo/references/modules/briefing-procedure.md) e hoje a fonte mais rica do lifecycle;
2. [cowork-plugin/skills/prumo/references/prumo-core.md](/Users/tharsovieira/Documents/DailyLife/Prumo/cowork-plugin/skills/prumo/references/prumo-core.md) repete guardrails do briefing;
3. [runtime/prumo_runtime/commands/briefing.py](/Users/tharsovieira/Documents/DailyLife/Prumo/runtime/prumo_runtime/commands/briefing.py) implementa parte relevante da coleta, snapshots, estado e proposta;
4. [README.md](/Users/tharsovieira/Documents/DailyLife/Prumo/README.md) e [LOCAL-RUNTIME-PHASE1-PLAN.md](/Users/tharsovieira/Documents/DailyLife/Prumo/LOCAL-RUNTIME-PHASE1-PLAN.md) repetem regra para compensar a falta de casa unica.

Decisao:

1. o procedimento de briefing precisa ser extraido para uma area neutra;
2. `briefing.py` passa a obedecer esse canon em vez de competir com ele;
3. detalhes de bridge do Cowork saem do procedimento compartilhado.

### 3. Disciplina conversacional

Duplicacao real:

1. [cowork-plugin/skills/prumo/references/modules/interaction-format.md](/Users/tharsovieira/Documents/DailyLife/Prumo/cowork-plugin/skills/prumo/references/modules/interaction-format.md) ja e canon de fato;
2. [cowork-plugin/skills/prumo/references/prumo-core.md](/Users/tharsovieira/Documents/DailyLife/Prumo/cowork-plugin/skills/prumo/references/prumo-core.md) repete guardrails de continuidade;
3. [runtime/prumo_runtime/commands/start.py](/Users/tharsovieira/Documents/DailyLife/Prumo/runtime/prumo_runtime/commands/start.py) embute tom e algumas regras de interface no texto;
4. [ANTIGRAVITY-ADAPTER-PLAYBOOK.md](/Users/tharsovieira/Documents/DailyLife/Prumo/ANTIGRAVITY-ADAPTER-PLAYBOOK.md) e docs de comparacao carregam parte da disciplina como comentario de campo.

Decisao:

1. `interaction-format.md` vence;
2. playbooks de host passam a apontar para essa regra, nao a reescreve-la;
3. o runtime nao deve continuar semeando persona em strings soltas como quem esconde contrato em papel de pao.

### 4. Load policy

Duplicacao real:

1. [cowork-plugin/skills/prumo/references/modules/load-policy.md](/Users/tharsovieira/Documents/DailyLife/Prumo/cowork-plugin/skills/prumo/references/modules/load-policy.md) define base, leitura leve e aprofundamento;
2. [cowork-plugin/skills/prumo/references/prumo-core.md](/Users/tharsovieira/Documents/DailyLife/Prumo/cowork-plugin/skills/prumo/references/prumo-core.md) repete a politica em resumo;
3. [cowork-plugin/skills/prumo/references/modules/briefing-procedure.md](/Users/tharsovieira/Documents/DailyLife/Prumo/cowork-plugin/skills/prumo/references/modules/briefing-procedure.md) depende dela;
4. [runtime/prumo_runtime/templates.py](/Users/tharsovieira/Documents/DailyLife/Prumo/runtime/prumo_runtime/templates.py) hoje injeta apenas a ordem de leitura do `AGENT.md`, sem um modulo compartilhado correspondente.

Decisao:

1. `load-policy.md` sobrevive;
2. o resto referencia;
3. quando o runtime precisar desse contrato, deve consumi-lo por derivacao ou reimplementacao consciente, nao por folklore.

### 5. Governanca documental

Duplicacao real:

1. [cowork-plugin/skills/prumo/references/modules/runtime-file-governance.md](/Users/tharsovieira/Documents/DailyLife/Prumo/cowork-plugin/skills/prumo/references/modules/runtime-file-governance.md) define jurisdicao de `CLAUDE.md`, `PAUTA.md` e `REGISTRO.md`;
2. [cowork-plugin/skills/prumo/references/modules/claude-hygiene.md](/Users/tharsovieira/Documents/DailyLife/Prumo/cowork-plugin/skills/prumo/references/modules/claude-hygiene.md) aplica a regra no host legacy;
3. [runtime/prumo_runtime/templates.py](/Users/tharsovieira/Documents/DailyLife/Prumo/runtime/prumo_runtime/templates.py) e [runtime/prumo_runtime/workspace.py](/Users/tharsovieira/Documents/DailyLife/Prumo/runtime/prumo_runtime/workspace.py) codificam parte da mesma estrutura;
4. [REPO-WORKSPACE-JURISDICTION.md](/Users/tharsovieira/Documents/DailyLife/Prumo/REPO-WORKSPACE-JURISDICTION.md) resolve a fronteira repo/workspace/oficina, mas e regra de desenvolvimento, nao do produto para o usuario.

Decisao:

1. separar governanca de produto da jurisdicao de desenvolvimento;
2. extrair o miolo de produto para area canonica;
3. deixar templates e `workspace.py` como implementacao da topologia, nao como cartorio concorrente.

### 6. Inbox processing

Duplicacao real:

1. [cowork-plugin/skills/prumo/references/modules/inbox-processing.md](/Users/tharsovieira/Documents/DailyLife/Prumo/cowork-plugin/skills/prumo/references/modules/inbox-processing.md) guarda taxonomia, commit, `_processed.json` e roteamento;
2. [cowork-plugin/skills/prumo/references/modules/briefing-procedure.md](/Users/tharsovieira/Documents/DailyLife/Prumo/cowork-plugin/skills/prumo/references/modules/briefing-procedure.md) o invoca;
3. [runtime/prumo_runtime/commands/briefing.py](/Users/tharsovieira/Documents/DailyLife/Prumo/runtime/prumo_runtime/commands/briefing.py) ja coleta preview e resume parte da fila, mas nao aponta para uma casa canonica fora do plugin.

Decisao:

1. `inbox-processing.md` vira candidato claro a canon compartilhado;
2. o runtime passa a referenciar a mesma taxonomia;
3. README para de repetir isso em forma de manifesto informal.

### 7. Higiene e sanitizacao

Duplicacao real:

1. [cowork-plugin/skills/prumo/references/modules/claude-hygiene.md](/Users/tharsovieira/Documents/DailyLife/Prumo/cowork-plugin/skills/prumo/references/modules/claude-hygiene.md) mistura regra geral de governanca com o caso especifico de `CLAUDE.md`;
2. [cowork-plugin/skills/prumo/references/modules/sanitization.md](/Users/tharsovieira/Documents/DailyLife/Prumo/cowork-plugin/skills/prumo/references/modules/sanitization.md) carrega automacao historica;
3. backlog e docs mais novos falam em higiene, limpeza assistida e delegacao otimista em lugares separados.

Decisao:

1. separar "politica geral de higiene" de "higiene do `CLAUDE.md`";
2. o caso `CLAUDE.md` vira adapter/host-specific ou arquivo-specific;
3. a politica geral vira canon reutilizavel para `AGENT.md`, `PAUTA.md` e outras memorias vivas.

## O que deve morrer como fonte de verdade

Nao precisa morrer como documentacao historica. Precisa morrer como autoridade silenciosa.

1. `README.md` como lugar de regra fina;
2. playbooks de host como lugar de canon de produto;
3. `PRUMO-CORE.md` do plugin como agregador de regras que ja deveriam estar modularizadas fora dele;
4. strings de `start.py` e wrappers como fonte primaria de disciplina conversacional;
5. qualquer template que continue ensinando regra sem apontar para a casa canonica.

## Ordem recomendada de consolidacao

1. invocacao;
2. disciplina conversacional;
3. load policy;
4. governanca documental;
5. briefing;
6. inbox processing;
7. higiene.

Se inverter isso e tentar extrair o briefing inteiro antes de dar casa para interface, leitura e governanca, o produto vai mudar de endereco com as caixas ainda abertas. Sempre termina com prato quebrado.

## Resultado pratico desta matriz

1. a duplicacao importante foi localizada;
2. a principal fonte herdada continua sendo `cowork-plugin/skills/prumo/references/modules/`;
3. o runtime ja implementa bastante coisa, mas ainda com canon insuficientemente desacoplado;
4. a extracao do canon agora pode ser feita por fatias, nao por devocao abstrata a "refatorar o plugin".
