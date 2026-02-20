# Melhoria: links clicáveis ao referenciar arquivos

## Contexto (dogfooding)
Quando o agente menciona um arquivo salvo ("transcrição salva em Referencias/..."), o usuário não consegue acessar sem navegar manualmente. No Cowork, links `computer://` são clicáveis e abrem o arquivo direto.

## O que mudar

### No `claude-md-template.md`:

Adicionar como regra nova (pode ser uma sub-regra da Regra 1 "SEMPRE DOCUMENTAR") ou como nota no briefing:

```
### LINKS CLICÁVEIS

Sempre que referenciar um arquivo do sistema na conversa (ex: transcrição salva, documento movido, referência indexada), incluir um link clicável no formato:

[Descrição do arquivo](computer:///caminho/completo/do/arquivo.ext)

Nunca expor caminhos internos como texto cru. O link é a interface.
```

## Por que importa
A diferença entre "salvo em Referencias/arquivo.md" e "[Ver arquivo](computer://...)" é a diferença entre informar e entregar. O sistema deve entregar, não só informar.
