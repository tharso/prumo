# Decisao: papel do cowork-plugin na arquitetura atual

Status: decisao operacional da Wave 1a  
Data: 2026-03-28

Relacionados:

1. [AUDIT-CANON-ADAPTER-MAP-2026-03-28.md](/Users/tharsovieira/Documents/DailyLife/Prumo/AUDIT-CANON-ADAPTER-MAP-2026-03-28.md)
2. [PRUMO-CAPABILITY-BACKEND-ARCHITECTURE.md](/Users/tharsovieira/Documents/DailyLife/Prumo/PRUMO-CAPABILITY-BACKEND-ARCHITECTURE.md)
3. [PRUMO-PLUGIN-VS-RUNTIME-COMPARISON.md](/Users/tharsovieira/Documents/DailyLife/Prumo/PRUMO-PLUGIN-VS-RUNTIME-COMPARISON.md)
4. Issue [#46](https://github.com/tharso/prumo/issues/46)

## 1. Decisao em uma frase

O `cowork-plugin` passa a ser tratado como **adapter legado suportado e bundle de distribuicao**, em **processo de emagrecimento**, e **nao** como lugar legitimo para nascer regra host-agnostica nova.

## 2. O que isso significa na pratica

## 2.1 O plugin continua existindo

Nao vamos apagar o `cowork-plugin` nem enterrá-lo com pressa de decorador de apartamento alugado.

Ele continua necessario para:

1. distribuicao no ecossistema Cowork/Claude plugin
2. compatibilidade com usuarios existentes
3. comando e skill de host enquanto Cowork seguir suportado
4. ponte de transicao para o runtime em contextos ainda nao totalmente migrados

## 2.2 O plugin deixa de ser origem de produto

Daqui para frente:

1. regra de produto nova nasce fora do adapter
2. canon novo nasce em area canônica ou no runtime quando for capability real
3. o plugin consome, adapta e distribui
4. o plugin nao volta a ser apartamento inteiro do produto

## 2.3 O plugin ainda guarda sabedoria operacional real

O fato de ele deixar de ser origem futura nao significa que sua historia ja foi extraida.

Hoje ele ainda guarda:

1. modulos de briefing
2. disciplina de interface
3. politica de leitura incremental
4. governanca documental
5. heuristicas de continuidade e compatibilidade

Por isso a postura correta nao e abandono. E extracao.

## 3. Por que esta e a decisao correta

## 3.1 O repo ja mudou de centro de gravidade

Evidencias:

1. [README.md](/Users/tharsovieira/Documents/DailyLife/Prumo/README.md) ja trata `Antigravity` e `Codex` como trilhos prioritarios
2. o runtime ja concentra CLI, templates, workspace schema, migrate, repair, start e briefing
3. a qualidade de cobertura e testes esta no runtime, nao no plugin

Conclusao:

1. fingir que o plugin ainda e o centro do produto seria fanfic com versionamento

## 3.2 O plugin ainda e util demais para ser jogado fora

Evidencias:

1. [plugin.json](/Users/tharsovieira/Documents/DailyLife/Prumo/plugin.json) e [marketplace.json](/Users/tharsovieira/Documents/DailyLife/Prumo/marketplace.json) continuam ativos
2. a arvore `cowork-plugin/skills/prumo/references/` ainda tem canon herdado que nao foi todo reencarnado
3. os smokes do plugin ainda cobrem parte importante do trilho de compatibilidade

Conclusao:

1. aposentadoria imediata seria vaidade, nao engenharia

## 3.3 O maior risco seria continuar no meio-termo

O modelo que nao serve mais:

1. plugin continua vivo
2. runtime cresce
3. regra nasce nos dois
4. docs justificam a bagunca depois

Isso daria:

1. duas fontes de verdade
2. tres tipos de fallback
3. uma bela colecao de regressao emocional

## 4. Politica daqui para frente

## 4.1 O que pode continuar nascendo no plugin

1. wrapper de host especifico
2. command metadata
3. manifesto de distribuicao
4. bridge de compatibilidade para Cowork
5. ajustes necessarios para continuar entregando a experiencia nesse host

## 4.2 O que nao deve mais nascer no plugin

1. regra host-agnostica nova
2. governanca documental nova
3. orquestracao principal do produto
4. contrato canonico de memoria
5. decisao estrutural de runtime

## 4.3 O que deve ser extraido do plugin

Prioridades:

1. disciplina conversacional
2. load policy
3. governanca documental
4. briefing/orquestracao herdados
5. material de setup e templates que ainda sejam canonicos

## 5. Definicao operacional do papel do cowork-plugin

O `cowork-plugin` passa a ter quatro papeis legitimos:

1. **adapter Cowork**
2. **bundle de distribuicao**
3. **casca de compatibilidade**
4. **fonte historica de extracao de canon**

E deixa de ter um papel:

1. **centro vivo da inteligencia do produto**

## 6. Implicacoes para a execucao

## 6.1 Para a issue de auditoria

A auditoria deve tratar a pasta `cowork-plugin/skills/prumo/references/` como mina principal de extracao de canon, e o resto da arvore como adapter e compatibilidade.

## 6.2 Para a issue de extracao de canon

A issue `#50` nao deve tentar "refatorar o plugin". Deve:

1. inventariar o que e regra host-agnostica ali
2. mover isso para casa propria
3. deixar o plugin mais magro depois

## 6.3 Para o roadmap

Nao faz sentido abrir feature host-agnostica nova primeiro no plugin.

O fluxo correto passa a ser:

1. decidir no canon
2. implementar em capability ou area canônica
3. adaptar no host
4. manter compatibilidade no plugin se necessario

## 7. Criterio para revisitar esta decisao

Esta decisao deve ser revisitida so se um destes fatos mudar:

1. Cowork voltar a ser host prioritario de produto, o que hoje nao e o caso
2. o plugin deixar de ser necessario como bundle real de distribuicao
3. a extracao do canon for concluida a ponto de o plugin virar casca fina de verdade

Sem um desses fatos, reabrir a discussao seria so nostalgia pedindo reunião.

## 8. Conclusao

O `cowork-plugin` nao sera nem santificado nem sacrificado.

Ele continua vivo, mas subordinado.

Isso e o meio-termo certo entre duas burrices populares:

1. fingir que ele ainda e o coracao do Prumo
2. fingir que ele ja nao importa para nada

Em frase curta:

o plugin agora e casca, ponte e acervo. O produto mesmo precisa nascer em outro endereco.
