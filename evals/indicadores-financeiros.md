# Eval: indicadores-financeiros

## Cenário 1: tabela de indicadores em 3 exercícios

**Prompt**: "Calcula os principais indicadores financeiros da CEEE-G (geração de
energia, RS) nos últimos 3 exercícios: liquidez, endividamento, margens,
rentabilidade, EBITDA e cobertura de juros. Quero uma tabela com a evolução."

**Esperado com a skill**:
- Usa os campos exatos do payload (`ativo_circulante`, `passivo_circulante`,
  `patrimonio_liquido`, `receita_liquida`, `lucro_liquido`...) com as fórmulas da
  skill; ROE e ROA com PL/ativo de fim de exercício, declarado.
- Declara EBITDA e cobertura de juros como incomputáveis pelo dado estruturado e
  aponta o caminho pelo texto.
- Pareia BP e DRE pelo mesmo `exercicio`; não mistura anos.
- Sinaliza `fonte` (llm/xbrl) e `consolidado` quando variam entre exercícios.
