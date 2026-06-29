# Guia: Atalho mobile para captura rápida

> Este guia é lido pelo agente durante o setup (Etapa 7) e apresentado ao usuário
> de forma conversacional. Ser breve e direto.

## Link de instalação (iPhone/iPad/Mac)

**Download direto:** https://www.icloud.com/shortcuts/02a3b96c0829419eaa628e5f9361cc12

O usuário toca no link, confirma a instalação, e o atalho "Send2Prumo" aparece no app Atalhos.

## O que o atalho faz

Seis modos de captura num único atalho:

| Modo | O que faz |
|------|-----------|
| **Texto** | Abre campo de texto, salva como .txt |
| **Tirar foto** | Abre câmera, salva foto |
| **Galeria** | Seleciona fotos existentes, salva |
| **Áudio** | Grava áudio, salva gravação |
| **Email** | Abre Gmail com subject "PRUMO" pré-preenchido |
| **Share Sheet** | Aceita qualquer conteúdo compartilhado de outros apps |

Tudo é salvo na pasta `Inbox4Mobile/` com nome baseado em data/hora.
O agente processa no próximo briefing.

## Configuração pós-instalação (2 minutos)

Após instalar, o usuário precisa ajustar duas coisas:

### 1. Pasta de destino

O atalho salva em `Inbox4Mobile/` por padrão. O usuário precisa apontar
para a pasta correta dentro do seu workspace:

- Abrir o atalho no app Atalhos (editar)
- Encontrar as ações de "Salvar" (são 4: texto, foto, galeria, áudio)
- Em cada uma, ajustar o caminho para a pasta Inbox4Mobile/ do workspace
- A pasta precisa estar acessível pelo celular (iCloud Drive, Google Drive, etc.)

### 2. Email (na opção "Enviar email")

O atalho abre o Gmail com subject "PRUMO" mas sem destinatário:
- Abrir o atalho, encontrar a ação de "Abrir URL"
- Adicionar o email do usuário no campo `to=`
- Formato: `googlegmail://co?to=SEUEMAIL@gmail.com&subject=PRUMO`

Se o usuário NÃO usa Gmail, pode trocar por:
- Mail nativo: `mailto:SEUEMAIL@gmail.com?subject=PRUMO`

### 3. Adicionar à Home Screen (opcional mas recomendado)

- No app Atalhos, tocar e segurar o atalho
- "Adicionar à Tela de Início"
- Escolher ícone e cor
- Agora é um toque pra capturar

## Se a pasta NÃO está na nuvem

O atalho precisa de uma pasta acessível pelo celular. Se o workspace do
usuário não está no iCloud Drive ou similar, duas alternativas:

1. **Criar Inbox4Mobile/ dentro do iCloud Drive** e apontar o atalho pra lá.
   O agente verifica essa pasta no briefing.

2. **Usar só o modo email**: Não precisa de pasta na nuvem. O agente busca
   emails com subject "PRUMO" (ou o nome do agente) via Gmail no briefing.

## Android

No Android não existe o app Atalhos. Alternativas:

**Opção recomendada: Email**
- Criar atalho na home screen que abre email pré-preenchido com subject "PRUMO"
- Funciona com qualquer app de email
- O agente busca esses emails no briefing via Gmail

**Opção avançada: Tasker ou Automate**
- Apps de automação que podem replicar o fluxo (captura → salva em pasta Google Drive)
- Mais trabalho de setup, mas resultado equivalente ao iOS

## Tipos de conteúdo que chegam pro agente

| O que o usuário faz | O que chega na pasta | Exemplo |
|----------------------|----------------------|---------|
| Digita texto | `_text.txt` | "Lembrar de ligar pro dentista" |
| Compartilha link | `_text.txt` com URL | "https://artigo-interessante.com" |
| Tira foto | `_share.jpeg` | Foto de documento, recibo |
| Compartilha screenshot | `_share.jpeg` | Print de conversa WhatsApp |
| Grava áudio | `_audio.m4a` | Nota de voz rápida |
| Compartilha PDF | `_share.pdf` | Documento recebido |

O agente DEVE saber interpretar todos esses tipos no briefing, inclusive abrir imagens
(screenshots frequentemente contêm informações críticas como agendamentos, conversas, comprovantes).
