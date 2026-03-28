# Orquestracao do Briefing

Data de extracao: 2026-03-28

Este arquivo define a partitura compartilhada do briefing do Prumo. O runtime coleta e executa. O host conversa e conduz. Nenhum dos dois deveria improvisar um briefing paralelo como se estivesse montando feira livre.

## Objetivo

O briefing deve:

1. situar o dia no fuso certo;
2. resumir estado operacional sem afogar o usuario;
3. propor o proximo movimento mais sensato;
4. permitir aprofundamento sob demanda;
5. documentar e persistir o estado certo.

## Passos canonicos

### 0. Pre-carga

Antes de abrir o briefing:

1. ler `AGENT.md`;
2. ler `PRUMO-CORE.md`;
3. aplicar a `load-policy`;
4. garantir que o workspace exista de verdade.

### 1. Preflight

Antes do panorama:

1. checar se o motor ou core local estao defasados;
2. avisar diferenca de versao sem sequestrar a manha inteira;
3. oferecer alternativas curtas quando houver decisao real.

### 2. Estado operacional

Ler, no minimo:

1. `PAUTA.md`;
2. `INBOX.md`;
3. estado tecnico relevante (`last_briefing_at`, interrupcao, refresh de integracoes);
4. pendencias operacionais que nao podem ser ignoradas.

### 3. Fontes primarias

Usar a melhor fonte disponivel na ordem certa:

1. conector oficial/MCP do host, quando ele existir e estiver saudavel;
2. snapshots estruturados e caches confiaveis;
3. fallback tecnico do runtime, quando realmente precisar.

Se uma fonte falhar:

1. preservar dado parcial;
2. avisar a limitacao em uma linha;
3. seguir, se o briefing ainda puder respirar.

### 4. Persistir abertura

Antes da primeira resposta com panorama e proposta:

1. persistir `last_briefing_at`;
2. limpar estado de interrupcao anterior quando couber;
3. validar que a persistencia aconteceu.

Sem isso, o briefing nao abriu. So fez pose.

### 5. Panorama

Entregar automaticamente:

1. data correta no fuso do usuario;
2. agenda consolidada;
3. estado resumido da inbox;
4. alertas operacionais que realmente importam;
5. numeração contínua.

Quando houver contexto externo vindo do host:

1. usar isso para iluminar agenda, email e documentos do dia;
2. nao despejar dado bruto no palco principal;
3. marcar origem e freshness de forma curta quando isso afetar confianca.

No panorama:

1. nao despejar arquivo bruto;
2. nao abrir conteudo profundo sem gatilho;
3. nao transformar o usuario em operador de central de monitoramento.

### 6. Proposta do dia

Oferecer proposta concreta considerando:

1. deadlines;
2. blockers;
3. agenda disponivel;
4. itens com cobranca elegivel;
5. continuidade de trabalho.

Quando houver escolha:

1. usar alternativas curtas e respondiveis;
2. evitar cardapio gigante;
3. permitir `a) aceitar e seguir`.

### 7. Detalhe sob demanda

Se o usuario pedir detalhe:

1. mostrar contexto completo relevante;
2. manter numeracao continua;
3. nao resetar o fluxo;
4. preservar as opcoes abertas quando ainda fizerem sentido.

### 8. Escape hatch

Se o usuario quiser parar:

1. gravar interrupcao e ponto de retomada;
2. manter `last_briefing_at` ja aberto;
3. encerrar sem cobranca adicional.

### 9. Escrita e fechamento

Depois do briefing:

1. atualizar `PAUTA.md` se algo mudou;
2. registrar acoes em `REGISTRO.md`;
3. manter os artefatos tecnicos sincronizados;
4. limpar estado de interrupcao quando o fluxo concluiu normalmente.

## Guardrails

1. briefing e progressivo;
2. primeira resposta nao abre bruto por vaidade;
3. persistencia vem antes de prosa;
4. erro tecnico nao autoriza teatro explicativo interminavel;
5. fonte parcial e melhor do que mentira inteira;
6. briefing nao pode depender de detalhe especifico de um host.

## Fronteira

Este arquivo define o fluxo compartilhado.

Ele nao define:

1. o bridge do Cowork;
2. shell paths;
3. affordance visual de cada host;
4. implementacao de snapshot por provider.

Isso mora em runtime e adapters.
