# Playbook Operacional: Adapter Antigravity

Este documento existe para impedir outro atalho mental vagabundo: tratar `Antigravity` como `Gemini CLI com perfume de interface`.

Não é.

Se o `Gemini CLI` já mostrou autonomia ruim no terminal, assumir que `Antigravity` vai se comportar melhor só porque tem mais móveis na sala seria um ótimo jeito de trocar método por esperança.

## 1. Estado atual deste host

Hoje, a situação do `Antigravity` é esta:

1. temos documentação oficial suficiente para provar que é outro host;
2. a validação de campo neste projeto já foi feita;
3. o resultado foi melhor do que no `Gemini CLI`, mas ainda não limpo o bastante para carimbar sem ressalva;
4. ele vem depois do `Gemini CLI`, não porque seja menos importante, mas porque a superfície é mais complexa.

## 1.1. Resultado da validação de campo (2026-03-21)

O teste real no `Antigravity` mostrou um retrato bem menos ruim do que o do `Gemini CLI`:

1. `Prumo` levou o host a executar `prumo start --format json`;
2. o host também executou `prumo briefing --workspace . --refresh-snapshot` e `prumo context-dump --workspace ... --format json`;
3. não houve leitura de arquivos para fingir runtime;
4. não houve escrita manual em `_state/`;
5. o host, porém, rodou comandos extras sem necessidade;
6. insistiu em `prumo briefing --format json` mesmo depois de o erro deixar claro que essa flag não existe;
7. chegou a tentar executar `a` como comando de shell, confundindo opção de menu com instrução operacional;
8. `Apple Reminders` continuou em `denied/notDetermined`, então a integração local ainda não passou neste host.

Conclusão prática:

1. `Antigravity` está aprovado, por enquanto, como host que respeita o runtime melhor do que o `Gemini CLI`;
2. `Antigravity` está pendente em disciplina de execução;
3. `Antigravity` está pendente em `Apple Reminders` por permissão por app.

## 2. Fontes oficiais que importam

1. Codelab oficial: [codelabs.developers.google.com/getting-started-google-antigravity](https://codelabs.developers.google.com/getting-started-google-antigravity)
2. Blog do Google: [blog.google/intl/en-mena/product-updates/explore-get-answers/gemini-3-launches-in-mena/](https://blog.google/intl/en-mena/product-updates/explore-get-answers/gemini-3-launches-in-mena/)

O que isso nos autoriza a assumir:

1. `Antigravity` é host agent-first;
2. trabalha com workspace local, editor, terminal e browser;
3. permissões e autonomia são parte explícita da superfície do produto.

## 3. O que ele não é

`Antigravity` não deve ser tratado como:

1. `Gemini CLI` com interface gráfica;
2. "o adapter Gemini" em versão bonita;
3. host cuja política de autonomia pode ser ignorada porque já entendemos shell.

## 4. Porta canônica

Para `Antigravity`, o contrato continua o mesmo:

1. `Prumo` -> `prumo`
2. briefing explícito -> `prumo briefing --workspace . --refresh-snapshot`
3. rota estruturada -> `prumo start --format json`

Mas a validação aqui terá de olhar também:

1. terminal
2. affordance da interface
3. políticas de autonomia
4. leitura de arquivos-guia do workspace

E, depois do teste real, mais duas coisas:

5. se o host resiste à tentação de rodar comando extra só porque ficou animado;
6. se o host para depois de um erro explícito, em vez de repetir a mesma linha como papagaio elétrico.

## 5. Risco principal

O risco aqui é simples:

1. pular direto para `Antigravity` sem aprender nada com o fracasso do `Gemini CLI`;
2. confundir superfície gráfica com maturidade de adapter;
3. repetir o mesmo improviso, só com mais janelas abertas.

## 6. Próximo passo neste host

1. tratar `Antigravity` como host parcialmente validado;
2. endurecer o contrato textual contra dois vícios já vistos:
   - rodar comando extra sem ser pedido;
   - insistir em comando inválido depois de erro explícito;
3. manter `Apple Reminders` como pendência específica deste app até o TCC se comportar como gente.

## 7. Checklist de aceite

Status atual do checklist:

1. `Prumo` vira `prumo` -> `SIM`
2. briefing explícito vira `prumo briefing --workspace . --refresh-snapshot` -> `SIM`
3. `prumo start --format json` volta com estrutura íntegra e o host a respeita -> `SIM`
4. o host não improvisa briefing fora do runtime -> `SIM`
5. o host não executa comandos extras sem necessidade -> `NAO`
6. o host não repete comando inválido depois de erro explícito -> `NAO`
7. `Apple Reminders` funciona no próprio app -> `NAO`
