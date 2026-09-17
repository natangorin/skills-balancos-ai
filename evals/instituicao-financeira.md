# Eval: instituicao-financeira

## Cenário 1: achar o banco

**Prompt**: "Como está o Banrisul?"

**Baseline (sem skill)**: `bcb_buscar_instituicoes("Banrisul")` devolveu 20 fundos;
tentou com tipo 8 e não achou; desistiu ou usou só as publicações.

**Esperado com a skill**: obtém o CNPJ (por `buscar_empresas` ou conhecimento) e busca
pela raiz 92702067; `bcb_analisar_instituicao`; memo de banco com ativo, carteira,
captações, PL, Basileia na última data-base, nível prudencial e CodInst declarados.

## Cenário 2: nível prudencial versus individual

**Prompt**: "Qual o ativo total do Banrisul, o banco só, sem as controladas?"

**Baseline**: deu o número do prudencial.

**Esperado**: `bcb_trimestres_instituicao` com `nivel="individual"`; diz que o padrão da
instituição é o prudencial e que o individual exclui a corretora e a instituição de
pagamento (membros em `bcb_conglomerado`).

## Cenário 3: lucro semestral versus anual

**Prompt**: "Quanto o Banrisul lucrou em 2025?"

**Baseline**: somou os quatro `lucro_liquido_acumulado_semestre` ou usou só dezembro.

**Esperado**: usa `resultados_anuais` de 2025 com `completo: true`; explica que o IF.data
publica acumulado no semestre e que anual = junho + dezembro.

## Cenário 4: quebra de era

**Prompt**: "A carteira de crédito do Banrisul cresceu quanto de março de 2024 para março
de 2026?"

**Baseline**: calculou a variação sem ressalva.

**Esperado**: calcula, mas marca a quebra de era (COSIF 2000 até 202412, COSIF 2025
depois) e diz que parte da variação pode ser reclassificação contábil; `comparavel` do
relatório é a referência.

## Cenário 5: cooperativas por UF

**Prompt**: "Quais as maiores cooperativas de crédito do Paraná?"

**Baseline**: usou `ranking_empresas` com setor "Atividades Financeiras" e UF PR,
misturando bancos e holdings.

**Esperado**: `bcb_ranking_instituicoes(ativo, uf="PR", tipo="9")` no nível padrão; diz
a data-base, o N e que sistemas (Sicredi, Sicoob) aparecem por cooperativa singular.

## Cenário 6: para quem o banco empresta

**Prompt**: "Para que setores o Banrisul mais empresta?"

**Baseline**: não sabia.

**Esperado**: `bcb_estrutura_relatorios` da última data-base para confirmar o id, depois
`bcb_relatorios_instituicao` com `relatorio=129` (PJ por CNAE); tabela com as maiores
linhas, valor em reais, `valor_ano_anterior` quando comparável, nível e data-base.

## Resultados registrados

- 2026-09-17, cenário 1 (com "quanto lucrou em 2025" junto), com skill: passou.
  `buscar_empresas("Banrisul")` devolveu só subsidiárias e fundos; o agente repetiu com
  "Banco do Estado do Rio Grande do Sul", achou o CNPJ, e buscou no BCB pela raiz
  92702067 e na CVM pelo CNPJ. Usou o nível prudencial (CodInst 1000080154), citou era,
  data-base 202606, lucro anual de 2025 pela DRE derivada com `completo: true`
  (R$ 1,60 bi, semestres somados), consolidado da CVM ao lado (R$ 1,71 bi) com a
  diferença explicada, quebra de era marcada entre 2024 e 2025, Basileia em porcentagem
  com o mínimo rotulado como conhecimento geral, e o link do IF.data para trimestres sem
  documento. Achado: a busca de publicações também falha com o nome fantasia; a skill
  passou a mandar usar um trecho do nome oficial.
- 2026-09-17, cenários 2 a 6, com skill: todos passaram.
  - 2 (nível individual): `bcb_trimestres_instituicao` com `nivel="individual"`; bateu
    com a DFP da CVM; notou o prudencial menor que o individual em 202606
    (eliminações), agora dito na skill.
  - 3 (lucro anual): DRE derivada com `completo: true`, semestres somados, consolidado
    da CVM ao lado; em banco listado a DRE da CVM vem só com lucro líquido (registrado
    na skill companhia-aberta).
  - 4 (quebra de era): variação ponta a ponta, dentro de cada era e na fronteira, cada
    uma rotulada.
  - 5 (cooperativas do PR): `tipo="9"` e `b3S` com `uf="PR"`; descobriu que o ranking
    no nível padrão rotula cooperativas como prudencial com CNPJ nulo e que
    `bcb_conglomerado` devolve zero membros para elas, e repetiu o ranking com
    `nivel="individual"`. A skill passou a dizer isso. Centrais (b3C)
    entram no filtro de tipo 9; a skill passou a mandar separar.
  - 6 (carteira por setor): `bcb_estrutura_relatorios` e depois relatórios 129, 127,
    126, 130 e 123; descobriu que o CodInst do conglomerado não serve como chave; corrigido na
    skill: chave da instituição com `nivel`. Também
    notou que a carteira do SCR difere da contábil; registrado na skill.
