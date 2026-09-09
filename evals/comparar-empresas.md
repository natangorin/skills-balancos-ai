# Eval: comparar-empresas

## Cenário 1: três empresas do mesmo grupo

**Prompt**: "Compara a Gerdau S.A., a Metalúrgica Gerdau e a Gerdau Aços Longos: qual
é maior, qual é mais rentável, qual está mais endividada. Quero uma tabela lado a
lado."

**Esperado com a skill**:
- Resolve as três chaves via `buscar_empresas` e confirma que são as empresas certas.
- Alinha pelo **mesmo exercício** e declara quando uma empresa não tem aquele ano.
- Avisa que Metalúrgica Gerdau é controladora da Gerdau S.A. (CNAE/natureza) e que
  comparar holding com operacional distorce; sinaliza `consolidado` e `fonte`.
- Tabela com os indicadores da skill e leitura curta; links das três.
