# Auditoria do repo: canon, adapter, capability, workaround e oficina

Status: auditoria operacional da Wave 1a  
Data: 2026-03-28

Relacionados:

1. [PRUMO-CAPABILITY-BACKEND-ARCHITECTURE.md](/Users/tharsovieira/Documents/DailyLife/Prumo/PRUMO-CAPABILITY-BACKEND-ARCHITECTURE.md)
2. [GITHUB-ISSUE-BACKLOG-CAPABILITY-BACKEND.md](/Users/tharsovieira/Documents/DailyLife/Prumo/GITHUB-ISSUE-BACKLOG-CAPABILITY-BACKEND.md)
3. [REPO-WORKSPACE-JURISDICTION.md](/Users/tharsovieira/Documents/DailyLife/Prumo/REPO-WORKSPACE-JURISDICTION.md)
4. [COWORK-PLUGIN-ROLE-DECISION.md](/Users/tharsovieira/Documents/DailyLife/Prumo/COWORK-PLUGIN-ROLE-DECISION.md)

## 1. Veredicto curto

O repo nao esta esquizofrenico. Mas esta claramente **estratificado em epocas**:

1. uma camada viva e forte de runtime local;
2. uma camada legado-util do plugin Cowork;
3. uma camada de planos, playbooks e docs historicos;
4. uma camada de oficina que estava mal nomeada e ja foi separada como `.workbench/`;
5. uma pequena camada de sedimento e scaffolding morto.

Em portugues simples: nao e um repositorio em ruinas. Mas tambem nao e um jardim japones. Ele parece mais uma casa boa que foi ampliada tres vezes por moradores competentes e impacientes.

## 2. Regra de classificacao usada

Nesta auditoria, cada area cai principalmente em uma destas caixas:

1. **canon**: regra de produto que deveria sobreviver ao host
2. **adapter**: casca, comando, skill ou manifesto especifico de host
3. **capability**: motor tecnico reutilizavel do runtime
4. **workaround historico**: ponte de transicao ou compatibilidade de epoca
5. **oficina**: coordenacao interna de desenvolvimento
6. **sedimento**: resquicio, placeholder ou material que nao deveria orientar nada

## 3. Fotografia rapida do repo

Contagem por area:

1. `runtime/`: 58 arquivos
2. `cowork-plugin/`: 59 arquivos
3. `commands/`: 8 arquivos
4. `docs/`: 18 arquivos
5. `github-issues/`: 14 arquivos
6. `.claude-plugin/`: 2 arquivos
7. `.github/`: 1 arquivo
8. `scripts/`: 8 arquivos
9. `skills/`: 2 arquivos efetivos e sem corpo real
10. `_lixeira/`: 110 arquivos
11. `.workbench/`: 5 arquivos

O numero que interessa nao e o bruto. E o contraste:

1. `runtime/` e `cowork-plugin/` ainda dividem o coracao do produto;
2. `skills/` no topo esta praticamente morto;
3. `_lixeira/` e volumosa, mas explicitamente nao canônica;
4. `docs/` segue larga demais como nome, mesmo tendo material util.

## 4. Mapa por area

## 4.1 `runtime/`

Classificacao principal:

1. **capability**
2. **canon**, em partes

Evidencia:

1. [runtime/prumo_runtime/cli.py](/Users/tharsovieira/Documents/DailyLife/Prumo/runtime/prumo_runtime/cli.py) define a porta tecnica oficial do produto
2. [runtime/prumo_runtime/workspace.py](/Users/tharsovieira/Documents/DailyLife/Prumo/runtime/prumo_runtime/workspace.py) define schema, arquivos gerados, repair e migrate
3. [runtime/prumo_runtime/templates.py](/Users/tharsovieira/Documents/DailyLife/Prumo/runtime/prumo_runtime/templates.py) ja carrega parte do canon do workspace
4. [runtime/prumo_runtime/daily_operator.py](/Users/tharsovieira/Documents/DailyLife/Prumo/runtime/prumo_runtime/daily_operator.py) concentra parte da orquestracao do produto
5. a cobertura de testes em [runtime/tests](/Users/tharsovieira/Documents/DailyLife/Prumo/runtime/tests) mostra que essa camada ja e a mais disciplinada do repo

Leitura honesta:

1. o runtime ja e o motor tecnico do produto
2. ele tambem ja carrega regra de produto demais para ser chamado so de "backend burro"
3. a fronteira entre capability e canon ainda nao foi totalmente extraida

Recomendacao:

1. tratar `runtime/` como area principal de capabilities
2. extrair para area canonica separada as regras de produto que hoje ainda estao embutidas em `templates.py`, `workspace.py` e `daily_operator.py`

## 4.2 `cowork-plugin/`

Classificacao principal:

1. **adapter**
2. **canon herdado**
3. **workaround historico**

Evidencia:

1. [plugin.json](/Users/tharsovieira/Documents/DailyLife/Prumo/plugin.json) e [marketplace.json](/Users/tharsovieira/Documents/DailyLife/Prumo/marketplace.json) ainda apontam para essa arvore como pacote publicavel
2. skills como [cowork-plugin/skills/briefing/SKILL.md](/Users/tharsovieira/Documents/DailyLife/Prumo/cowork-plugin/skills/briefing/SKILL.md) ja funcionam como bridge para o runtime
3. a pasta [cowork-plugin/skills/prumo/references/modules](/Users/tharsovieira/Documents/DailyLife/Prumo/cowork-plugin/skills/prumo/references/modules) ainda guarda muita regra canônica de produto
4. os smokes em [cowork-plugin/scripts/tests](/Users/tharsovieira/Documents/DailyLife/Prumo/cowork-plugin/scripts/tests) mostram que o plugin virou camada de compatibilidade e verificacao do runtime

Leitura honesta:

1. o `cowork-plugin` nao e mais o centro do produto
2. tambem nao e descartavel
3. ele hoje e uma mistura de adapter legado, bundle de distribuicao e deposito de sabedoria operacional ainda nao extraida

Recomendacao:

1. congelar o plugin como origem de **novas** regras host-agnosticas
2. mantê-lo como adapter legado suportado e bundle de compatibilidade
3. extrair gradualmente o canon herdado da pasta `references/`

## 4.3 `cowork-plugin/skills/prumo/references/`

Classificacao principal:

1. **canon herdado**

Evidencia forte:

1. [modules/interaction-format.md](/Users/tharsovieira/Documents/DailyLife/Prumo/cowork-plugin/skills/prumo/references/modules/interaction-format.md) define disciplina de interface que vale para mais de um host
2. [modules/load-policy.md](/Users/tharsovieira/Documents/DailyLife/Prumo/cowork-plugin/skills/prumo/references/modules/load-policy.md) define politica incremental de leitura
3. [modules/runtime-file-governance.md](/Users/tharsovieira/Documents/DailyLife/Prumo/cowork-plugin/skills/prumo/references/modules/runtime-file-governance.md) define jurisdicao documental
4. [references/prumo-core.md](/Users/tharsovieira/Documents/DailyLife/Prumo/cowork-plugin/skills/prumo/references/prumo-core.md) ainda e fonte textual de regras do sistema
5. [references/apps-script-setup.md](/Users/tharsovieira/Documents/DailyLife/Prumo/cowork-plugin/skills/prumo/references/apps-script-setup.md) e os templates `.gs` ainda sao documentacao util de integracao

Leitura honesta:

1. esta area e o maior extrato bancario da "sabedoria acidental" do plugin
2. ela tem valor demais para continuar escondida dentro de um adapter especifico
3. boa parte da `Wave 1b` existe justamente por causa disso

Recomendacao:

1. tratar essa area como principal mina de extracao de canon
2. decompor a issue `#50` em subblocos baseados nesses modulos, nao em refatoracao genérica

## 4.4 `commands/`

Classificacao principal:

1. **adapter**
2. **compatibilidade historica**

Evidencia:

1. [commands/prumo.md](/Users/tharsovieira/Documents/DailyLife/Prumo/commands/prumo.md) se assume como alias legado
2. [commands/start.md](/Users/tharsovieira/Documents/DailyLife/Prumo/commands/start.md) e os outros arquivos sao descritores de slash command / host command

Leitura honesta:

1. isso nao e canon do produto
2. isso tambem nao e lixo
3. e casca de host e compatibilidade de distribuicao

Recomendacao:

1. manter como adapter docs enquanto Cowork seguir suportado
2. nao deixar regra sistemica nascer aqui

## 4.5 `.claude-plugin/`, `plugin.json` e `marketplace.json`

Classificacao principal:

1. **adapter/distribuicao**
2. **compatibilidade historica**

Evidencia:

1. `.claude-plugin/plugin.json` e [plugin.json](/Users/tharsovieira/Documents/DailyLife/Prumo/plugin.json) sao virtualmente espelhos
2. [marketplace.json](/Users/tharsovieira/Documents/DailyLife/Prumo/marketplace.json) continua necessario para o fluxo Cowork/Claude

Leitura honesta:

1. essas duplicacoes sao feias, mas hoje sao funcionais
2. sao duplicacao de manifesto, nao duplicacao de inteligencia do produto

Recomendacao:

1. tolerar a duplicacao enquanto houver suporte real a Cowork/Claude plugin marketplace
2. proteger via teste/sync, nao via indignacao moral

## 4.6 `docs/`

Classificacao principal:

1. **documentacao de produto e integracao**
2. **naming frouxo**

Evidencia:

1. [bridges/google-apps-script/apps-script-setup.md](/Users/tharsovieira/Documents/DailyLife/Prumo/bridges/google-apps-script/apps-script-setup.md) e material util
2. [docs/stories/us-001-antigravity-adapter.md](/Users/tharsovieira/Documents/DailyLife/Prumo/docs/stories/us-001-antigravity-adapter.md) e story valida
3. `docs/` tambem acumulava drafts ignorados de issues antes da limpeza

Leitura honesta:

1. `docs/` nao esta errada como conteudo
2. esta errada como nome-guarda-chuva

Recomendacao:

1. reorganizar por papel em momento oportuno
2. nao usar `docs/` como deposito de qualquer markdown que apareceu de madrugada

## 4.7 `github-issues/`

Classificacao principal:

1. **artefato de desenvolvimento rastreavel**

Leitura honesta:

1. e um bom meio-termo entre backlog vivo no GitHub e rascunho no repo
2. ajuda a impedir que a memoria da execucao viva so em comentario de issue

Recomendacao:

1. manter
2. usar para drafts rastreaveis, nao para substituir o GitHub

## 4.8 `.workbench/`

Classificacao principal:

1. **oficina**

Leitura honesta:

1. agora esta no lugar certo conceitualmente
2. nao e produto
3. nao e workspace do usuario

Recomendacao:

1. manter ignorado
2. nao deixar nenhum documento versionado tratar isso como `_state/`

## 4.9 `skills/`

Classificacao principal:

1. **sedimento / scaffolding morto**

Evidencia:

1. a pasta tem praticamente so `.DS_Store` e um esqueleto vazio
2. o produto real nao esta saindo daqui

Leitura honesta:

1. esse diretorio hoje mais confunde do que ajuda

Recomendacao:

1. marcar para limpeza futura
2. nao usar como area canônica de extensao enquanto estiver vazia e ambigua

## 4.10 `_lixeira/`

Classificacao principal:

1. **sedimento arquivado**

Leitura honesta:

1. nao deve orientar arquitetura
2. tambem nao precisa ser tratado como problema urgente enquanto estiver fora da linha de fogo

## 4.11 Docs de plano e playbooks na raiz

Classificacao principal:

1. **documentacao operacional**
2. **contexto historico**

Exemplos:

1. [LOCAL-RUNTIME-TRANSITION-PLAN.md](/Users/tharsovieira/Documents/DailyLife/Prumo/LOCAL-RUNTIME-TRANSITION-PLAN.md)
2. [LOCAL-RUNTIME-PHASE1-PLAN.md](/Users/tharsovieira/Documents/DailyLife/Prumo/LOCAL-RUNTIME-PHASE1-PLAN.md)
3. [HOST-ADAPTER-IMPLEMENTATION-PLAN.md](/Users/tharsovieira/Documents/DailyLife/Prumo/HOST-ADAPTER-IMPLEMENTATION-PLAN.md)
4. playbooks por host

Leitura honesta:

1. sao documentos validos
2. mas nem todos sao "canon atual"
3. varios ja viraram contexto historico importante, nao contrato de presente

Recomendacao:

1. deixar claro em cada documento seu status real
2. evitar que plano antigo concorra com plano novo como se ambos mandassem em igual medida

## 5. Duplicacoes relevantes

## 5.1 Manifestos de plugin

Duplicacao aceitavel:

1. [plugin.json](/Users/tharsovieira/Documents/DailyLife/Prumo/plugin.json)
2. [.claude-plugin/plugin.json](/Users/tharsovieira/Documents/DailyLife/Prumo/.claude-plugin/plugin.json)
3. [marketplace.json](/Users/tharsovieira/Documents/DailyLife/Prumo/marketplace.json)
4. [.claude-plugin/marketplace.json](/Users/tharsovieira/Documents/DailyLife/Prumo/.claude-plugin/marketplace.json)

Isto e distribuicao. Nao e a pior duplicacao do repo.

## 5.2 Regras de produto entre runtime e referencias do plugin

Duplicacao perigosa:

1. templates e wrappers no runtime
2. `prumo-core.md` e modulos em `cowork-plugin/skills/prumo/references/`
3. briefing/orquestracao parcialmente no runtime e parcialmente nos modulos do plugin

Isto sim e o coracao da `Wave 1b`.

## 5.3 Planos e backlog

Duplicacao toleravel, mas precisa de hierarquia:

1. planos historicos de runtime local
2. novo backlog capability-backend
3. playbooks host-specificos

Se isso nao tiver status claro, cada doc vira papa de uma igreja pequena.

## 6. Sedimentos e alertas

## 6.1 `skills/` vazio

Alerta:

1. parece lugar canônico
2. nao e usado de verdade

Conclusao:

1. ou ganha funcao clara
2. ou sai da frente

## 6.2 `docs/issues/` ignorado

Alerta:

1. havia drafts importantes indo para uma area ignorada
2. isso ja foi corrigido com `github-issues/`

Conclusao:

1. nao voltar a usar `docs/issues/` como backlog vivo

## 6.3 `_state` duplicado

Alerta resolvido:

1. `_state/` do usuario e `.workbench/` do repo agora estao separados conceitualmente e fisicamente

## 7. Decisoes operacionais recomendadas

## 7.1 O que conta como canon hoje

Canon hoje nao esta num unico lugar. Esta repartido entre:

1. runtime (`workspace.py`, `templates.py`, `daily_operator.py`)
2. referencias modulares do plugin em `cowork-plugin/skills/prumo/references/`
3. contratos e docs canônicos mais novos na raiz

Isso confirma que a issue `#50` nao e detalhe. E cirurgia principal.

## 7.2 O que conta como adapter hoje

1. `cowork-plugin/skills/*` fora da pasta `references/`
2. `commands/`
3. manifests de plugin/marketplace
4. playbooks por host

## 7.3 O que conta como capability hoje

1. comandos do runtime
2. providers/integracoes
3. repair/migrate/setup/start/briefing/inbox-preview/context-dump

## 7.4 O que conta como workaround historico hoje

1. bridge do Cowork para runtime
2. alias legados de comando
3. duplicacao de manifests
4. parte dos fluxos de fallback descritos nas skills do plugin

## 8. Conclusao

O repo ja tem um motor melhor do que tinha.

O que ainda nao tem e uma fronteira suficientemente limpa entre:

1. **motor tecnico**
2. **canon de produto**
3. **casca de host**

Por isso a conclusao operacional desta auditoria e simples:

1. `runtime/` vira centro declarado das capabilities
2. `cowork-plugin/` continua vivo, mas rebaixado a adapter legado suportado
3. `cowork-plugin/skills/prumo/references/` vira mina oficial de extracao de canon
4. `commands/`, manifests e playbooks continuam como casca de host e distribuicao
5. `skills/` no topo entra na fila de limpeza futura
6. `.workbench/` segue como backstage local e ignorado

O repo nao precisa de terapia de casal. Precisa de inventario, cerca e retroescavadeira na hora certa.
