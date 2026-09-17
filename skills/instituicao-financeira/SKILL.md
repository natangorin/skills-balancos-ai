---
name: instituicao-financeira
description: Use quando a empresa for banco, cooperativa de crédito, financeira, corretora ou outra instituição do IF.data do Banco Central, e o pedido envolver carteira de crédito, captações, Basileia, conglomerado, série trimestral ou ranking de instituições, com o MCP do Balanços.AI conectado. Assume a skill balancos-ai.
license: MIT
compatibility: Requer o MCP do Balanços.AI conectado. Assume a skill balancos-ai.
metadata:
  author: Balanços.AI
  version: "0.2"
---

# Instituição financeira pelo IF.data

## Resultado

O mesmo tipo de entrega da skill que chamou, com **nível de consolidação**, **data-base**
e **era contábil** declarados em cada número. Sem liquidez corrente, margem bruta nem giro:
banco tem vocabulário próprio (abaixo).

## Fluxo

1. `bcb_buscar_instituicoes(termo, uf, tipo, consolidado_bancario)`. **Raiz do CNPJ
   (8 dígitos) primeiro.** Nome só com `tipo` (8 banco múltiplo, 9 cooperativa de crédito)
   e sabendo de dois problemas: fundos de investimento poluem a busca ("Banrisul" devolve
   20 fundos e não o banco) e nome fantasia não casa com o oficial ("Banrisul" com tipo 8
   devolve zero; o oficial é "Banco do Estado do Rio Grande do Sul"). Se o usuário deu nome
   fantasia, obtenha o CNPJ por `buscar_empresas` das publicações ou pelo MCP do cnpj.ai
   se disponível, e busque pela raiz.
2. `bcb_analisar_instituicao(chave)`, chave = CodInst, CNPJ ou raiz. Uma chamada: ficha
   (`tipo`, `consolidado_bancario`, `segmento_prudencial`, sede, `conglomerados`,
   `niveis[]` com o CodInst de cada um e `padrao`, `ultima_data_base_resumo`), série
   `trimestres[]` do nível padrão e `resultados_anuais[]` (DRE derivada).
3. `bcb_trimestres_instituicao(chave, nivel, desde, ate)` para outro nível ou janela.
4. `bcb_resultados_instituicao(chave, nivel, periodo)` para trimestre isolado
   (`periodo="trimestre"`).
5. `bcb_estrutura_relatorios(data_base)` para achar o `relatorio`, depois
   `bcb_relatorios_instituicao(chave, nivel, data_base, relatorio)`: **um relatório por
   chamada**; sem `relatorio` a resposta é grande.
6. `bcb_conglomerado(codinst, nivel)` para os membros de um conglomerado, cada um com CNPJ
   e link de empresa.
7. `bcb_ranking_instituicoes(metrica, data_base, nivel, uf, tipo, consolidado_bancario,
   limite)`.
8. `bcb_data_bases()` para a última data-base e a era de cada uma.

Campos de cada resposta em [references/payloads.md](references/payloads.md).

## Níveis de consolidação

- `individual`, `financeiro` e `prudencial`, cada um com o próprio CodInst em
  `niveis[]`. Banco grande reporta pelo **prudencial**, que é o `nivel_padrao`; cooperativa
  singular e instituição independente reportam pelo individual.
- Compare instituições no nível padrão de cada uma: `nivel="padrao"` no ranking dá uma
  linha por grupo. Nunca some o individual ao prudencial do mesmo grupo.
- Linhas prudenciais do ranking vêm com `cnpj` e `empresa` nulos ("ITAU - PRUDENCIAL"):
  para chegar à empresa e ao link, `bcb_conglomerado(codinst)` lista os membros em ordem
  de ativo, com CNPJ e link.
- Diga qual nível usou e o CodInst, em toda tabela.

## Tempo

- Data-base `AAAAMM` com mês 03, 06, 09 ou 12. A última vem em `ultima_data_base` da
  ficha e em `bcb_data_bases`.
- O IF.data publica **lucro acumulado no semestre** (`lucro_liquido_acumulado_semestre`):
  março traz janeiro a março, junho traz janeiro a junho, setembro traz julho a setembro,
  dezembro traz julho a dezembro. Trimestre isolado: T1 = mar, T2 = jun − mar, T3 = set,
  T4 = dez − set; anual = jun + dez. A DRE derivada (`resultados`) já faz isso e marca
  `completo`; use-a em vez de recalcular. Não compare lucro de junho com lucro de setembro
  como se fossem o mesmo período.
- Era contábil: `cosif_2000` até 202412 e `cosif_2025` de 202503 em diante. Comparação
  ano contra ano só dentro da mesma era; `bcb_relatorios_instituicao` devolve
  `comparavel` e `valor_ano_anterior` já respeitando isso. Numa série que cruza a
  fronteira, marque a quebra e não atribua a ela variação de negócio.
- Campos nulos em trimestres antigos (`tvm` antes de 2025, `indices` antes de 2015,
  `rede` em toda a série de alguns bancos) ficam em branco, nunca zero.
- `link_documento` só existe em trimestres de dezembro (publicação anual); nos demais,
  aponte `link_ifdata`.

## Índices

- `indices.basileia`, `imobilizacao` e `alavancagem` vêm em **fração** (0,159 é 15,9%).
  No ranking, `unidade` diz se `valor` é reais ou fração.
- Basileia se compara com o mínimo regulatório vigente; o mínimo é conhecimento geral e vai
  rotulado "de conhecimento geral, não confirmado na base". Idem imobilização e
  alavancagem.
- `patrimonio_referencia` e `rwa` em reais; Basileia = PR / RWA.

## Indicadores próprios

| Indicador | Fórmula | Leitura |
|---|---|---|
| ROE anual | `lucro_liquido` anual (`resultados_anuais`, `completo: true`) / `patrimonio_liquido` de dezembro | PL de fim de ano; diga |
| Carteira sobre ativo | `carteira_credito` / `ativo_total` | quanto do balanço é crédito |
| Captações sobre ativo | `captacoes` / `ativo_total` | dependência de funding |
| Crescimento de carteira | carteira(t) / carteira(t − 4 trimestres) − 1 | mesma era |
| Crescimento de captações | idem | |
| Basileia, imobilização, alavancagem | `indices` | fração; mínimo rotulado |
| Lucro semestral | `lucro_liquido_acumulado_semestre` em junho e em dezembro | sazonal; não some com março |
| Rede | `rede.agencias`, `rede.postos` | quando existir |
| TVM sobre ativo | `tvm` / `ativo_total` | só a partir de 2025 |

A DRE derivada tem `receita_liquida` (receitas de intermediação financeira e de serviços),
`custo` (despesas de intermediação) e `lucro_bruto` (resultado de intermediação). Explique
isso antes de qualquer razão e chame de "margem de intermediação", nunca "margem bruta".
`lucro_operacional` e `lucro_liquido` seguem o sentido usual.

## Relatórios conta a conta

Ids mudam por era: **reconfira com `bcb_estrutura_relatorios(data_base)`** antes de pedir.
Na era COSIF 2025 (202503 em diante): Resumo 121 (prudencial), 119 (financeiro), 120
(individual); Ativo 105/107/106; Passivo 108/110/109; Demonstração de Resultado
116/118/117; Informações de Capital 115; carteira de crédito 123 a 130; Segmentação 131.
Lista completa em [references/relatorios-ifdata.md](references/relatorios-ifdata.md).

"Para quem o banco empresta" responde-se com carteira PJ por atividade econômica (129),
por porte do tomador (127) e por região (126); "que tipo de crédito" com PF (123) e PJ
(128) por modalidade e prazo; "risco" com por instrumento (130) e por indexador (125).
Cada linha traz `formato` (`mil` = reais, `pct` = fração, `inteiro` = contagem),
`valor` e `valor_ano_anterior`.

## Cooperativas e sistemas

Cooperativa singular é `consolidado_bancario` `b3S`, tipo 9, nível individual. Sistemas
(Sicredi, Sicoob, Unicred) são centenas de CNPJs; a central e o banco do sistema aparecem
como conglomerado. Diga qual entidade analisou e não some cooperativas por conta própria.
Ranking de cooperativas por UF: `tipo="9"` ou `consolidado_bancario="b3S"` com `uf`.

## O que o BCB não tem

Parecer do auditor (CVM, se listado, ou texto da publicação), notas explicativas, DFC,
valor de mercado, instituições fora do IF.data (instituições de pagamento só de 2020 em
diante), fundos de investimento com série útil (aparecem na busca com uma ou poucas
data-bases: ignore-os).

## Ao apresentar

- Nível, CodInst, data-base e era em cada tabela; `link_documento` quando houver ou
  `link_ifdata`; link da `empresa` no balancos.ai.
- Valores em R$ mi ou bi com a unidade escrita; índices em porcentagem com uma casa.
- `dados_atualizados_em` da família BCB.
- Ranking é dentro do IF.data na data-base; diga o N e o nível.
