# Melhoria #005: Proteção de arquivos existentes no setup

## Contexto

O setup (Etapa 9 do SKILL.md) gera todos os arquivos sem verificar se já existem. Isso é perigoso: se o usuário rodar o setup numa pasta que já tem dados (migração, reconfiguração, ou simplesmente um re-setup), os READMEs das áreas, PAUTA.md, REGISTRO.md e outros arquivos com conteúdo acumulado seriam sobrescritos por templates vazios.

Bug descoberto durante dogfooding real (13/02/2026): tentativa de migrar o sistema "Claudia" (com semanas de dados) para rodar em cima do Prumo. Sem essa proteção, o setup destruiria todo o contexto acumulado.

## O que implementar

### 1. No SKILL.md, Etapa 9, adicionar verificação antes de gerar cada arquivo:

Antes de criar qualquer arquivo, verificar se ele já existe na pasta do usuário. Se existir:

- **CLAUDE.md**: Sempre sobrescrever (é o objetivo do setup/reconfiguração). Mas antes, criar backup automático em `_backup/CLAUDE.md.YYYY-MM-DD` e informar o usuário.
- **PRUMO-CORE.md**: Sempre sobrescrever (é atualizável por design).
- **PAUTA.md, REGISTRO.md, IDEIAS.md, PESSOAS.md, INDICE.md**: NÃO sobrescrever. Informar: "Encontrei [arquivo] com conteúdo existente. Mantendo o atual."
- **[Area]/README.md**: NÃO sobrescrever. Informar: "A pasta [Area] já tem um README com contexto. Mantendo."
- **Pastas (Inbox4Mobile/, _logs/, Referencias/)**: Criar apenas se não existirem.

### 2. Adicionar mensagem de resumo ao final da Etapa 9:

Após gerar os arquivos, listar:
- Arquivos criados (novos)
- Arquivos mantidos (já existiam)
- Arquivos sobrescritos (CLAUDE.md, PRUMO-CORE.md) com localização do backup

### 3. No SKILL.md, seção "Reconfiguração", referenciar esse comportamento:

A opção 5 ("Reset completo") já diz "manter dados existentes, regerar CLAUDE.md". Tornar esse comportamento explícito e consistente com a Etapa 9.

## Prompt para aplicar

Cole o seguinte na janela do Prumo:

---

No SKILL.md, na Etapa 9 ("Gerar arquivos"), adicione um bloco de verificação ANTES da geração. O setup deve checar se cada arquivo já existe no workspace. Regras:

1. CLAUDE.md e PRUMO-CORE.md: sempre gerar (sobrescrever). Se CLAUDE.md existir, criar backup em `_backup/CLAUDE.md.YYYY-MM-DD` antes.
2. Todos os outros arquivos (PAUTA.md, INBOX.md, REGISTRO.md, IDEIAS.md, PESSOAS.md, INDICE.md, [Area]/README.md): NÃO gerar se já existirem. Informar o usuário que o arquivo foi mantido.
3. Pastas: criar apenas se não existirem.
4. Ao final da Etapa 9, mostrar resumo: arquivos criados vs. mantidos vs. sobrescritos (com backup).
5. Na seção "Reconfiguração", atualizar a opção 5 ("Reset completo") para referenciar esse comportamento.

Essa proteção permite que o setup rode com segurança em workspaces que já contêm dados reais, sem risco de perda de contexto acumulado.
