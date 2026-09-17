# Eval: originacao-ma

## Cenário 1: alvos e compradores

**Prompt**: "Assessoro um fundo que quer comprar empresas de energia no Sul do Brasil
(RS, SC, PR), de porte médio, com receita entre R$ 100 milhões e R$ 1 bilhão. Mapeia
alvos de aquisição pra mim, com uma tese curta pra cada um. E me diz também quem
poderia ser comprador estratégico da CEEE-G."

**Baseline (sem skill)**: 62 chamadas e 229 mil tokens, metade gastos descobrindo que o
rótulo do setor é "Eletricidade e Gás" e não "energia"; acertou tiers por localização do
ativo e descartou comercializadoras e dado velho, mas com controladores e localização de
usinas vindos de conhecimento externo, rotulados "a confirmar".

**Esperado com a skill**:
- Roda `ranking_empresas` por UF (uma chamada por UF) e por métrica, e filtra a faixa
  de receita do lado do agente, declarando o teto de 50 por chamada.
- Descarta linhas com receita zero ou irrisória e holdings (CNAE) antes de listar.
- Não usa o ranking de crescimento como "quem cresce" sem filtrar base mínima de
  ativo; explica que é crescimento de ativo total.
- Longlist com tese de uma linha e link; shortlist de compradores com capacidade
  (PL, liquidez) e encaixe; diz que controle acionário e sócios não estão na base.

## Cenário novo: cooperativas alvo

**Prompt**: "Mapeia cooperativas de crédito no Rio Grande do Sul que podem ser alvo de
incorporação."

**Esperado**: `bcb_ranking_instituicoes` por ativo e carteira com `uf="RS"` e `tipo="9"`;
tese por PL, Basileia e crescimento de carteira; diz o N e a data-base.

## Cenário novo: compradores abertos

**Prompt**: "Quem poderia comprar a <companhia aberta do setor X>?"

**Esperado**: `cvm_ranking_companhias` por patrimônio na família comercial, cruzando CNAE
pela ficha; capacidade por caixa e dívida líquida do conta a conta.
