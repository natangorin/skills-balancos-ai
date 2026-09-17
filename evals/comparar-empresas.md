# Eval: comparar-empresas

## Cenário 1: três empresas do mesmo grupo

**Prompt**: "Compara a Gerdau S.A., a Metalúrgica Gerdau e a Gerdau Aços Longos: qual
é maior, qual é mais rentável, qual está mais endividada. Quero uma tabela lado a
lado."

**Baseline (sem skill)**: alinhou pelo mesmo exercício e viu a cadeia holding, controladora
e operadora, mas ao achar a DRE 2025 da Gerdau Aços Longos com `escala_publicada`
"unidade" e valores em milhares, multiplicou por mil por conta própria; derivou campos
`null` por identidade sem avisar de forma consistente; e trouxe a estrutura societária
(GOAU, GGBR, Cosigua) de memória.

**Esperado com a skill**:
- Resolve as três chaves via `buscar_empresas` e confirma que são as empresas certas.
- Alinha pelo **mesmo exercício** e declara quando uma empresa não tem aquele ano.
- Avisa que Metalúrgica Gerdau é controladora da Gerdau S.A. (CNAE/natureza) e que
  comparar holding com operacional distorce; sinaliza `consolidado` e `fonte`.
- Tabela com os indicadores da skill e leitura curta; links das três.

## Cenário novo: aberta com fechada

**Prompt**: "Compara a Gerdau S.A. com a Gerdau Aços Longos."

**Esperado**: percebe que são andares do mesmo grupo; se comparar, iguala a visão
(individual da CVM contra individual das publicações) e diz o que se perde; não põe
consolidado de uma contra individual da outra.

## Cenário novo: bancos

**Prompt**: "Banrisul versus Banco do Brasil: quem é maior e mais rentável?"

**Esperado**: tabela de bancos (ativo, carteira, captações, PL, lucro anual, ROE, Basileia)
na mesma data-base e no nível padrão; BB via `bcb_conglomerado` para o link; sem liquidez
corrente nem margem bruta.
