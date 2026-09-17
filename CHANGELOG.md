# Changelog

Mudanças visíveis para quem usa as skills, por versão. A tag `vX.Y.Z` do repositório
corresponde à `metadata.version` `X.Y` das skills que mudaram. Formato inspirado em
[Keep a Changelog](https://keepachangelog.com/pt-BR/1.1.0/).

## [0.2.0] - 2026-09-17

O MCP passou a expor três fontes: publicações legais, CVM (companhias abertas) e BCB
(instituições financeiras do IF.data). As skills foram reorganizadas em cima disso.

### Adicionado

- Skill `companhia-aberta`: fonte CVM, com visão consolidada e individual, conta a
  conta (BPA, BPP, DRE, DRA, DFC, DMPL, DVA), parecer do auditor estruturado,
  reapresentações e ranking de companhias abertas. Referências com os payloads e o mapa
  de códigos de conta da DFP.
- Skill `instituicao-financeira`: fonte BCB, com níveis de consolidação, série
  trimestral, lucro acumulado no semestre, eras contábeis COSIF 2000 e 2025, índices de
  Basileia, relatórios conta a conta do IF.data, conglomerados e ranking de
  instituições. Referências com os payloads e os ids de relatório por era.
- `balancos-ai`: roteamento por CNPJ entre as três fontes, tabela das tools de CVM e
  BCB e o que cada fonte não tem.
- `indicadores-financeiros`: EBITDA, dívida líquida, cobertura de juros e caixa
  operacional passam a ser computáveis para companhia aberta, com o código da conta.
- `investigar-empresa`: variantes de memo para companhia aberta e para banco.
- `comparar-empresas`: regra de mesma fonte, família e visão; pares pelos rankings da
  CVM e do BCB; tabela própria para bancos.
- `due-diligence-financeira`: parecer estruturado, dívida e caixa do conta a conta,
  trimestre mais recente do BCB; roteiro de notas com a coluna "Na CVM".
- `originacao-ma`: alvos e compradores pelos rankings da CVM e do BCB.
- `ler-publicacao`: parecer e conta a conta pela CVM quando a DFP não tem texto.
- `scripts/check.py` reconhece as tools `cvm_*` e `bcb_*`.
- Evals das duas skills novas e cenários novos nas demais, rodados contra produção em
  2026-09-17.

### Corrigido

- Busca de banco pelo nome fantasia: a skill manda usar a raiz do CNPJ ou um trecho do
  nome oficial.
- Chave das tools `bcb_*`: CodInst da instituição com `nivel`, nunca o do conglomerado.
- Ranking do BCB no nível padrão: cooperativas e independentes sem CNPJ; a skill manda
  repetir com `nivel="individual"`.
- Reapresentações na CVM: conferir `visoes` da v1 antes de pedir demonstrações.
- Arrendamento fora de 2.01.04 no cálculo de dívida bruta.

## [0.1.0] - 2026-09-10

Primeira versão pública do conjunto, escrita a partir dos baselines de sete cenários.

### Adicionado

- Skills `balancos-ai`, `indicadores-financeiros`, `investigar-empresa`,
  `comparar-empresas`, `due-diligence-financeira`, `originacao-ma` e `ler-publicacao`.
- Evals com o baseline sem skill e o comportamento esperado de cada cenário.
- `scripts/check.py` e CI com `make check`.
- Plugin do Claude Code com o MCP configurado.

[0.2.0]: https://github.com/natangorin/skills-balancos-ai/releases/tag/v0.2.0
[0.1.0]: https://github.com/natangorin/skills-balancos-ai/releases/tag/v0.1.0
