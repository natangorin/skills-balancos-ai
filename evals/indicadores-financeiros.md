# Eval: indicadores-financeiros

## Cenário 1: tabela de indicadores em 3 exercícios

**Prompt**: "Calcula os principais indicadores financeiros da CEEE-G (geração de
energia, RS) nos últimos 3 exercícios: liquidez, endividamento, margens,
rentabilidade, EBITDA e cobertura de juros. Quero uma tabela com a evolução."

**Baseline (sem skill)**: fórmulas corretas e EBITDA declarado incomputável, mas derivou o
resultado financeiro de 2023 por regra de três a partir de uma frase do relatório
("caiu 15,7%"), manteve na série um exercício com ativo de R$ 1.000 até notar, buscou
pela razão social completa acentuada e obteve zero, e não sabia que `lucro_operacional`
muda de sentido entre xbrl e llm.

**Esperado com a skill**:
- Usa os campos exatos do payload (`ativo_circulante`, `passivo_circulante`,
  `patrimonio_liquido`, `receita_liquida`, `lucro_liquido`...) com as fórmulas da
  skill; ROE e ROA com PL/ativo de fim de exercício, declarado.
- Declara EBITDA e cobertura de juros como incomputáveis pelo dado estruturado e
  aponta o caminho pelo texto.
- Pareia BP e DRE pelo mesmo `exercicio`; não mistura anos.
- Sinaliza `fonte` (llm/xbrl) e `consolidado` quando variam entre exercícios.

## Cenário novo: EBITDA de companhia aberta

**Prompt**: "Calcula o EBITDA e a dívida líquida / EBITDA da Gerdau nos últimos três
anos."

**Esperado**: reconhece que na CVM é computável, remete à skill companhia-aberta, usa
3.05 + |7.04.01| e dívida bruta − caixa − aplicações, um `id_doc` por exercício, visão
consolidada.

## Cenário novo: banco

**Prompt**: "Qual a liquidez corrente e a margem bruta do Banrisul?"

**Esperado**: diz que esses indicadores não se aplicam a banco, oferece carteira sobre
ativo, captações, Basileia e margem de intermediação (skill instituicao-financeira).
