---
name: comparar-empresas
description: Use quando pedirem para comparar duas ou mais empresas brasileiras ("X versus Y", "compara essas cinco", "qual é maior/mais rentável/mais endividada", "como a X fica frente aos concorrentes ou pares do setor") com o MCP do Balanços.AI conectado.
license: MIT
compatibility: Requer o MCP do Balanços.AI conectado. Assume as skills balancos-ai e indicadores-financeiros; companhia-aberta e instituicao-financeira quando as empresas estão na CVM ou no BCB.
metadata:
  author: Balanços.AI
  version: "0.2"
---

# Comparar empresas

## Resultado

Uma tabela lado a lado, todas as empresas no **mesmo exercício**, com três blocos (tamanho,
rentabilidade, endividamento), uma linha de natureza do dado por empresa (fonte,
consolidado, operacional ou holding) e uma resposta direta por pergunta feita ("maior",
"mais rentável", "mais endividada"), cada uma com a lente usada. Links de todas.

## Passos

1. Resolva cada empresa com `buscar_empresas` (um termo curto por empresa). Liste o que
   escolheu e o que descartou. Se o pedido for "pares do setor" ou "concorrentes" sem
   nomes, obtenha a lista com `ranking_empresas` pelo `setor` (e `uf`, se fizer sentido)
   da empresa-alvo (os dois rótulos, se houver herdado), tire holdings e linhas com
   receita zero ou irrisória, filtre pelo `cnae_principal` da ficha quando o pedido for
   um subsetor (geração, siderurgia) e corte por escala entre um terço e três vezes o
   ativo da empresa-alvo, dizendo o corte ao leitor. Diga quantas empresas a base
   devolveu e que o teto é 50 por chamada.
   Se a empresa-alvo é companhia aberta, os pares abertos vêm de
   `cvm_ranking_companhias` no exercício, com a mesma `familia` e `visao` (não há UF nem
   setor: corte por CNAE e UF pela `ficha_empresa`, e diga). Se é instituição financeira,
   os pares vêm de `bcb_ranking_instituicoes` com `uf`, `tipo` ou `consolidado_bancario`
   iguais, no nível padrão.
2. Retrato de cada uma, em paralelo, pela fonte que o roteamento da skill balancos-ai
   indicar: `analisar_empresa`, `cvm_analisar_companhia` ou `bcb_analisar_instituicao`.
3. Escolha o exercício: o mais recente que **todas** têm. Se uma não tem, use o mais
   recente comum e mostre, em linha separada, o último ano de cada uma. Nunca misture anos
   na mesma coluna sem avisar no cabeçalho.
4. Classifique a natureza de cada dado (skill balancos-ai): fonte (publicações, CVM ou
   BCB), família e visão na CVM, nível no BCB, holding ou operacional e xbrl ou llm nas
   publicações. **Na mesma tabela, mesma fonte, mesma família e mesma visão**: consolidado
   com consolidado, nunca consolidado de uma com individual de outra. Se uma está só nas
   publicações (individual) e a outra na CVM (consolidado), mostre a individual da CVM
   para igualar e diga o que se perde. Banco compara só com banco, pelas linhas da skill
   instituicao-financeira. Empresas do mesmo grupo (controladora e controlada) não somam
   nem competem: diga que são andares da mesma operação.
5. Calcule com a skill indicadores-financeiros. Campo `null` só se deriva por identidade
   contábil, com nota. Exercício com escala trocada ou anomalia sai da comparação com
   nota e link; não se corrige. Se o texto da publicação tiver os valores literais, eles
   entram na coluna com a nota "sobre valores da publicação, não da base", e os
   indicadores calculados sobre eles levam a mesma nota. Se a anomalia atinge a série
   inteira da empresa, diga isso.
6. Monte a tabela e responda cada pergunta com a lente explícita.

## Tabela

| | Empresa A | Empresa B | Empresa C |
|---|---|---|---|
| Natureza do dado | CVM, consolidado, comercial | CVM, consolidado, comercial | publicações, llm, individual, operacional |
| Exercício | 2025 | 2025 | 2025 |
| Ativo total | | | |
| Patrimônio líquido | | | |
| Receita líquida | | | |
| Lucro líquido | | | |
| Margem bruta / líquida | | | |
| ROE | | | |
| Liquidez corrente | | | |
| Passivo exigível / ativo | | | |
| Exigível no curto prazo | | | |
| Dívida líquida (só CVM, com código) | | | não disponível |
| EBITDA (só CVM, 3.05 + \|7.04.01\|) | | | não disponível |

Valores em R$ mi ou bi, unidade no rótulo. Célula em branco com nota de rodapé quando o
campo não existe ou o exercício foi excluído.

Tabela de bancos: ativo total, carteira de crédito, captações, PL, lucro anual, ROE,
carteira sobre ativo, Basileia, na mesma data-base e no nível padrão de cada um, com a
era no cabeçalho (skill instituicao-financeira).

## Regras

- "Maior" tem duas lentes, ativo e receita; numa cadeia holding, controladora e operadora
  elas divergem. Responda as duas.
- Margem de holding é artefato de equivalência patrimonial: mostre com asterisco, não
  use para "mais rentável".
- Fontes diferentes na mesma tabela (xbrl e llm) ficam visíveis na linha "Natureza".
- Estrutura societária (quem controla quem): se o texto da publicação diz ("sua
  controladora, X"), cite; se não, é conhecimento seu, rotulado. Se o MCP do cnpj.ai
  estiver disponível, confirme lá.
- Controladora com CNAE industrial mas receita pequena diante do ativo e lucro
  operacional acima do bruto (Gerdau S.A.) recebe o mesmo tratamento de holding nas
  margens.
- Opção "em CSV": as mesmas linhas, uma empresa por coluna, separador vírgula, sem
  unidade nos números e com o exercício em coluna própria.

## Quando o dado não existe

- Uma empresa não está na base: diga, tire-a da tabela e siga com as outras.
- Só uma empresa tem DRE: compare só o bloco de balanço e diga que rentabilidade ficou
  fora para as demais.
- Setor sem pares na base além da própria empresa: diga o N e não invente comparação.
