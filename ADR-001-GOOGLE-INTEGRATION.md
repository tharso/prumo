# ADR-001 — Integracao Google no runtime via Google APIs diretas

Status: superado para o MVP atual

Data: 2026-03-19
Atualizado em: 2026-03-28

Relacionado:

1. [#41](https://github.com/tharso/prumo/issues/41)
2. [LOCAL-RUNTIME-TRANSITION-PLAN.md](/Users/tharsovieira/Documents/DailyLife/Prumo/LOCAL-RUNTIME-TRANSITION-PLAN.md)
3. [LOCAL-RUNTIME-PHASE1-PLAN.md](/Users/tharsovieira/Documents/DailyLife/Prumo/LOCAL-RUNTIME-PHASE1-PLAN.md)
4. [Use Google Workspace connectors | Claude Help Center](https://support.claude.com/en/articles/10166901-use-google-workspace-connectors)

## Contexto original

O runtime local do Prumo precisa de uma fonte previsivel para agenda e email.

O caminho atual via `Gemini + MCP` foi util como ponte, mas falhou no papel mais importante: abastecer o briefing com consistencia. Mesmo no laboratorio `aVida`, com uma conta so (`pessoal`), o refresh continuou expirando.

Ja vimos tambem o custo politico dessa abordagem:

1. Gemini vira atravessador de algo que deveria ser integracao do produto;
2. timeout e comportamento do host parecem problema do Prumo;
3. briefing fica acoplado a uma cadeia mais temperamental do que deveria.

## Decisao original

O Prumo passa a tratar **Google APIs diretas** como direcao estrutural da integracao Google no runtime local.

Na pratica:

1. Gmail, Calendar e Drive devem ser acessados por uma camada propria do runtime;
2. Gemini+MCP deixa de ser direcao principal;
3. snapshots e caminhos intermediarios continuam valendo como ponte e fallback, nao como espinha dorsal.

Para a Fase 1, isso significa:

1. uma conta principal (`pessoal`) por padrao;
2. multi-conta fora do caminho;
3. preparar o runtime para integracao direta sem fingir que o problema vai desaparecer sozinho com mais timeout.

## Alternativas consideradas

### 1. Continuar com Gemini+MCP como fonte principal

Rejeitada.

Motivo:

1. tempo de resposta ruim;
2. dependencia excessiva de host/CLI externo;
3. comportamento imprevisivel ate com uma conta so;
4. arquitetura errada para um produto que quer ser agnostico.

### 2. Manter apenas snapshots externos via Apps Script/Drive

Parcialmente aceita como ponte.

Motivo:

1. e pragmatica;
2. ajuda a desacoplar briefing de consulta ao vivo;
3. mas nao deve ser a forma principal de integracao do runtime no longo prazo.

### 3. Integracao direta via Google APIs

Aceita.

Motivo:

1. elimina o LLM como atravessador operacional;
2. deixa o runtime dono da coleta e do cache;
3. combina com o desenho local-first;
4. torna Claude, Codex, Gemini e IDEs apenas interfaces para um motor proprio.

## Revisao de escopo do MVP

Depois da evolucao dos hosts principais, o quadro mudou.

Hoje, `Codex`, `Claude Code` e outros hosts relevantes ja oferecem conectores oficiais/MCP para Gmail, Google Calendar e Google Drive. Para o MVP, isso muda a pergunta.

A pergunta deixa de ser:

1. "como o runtime vira dono da coleta Google?"

E passa a ser:

1. "como o Prumo consome bem o que o host ja coleta?"

Por isso, esta ADR fica **superada para o MVP atual**.

O corte pragmatico agora e:

1. conectores oficiais do host como trilha preferencial de aquisicao;
2. Prumo como camada de briefing, triagem, continuidade e memoria local;
3. integracao Google direta no runtime rebaixada para fallback, automacao futura ou suporte a host sem conector.

Em portugues simples: para o MVP, o Prumo consome Google via host. Nao precisa virar provedor de Google.

## Consequencias

### Para o MVP atual

1. o runtime deixa de ser o caminho preferencial para Gmail, Calendar e Drive;
2. backlog e documentacao devem refletir conectores do host como linha principal;
3. qualquer codigo de integracao Google no runtime passa a ser considerado fallback/infra futura, nao eixo do produto.

### Positivas

1. menos engenharia duplicada;
2. menos setup no produto;
3. mais foco naquilo que so o Prumo entrega: briefing, acao, memoria e continuidade.
2. menor dependencia de plugin, marketplace e MCP do host;
3. caminho mais claro para uma interface local de configuracao de contas/fontes;
4. maior previsibilidade para cache, healthcheck e diagnostico.

### Custos

1. OAuth local passa a entrar na nossa conta;
2. seguranca e armazenamento de credenciais deixam de ser problema terceirizado;
3. implementacao inicial e mais trabalhosa do que continuar pedindo milagre ao Gemini.

## Diretrizes praticas

1. nao expandir multi-conta antes de uma conta funcionar bem;
2. tratar snapshots como fallback e transicao, nao destino final;
3. tornar a camada de integracao explicita no runtime;
4. expor no produto qual fonte esta ativa, qual conta esta conectada e quando o cache foi atualizado.

## Proximo corte recomendado

1. criar um modulo de integracao Google no runtime;
2. definir contrato de credenciais e cache local;
3. atacar primeiro Calendar e Drive;
4. depois Gmail;
5. so depois reabrir a conversa de multi-conta.
