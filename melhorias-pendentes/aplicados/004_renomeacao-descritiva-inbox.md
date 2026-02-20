# Melhoria: renomeação descritiva ao mover do inbox

## Contexto (dogfooding)
Arquivos do inbox mobile chegam com nomes tipo "10 de fev. de 2026, 12:09_text.txt" ou "share.jpeg". Quando movidos pra destino (Referencias, Pessoal/Documentos, etc.), precisam ser renomeados com nome descritivo que permita encontrar o item sem precisar abrir. Ex: `SJSP_Passo-a-Passo-MTB_2026.pdf`, `DNE-Digital_Tharso-Vieira_val-2027.png`.

## O que mudar

### No `claude-md-template.md` (Regra 3 - PROCESSAR O INBOX):

Expandir o item "Movidos para PAUTA.md ou para o README.md da área":

```
- Movidos para PAUTA.md ou README.md da área, **com renomeação descritiva** ao salvar no destino. O nome do arquivo deve ser autoexplicativo: `Fonte_Titulo-Curto_Ano.extensão` para referências, `Descricao_Contexto.extensão` para documentos pessoais. Ninguém deveria precisar abrir um arquivo pra saber o que tem dentro.
```

### No `claude-md-template.md` (Regra 4 - MATERIAL DE REFERÊNCIA):

Já menciona renomeação. Reforçar que o padrão vale pra TODOS os arquivos que saem do inbox, não só referências.

## Por que importa
"share.jpeg" salvo em Pessoal/Documentos é lixo com endereço nobre. Nome descritivo é o mínimo pra o sistema funcionar como memória externa.
