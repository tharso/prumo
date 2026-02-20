# Migração Claudia → Prumo (dogfooding real)

> Registro da migração do sistema pessoal "Claudia" para rodar em cima do Prumo.
> Data: 13/02/2026

## Por que estamos fazendo isso

Tharso criou o Prumo como produto a partir da experiência com a Claudia, mas nunca usou o Prumo de verdade. O sistema pessoal (Claudia) e o produto (Prumo) divergiam silenciosamente: melhorias iam pra um ou pro outro, aleatoriamente, e o produto estava sendo divulgado sem ter sido testado pelo próprio criador.

Decisão: migrar a Claudia pra rodar em cima do Prumo. Dogfooding real, não sandbox.

## O que existia antes

- CLAUDE.md da Claudia: ~200 linhas, escrito à mão, evoluiu organicamente desde 05/02/2026
- Estrutura de pastas com READMEs acumulados (BRISE, Blurp, GHz, Saúde, etc.)
- PAUTA.md com 30+ itens reais
- REGISTRO.md com 50+ entradas
- IDEIAS.md, PESSOAS.md, Referencias/INDICE.md, tudo populado

## Salvaguardas

1. CLAUDE.md original da Claudia salvo em pasta `Claudia/` (backup + gabarito de comparação)
2. Melhoria #005 aplicada no SKILL.md: setup agora protege arquivos existentes (não sobrescreve PAUTA, REGISTRO, READMEs, etc.)
3. Apenas CLAUDE.md e PRUMO-CORE.md são gerados/sobrescritos pelo setup

## O plano

1. ✅ Identificar o problema (Claudia ≠ Prumo, divergência silenciosa)
2. ✅ Criar melhoria #005 (proteção de arquivos existentes no setup)
3. ✅ Aplicar melhoria #005 no SKILL.md (Tharso aplicou)
4. ⬜ Salvar CLAUDE.md atual em `Claudia/CLAUDE.md`
5. ⬜ Rodar setup do Prumo (Tharso faz sozinho, experiência real de usuário)
6. ⬜ Comparar output gerado vs. CLAUDE.md original (diff brutal)
7. ⬜ Identificar gaps (o que a Claudia tinha e o Prumo não gerou)
8. ⬜ Cada gap vira melhoria no produto
9. ⬜ Viver com o output do Prumo por pelo menos 1 semana
10. ⬜ Revisão pós-migração: o que funcionou, o que quebrou, o que melhorou

## Bugs/gaps encontrados durante o processo

| # | Descrição | Status |
|---|-----------|--------|
| 1 | Setup sobrescreve arquivos existentes sem verificar | Corrigido (melhoria #005, v2.1) |

## Notas pós-migração

_A preencher depois que Tharso rodar o setup e voltar com feedback._
