# Playbook Operacional: Adapter Gemini CLI

Este documento existe para evitar uma preguiça simétrica à do universo Claude: achar que `Gemini CLI` e `Antigravity` são a mesma coisa só porque carregam o mesmo sobrenome.

Não são.

`Gemini CLI` é o host de terminal. É por ele que faz sentido começar a validar o lado Gemini do Prumo sem levar interface gráfica, browser agent e política de autonomia para a dança antes da hora.

## 1. Estado atual deste host

Hoje, a situação do `Gemini CLI` é esta:

1. a base documental oficial é boa;
2. o contrato do runtime já está pronto para ele;
3. a validação de campo neste projeto ainda não foi feita.

Traduzindo: aqui o problema ainda não é bug conhecido. É chão ainda não pisado.

## 2. Fontes oficiais que importam

1. Google for Developers summary: [developers.google.com/gemini-code-assist/docs/gemini-cli](https://developers.google.com/gemini-code-assist/docs/gemini-cli)
2. Repositório oficial: [github.com/google-gemini/gemini-cli](https://github.com/google-gemini/gemini-cli)

O que isso nos autoriza a assumir:

1. `Gemini CLI` é agente de terminal com shell local;
2. operações de arquivo são parte do terreno oficial;
3. MCP, ferramentas e saídas estruturadas já fazem parte do ecossistema;
4. não precisamos inventar metafísica para justificar um adapter fino.

## 3. O que ele não é

`Gemini CLI` não deve ser tratado como:

1. `Antigravity` sem interface;
2. "o mesmo adapter do Codex, mas com outro logo";
3. host que herda automaticamente tudo o que funcionou em `Codex`.

Se cairmos nisso, trocamos arquitetura por superstição com documentação em PDF.

## 4. Porta canônica

Para `Gemini CLI`, o contrato é este:

1. se o usuário disser `Prumo`, `bom dia, Prumo` ou equivalente, o host deve rodar `prumo`;
2. se o pedido for briefing explícito, o host deve rodar `prumo briefing --workspace . --refresh-snapshot`;
3. se o host quiser renderizar ações com mais inteligência, deve usar `prumo start --format json`.

## 5. Como consumir `prumo start --format json`

O adapter do `Gemini CLI` deve respeitar:

1. `adapter_contract_version`
2. `workspace_resolution`
3. `adapter_hints`
4. `actions[].kind`
5. `actions[].shell_command`
6. `actions[].host_prompt`

Em português curto:

1. `kind = shell` -> executar `shell_command`
2. `kind = host-prompt` -> usar `host_prompt`
3. `adapter_hints.preferred_entrypoint` -> porta curta
4. `adapter_hints.briefing_entrypoint` -> briefing explícito
5. `adapter_hints.structured_entrypoint` -> rota estruturada

## 6. Regras práticas

1. Resolver o workspace pelo diretório atual quando possível.
2. Respeitar `AGENT.md`, `AGENTS.md` e `CLAUDE.md` como wrappers do runtime.
3. Não assumir paridade automática com `Codex` só porque ambos vivem bem no terminal.
4. Não contaminar esse adapter com premissas de `Antigravity`.
5. Tratar permissões locais por app. Se um dia formos usar integrações locais de macOS por este host, a autorização será do app/processo dele, não do vizinho.

## 7. Checklist de aceite

O adapter `Gemini CLI` passa quando:

1. `Prumo` vira `prumo`;
2. briefing explícito vira `prumo briefing --workspace . --refresh-snapshot`;
3. `prumo start --format json` volta com estrutura íntegra e o host a respeita;
4. o host não improvisa briefing fora do runtime;
5. o usuário não precisa decorar subcomando para começar.

## 8. Risco principal

O risco mais provável aqui não é TCC nem plugin store. É outro:

1. o projeto assumir que "terminal é terminal" e copiar o adapter do `Codex` sem validar o comportamento real do `Gemini CLI`.

Isso seria rápido. E burro.

## 9. Próximo passo neste host

1. rodar validação real em campo;
2. testar invocação curta;
3. testar briefing explícito;
4. testar consumo de `start --format json`;
5. registrar qualquer diferença concreta de shell, affordance e renderização em relação ao `Codex`.
