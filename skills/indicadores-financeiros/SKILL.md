---
name: indicadores-financeiros
description: Use quando precisar calcular ou interpretar liquidez, endividamento, alavancagem, margens, ROE, ROA, giro, capital de giro, CAGR ou tendência a partir dos balanços e DREs do MCP do Balanços.AI, ou quando pedirem EBITDA, dívida líquida, cobertura de juros e fluxo de caixa de uma empresa da base.
license: MIT
compatibility: Requer o MCP do Balanços.AI conectado. Assume a skill balancos-ai.
metadata:
  author: Balanços.AI
  version: "0.3"
---

# Indicadores financeiros com o dado do Balanços.AI

## Princípio

Cada indicador usa só campos que a resposta do MCP traz, com o nome exato do campo. O que
não dá para calcular com esses campos é declarado incomputável, com o caminho pelo texto
da publicação. Nada é estimado, inferido de frase de relatório ou trazido de memória.

## Campos disponíveis

BP (`balancos[].valores_em_reais`): `ativo_total`, `ativo_circulante`,
`ativo_nao_circulante`, `passivo_circulante`, `passivo_nao_circulante`, `passivo_total`
(exigível, sem PL), `patrimonio_liquido`, `passivo_e_pl_total`.

DRE (`dres[].valores_em_reais`): `receita_bruta`, `receita_liquida`, `custo`,
`lucro_bruto`, `lucro_operacional`, `lucro_liquido`.

Pareie BP e DRE pelo mesmo `exercicio`. Um ano sem BP ou sem DRE entra na tabela com o
indicador em branco, nunca com o ano vizinho no lugar.

Os mesmos nomes de campo voltam em `cvm_balancos_companhia` e `cvm_dres_companhia` (skill
companhia-aberta), com `visao` a mais: as fórmulas valem, e o cabeçalho diz a visão.
`bcb_resultados_instituicao` também usa esses nomes, mas com semântica de intermediação
financeira: não aplique esta skill a banco; use a skill instituicao-financeira.

## Fórmulas

| Indicador | Fórmula | Leitura |
|---|---|---|
| Liquidez corrente | `ativo_circulante` / `passivo_circulante` | abaixo de 1 = curto prazo não coberto |
| Liquidez geral | (`ativo_circulante` + `ativo_nao_circulante`) / `passivo_total` | |
| Capital de giro líquido | `ativo_circulante` − `passivo_circulante` | em reais |
| Endividamento geral | `passivo_total` / `ativo_total` | fração do ativo financiada por terceiros |
| Alavancagem | `passivo_total` / `patrimonio_liquido` | |
| Composição do endividamento | `passivo_circulante` / `passivo_total` | quanto do exigível vence em 12 meses |
| Imobilização do PL | `ativo_nao_circulante` / `patrimonio_liquido` | |
| Margem bruta | `lucro_bruto` / `receita_liquida` | |
| Margem operacional | `lucro_operacional` / `receita_liquida` | ver ressalva de `lucro_operacional` |
| Margem líquida | `lucro_liquido` / `receita_liquida` | |
| ROE | `lucro_liquido` / `patrimonio_liquido` | PL de fim de exercício; diga isso |
| ROA | `lucro_liquido` / `ativo_total` | ativo de fim de exercício |
| Giro do ativo | `receita_liquida` / `ativo_total` | |
| Variação anual | valor(ano) / valor(ano − 1) − 1 | receita, lucro, ativo, PL |
| CAGR | (valor(fim) / valor(início))^(1 / anos) − 1 | só com início positivo |

Use `custo` em valor absoluto: vem negativo no xbrl e positivo no llm.

## Derivações permitidas quando um campo vem `null`

Só identidades contábeis, e sempre dizendo que derivou:

- `passivo_total` = `passivo_circulante` + `passivo_nao_circulante`
- `lucro_bruto` = `receita_liquida` − |`custo`|
- `ativo_total` = `ativo_circulante` + `ativo_nao_circulante`
- `patrimonio_liquido` = `ativo_total` − `passivo_total`

Se faltar mais de um termo da identidade, o indicador fica em branco.

## Incomputável com o dado estruturado

| Pedido | Na fonte publicações | Na CVM (companhia aberta, skill companhia-aberta) |
|---|---|---|
| EBITDA | não há depreciação; "EBITDA ajustado" do relatório da administração, ou EBIT + depreciação da DVA no texto, rotulado aproximado | 3.05 + \|7.04.01\| da DVA, proveniência 1 |
| Dívida bruta e líquida | nota de empréstimos e nota de caixa no texto | 2.01.04 + 2.02.01, menos 1.01.01 e 1.01.02 |
| Cobertura de juros | DRE completa no texto; encargos de empréstimos na DVA | 3.05 / \|3.06.02\| |
| Fluxo de caixa | DFC no texto (depois da DMPL, antes das notas) | 6.01, 6.02, 6.03 da DFC |
| Prazo médio de recebimento, estoque, pagamento | notas explicativas | 1.01.03, 1.01.04, 2.01.02 sobre 3.01 e 3.02 |
| ROIC, múltiplos | fora da base | falta valor de mercado; fora |

Em instituição financeira nenhuma linha desta tabela se aplica; o vocabulário é carteira,
captações, Basileia e resultado de intermediação (skill instituicao-financeira).

Não use `lucro_operacional` como proxy de EBITDA, nem `passivo_total` como "dívida". Diga
"passivo exigível, que inclui fornecedores, tributos e provisões" quando usar alavancagem.

A **DVA** (demonstração do valor adicionado) traz "depreciação e amortização" e "encargos
de empréstimos" em linha própria; a DFC traz "caixa líquido das atividades operacionais" e
"pagamentos de juros". No texto da publicação, chegue a elas com `termo` em
`texto_documento` ("valor adicionado", "depreciação", "atividades operacionais", "juros
pagos") e leia o entorno com `inicio`. Cite-as literalmente com o link, na escala do
cabeçalho do documento.

Com valores citados do texto, é permitido montar indicador composto (EBIT da base sobre
despesa financeira do texto; dívida bruta menos caixa do texto; EBIT mais depreciação da
DVA), desde que cada parcela seja citada com link, a escala conferida e o resultado
rotulado "aproximado, com <linha> da publicação de <ano>". Indicadores calculados só
sobre valores literais da publicação (quando o exercício da base foi excluído por
anomalia) levam o rótulo "sobre valores da publicação, não da base". Inferir um valor a
partir de uma frase ("caiu 15,7%") continua proibido.

## `lucro_operacional` muda de sentido com a `fonte`

- `xbrl`: "resultado antes do resultado financeiro e dos tributos" (EBIT).
- `llm`: a linha que o PDF chamou de resultado operacional; pode conter o financeiro.

Margem operacional acima da margem bruta indica outras receitas ou equivalência
patrimonial dentro da linha, típico de holding ou de ano com ganho não recorrente.
Sinalize na tabela em vez de interpretar como eficiência.

## Tendência e anomalias

- Série de 3 a 5 exercícios, mais recente à direita, com `fonte` por ano quando varia.
- Exclua da série o exercício com ativo total de R$ 1.000 (contexto vazio), receita
  negativa, custo com sinal invertido ou salto de mil vezes num ano só. Diga qual excluiu,
  por quê, e ponha o link do documento para conferência.
- Salto de passivo entre circulante e não circulante muda liquidez corrente sem mudar a
  dívida total: mostre os dois e chame de "reclassificação", sem atribuir causa (covenant,
  vencimento) sem o texto da nota.
- Holding (`consolidado: false` com receita irrisória): margens e giro não fazem sentido;
  mostre só ROE, alavancagem e a tendência de PL e lucro, e diga por quê.

## Apresentação

Tabela com o ano no cabeçalho, valores em R$ mi ou bi com a unidade escrita, indicadores
com uma casa decimal ou em porcentagem, e uma linha de leitura por bloco (liquidez,
endividamento, margens, rentabilidade). Termine com a lista do que ficou incomputável e o
link da empresa.
