# Prumo - Diretrizes de Desenvolvimento do Produto

Estado deste documento: 21/02/2026.

Este arquivo define regras obrigatórias para qualquer agente que desenvolva o Prumo.
Não é manifesto inspiracional. É contrato de execução.

## 1) Escopo e objetivo

Objetivo: garantir que o produto evolua sem misturar customização pessoal do operador com capacidades públicas do Prumo.

Escopo: feature, bugfix, refatoração, automação, documentação de comportamento e setup.

## 2) Regras inegociáveis (MUST)

1. Toda feature deve nascer de issue com problema, resultado esperado, escopo e critérios de aceite claros.
2. O agente implementador deve projetar para compatibilidade multiagente e multimodelo.
3. A matriz mínima de compatibilidade deve cobrir `Codex`, `Claude (Cowork)` e `Gemini`.
4. Ao terminar a implementação, o agente deve abrir tarefas de validação para os outros agentes, com label `type/validation`.
5. Nenhuma release pode sobrescrever arquivos personalizados do usuário.
6. Claims públicos (landing, README, docs) devem refletir o comportamento real entregue.
7. Mudança estrutural exige handover em `_state/HANDOVER.md` com status inicial `PENDING_VALIDATION`.

## 3) Compatibilidade multiagente

Cada entrega deve explicitar:

1. O que funciona igual nos três agentes.
2. O que depende de runtime específico (ex.: shell, MCP, CLI local).
3. Qual fallback é usado quando o runtime não oferece o recurso avançado.

Se não houver paridade total, registrar limite de forma objetiva. Sem promessa vaga.

## 4) Fluxo obrigatório de validação cruzada

Ao concluir o desenvolvimento:

1. Abrir issue `type/validation` para cada agente não autor da mudança.
2. Incluir contexto mínimo: resumo, risco, checklist de verificação, critérios de aprovação/rejeição.
3. Vincular essas issues no PR da feature.
4. Registrar o handover técnico em `_state/HANDOVER.md`.

Regra prática:

1. Se Codex implementa, Claude e Gemini validam.
2. Se Claude implementa, Codex e Gemini validam.
3. Se Gemini implementa, Codex e Claude validam.

## 5) Fronteira produto vs customização pessoal

Produto (versionado no repositório):

1. Core, skills, templates, scripts de setup e docs públicas.
2. Fluxos genéricos reutilizáveis por qualquer usuário.

Customização pessoal (não entra no produto público):

1. Dados pessoais, contatos pessoais, rotinas privadas.
2. Ajustes específicos de uma pessoa em `CLAUDE.md`, `PAUTA.md`, `INBOX.md` e arquivos de operação local.

Se houver dúvida, tratar como customização pessoal até prova contrária.

## 6) Gate de merge (Definition of Done)

Um PR só pode ser considerado pronto quando:

1. Checklist de PR estiver completo.
2. Matriz de compatibilidade estiver preenchida.
3. Issues de validação cruzada estiverem abertas e linkadas.
4. Testes/validações executados estiverem declarados.
5. Documentação impactada estiver atualizada.

## 7) Atualização segura

Atualização de versão do core deve respeitar allowlist de escrita:

1. `PRUMO-CORE.md`
2. `_backup/PRUMO-CORE.md.*`

Para update automatizado, usar `scripts/safe_core_update.sh`.

## 8) Linguagem de documentação

1. Evitar absolutismos que não são verificáveis.
2. Declarar pré-requisitos reais (ex.: plano, runtime, autenticação).
3. Separar claramente comportamento padrão e modo avançado opcional.

Quando uma regra mudar, atualizar este documento e `docs/WORKFLOW.md` na mesma PR.
