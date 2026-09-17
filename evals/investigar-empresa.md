# Eval: investigar-empresa

## Cenário 1: holding com receita irrisória

**Prompt**: "Me conta sobre a CPFL Energia: o que a empresa é, que tamanho tem, como
está financeiramente nos últimos anos e o que ela publicou recentemente."

**Baseline (sem skill)**: detectou a holding e ressalvou o consolidado, mas misturou
conhecimento externo (controlador, revisões tarifárias) com dado da base sem rotular,
citou fatos do relatório a partir do preview de 2 KB, não sabia o que fazer com receita
negativa em 2020 e custo positivo em 2024, e chamou de "1º do setor" um ranking de 11
empresas misturando holding e operacionais.

**Esperado com a skill**:
- Uma chamada de `analisar_empresa` (depois de resolver a chave) em vez de várias.
- Percebe pela ficha (CNAE de holding) e pelo contraste receita × ativo que o
  exercício disponível pode ser o individual da holding, e diz isso em vez de
  concluir "receita despencou".
- Memo no formato da skill: identidade, tamanho, tendência, rentabilidade,
  estrutura de capital, publicações, ressalvas, links.
- Cita `dados_atualizados_em` e os links da empresa e dos documentos.

## Cenário novo: companhia aberta

**Prompt**: "Me conta sobre a Gerdau S.A."

**Esperado**: memo na variante CVM: natureza do dado com código CVM, família e visão
consolidada; tamanho e trajetória consolidados; seção 5 com EBITDA, dívida líquida,
cobertura e caixa operacional com código; tipo do último parecer.

## Cenário novo: banco

**Prompt**: "Me conta sobre a Cooperativa de Economia e Crédito Mútuo dos Empregados do
Banrisul."

**Esperado**: memo na variante BCB, nível individual (cooperativa singular, b3S), oito
trimestres, ROE anual, Basileia com o mínimo rotulado como conhecimento geral.
