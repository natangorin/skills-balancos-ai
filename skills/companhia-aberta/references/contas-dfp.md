# Mapa de contas padronizadas da DFP

Códigos com `padronizada: true` no plano de contas da CVM para a família `comercial`.
Os valores vêm em reais em `cvm_demonstracoes`. Os códigos são os mesmos na DFP e no ITR. Contas abaixo do nível 3 costumam
variar por companhia (`padronizada: false`): cite código e descrição ao usá-las.

## BPA (`demonstracao="bpa"`)

| Código | Conta | Uso |
|---|---|---|
| 1 | Ativo Total | |
| 1.01 | Ativo Circulante | |
| 1.01.01 | Caixa e Equivalentes de Caixa | dívida líquida |
| 1.01.02 | Aplicações Financeiras | dívida líquida |
| 1.01.03 | Contas a Receber | prazo médio de recebimento |
| 1.01.04 | Estoques | prazo médio de estoque |
| 1.01.06 | Tributos a Recuperar | |
| 1.02 | Ativo Não Circulante | |
| 1.02.01 | Ativo Realizável a Longo Prazo | |
| 1.02.01.01 a 1.02.01.03 | Aplicações Financeiras de longo prazo | fora da dívida líquida por padrão |
| 1.02.01.07 | Tributos Diferidos | qualidade do lucro |
| 1.02.01.09 | Créditos com Partes Relacionadas | due diligence |
| 1.02.02 | Investimentos | equivalência |
| 1.02.03 | Imobilizado | |
| 1.02.04 | Intangível | |
| 1.02.04.02 | Goodwill | impairment |

## BPP (`demonstracao="bpp"`)

| Código | Conta | Uso |
|---|---|---|
| 2 | Passivo Total (inclui PL) | |
| 2.01 | Passivo Circulante | |
| 2.01.02 | Fornecedores | prazo médio de pagamento |
| 2.01.04 | Empréstimos e Financiamentos (curto prazo) | dívida bruta |
| 2.01.04.01 | Empréstimos e Financiamentos | |
| 2.01.04.02 | Debêntures | |
| 2.01.04.03 | Financiamento por Arrendamento | dizer se entrou na dívida |
| 2.01.05.01 | Passivos com Partes Relacionadas | due diligence |
| 2.01.06 | Provisões | contingências |
| 2.02 | Passivo Não Circulante | |
| 2.02.01 | Empréstimos e Financiamentos (longo prazo) | dívida bruta |
| 2.02.01.01 / .02 / .03 | Empréstimos, Debêntures, Arrendamento | |
| 2.02.02.01 | Passivos com Partes Relacionadas | |
| 2.02.04 | Provisões | contingências |
| 2.02.04.01 | Provisões Fiscais, Previdenciárias, Trabalhistas e Cíveis | |
| 2.03 | Patrimônio Líquido (Consolidado) | |
| 2.03.01 | Capital Social Realizado | |
| 2.03.04 | Reservas de Lucros | |
| 2.03.05 | Lucros/Prejuízos Acumulados | |
| 2.03.09 | Participação dos Acionistas Não Controladores | PL dos controladores = 2.03 − 2.03.09 |

`passivo_total` de `balancos[]` (exigível) = 2.01 + 2.02, sem 2.03.

## DRE (`demonstracao="dre"`)

| Código | Conta | Uso |
|---|---|---|
| 3.01 | Receita de Venda de Bens e/ou Serviços | = `receita_liquida` |
| 3.02 | Custo dos Bens e/ou Serviços Vendidos | negativo |
| 3.03 | Resultado Bruto | |
| 3.04 | Despesas/Receitas Operacionais | |
| 3.04.01 | Despesas com Vendas | |
| 3.04.02 | Despesas Gerais e Administrativas | |
| 3.04.03 | Perdas pela Não Recuperabilidade de Ativos | impairment, não recorrente |
| 3.04.04 / 3.04.05 | Outras Receitas / Outras Despesas Operacionais | |
| 3.04.06 | Resultado de Equivalência Patrimonial | |
| 3.05 | Resultado Antes do Resultado Financeiro e dos Tributos | EBIT = `lucro_operacional` |
| 3.06 | Resultado Financeiro | |
| 3.06.01 | Receitas Financeiras | |
| 3.06.02 | Despesas Financeiras | cobertura de juros; inclui variação cambial |
| 3.07 | Resultado Antes dos Tributos sobre o Lucro | |
| 3.08 | Imposto de Renda e Contribuição Social | 3.08.01 corrente, 3.08.02 diferido |
| 3.09 | Resultado Líquido das Operações Continuadas | |
| 3.10 | Resultado Líquido de Operações Descontinuadas | não recorrente |
| 3.11 | Lucro/Prejuízo (Consolidado) do Período | = `lucro_liquido` |
| 3.11.01 | Atribuído a Sócios da Empresa Controladora | ROE dos controladores |
| 3.11.02 | Atribuído a Sócios Não Controladores | |
| 3.99 | Lucro por Ação | em reais por ação, não em milhares |

## DFC (`demonstracao="dfc"`)

| Código | Conta | Uso |
|---|---|---|
| 6.01 | Caixa Líquido Atividades Operacionais | geração de caixa |
| 6.01.01 | Caixa Gerado nas Operações | abaixo, linhas não padronizadas: lucro, depreciação, juros |
| 6.01.02 | Variações nos Ativos e Passivos | capital de giro |
| 6.01.03 | Outros | juros e IR pagos costumam estar aqui |
| 6.02 | Caixa Líquido Atividades de Investimento | capex nas linhas não padronizadas |
| 6.03 | Caixa Líquido Atividades de Financiamento | captações, amortizações, dividendos |
| 6.04 | Variação Cambial sobre Caixa e Equivalentes | |
| 6.05 | Aumento (Redução) de Caixa e Equivalentes | 6.05.01 inicial, 6.05.02 final |

Depreciação na DFC é linha não padronizada dentro de 6.01.01: use a DVA (7.04.01) para
EBITDA e cite a DFC só como conferência.

## DVA (`demonstracao="dva"`)

| Código | Conta | Uso |
|---|---|---|
| 7.01 | Receitas | 7.01.01 vendas, 7.01.02 outras, 7.01.04 PCLD |
| 7.02 | Insumos Adquiridos de Terceiros | |
| 7.03 | Valor Adicionado Bruto | |
| 7.04.01 | Depreciação, Amortização e Exaustão | EBITDA (valor absoluto) |
| 7.06.01 | Resultado de Equivalência Patrimonial | |
| 7.06.02 | Receitas Financeiras | |
| 7.08.01 | Pessoal | |
| 7.08.02 | Impostos, Taxas e Contribuições | |
| 7.08.03 | Remuneração de Capitais de Terceiros | 7.08.03.01 juros, quando preenchido |
| 7.08.04 | Remuneração de Capitais Próprios | JCP, dividendos, lucros retidos |

## DRA e DMPL

`dra` (resultado abrangente) e `dmpl` (mutações do PL) existem; use a DMPL para
dividendos declarados e movimentação de reservas, citando a descrição da linha.
