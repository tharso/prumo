# Playbook Operacional: Adapter Antigravity

Este documento existe para impedir outro atalho mental vagabundo: tratar `Antigravity` como `Gemini CLI com perfume de interface`.

Não é.

Se o `Gemini CLI` já mostrou autonomia ruim no terminal, assumir que `Antigravity` vai se comportar melhor só porque tem mais móveis na sala seria um ótimo jeito de trocar método por esperança.

## 1. Estado atual deste host

Hoje, a situação do `Antigravity` é esta:

1. temos documentação oficial suficiente para provar que é outro host;
2. ainda não temos validação de campo neste projeto;
3. ele vem depois do `Gemini CLI`, não porque seja menos importante, mas porque a superfície é mais complexa.

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

## 5. Risco principal

O risco aqui é simples:

1. pular direto para `Antigravity` sem aprender nada com o fracasso do `Gemini CLI`;
2. confundir superfície gráfica com maturidade de adapter;
3. repetir o mesmo improviso, só com mais janelas abertas.

## 6. Próximo passo neste host

1. deixar registrado que o teste de `Gemini CLI` falhou feio;
2. só depois abrir a validação de campo em `Antigravity`;
3. entrar já procurando especificamente:
   - se o host executa `prumo`;
   - se respeita `start --format json`;
   - se evita improvisar briefing e estado.
