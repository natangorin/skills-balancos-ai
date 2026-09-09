# Eval: investigar-empresa

## Cenário 1: holding com receita irrisória

**Prompt**: "Me conta sobre a CPFL Energia: o que a empresa é, que tamanho tem, como
está financeiramente nos últimos anos e o que ela publicou recentemente."

**Esperado com a skill**:
- Uma chamada de `analisar_empresa` (depois de resolver a chave) em vez de várias.
- Percebe pela ficha (CNAE de holding) e pelo contraste receita × ativo que o
  exercício disponível pode ser o individual da holding, e diz isso em vez de
  concluir "receita despencou".
- Memo no formato da skill: identidade, tamanho, tendência, rentabilidade,
  estrutura de capital, publicações, ressalvas, links.
- Cita `dados_atualizados_em` e os links da empresa e dos documentos.
