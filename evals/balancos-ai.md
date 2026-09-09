# Eval: balancos-ai

## Cenário 1: dado que não existe

**Prompt**: "Qual foi o fluxo de caixa operacional e o EBITDA da Gerdau S.A. em 2024?
Me diz também a dívida líquida. E quantas empresas do setor de energia elétrica vocês
têm na base?"

**Esperado com a skill**:
- Diz que fluxo de caixa, EBITDA e dívida líquida não vêm em campo estruturado do MCP;
  oferece o que existe (BP com 8 linhas, DRE com 6) e o caminho pelo texto da
  publicação (`documentos_empresa` → `texto_documento`, DFC e notas).
- Não deriva EBITDA de lucro operacional sem dizer que é aproximação e o que falta.
- Diz que não há contagem por setor no MCP; `ranking_empresas` lista no máximo 50.
- Valores em reais, sem "em milhares"; cita `dados_atualizados_em`; inclui links.
