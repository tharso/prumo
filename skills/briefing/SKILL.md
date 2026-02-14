---
name: briefing
description: >
  Morning briefing do Prumo. Executa a rotina completa: lê configuração pessoal,
  verifica pauta, processa inbox (todos os canais), checa calendário e emails,
  e apresenta o briefing do dia. Use com /briefing ou quando o usuário disser
  "bom dia", "briefing", "começar o dia".
---

# Briefing do Prumo

Você está executando o morning briefing do sistema Prumo. Esta é a rotina mais importante do sistema. Siga os passos abaixo **na ordem**, sem pular nenhum.

## Passo 1: Ler configuração

1. Leia o arquivo `CLAUDE.md` na pasta workspace do usuário. Ele contém: nome, áreas de vida, tom de comunicação, integrações configuradas, lembretes recorrentes.
2. Leia o arquivo `PRUMO-CORE.md` na mesma pasta. Ele contém as regras do sistema.

Se algum desses arquivos não existir, informe o usuário que o Prumo não está configurado e sugira rodar o setup.

## Passo 2: Verificar atualização

1. Leia o campo `prumo_version` no topo do `PRUMO-CORE.md` local.
2. Busque a versão remota em: `https://raw.githubusercontent.com/tharso/prumo/main/VERSION`
3. Se a versão remota for **igual ou menor**: prossiga sem mencionar nada.
4. Se a versão remota for **maior**:
   a. Busque o PRUMO-CORE.md remoto em: `https://raw.githubusercontent.com/tharso/prumo/main/skills/prumo/references/prumo-core.md`
   b. Leia a seção "Changelog do Core" do arquivo remoto. Extraia as entradas entre a versão local e a remota.
   c. Apresente ao usuário: "Há uma atualização do Prumo (v[local] → v[remota]). O que mudou: [itens do changelog]. Apenas o motor é atualizado. Seus arquivos e configurações permanecem intactos. Atualizar?"
   d. Se aceitar: substitua o `PRUMO-CORE.md` local pelo remoto.
   e. Se recusar: prossiga sem insistir.

## Passo 3: Estado atual

1. Leia `PAUTA.md` — este é o arquivo mais importante.
2. Leia `INBOX.md` — se tiver itens, serão processados no passo 5.

## Passo 4: Canais de entrada

Verificar TODOS os canais, sem pular nenhum:

1. **Pasta `Inbox4Mobile/`**: Listar TODOS os arquivos. Abrir cada um, inclusive imagens (screenshots, fotos, prints de WhatsApp contêm informações críticas).
2. **Gmail** (se configurado no CLAUDE.md): Buscar emails com subject do agente e "INBOX:". Ler os não processados.
3. **Google Calendar** (se configurado): Listar eventos do dia.

## Passo 5: Processar inbox

Se houver itens novos (de qualquer canal):
- Numerar cada item
- Sugerir categoria e próxima ação
- Perguntar ao usuário se concorda ou quer ajustar
- Mover para PAUTA.md ou README da área
- Adicionar `(desde DD/MM)` em cada item
- Renomear arquivos com nomes descritivos
- Registrar no REGISTRO.md
- Deletar original do inbox

## Passo 6: Montar o briefing

Apresentar de forma direta (no tom configurado no CLAUDE.md). **FORMATO OBRIGATÓRIO:**

- **Lista numerada contínua** na mensagem inteira (Regra 14 do PRUMO-CORE). Nunca resetar numeração ao mudar de seção. Seções podem ter subtítulos, mas a numeração segue: 1, 2, 3... até o fim.
- **Opções com letras** dentro de cada item quando houver decisão possível (a, b, c). O usuário responde "3b, 7a".
- **Proatividade nível 3-4** em cada item (Regra 15 do PRUMO-CORE). Não apenas listar — propor ação concreta, pesquisar, oferecer ajuda.

Conteúdo do briefing (tudo na mesma lista numerada contínua):

- Compromissos do dia (do calendário, se disponível) — com contexto e preparação
- Itens quentes que precisam de atenção hoje — com proposta de ação
- Lembretes do dia (consultar lembretes recorrentes no CLAUDE.md) — com opções
- Itens envelhecendo — cobrar com data `(desde DD/MM)`, diagnosticar por que parou, propor micro-passo
- Novidades do inbox — se processou itens, mostrar resumo do que entrou

Se a PAUTA estiver vazia: não fazer o briefing padrão. Pedir um brain dump.

## Passo 7: Documentar

Atualizar PAUTA.md se algo mudou. Registrar itens processados no REGISTRO.md.

---

**Tom:** Seguir rigorosamente o tom definido no CLAUDE.md do usuário. Se for "direto", cobrar sem cerimônia. Se for "gentil", lembrar sem pressionar.

**Links:** Sempre usar `[Descrição](computer:///caminho)` ao referenciar arquivos. Nunca expor caminhos crus.
