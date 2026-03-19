# Plano de transição: Prumo como runtime local com adapters finos

Status: proposta de arquitetura

Relacionado:

- Issue pública: [#40](https://github.com/tharso/prumo/issues/40)
- Contexto atual: [PLUGIN-MIGRATION-PHASES.md](/Users/tharsovieira/Documents/DailyLife/Prumo/PLUGIN-MIGRATION-PHASES.md)
- Operação atual do Cowork: [COWORK-MARKETPLACE-PLAYBOOK.md](/Users/tharsovieira/Documents/DailyLife/Prumo/COWORK-MARKETPLACE-PLAYBOOK.md)

## 1. Problema que estamos realmente tentando resolver

O Prumo nasceu com promessa de ser sistema de organização local-first, agnóstico a modelo e a host. Na prática, o desenvolvimento recente gastou energia demais com:

1. comportamento de plugin/marketplace do Claude/Cowork;
2. bugs e caches de runtime de terceiros;
3. versionamento partido entre repo, plugin, marketplace, workspace e UI.

Isso cria três distorções:

1. bug de plataforma parece bug do Prumo;
2. o produto começa a ser desenhado para o host, não para o usuário;
3. a promessa de portabilidade vira discurso bonito com sapato apertado.

Em português menos diplomático: estamos discutindo o porteiro do prédio enquanto o prédio ainda está decidindo se quer ser casa, hotel ou shopping.

## 2. Tese de produto

O Prumo não deve ser “um plugin do Claude”.

O Prumo deve ser:

1. um runtime local instalado na máquina do usuário;
2. com estado e lógica canônicos fora do host;
3. com adapters finos para hosts diferentes:
   - Claude/Cowork
   - Codex
   - Gemini
   - IDEs

Plugin deixa de ser arquitetura. Vira distribuição e interface.

## 3. Decisão estratégica proposta

### 3.1. O que manter

Manteremos:

1. `workspace` do usuário como fonte de verdade do estado vivo:
   - `CLAUDE.md`
   - `PAUTA.md`
   - `INBOX.md`
   - `REGISTRO.md`
   - `_state/`
2. módulos e contratos já consolidados do Prumo;
3. adapters/plugin onde eles fizerem sentido como canal de entrada.

### 3.2. O que mudar

Moveremos a lógica canônica para um runtime local do Prumo.

Esse runtime passa a ser responsável por:

1. comando canônico;
2. resolução de módulos;
3. versionamento;
4. update e migração;
5. telemetria local;
6. integração com ferramentas externas;
7. diagnósticos de ambiente e drift.

### 3.3. O que não fazer

Não faremos:

1. reescrever todo o produto de uma vez;
2. depender de um daemon pesado só para parecer “plataforma”;
3. mover os dados do usuário para banco fechado ou cloud;
4. tornar o workspace irrelevante;
5. transformar adapters em fontes concorrentes de verdade.

## 4. Arquitetura alvo

### 4.1. Camadas

O produto passa a ter quatro camadas explícitas.

#### Camada 1: Workspace do usuário

Pasta escolhida pelo usuário (ex.: `DailyLife/`).

Responsabilidade:

1. armazenar estado e contexto do usuário;
2. continuar legível e útil sem o Prumo;
3. permanecer local-first e auditável.

#### Camada 2: Runtime local do Prumo

Instalação fora do workspace, por exemplo:

- `~/.prumo/`
- `~/Library/Application Support/Prumo/`

Responsabilidade:

1. carregar módulos canônicos;
2. expor comandos;
3. rodar scripts;
4. checar versão;
5. aplicar migrações seguras;
6. coordenar adapters;
7. centralizar conectores locais e diagnósticos.

#### Camada 3: Adapters de host

Peças finas para cada ambiente:

1. Cowork/Claude plugin
2. Codex adapter
3. Gemini adapter
4. IDE adapter

Responsabilidade:

1. receber input do host;
2. encaminhar para o runtime local;
3. devolver resposta formatada;
4. expor affordances do host (slash commands, autocomplete, menus, etc.).

Esses adapters não carregam regra canônica de negócio.

#### Camada 4: Integrações externas

Exemplos:

1. Google Apps Script snapshots
2. Gmail/Calendar/Drive
3. shell local
4. browser automation
5. possíveis conectores OAuth próprios no futuro

Responsabilidade:

1. trazer dados para o runtime;
2. nunca virar o próprio runtime.

## 5. Estrutura proposta do runtime

Uma estrutura inicial plausível:

```text
~/.prumo/
├── VERSION
├── runtime/
│   ├── commands/
│   ├── modules/
│   ├── scripts/
│   ├── adapters/
│   │   ├── cowork/
│   │   ├── codex/
│   │   ├── gemini/
│   │   └── ide/
│   ├── manifests/
│   └── templates/
├── cache/
├── logs/
├── migrations/
└── config/
```

No repositório, isso corresponderia a uma nova área canônica, sem matar o pacote atual no primeiro dia.

## 6. Contrato de execução

### 6.1. Comando canônico

O produto deve poder ser chamado assim:

```bash
prumo setup
prumo briefing
prumo doctor
prumo sanitize
prumo higiene
prumo handover
```

Cada comando:

1. recebe o caminho do workspace;
2. resolve módulos do runtime;
3. lê/escreve arquivos do workspace;
4. devolve saída estruturada para o host.

### 6.2. Contrato de adapter

Cada adapter deve implementar, no mínimo:

1. descoberta de comando;
2. passagem de contexto do host;
3. passagem do workspace ativo;
4. rendering da resposta;
5. fallback claro quando o host não suporta determinada capacidade.

### 6.3. Contrato de módulo

Cada módulo do Prumo deve declarar:

1. objetivo;
2. entradas mínimas;
3. arquivos que lê;
4. arquivos que escreve;
5. scripts auxiliares que pode chamar;
6. guardrails.

Hoje boa parte disso já existe em Markdown. A transição é mais de execução do que de semântica.

## 7. Atualizações

### 7.1. Problema atual

Hoje update mistura:

1. atualização do plugin;
2. atualização do marketplace;
3. atualização do core no workspace;
4. drift de cache/UI.

Isso é um casamento poliamoroso sem combinado.

### 7.2. Modelo proposto

Separar update em três operações distintas.

#### A. Update do runtime

```bash
prumo self-update
```

Responsável por:

1. atualizar runtime local;
2. atualizar módulos, scripts, adapters e manifests;
3. não tocar no conteúdo do workspace do usuário.

#### B. Migração do workspace

```bash
prumo migrate /caminho/do/workspace
```

Responsável por:

1. atualizar arquivos gerados pelo sistema;
2. criar backups;
3. aplicar mudanças compatíveis;
4. registrar migrações no `REGISTRO.md` ou `_state/`.

#### C. Update do adapter

Exemplo:

1. plugin do Cowork atualizado pelo próprio host;
2. extensão da IDE atualizada pela loja da IDE.

Se o adapter estiver um pouco atrás, o runtime ainda continua sendo a fonte da verdade.

### 7.3. Princípio

Runtime e workspace precisam poder ficar um pouco fora de sincronia sem virar colapso teatral.

## 8. Skills e módulos

### 8.1. O erro a evitar

“Skill do Claude” não pode continuar sendo o recipiente canônico de lógica do Prumo.

### 8.2. Modelo proposto

As skills passam a ser vistas como:

1. módulos do Prumo;
2. com representações específicas por host quando necessário.

Exemplo:

- módulo canônico: `briefing`
- adapter Cowork: slash command `/briefing`
- adapter Codex: comando ou skill que chama `prumo briefing`
- adapter Gemini: idem

### 8.3. Consequência

O centro de gravidade sai do host e volta para o produto.

## 9. Multi-LLM e IDEs

### 9.1. Cenário realista

“Agnóstico” não significa “funciona idêntico em qualquer superfície do universo”.

Significa:

1. o motor é um só;
2. a casca muda;
3. as limitações do host são explicitadas.

### 9.2. Claude/Cowork

Bom para:

1. slash commands;
2. UX conversacional;
3. distribuição.

Risco:

1. marketplace/store/cache.

### 9.3. Codex

Bom para:

1. shell;
2. arquivos locais;
3. operação em repo;
4. automação previsível.

Pode ser um dos melhores hosts para operação séria do Prumo.

### 9.4. Gemini CLI

Bom para:

1. acesso local e shell quando disponível;
2. outra superfície LLM sem dependência do ecossistema Claude.

### 9.5. IDEs

Modelo plausível:

1. extensão mínima;
2. command palette chama `prumo ...`;
3. output aparece em painel da IDE;
4. edição continua local.

Boa integração para quem vive em editor. Péssima ideia se a extensão tentar reinventar o runtime.

### 9.6. Web chat puro

Sem acesso a arquivos ou shell local, o valor cai.

Pode haver modo assistido/manual, mas não deve ser o caso canônico.

## 10. Integrações externas

### 10.1. Curto prazo

Continuar usando integrações pragmáticas, como:

1. snapshots via Apps Script e Drive;
2. shell;
3. browser automation quando necessário.

### 10.2. Médio prazo

Avaliar conectores próprios do runtime para:

1. Gmail
2. Calendar
3. Drive
4. outros serviços recorrentes

### 10.3. Princípio

Integração deve servir ao runtime local. Não capturá-lo.

## 11. Plano de transição

### Fase 0: Congelar a ambição errada

Objetivo:

1. declarar plugin como adapter, não como motor;
2. documentar isso como posição oficial do produto.

Entregas:

1. este plano;
2. alinhamento de docs;
3. decisão explícita de arquitetura.

### Fase 1: Extrair o runtime canônico

Objetivo:

1. criar CLI `prumo`;
2. mover comandos canônicos para o runtime local;
3. manter compatibilidade com o workspace atual.

Entregas:

1. `prumo setup`
2. `prumo briefing`
3. `prumo doctor`
4. `prumo sanitize`
5. `prumo higiene`
6. `prumo handover`

Risco:

1. duplicar lógica entre runtime novo e plugin velho.

Mitigação:

1. adapter do Cowork deve começar a delegar cedo ao runtime.

### Fase 2: Tornar o Cowork um adapter fino

Objetivo:

1. manter UX boa no Cowork;
2. retirar do plugin a responsabilidade por lógica central.

Entregas:

1. slash commands chamando runtime local;
2. redução do pacote distribuído;
3. menos estado escondido no host.

### Fase 3: Adapters para Codex e Gemini

Objetivo:

1. provar que o Prumo é de fato host-agnostic;
2. manter paridade funcional mínima entre superfícies.

Entregas:

1. adapter Codex
2. adapter Gemini
3. contrato de compatibilidade por host

### Fase 4: IDE adapter

Objetivo:

1. permitir uso dentro do fluxo de trabalho de editor;
2. sem reconstruir o produto como extensão monolítica.

### Fase 5: Integrações próprias

Objetivo:

1. reduzir dependência de MCPs e conectores do host;
2. trazer olhos e mãos para dentro do runtime do Prumo.

## 12. Critérios de sucesso

O plano será bem-sucedido se, ao final da transição:

1. update do produto não depender do humor do marketplace do host;
2. o mesmo workspace funcionar com Claude, Codex e Gemini com diferenças previsíveis;
3. bug de host não parecer automaticamente bug do Prumo;
4. módulos do produto não dependerem de instrução enterrada em plugin específico;
5. o usuário puder trocar de interface sem sentir que mudou de produto.

## 13. Riscos reais

1. querer fazer tudo de uma vez e produzir um segundo sistema quebrado;
2. subestimar o trabalho de adapter;
3. cair na tentação de criar um daemon complexo sem necessidade;
4. perder simplicidade local-first por excesso de engenharia;
5. demorar demais para começar a extrair o runtime e continuar preso ao plugin por inércia.

## 14. Decisões recomendadas agora

1. Aprovar a tese: Prumo é runtime local com adapters finos.
2. Tratar plugin/marketplace como canal, não centro.
3. Planejar a Fase 1 como próxima frente concreta de execução.
4. Pedir crítica externa de Cowork e Gemini antes da implementação.

## 15. Perguntas em aberto para a rodada de crítica

1. O runtime deve nascer como CLI puro ou CLI + biblioteca interna?
2. O adapter do Cowork deve chamar shell diretamente ou um pequeno bridge estável?
3. Qual é o contrato mínimo de paridade entre Cowork, Codex e Gemini?
4. Em que momento vale investir em conectores próprios, em vez de seguir com snapshots/arquivos intermediários?
5. Qual é o menor recorte de Fase 1 que prova a tese sem reescrever metade do produto?

## 16. Recomendação final

Não abandonar plugin. Rebaixá-lo.

Plugin é elevador. Runtime é prédio.

Se tratarmos elevador como arquitetura, cada manutenção vira crise existencial. Se tratarmos elevador como acesso, a engenharia volta para o lugar certo.
