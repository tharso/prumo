# Aprendizados: instalação e setup do Prumo

> Registro dos problemas encontrados e soluções aplicadas entre 13-14/02/2026.
> Objetivo: não repetir os erros e servir de referência pro futuro.

---

## O problema raiz

Construímos o Prumo inteiro sem testar a instalação de ponta a ponta. Escrevemos instruções de instalação baseadas em suposições, não em testes reais. O resultado foi uma cadeia de falhas que só apareceu quando um usuário de verdade (o próprio Tharso) tentou instalar.

## Cadeia de falhas

### 1. Comandos CLI que não existem

**O que fizemos:** Publicamos na landing page comandos de instalação via terminal:
```
/plugin marketplace add tharso/prumo
/plugin install prumo@prumo
```

**O que aconteceu:** "Habilidade ou comando desconhecido: plugin." O comando `/plugin` é do Claude Code (CLI), não do Cowork (desktop). São plataformas diferentes com interfaces diferentes.

**Lição:** Não assumir que funcionalidades do CLI existem no desktop (e vice-versa). Testar o comando antes de publicar.

### 2. Extensões ≠ Plugins

**O que fizemos:** Corrigimos pra "faça upload via a interface do Cowork" e apontamos pra página de "Extensões".

**O que aconteceu:** A página de Extensões aceita .DXT e .MCPB (formatos de MCP servers). Nosso .zip com `.claude-plugin/plugin.json` não é uma extensão. Erro: "No manifest.json found in extension folder."

**Lição:** No Cowork, "Extensões" e "Plugins" são coisas completamente diferentes. Extensões = servidores MCP. Plugins = skills com `.claude-plugin/`. A UI fica em lugares separados na sidebar.

### 3. Seleção de pasta no meio da conversa

**O que fizemos:** A Etapa 0 do setup instruía o usuário a "clicar no ícone de pasta na barra lateral" pra selecionar o diretório de trabalho.

**O que aconteceu:** Duas falhas simultâneas:
- O seletor de pasta não fica na sidebar. Fica abaixo e à esquerda da caixa de input.
- A seleção de pasta precisa ser feita ANTES de iniciar a conversa. Não dá pra mudar no meio da sessão. É uma limitação da plataforma.

**Lição:** Interações que dependem da UI da plataforma precisam ser testadas na plataforma, não imaginadas. E quando a plataforma tem uma limitação, a solução é adaptar o fluxo (não tentar contornar).

### 4. Trigger "quero organizar minha vida"

**O que fizemos:** Definimos como frase de ativação do setup.

**O que aconteceu:** Feedback direto: "parece autoajuda barata". E tínhamos combinado de usar slash commands desde o início.

**Lição:** O tom da primeira interação define a percepção do produto. "Quero organizar minha vida" é genérico e emocional. `/Prumo` é preciso e profissional.

## Soluções aplicadas

### Instalação (v3.0)
- Landing page: botão de download do .zip + instruções visuais de upload via Plugins → "+"
- README: mesmas instruções atualizadas
- Removidos todos os comandos CLI

### Setup (v3.1)
- Trigger: `/Prumo`
- Etapa 0: detecção automática de pasta (real vs temporária). Se temporária, instrui o usuário a fechar, selecionar pasta, e voltar. Sem workarounds.
- Localização correta do seletor de pasta: "abaixo e à esquerda da caixa de input"

## Princípios extraídos

1. **Teste antes de documentar.** Instruções não testadas são ficção.
2. **A plataforma é soberana.** Se algo precisa ser feito na UI, teste na UI. Não na imaginação.
3. **Detectar > Instruir.** Em vez de pedir pro usuário fazer algo que pode dar errado, detecte o estado e reaja.
4. **O tom do primeiro contato define tudo.** Se a frase de ativação soa brega, o produto parece brega.
5. **Nomes importam.** Extensão ≠ Plugin. Sidebar ≠ Input box. Precisão na linguagem evita confusão.

---

*Documento gerado em 14/02/2026 como parte da v3.1 do Prumo.*
