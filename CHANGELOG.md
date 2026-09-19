# Changelog

Mudanças visíveis para quem usa as skills, por versão. A tag `vX.Y.Z` do repositório
corresponde à `metadata.version` `X.Y` das skills que mudaram. A seção mais recente no
topo define a versão: no merge na `main`, se a tag dela não existe, a release sai sozinha. Formato inspirado em
[Keep a Changelog](https://keepachangelog.com/pt-BR/1.1.0/).

## [0.4.0] - 2026-09-19

O MCP 0.4.0 passou a servir o ITR da CVM: entregas trimestrais, série trimestral com
trimestre, acumulado e últimos doze meses, e ranking por doze meses. Quatro tools da CVM
mudaram de nome sem alias, e as skills 0.3 chamavam os nomes antigos.

### Alterado

- Nomes das tools da CVM em todas as skills: `cvm_dfps_companhia` virou
  `cvm_entregas_companhia` (com `tipo` `dfp` ou `itr`), `cvm_entrega_dfp` virou
  `cvm_entrega`, `cvm_demonstracoes_dfp` virou `cvm_demonstracoes` e `cvm_parecer_dfp`
  virou `cvm_parecer`. Cliente que ainda mostra os nomes antigos precisa reconectar o MCP.
- `companhia-aberta`: seção nova "Trimestral e últimos doze meses" (dado mais recente é o
  ITR, 12M pronto e sem soma de trimestres, `derivado`, `consistente: false`, rótulo pela
  data de referência e exercício social fora de dezembro, conta a conta do ITR com
  trimestre isolado e acumulado, EBITDA e dívida líquida atuais, revisão do auditor no
  ITR); ranking com `periodo="12m"`; payloads de `cvm_trimestres_companhia`,
  `cvm_resultados_companhia`, do bloco `trimestral` de `cvm_analisar_companhia` e do
  ranking por doze meses.
- `balancos-ai`: tabela das 22 tools de CVM e BCB, fonte CVM com ITR e série trimestral,
  documento "Informações Trimestrais" no roteamento e no índice, ITR sem texto extraído,
  dois erros comuns novos.
- `due-diligence-financeira`: coluna com o BP do ITR e os doze meses na seção 3, revisão
  do ITR na seção 5, trimestre inconsistente na fonte como sinal.
- `investigar-empresa`: linha "mais recente" no memo de companhia aberta.
- `comparar-empresas`: bloco de doze meses na mesma data de referência entre companhias
  abertas; pares pelo ranking por doze meses.
- `originacao-ma`: corte de receita pelo ranking por doze meses.
- `indicadores-financeiros`: campos da série trimestral e ROE e ROA com doze meses.
- `ler-publicacao`: ITR sem texto, como a DFP; ressalva se responde com o parecer da DFP.
- `scripts/check.py` reconhece as 12 tools `cvm_*` do MCP 0.4.

### Removido

- "Sem ITR trimestral" das limitações da fonte CVM, do README e do memo de companhia
  aberta.

## [0.3.0] - 2026-09-17

O MCP 0.3.0 passou a entregar o texto integral das publicações: `texto_documento` ganhou
`inicio`, `tamanho` e `termo`, e o corte de 50 mil caracteres acabou. As skills que liam
texto foram reescritas em cima disso.

### Alterado

- `ler-publicacao`: fluxo novo. Pedido com assunto vai por `termo` (até 20 trechos com
  contexto e posição), entorno com `inicio`; pedido sobre o documento inteiro vai em
  pedaços com `proximo_inicio` até `truncado: false`. "Não está no documento" só depois
  de dois termos sem ocorrência ou da leitura integral. Orçamento de chamadas por tipo de
  pedido e nota sobre resultado gravado em arquivo no Claude Code.
- `balancos-ai`: tabela de tools, payload de `texto_documento` em `references/payloads.md`
  (dois modos, `origem_texto`), seção "Texto de publicações" e novo erro comum.
- `due-diligence-financeira`: roteiro de notas vira uma busca por `termo` por assunto;
  item ausente só depois de dois termos sem ocorrência.
- `indicadores-financeiros`: DVA e DFC no texto localizadas por `termo`.
- `investigar-empresa`: leitura do relatório por `termo` ou em pedaços.
- README: limitação dos 50 mil caracteres removida.

### Removido

- Instruções de contorno do corte de 50 mil caracteres (ler a publicação do ano anterior
  para pegar o que ficou fora, "não localizado nos primeiros 50 mil").

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

[0.3.0]: https://github.com/natangorin/skills-balancos-ai/releases/tag/v0.3.0
[0.2.0]: https://github.com/natangorin/skills-balancos-ai/releases/tag/v0.2.0
[0.1.0]: https://github.com/natangorin/skills-balancos-ai/tree/14d0e05
