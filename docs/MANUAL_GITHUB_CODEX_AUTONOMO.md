# Prumo - Manual Prático (GitHub Projects + Issues + Codex Autônomo)

Estado deste documento: 21/02/2026.

Este manual é para operação. Menos teoria, mais execução.

## 1) Pré-requisitos (uma vez só)

1. Ter acesso ao repositório no GitHub.
2. Estar autenticado no GitHub CLI (`gh auth status`).
3. Ter labels e Project base criados:

```bash
cd /Users/tharsovieira/Documents/DailyLife/Prumo
./scripts/github/bootstrap_labels.sh
./scripts/github/bootstrap_project.sh
```

## 2) Onde cada coisa vive

1. Ideias e demandas: Issues.
2. Priorização e andamento: Project.
3. Implementação: Pull Request.
4. Regra de qualidade: checklist do PR + CI.

Regra curta:

1. Sem issue, não existe trabalho.
2. Sem critério de aceite, não existe "pronto".

## 3) Fluxo diário em 10 minutos

1. Abrir o Project e olhar `status/triage`.
2. Refinar as novas issues (escopo e critérios de aceite).
3. Promover para `status/ready` o que está claro.
4. Definir prioridade (`priority/p0` ... `priority/p3`).
5. Definir agente principal (`agent/codex`, `agent/cowork`, `agent/gemini`).
6. Acionar o Codex para executar a issue `status/ready`.

## 4) Como abrir uma issue que o Codex consegue resolver

Use sempre os templates em `.github/ISSUE_TEMPLATE/`.

Checklist mínimo da issue:

1. Problema real (qual dor existe hoje).
2. Resultado esperado (como fica depois).
3. Escopo (o que entra e o que não entra).
4. Critérios de aceite objetivos (checklist verificável).
5. Matriz de compatibilidade (`Codex`, `Claude`, `Gemini`).
6. Plano de validação cruzada.

Se faltar isso, o agente vai adivinhar. Adivinhação é prima da regressão.

## 5) Como acionar o Codex de forma autônoma

Use um prompt direto como este:

```text
Resolva a issue #<NUMERO> do repositório Prumo em modo autônomo.
Regras:
1) execute ponta a ponta sem parar em plano;
2) respeite estritamente o escopo e critérios de aceite da issue;
3) abra PR vinculando "Closes #<NUMERO>";
4) abra as issues de validação cruzada (type/validation) para os outros agentes;
5) atualize docs/version/changelog se houver mudança pública;
6) mova a issue para status/review ao final.
```

Versão curta (uso diário):

```text
Execute a issue #<NUMERO> em modo yolo, com PR completo, validação cruzada e sem sair do escopo.
```

## 6) Quando o Codex deve recusar execução imediata

1. Issue sem critério de aceite.
2. Escopo contraditório.
3. Dependência externa bloqueante não descrita.
4. Pedido para mexer em customização pessoal dentro do produto público.

Se cair nesses casos, primeiro refinamento, depois execução.

## 7) Como revisar o resultado sem perder tempo

No PR, valide nesta ordem:

1. Escopo bate com a issue.
2. Critérios de aceite estão comprovados.
3. Matriz de compatibilidade preenchida.
4. Issues `type/validation` abertas para os agentes pares.
5. Risco e rollback descritos quando necessário.

Se qualquer item acima falhar, não é review. É aposta.

## 8) Validação cruzada entre agentes (obrigatória)

Para cada feature entregue:

1. Criar issue com template `validation.yml`.
2. Definir agente validador.
3. Registrar resultado (`APPROVED` ou `REJECTED`) com evidências.
4. Vincular no PR da feature.

## 9) Produto vs customização pessoal (regra prática)

Vai para produto:

1. O que serve para qualquer usuário.
2. Fluxo, regra, template, script, docs públicas.

Fica local/pessoal:

1. Dados privados.
2. Preferências e rotinas pessoais específicas.

Se estiver em dúvida, trate como pessoal até provar que é genérico.

## 10) Comandos úteis (CLI)

Listar issues abertas:

```bash
gh issue list --repo tharso/prumo --state open
```

Ver detalhes de uma issue:

```bash
gh issue view <NUMERO> --repo tharso/prumo
```

Criar issue de validação rápido:

```bash
gh issue create \
  --repo tharso/prumo \
  --title "validation: issue #<NUMERO> - compatibilidade" \
  --label "type/validation,status/triage,agent/cowork" \
  --body "Validar PR <LINK_PR> com foco em compatibilidade e regressão."
```

## 11) Anti-padrões que drenam o time

1. Abrir issue vaga e pedir "resolve aí".
2. Mudar escopo no meio sem atualizar issue.
3. Fechar issue sem evidência de aceite.
4. Chamar isso de agilidade.

## 12) Definição de sucesso

Você sabe que o fluxo está saudável quando:

1. Cada trabalho nasce e morre em issue/PR rastreável.
2. O Codex executa com autonomia sem virar loteria.
3. Nenhuma evolução do produto pisa nas customizações pessoais.
