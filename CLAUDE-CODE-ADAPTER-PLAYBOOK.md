# Playbook Operacional: Adapter Claude Code

Este documento existe para impedir um erro particularmente preguiçoso: tratar `Claude Code` como se fosse só "o mesmo Cowork sem vitrine".

Não é.

Os dois orbitam o universo Claude, mas o adapter do Prumo não é definido pelo sobrenome do modelo. É definido pela superfície real do host.

## 1. Estado atual deste host

Hoje, a situação do `Claude Code` é esta:

1. a base documental oficial é boa;
2. o contrato do runtime já está pronto para ele;
3. a validação de campo neste projeto ainda é menos rica do que em `Codex`.

Traduzindo sem maquiagem: aqui o terreno é melhor documentado do que no `Cowork`, mas ainda menos testado em produção do que no `Codex`.

## 2. Fontes oficiais que importam

1. Overview: [code.claude.com/docs/en/overview](https://code.claude.com/docs/en/overview)
2. CLI reference: [code.claude.com/docs/en/cli-reference](https://code.claude.com/docs/en/cli-reference)
3. Plugins reference: [code.claude.com/docs/en/plugins-reference](https://code.claude.com/docs/en/plugins-reference)
4. Slash commands / skills: [code.claude.com/docs/en/slash-commands](https://code.claude.com/docs/en/slash-commands)

O que isso nos autoriza a assumir:

1. `Claude Code` é superfície first-class de terminal/CLI.
2. Shell local e leitura de arquivos são parte do terreno oficial.
3. Skills, comandos e plugins existem como sistema formal.

## 3. O que ele não é

`Claude Code` não deve ser tratado como:

1. sinônimo de `Cowork`;
2. extensão do marketplace/store do `Cowork`;
3. adapter dependente de slash command legado do plugin.

Se o projeto esquecer isso, reabre exatamente a confusão que levou o Prumo a misturar host, plugin e produto como se fossem sopa.

## 4. Porta canônica

Para `Claude Code`, o contrato é este:

1. se o usuário disser `Prumo`, `bom dia, Prumo` ou equivalente, o host deve rodar `prumo`;
2. se o pedido for briefing explícito, o host deve rodar `prumo briefing --workspace . --refresh-snapshot`;
3. se o host quiser renderizar ações com mais inteligência, deve usar `prumo start --format json`.

## 5. Como consumir `prumo start --format json`

O adapter do `Claude Code` deve respeitar:

1. `adapter_contract_version`
2. `workspace_resolution`
3. `adapter_hints`
4. `actions[].kind`
5. `actions[].shell_command`
6. `actions[].host_prompt`

Em português simples:

1. `kind = shell` -> executar `shell_command`
2. `kind = host-prompt` -> usar `host_prompt` como continuação conversacional
3. `adapter_hints.preferred_entrypoint` -> porta curta
4. `adapter_hints.briefing_entrypoint` -> briefing explícito
5. `adapter_hints.structured_entrypoint` -> rota estruturada

## 6. Regras práticas

1. Resolver o workspace pelo diretório atual quando possível.
2. Respeitar `AGENT.md`, `AGENTS.md` e `CLAUDE.md` como wrappers do runtime.
3. Não cair no reflexo "já que é Claude, vou usar o fluxo do Cowork". Isso seria preguiça com gravata.
4. Não depender de plugin store, registry local ou slash command do `Cowork`.
5. Tratar permissões locais por app. `Claude Code` precisa das próprias permissões para Apple Reminders se quiser usar essa integração.

## 7. Checklist de aceite

O adapter `Claude Code` passa quando:

1. `Prumo` vira `prumo`;
2. briefing explícito vira `prumo briefing --workspace . --refresh-snapshot`;
3. `prumo start --format json` volta com estrutura íntegra e o host a respeita;
4. o host não puxa o plugin do `Cowork` como muleta conceitual;
5. o usuário não precisa decorar subcomando para começar.

## 8. Diferença operacional para Cowork

Esta é a parte que precisa ficar tatuada no plano:

1. `Cowork` pode até continuar usando slash command, plugin store e bridge de compatibilidade;
2. `Claude Code` não precisa herdar esse teatro;
3. o adapter de `Claude Code` deve ser avaliado mais perto da lógica do `Codex` do que da do `Cowork`, mas sem copiar contrato no escuro.

## 9. Próximo passo neste host

1. rodar validação real em campo, como foi feito no `Codex`;
2. testar invocação curta;
3. testar briefing explícito;
4. testar consumo de `start --format json`;
5. registrar o que for superfície própria do `Claude Code`, em vez de jogar tudo na conta da família Claude.
