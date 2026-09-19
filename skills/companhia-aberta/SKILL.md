---
name: companhia-aberta
description: Use quando a empresa for companhia aberta (S.A. com DFP ou ITR na CVM) e o pedido envolver consolidado, conta a conta, DFC, DVA, EBITDA, dívida líquida, cobertura de juros, parecer do auditor, reapresentação, resultado do trimestre, ITR, últimos doze meses ou ranking de companhias abertas, com o MCP do Balanços.AI conectado. Assume a skill balancos-ai.
license: MIT
compatibility: Requer o MCP do Balanços.AI conectado. Assume as skills balancos-ai e indicadores-financeiros.
metadata:
  author: Balanços.AI
  version: "0.4"
---

# Companhia aberta pela CVM

## Resultado

O mesmo tipo de entrega da skill que chamou (memo, tabela, relatório), com **visão**
(consolidado ou individual), **versão** e `id_doc` da entrega declarados em cada número,
a **data de referência** e o **período** (trimestre, acumulado, doze meses ou anual) de
cada resultado, e o código da conta ao lado de cada indicador derivado do conta a conta.

## Fluxo

1. `cvm_buscar_companhias(termo)`: trecho da denominação ou CNPJ. Até 20, com `cnpj`,
   `cd_cvm`, `denominacao` e `empresa` (slug e link do balancos.ai, quando está lá).
   Vindo da skill balancos-ai, use o CNPJ da ficha de publicações.
2. `cvm_analisar_companhia(chave)`, chave = CNPJ ou código CVM. Uma chamada traz a ficha
   (denominações anteriores, `familia`, primeiro e último exercício, número de entregas e
   de reapresentações, último parecer, capital social com ações em tesouraria), a linha do
   tempo `exercicios[]` das DFPs com `versoes[]` (`id_doc`, versão, `reapresentacao`,
   data, parecer, links), `balancos[]` e `dres[]` anuais por exercício e `visao`, na
   última versão de cada exercício, e `trimestral.mais_recente`: o ponto mais novo da
   série trimestral. Se a data de referência dele é posterior ao último exercício, ele é
   o dado atual e entra na resposta ao lado do anual. Só use `cvm_ficha_companhia`,
   `cvm_entregas_companhia`, `cvm_balancos_companhia` e `cvm_dres_companhia` para uma
   parte.
3. `cvm_trimestres_companhia(chave, desde?, ate?, visao?)`: série trimestral, um ponto por
   data de referência com o BP daquela data e três resultados (`trimestre`, `acumulado`,
   `doze_meses`). Sem intervalo vêm as 12 datas mais recentes (cerca de três anos) e um
   `aviso`; a história vai até 2011 com `desde`/`ate` (`AAAA-MM-DD`).
   `cvm_resultados_companhia(chave, periodo, desde?, ate?, visao?)` traz só a DRE da série
   num período (`trimestre`, `acumulado`, `12m` ou `anual`) e é a chamada leve para
   tendência.
4. `cvm_entregas_companhia(chave, tipo, ano?)`: `tipo="dfp"` (padrão, anual) ou `"itr"`
   (trimestral). Datas de referência decrescentes, versões crescentes, com o `id_doc` de
   cada versão.
5. `cvm_entrega(id_doc)` quando precisar saber quais visões e demonstrações a entrega
   tem (`visoes`, `demonstracoes_disponiveis`) antes de pedir o conta a conta. O campo
   `tipo` diz se é DFP ou ITR.
6. `cvm_demonstracoes(id_doc, demonstracao, visao)`: **uma demonstração por chamada**
   (`bpa`, `bpp`, `dre`, `dra`, `dfc`, `dmpl`, `dva`). Sem `demonstracao` a resposta é
   grande. Padrão da tool: consolidado, ou individual quando não há consolidado. Cada conta
   traz `codigo`, `descricao`, `nivel`, `padronizada`, `valor_atual` e `valor_anterior`;
   no ITR, veja a seção Trimestral.
7. `cvm_parecer(id_doc)`: `auditor.tipo`, `auditor.texto` integral e `declaracoes[]`
   (diretores sobre as demonstrações, diretores sobre o parecer, conselho fiscal).
8. `cvm_ranking_companhias(metrica, ...)`: por exercício (`ano`) ou pelos últimos doze
   meses (`periodo="12m"`); ver a seção Ranking.

Os três que recebem `id_doc` servem para DFP e ITR: o `id_doc` é único entre os dois.
Campos de cada resposta em [references/payloads.md](references/payloads.md).

## Visão

- **Consolidado é o padrão** para tamanho, operação, margens e comparação. É o que
  responde "que tamanho tem" e "quanto fatura".
- **Individual** só quando a pergunta é sobre a entidade (dividendos, capital social,
  obrigação própria, garantia dada pela controladora) ou quando não há consolidado (lista
  `visoes` em `cvm_entrega`; companhia sem controladas entrega só o individual).
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
  instituicao-financeira, que tem carteira, captações e Basileia. Em banco listado,
  `dres[]` da CVM vem só com `lucro_liquido` (receita, custo e bruto nulos) e `balancos[]`
  só com totais: use a CVM para consolidado, parecer e reapresentações, e o BCB para o
  resto.

## Trimestral e últimos doze meses

O dado mais recente de uma companhia aberta é o ITR; a DFP pode ter mais de um ano.
"Como está", "último resultado", "este ano" e qualquer pergunta sobre o presente vão à
série trimestral, com a data de referência escrita.

- **Três resultados por ponto.** `trimestre` = três meses isolados; `acumulado` = do
  início do exercício até a data; `doze_meses` = últimos doze meses (12M). Tendência sem
  sazonalidade: 12M. Sazonalidade: o trimestre contra o mesmo trimestre do ano anterior;
  contra o trimestre imediatamente anterior, só dizendo que há sazonalidade.
- **12M vem pronto; não some trimestres.** É acumulado corrente + DFP anterior −
  acumulado do mesmo ponto do ano anterior, e no fechamento é a própria DFP. A soma de
  quatro trimestres isolados diverge quando a fonte é inconsistente.
- **`derivado: true`**: o último trimestre do exercício não é publicado na CVM; é a DFP
  menos o acumulado de nove meses. Escreva "derivado" ao lado do número.
- **`consistente: false`**: na fonte, os trimestres isolados daquele exercício não fecham
  com o acumulado (reapresentação só de parte, isolado zerado, escala trocada). O número é
  o que a companhia entregou, sem correção: cite com esse aviso e prefira acumulado e 12M
  daquele exercício.
- **Rótulo pela data de referência** ("jun/26" ou "30/06/2026"), nunca "2T26". O
  exercício social pode não fechar em dezembro (Raízen, São Martinho, Camil), e
  `trimestre_exercicio` conta a partir do início do exercício da companhia, não do ano
  civil. Duas companhias se comparam na mesma data de referência; se o fechamento difere,
  diga.
- **Indicadores na série.** Liquidez e endividamento com o `balanco_em_reais` do ponto.
  ROE, ROA e giro com `doze_meses`, nunca com o trimestre isolado. Margem com receita e
  lucro do mesmo período, e o período no rótulo.
- **Conta a conta do ITR** (`cvm_demonstracoes` com o `id_doc` do ITR). Na DRE e na DRA,
  `valor_atual`/`valor_anterior` são o acumulado no exercício (atual e mesmo período do
  ano anterior), e `valor_trimestre_atual`/`valor_trimestre_anterior` o trimestre isolado.
  DFC e DVA vêm acumuladas no exercício. No BP, `valor_anterior` é o fechamento do
  exercício anterior, não o mesmo trimestre do ano anterior.
- **EBITDA e dívida líquida atuais.** Dívida bruta e líquida saem do BPP e do BPA do ITR
  mais recente. EBITDA 12M = (3.05 + |7.04.01|) acumulado no ITR + o mesmo da DFP
  anterior − o mesmo acumulado do ano anterior (`valor_anterior` do próprio ITR). Cite os
  dois `id_doc` e diga que o acumulado do ano anterior é o comparativo republicado.
  Dívida líquida / EBITDA com o BP e o EBITDA 12M da mesma data.
- **Parecer do ITR não é opinião.** No ITR o auditor faz revisão especial; `cvm_parecer`
  traz o Relatório de Revisão Especial com o mesmo campo `tipo`. "Tem ressalva" nas
  demonstrações anuais responde com a DFP. O ITR serve para ver se surgiu ênfase ou
  ressalva depois do último exercício.

## Versões e reapresentações

- A última versão de um exercício ou de uma data de referência é a que vale, e
  `cvm_analisar_companhia` e a série trimestral já a escolhem (`versao` e `id_doc` em
  cada linha de `balancos[]` e `dres[]`).
- `n_reapresentacoes` na ficha e `reapresentacao: true` na linha do tempo são sinal para
  due diligence, mas uma reapresentação pode ser só a inclusão do parecer (Gerdau 2024:
  v1 com `parecer: null`, v2 cinco dias depois com "Sem Ressalva"). A v1 costuma estar na
  base como casca vazia: `cvm_entrega` devolve `visoes: []` e o conta a conta responde
  "a entrega não tem a visão". Confira `visoes` da v1 antes de pedir demonstrações dela.
  Para saber se algum número mudou, compare o `valor_anterior` da DFP seguinte com o
  `valor_atual` da última versão do exercício; sem isso, diga só que houve reapresentação
  e a data.
- `valor_anterior` é o comparativo **republicado na mesma entrega** e pode divergir do
  `valor_atual` da entrega anterior. Série usa a última versão de cada exercício; quando o
  comparativo diverge mais de 1% do publicado no ano anterior, diga que houve
  reclassificação ou reapresentação do comparativo.
- O 12M de uma data muda quando qualquer das três entregas que o compõem é reapresentada;
  os links de origem do `doze_meses` listam as três.

## Parecer

- `auditor.tipo` é estruturado: "Sem Ressalva", "Com Ressalva", "Adverso", "Negativa de
  Opinião". Na linha do tempo, `parecer: null` significa entrega sem parecer carregado.
- Ênfase, incerteza relevante de continuidade e outros assuntos só lendo `auditor.texto`:
  procure "ênfase", "continuidade operacional", "incerteza relevante", "outros assuntos".
- "Principais assuntos de auditoria" não é ressalva nem ênfase.
- Firma e data ficam no fim do texto; cite as duas. Troca de firma entre exercícios é
  sinal: compare pareceres de dois `id_doc`.
- O texto vem sem quebras de linha entre seções; leia por frase. A resposta passa de
  40 mil caracteres: se o cliente a gravou em arquivo, leia o arquivo inteiro, não o
  preview.

## Ranking

- `periodo="anual"` (padrão): `ano` obrigatório; `metrica` = `ativo`, `patrimonio`,
  `receita` ou `lucro`. Valores da última versão de cada companhia no exercício.
- `periodo="12m"`: `metrica` = `receita` ou `lucro` (ativo e patrimônio são posição, use
  o anual); `data_referencia` opcional, e sem ela vem a mais recente com cobertura da
  maioria das companhias; `ano` é ignorado. É o ranking mais atual. Fica fora quem tem
  escala suspeita na fonte ou receita negativa; linha com `consistente: false` entra e
  vai com o aviso. As linhas não trazem `id_doc` nem versão: para citar a entrega, abra a
  série da companhia.
- `visao` (padrão consolidado), `familia` e o período explícitos na resposta.
- Grupos duplicam, por dupla listagem (JBS S.A. e JBS N.V. com a mesma receita) ou por
  controladora e controlada ambas abertas (Metalúrgica Gerdau e Gerdau S.A.): dedupe pelo
  `slug` da `empresa` ou pelo nome e diga que deduplicou.
- Não há filtro por UF nem setor: para setor, cruze com `cnae_principal` da
  `ficha_empresa` de publicações; para UF idem. Diga que o corte foi feito do lado do
  agente e que o teto é 50 por chamada.

## Indicadores com o conta a conta

Proveniência 1 (da base), com o código da conta ao lado na apresentação. Mapa completo em
[references/contas-dfp.md](references/contas-dfp.md), que vale para DFP e ITR. Use valor
absoluto de contas que vêm negativas (custo, despesas, depreciação).

| Indicador | Fórmula | Ressalva obrigatória |
|---|---|---|
| EBITDA | 3.05 + \|7.04.01\| (DVA) | depreciação da DVA inclui amortização e exaustão |
| Dívida bruta | 2.01.04 + 2.02.01 | arrendamento: se está em 2.01.04.03 e 2.02.01.03, entra; muitas companhias o lançam em "Outras Obrigações" (2.01.05.02.x e 2.02.02.02.x, "Arrendamento mercantil a pagar"), e aí fica fora; procure "arrendamento" nas descrições e diga o que fez |
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
No ITR, fluxos (EBITDA, caixa operacional, juros, prazos médios) são acumulados no
exercício: leve a 12M como na seção Trimestral, ou diga o período.

## O que a CVM não tem

Notas explicativas em campo estruturado (continuam no `texto_documento` da publicação),
texto e PDF do ITR, valor de mercado, companhias fechadas, DFP anterior a 2010 e ITR
anterior a 2011. Quando pedirem, diga e aponte a fonte publicações ou o link.

## Ao apresentar

- Visão, versão, tipo (DFP ou ITR) e `id_doc` da entrega usada; `link_documento`
  (balancos.ai) e `link_cvm` de cada entrega citada; link da `empresa`.
- Data de referência e período de cada resultado; "derivado" e o aviso de
  `consistente: false` quando aparecerem.
- Código da conta ao lado de cada indicador derivado.
- `dados_atualizados_em` da família CVM, que difere do das publicações.
- Ranking é dentro das companhias com DFP no exercício, ou com 12M na data de
  referência; diga o N, a família e o período.
