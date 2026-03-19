# Execution Notes

Este arquivo guarda descobertas tecnicas que mudam a direcao do trabalho. Nao e diario de bordo. Nao e ata de condomínio. E o que nao pode morrer com a sessao.

## Regras

1. Registrar aqui apenas descobertas tecnicas que alterem arquitetura, estrategia de execucao ou criterio de debug.
2. Cada nota deve dizer o que foi observado, por que importa e qual decisao isso puxou.
3. Microtestes, comandos triviais e tentativas sem valor duravel nao entram.
4. Toda nota daqui deve ter espelho em issue relevante quando afetar roadmap ou execucao.

## 2026-03-19 — Runtime local antes do plugin

### Descoberta

A maior parte do atrito recente nao veio do produto Prumo em si, mas do acoplamento ao plugin do Claude/Cowork: marketplace congelado, botao de update morto, checkout local velho e versoes divergentes entre runtime, plugin e core do workspace.

### Por que importa

Esse ruido estava mascarando o estado real do produto e consumindo tempo de desenvolvimento em burocracia de host, nao em capacidade do Prumo.

### Decisao

Fase 1 passa a ser validada sem depender do plugin. O plugin vira adapter futuro, nao trilho obrigatorio de execucao.

Issue relacionada: [#41](https://github.com/tharso/prumo/issues/41)

## 2026-03-19 — O briefing local funciona; o gargalo era a coleta dual

### Descoberta

No workspace laboratorio `aVida`, `migrate`, `context-dump` e `briefing` rodaram corretamente. O problema restante nao era o runtime nem o workspace, mas a coleta dual de agenda/email via Gemini.

### Por que importa

Sem essa separacao, qualquer falha externa parecia falha do briefing inteiro.

### Decisao

Criamos `prumo snapshot-refresh` e passamos a tratar agenda/email como cache local alimentado explicitamente, em vez de obrigar o briefing a carregar o mundo nas costas toda manhã.

Issue relacionada: [#41](https://github.com/tharso/prumo/issues/41)

## 2026-03-19 — O auth check do Gemini era mais caro que o proprio refresh

### Descoberta

O script `prumo-google-dual-snapshot.sh` fazia um sanity check com `gemini -p "Diga apenas OK"` antes de consultar o MCP. Na pratica, esse check estava gastando tempo demais e virando parte relevante do timeout total. Em paralelo, `gemini mcp list` ja era suficiente para validar se o perfil estava vivo e se o MCP estava configurado.

### Por que importa

Estavamos pagando duas vezes pelo mesmo pedagio: primeiro para descobrir se o Gemini respirava, depois para fazer a consulta de verdade.

### Decisao

Remover o auth check textual, validar via `gemini mcp list`, executar os perfis em paralelo e aumentar moderadamente a janela do refresh explicito. O briefing continua preferindo cache; o refresh explicito ganha mais chance de sucesso sem transformar a manhã do usuário em fila de cartório.

Issue relacionada: [#41](https://github.com/tharso/prumo/issues/41)

## 2026-03-19 — O gargalo remanescente e a consulta Gemini, nao mais o preflight

### Descoberta

Mesmo depois de remover o auth check redundante e adicionar resgate por perfil, o `snapshot-refresh` real no laboratorio `aVida` continuou expirando. Isso empurrou o tempo total para mais de um minuto sem produzir cache util.

### Por que importa

O problema deixou de ser custo administrativo antes da consulta. Agora o gargalo esta na propria consulta ao MCP via Gemini, provavelmente pela combinacao de ferramentas, perfis e prompt ainda pesado demais para esse caminho.

### Decisao

O proximo corte tecnico nao deve ser mais um aumento cego de timeout. Deve ser uma destas coisas:

1. reduzir o escopo da consulta e/ou separar agenda de email;
2. tornar o refresh orientado por perfil;
3. trocar a fonte dessa coleta por uma via local mais previsivel.

Issue relacionada: [#41](https://github.com/tharso/prumo/issues/41)
