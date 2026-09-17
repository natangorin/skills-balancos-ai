---
name: companhia-aberta
description: Use quando a empresa for companhia aberta (S.A. com DFP na CVM) e o pedido envolver consolidado, conta a conta, DFC, DVA, EBITDA, dívida líquida, cobertura de juros, parecer do auditor, reapresentação ou ranking de companhias abertas, com o MCP do Balanços.AI conectado. Assume a skill balancos-ai.
license: MIT
compatibility: Requer o MCP do Balanços.AI conectado. Assume as skills balancos-ai e indicadores-financeiros.
metadata:
  author: Balanços.AI
  version: "0.2"
---

# Companhia aberta pela CVM

## Resultado

O mesmo tipo de entrega da skill que chamou (memo, tabela, relatório), com **visão**
(consolidado ou individual), **versão** e `id_doc` da entrega declarados em cada número, e
o código da conta ao lado de cada indicador derivado do conta a conta.

## Fluxo

1. `cvm_buscar_companhias(termo)`: trecho da denominação ou CNPJ. Até 20, com `cnpj`,
   `cd_cvm`, `denominacao` e `empresa` (slug e link do balancos.ai, quando está lá).
   Vindo da skill balancos-ai, use o CNPJ da ficha de publicações.
2. `cvm_analisar_companhia(chave)`, chave = CNPJ ou código CVM. Uma chamada traz a ficha
   (denominações anteriores, `familia`, primeiro e último exercício, número de entregas e
   de reapresentações, último parecer, capital social com ações em tesouraria), a linha do
   tempo `exercicios[]` com `versoes[]` (`id_doc`, versão, `reapresentacao`, data,
   parecer, links) e `balancos[]` e `dres[]` por exercício e `visao`, na última versão de
   cada exercício. Só use `cvm_ficha_companhia`, `cvm_dfps_companhia`,
   `cvm_balancos_companhia` e `cvm_dres_companhia` para uma parte.
3. `cvm_entrega_dfp(id_doc)` quando precisar saber quais visões e demonstrações a entrega
   tem (`visoes`, `demonstracoes_disponiveis`) antes de pedir o conta a conta.
4. `cvm_demonstracoes_dfp(id_doc, demonstracao, visao)`: **uma demonstração por chamada**
   (`bpa`, `bpp`, `dre`, `dra`, `dfc`, `dmpl`, `dva`). Sem `demonstracao` a resposta é
   grande. Padrão da tool: consolidado, ou individual quando não há consolidado. Cada conta
   traz `codigo`, `descricao`, `nivel`, `padronizada`, `valor_atual` e `valor_anterior`.
5. `cvm_parecer_dfp(id_doc)`: `auditor.tipo`, `auditor.texto` integral e `declaracoes[]`
   (diretores sobre as demonstrações, diretores sobre o parecer, conselho fiscal).
6. `cvm_ranking_companhias(metrica, ano, visao, familia, limite)`: `ano` obrigatório.

Campos de cada resposta em [references/payloads.md](references/payloads.md).

## Visão

- **Consolidado é o padrão** para tamanho, operação, margens e comparação. É o que
  responde "que tamanho tem" e "quanto fatura".
- **Individual** só quando a pergunta é sobre a entidade (dividendos, capital social,
  obrigação própria, garantia dada pela controladora) ou quando não há consolidado (lista
  `visoes` em `cvm_entrega_dfp`; companhia sem controladas entrega só o individual).
- A visão vai no cabeçalho de toda tabela e ao lado de todo número solto.
- A regra de holding e controladora da skill balancos-ai **não se aplica** quando há
  consolidado: Gerdau S.A. tem receita individual de R$ 4,8 bi e consolidada de R$ 69,9 bi
  em 2025; o consolidado é a operação.
- Exercício antigo com receita zero na visão individual (Gerdau 2010) é lacuna da
  entrega, não receita zero: deixe em branco e diga.

## Família

`familia` vem na ficha: `comercial`, `financeira`, `seguradora` ou `desconhecida`.

- `comercial` usa o plano de contas padrão da CVM e o mapa de códigos desta skill.
- `financeira` e `seguradora` têm plano próprio: o mapa **não** vale, o ranking só compara
  dentro da família (`familia` no `cvm_ranking_companhias`), e banco vai para a skill
  instituicao-financeira, que tem carteira, captações e Basileia.

## Versões e reapresentações

- A última versão de um exercício é a que vale, e `cvm_analisar_companhia` já a escolhe
  (`versao` e `id_doc` em cada linha de `balancos[]` e `dres[]`).
- `n_reapresentacoes` na ficha e `reapresentacao: true` na linha do tempo são sinal para
  due diligence, mas uma reapresentação pode ser só a inclusão do parecer (Gerdau 2024:
  v1 com `parecer: null`, v2 cinco dias depois com "Sem Ressalva"). Para dizer o que mudou,
  compare `valor_atual` das duas versões pelo conta a conta; sem isso, diga só que houve
  reapresentação e a data.
- `valor_anterior` é o comparativo **republicado na mesma DFP** e pode divergir do
  `valor_atual` da entrega anterior. Série usa a última versão de cada exercício; quando o
  comparativo diverge mais de 1% do publicado no ano anterior, diga que houve
  reclassificação ou reapresentação do comparativo.

## Parecer

- `auditor.tipo` é estruturado: "Sem Ressalva", "Com Ressalva", "Adverso", "Negativa de
  Opinião". Na linha do tempo, `parecer: null` significa entrega sem parecer carregado.
- Ênfase, incerteza relevante de continuidade e outros assuntos só lendo `auditor.texto`:
  procure "ênfase", "continuidade operacional", "incerteza relevante", "outros assuntos".
- "Principais assuntos de auditoria" não é ressalva nem ênfase.
- Firma e data ficam no fim do texto; cite as duas. Troca de firma entre exercícios é
  sinal: compare pareceres de dois `id_doc`.
- O texto vem sem quebras de linha entre seções; leia por frase.

## Ranking

- `ano` obrigatório; `visao` (padrão consolidado) e `familia` explícitas na resposta.
- Grupos duplicam (JBS S.A. e JBS N.V. com a mesma receita de 2025): dedupe pelo `slug`
  da `empresa` ou pelo nome e diga que deduplicou.
- Não há filtro por UF nem setor: para setor, cruze com `cnae_principal` da
  `ficha_empresa` de publicações; para UF idem. Diga que o corte foi feito do lado do
  agente e que o teto é 50 por chamada.
- `metrica` = `ativo`, `patrimonio`, `receita` ou `lucro`. Valores em reais da última
  versão de cada companhia no exercício.

## Indicadores com o conta a conta

Proveniência 1 (da base), com o código da conta ao lado na apresentação. Mapa completo em
[references/contas-dfp.md](references/contas-dfp.md). Use valor absoluto de contas que
vêm negativas (custo, despesas, depreciação).

| Indicador | Fórmula | Ressalva obrigatória |
|---|---|---|
| EBITDA | 3.05 + \|7.04.01\| (DVA) | depreciação da DVA inclui amortização e exaustão |
| Dívida bruta | 2.01.04 + 2.02.01 | dizer se arrendamento (2.01.04.03 e 2.02.01.03) entrou; padrão: entra, porque está dentro da conta |
| Dívida líquida | dívida bruta − 1.01.01 − 1.01.02 | aplicações de longo prazo (1.02.01.01 a 1.02.01.03) ficam fora por padrão; diga |
| Cobertura de juros | 3.05 / \|3.06.02\| | 3.06.02 inclui variação cambial e perdas com derivativos; se a companhia abre 3.06.02.01 "Despesas Financeiras", use-a e diga |
| Caixa operacional | 6.01 | método em `metodo` (direto ou indireto) |
| Caixa operacional sobre dívida bruta | 6.01 / dívida bruta | |
| Juros pagos | linha com "juros" em 6.01.03 ou em 6.03 | não padronizada; cite a descrição |
| Capex | linhas de adição de imobilizado e intangível em 6.02 | não padronizada; cite a descrição |
| Lucro dos controladores | 3.11.01 | para ROE, com PL sem não controladores: 2.03 − 2.03.09 |
| Equivalência no resultado | 3.04.06 | dependência de coligadas e controladas em conjunto |
| Não recorrentes | 3.04.03 (impairment), 3.10 (descontinuadas) | |
| Prazos médios | contas a receber 1.01.03, estoques 1.01.04, fornecedores 2.01.02 sobre receita 3.01 e custo 3.02, vezes 365 | saldo de fim de exercício |

Contas com `padronizada: false` variam por companhia: cite código e descrição.
Indicadores da skill indicadores-financeiros (liquidez, endividamento, margens, ROE)
continuam valendo com os campos de `balancos[]` e `dres[]`, agora na visão escolhida.

## O que a CVM não tem

ITR trimestral, notas explicativas em campo estruturado (continuam no `texto_documento`
da publicação), valor de mercado, companhias fechadas, exercícios anteriores a 2010.
Quando pedirem, diga e aponte a fonte publicações ou o link.

## Ao apresentar

- Visão, versão e `id_doc` da entrega usada; `link_documento` (balancos.ai) e `link_cvm`
  de cada entrega citada; link da `empresa`.
- Código da conta ao lado de cada indicador derivado.
- `dados_atualizados_em` da família CVM, que difere do das publicações.
- Ranking é dentro das companhias com DFP no exercício; diga o N e a família.
