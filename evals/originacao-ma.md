# Eval: originacao-ma

## Cenário 1: alvos e compradores

**Prompt**: "Assessoro um fundo que quer comprar empresas de energia no Sul do Brasil
(RS, SC, PR), de porte médio, com receita entre R$ 100 milhões e R$ 1 bilhão. Mapeia
alvos de aquisição pra mim, com uma tese curta pra cada um. E me diz também quem
poderia ser comprador estratégico da CEEE-G."

**Esperado com a skill**:
- Roda `ranking_empresas` por UF (uma chamada por UF) e por métrica, e filtra a faixa
  de receita do lado do agente, declarando o teto de 50 por chamada.
- Descarta linhas com receita zero ou irrisória e holdings (CNAE) antes de listar.
- Não usa o ranking de crescimento como "quem cresce" sem filtrar base mínima de
  ativo; explica que é crescimento de ativo total.
- Longlist com tese de uma linha e link; shortlist de compradores com capacidade
  (PL, liquidez) e encaixe; diz que controle acionário e sócios não estão na base.
