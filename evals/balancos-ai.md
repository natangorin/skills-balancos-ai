# Eval: balancos-ai

## Cenário 1: dado que não existe

**Prompt**: "Qual foi o fluxo de caixa operacional e o EBITDA da Gerdau S.A. em 2024?
Me diz também a dívida líquida. E quantas empresas do setor de energia elétrica vocês
têm na base?"

**Baseline (sem skill)**: declarou EBITDA, fluxo de caixa e dívida líquida como não
estruturados e não estimou (bom), mas respondeu com o preview de 2 KB de um texto de
49 KB gravado em arquivo, quase leu `consolidado: false` da controladora como queda de
receita, estranhou o link do BP 2024 apontar para a DFP 2025 (`contexto: penultimo`) e
contou "empresas do setor" pelo ranking sem dizer que só cobre quem tem balanço.

**Esperado com a skill**:
- Diz que fluxo de caixa, EBITDA e dívida líquida não vêm em campo estruturado do MCP;
  oferece o que existe (BP com 8 linhas, DRE com 6) e o caminho pelo texto da
  publicação (`documentos_empresa` → `texto_documento`, DFC e notas).
- Não deriva EBITDA de lucro operacional sem dizer que é aproximação e o que falta.
- Diz que não há contagem por setor no MCP; `ranking_empresas` lista no máximo 50.
- Valores em reais, sem "em milhares"; cita `dados_atualizados_em`; inclui links.

## Cenário novo: empresa nas três fontes

**Prompt**: "Me dá um panorama do Banco do Estado do Rio Grande do Sul."

**Esperado**: `buscar_empresas`, percebe S.A. aberta e CNAE 64.22, busca na CVM pelo CNPJ e
no BCB pela raiz; diz qual fonte responde o quê (BCB para carteira e trimestre, CVM para
parecer, publicações para texto); cita o `dados_atualizados_em` de cada fonte.

## Resultados registrados

- 2026-09-17, cenário "empresa nas três fontes" (Banrisul), com skill: passou. Roteou
  pelas três, disse qual fonte responde o quê, citou os `dados_atualizados_em` de cada
  uma, leu o parecer da CVM inteiro do arquivo e apontou a ênfase sobre comparativos
  dispensados pela Resolução 4.966.
