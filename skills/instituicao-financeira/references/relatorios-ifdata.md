# Relatórios do IF.data e códigos de tipo

Ids de relatório valem por era contábil. A lista abaixo é da era COSIF 2025 (data-bases
202503 em diante), conferida em 202606. Antes de chamar `bcb_relatorios_instituicao`
para outra data-base, rode `bcb_estrutura_relatorios(data_base)` e confira o id.

## Relatórios (era COSIF 2025)

| Id | Nome | Grupo | Nível |
|---|---|---|---|
| 121 | Resumo | demonstracoes | prudencial |
| 119 | Resumo | demonstracoes | financeiro |
| 120 | Resumo | demonstracoes | individual |
| 105 | Ativo | demonstracoes | prudencial |
| 107 | Ativo | demonstracoes | financeiro |
| 106 | Ativo | demonstracoes | individual |
| 108 | Passivo | demonstracoes | prudencial |
| 110 | Passivo | demonstracoes | financeiro |
| 109 | Passivo | demonstracoes | individual |
| 116 | Demonstração de Resultado | demonstracoes | prudencial |
| 118 | Demonstração de Resultado | demonstracoes | financeiro |
| 117 | Demonstração de Resultado | demonstracoes | individual |
| 115 | Informações de Capital | capital | prudencial |
| 123 | Carteira de crédito ativa Pessoa Física, modalidade e prazo de vencimento | carteira | prudencial |
| 128 | Carteira de crédito ativa Pessoa Jurídica, modalidade e prazo de vencimento | carteira | prudencial |
| 129 | Carteira de crédito ativa Pessoa Jurídica, por atividade econômica (CNAE) | carteira | prudencial |
| 127 | Carteira de crédito ativa Pessoa Jurídica, por porte do tomador | carteira | prudencial |
| 124 | Carteira de crédito ativa, quantidade de clientes e de operações | carteira | prudencial |
| 130 | Carteira de crédito ativa, por carteiras de instrumentos financeiros | carteira | prudencial |
| 125 | Carteira de crédito ativa, por indexador | carteira | prudencial |
| 126 | Carteira de crédito ativa, por região geográfica | carteira | prudencial |
| 131 | Segmentação | segmentacao | prudencial |

O Resumo (121) traz, numa chamada, ativo total, carteira de crédito, TVM, passivo
exigível, captações, PL, lucro líquido, patrimônio de referência, Basileia e imobilização,
com `valor_ano_anterior` quando a era é a mesma.

Os relatórios de carteira e capital existem só no nível prudencial (ou individual, para
quem não tem conglomerado). A DRE (116) tem 60 colunas: receitas e despesas de
intermediação abertas por natureza, resultado de serviços, despesas de pessoal e
administrativas, provisões.

## Códigos de tipo de instituição (`tipo`, TI)

Os que apareceram nos testes; a lista do IF.data é maior.

| Código | Tipo |
|---|---|
| 8 | Banco múltiplo |
| 9 | Cooperativa de crédito |
| 15 | Sociedade corretora de TVM |
| 41 | Instituição de pagamento |
| 199 | Conglomerado prudencial (aparece no ranking, `nome` nulo) |

## Códigos de consolidado bancário (`consolidado_bancario`, TCB)

| Código | Grupo |
|---|---|
| b1 | Banco comercial ou múltiplo com carteira comercial |
| b2 | Banco múltiplo sem carteira comercial ou banco de investimento |
| b3S | Cooperativa de crédito singular |
| b3C | Cooperativa de crédito central |
| b4 | Banco de desenvolvimento |
| n1 | Não bancário de crédito |
| n2 | Não bancário de mercado de capitais |
| n4 | Instituição de pagamento |

`segmento_prudencial` vai de S1 (bancos sistêmicos) a S5 (menor porte).
