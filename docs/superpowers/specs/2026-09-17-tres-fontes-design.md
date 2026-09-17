# Skills sobre três fontes: publicações, CVM e BCB

Data: 2026-09-17. Estado: aprovado para plano de implementação.

## Contexto

As sete skills v0.1 foram escritas em cima das 8 tools originais do MCP do Balanços.AI
(família "publicações"): `buscar_empresas`, `ficha_empresa`, `analisar_empresa`,
`balancos_empresa`, `dres_empresa`, `documentos_empresa`, `texto_documento`,
`ranking_empresas`. O MCP passou a expor 29 tools, com duas famílias novas:

- `cvm_*` (11 tools): companhias abertas com DFP na CVM, exercícios de 2010 em diante,
  visões consolidado e individual, conta a conta de BPA, BPP, DRE, DRA, DFC, DMPL e DVA,
  parecer do auditor com texto integral, versões e reapresentações, ranking por exercício.
- `bcb_*` (10 tools): instituições financeiras do IF.data, série trimestral desde 2000,
  níveis individual, financeiro e prudencial, conglomerados, DRE derivada, relatórios conta
  a conta, ranking por data-base.

Quatro das limitações declaradas no README deixam de valer para companhias abertas e
bancos: ausência de consolidado, ausência de DFC/EBITDA/dívida líquida/cobertura de juros,
parecer fora do corte de 50 mil caracteres e ausência de dado intra-ano. As skills hoje
mandam o agente buscar no texto o que agora vem estruturado, e aplicam a bancos indicadores
que não fazem sentido (liquidez corrente, margem bruta). O checker reprova qualquer tool
fora das 8 originais, então nem dá para citar `cvm_*` numa skill.

Caminho escolhido (entre enxerto mínimo, duas skills por fonte e reestruturar por fonte):
**a base vira mapa e roteador, entram duas skills novas por fonte, as seis existentes ganham
desvios curtos**. As skills continuam organizadas por tarefa, que é como o usuário pergunta.

## Fatos verificados contra o MCP em 2026-09-17

Chamadas feitas durante o desenho, que as skills devem refletir:

- `ficha_empresa` (publicações) **não** indica se a empresa está na CVM ou no IF.data. O
  roteamento é regra da skill. As três famílias aceitam CNPJ como chave; `cvm_*` aceita
  também código CVM; `bcb_*` aceita CodInst e raiz de CNPJ (8 dígitos).
- `cvm_buscar_companhias` e `bcb_buscar_instituicoes` devolvem o objeto `empresa` com
  `slug` e `link` do balancos.ai quando a empresa está lá. A ponte de volta existe.
- `bcb_buscar_instituicoes("Banrisul")` devolve 20 fundos de investimento e não o banco.
  Com `tipo="8"` devolve zero, porque o nome oficial é "BANCO DO ESTADO DO RIO GRANDE DO
  SUL S.A.". Pela raiz `92702067` acha na hora.
- Gerdau S.A. (cd_cvm 3980): consolidado 2025 com receita líquida de R$ 69,9 bi e ativo de
  R$ 81,7 bi; individual com receita de R$ 4,8 bi e lucro operacional acima do bruto. A
  regra "trate como holding" da base é substituída por "use a visão consolidada" quando a
  companhia está na CVM.
- Gerdau 2024 tem v1 (2025-02-19, `parecer: null`) e v2 (2025-02-24, reapresentação,
  "Sem Ressalva"). Reapresentação pode ser só a inclusão do parecer, não correção de número.
- `cvm_ranking_companhias(receita, 2025)` lista JBS S.A. e JBS N.V. com a mesma receita
  (R$ 480,6 bi). Grupos duplicam.
- `cvm_demonstracoes_dfp` traz `padronizada: true|false` por conta. Depreciação na DFC é
  conta não padronizada (na Gerdau, 6.01.01.02); na DVA é padronizada (7.04.01).
- Banrisul no IF.data: níveis individual (92702067), financeiro (30173) e prudencial
  (1000080154, padrão). Última data-base 202606. Era `cosif_2000` até 202412 e
  `cosif_2025` a partir de 202503. `tvm` nulo antes de 2025; índices nulos até 2014;
  `rede` nula na série. `link_documento` só em trimestres de dezembro.
- `bcb_ranking_instituicoes(ativo)` no nível padrão devolve linhas prudenciais com `cnpj`
  e `empresa` nulos ("ITAU - PRUDENCIAL"). O link de empresa vem por `bcb_conglomerado`.
- `bcb_relatorios_instituicao` devolve `comparavel: true|false` e `valor_ano_anterior`;
  linhas com `formato` em `mil` (reais), `pct` (fração) ou `inteiro`.
- `bcb_estrutura_relatorios("202606")`: 22 relatórios na era COSIF 2025. Resumo 121
  (prudencial), 119 (financeiro), 120 (individual); Ativo 105/107/106; Passivo 108/110/109;
  DRE 116/118/117; Informações de Capital 115; carteira de crédito 123 a 130 (PF por
  modalidade e prazo, PJ por modalidade e prazo, PJ por CNAE, PJ por porte, quantidade de
  clientes e operações, por instrumento, por indexador, por região); Segmentação 131.

## Seção 1. Skill `balancos-ai`: mapa e roteador

### Estrutura nova do SKILL.md

1. **Três fontes** (nova, no topo, depois de "O que a base é"): uma tabela com fonte,
   quem está, período, o que traz, o que não traz, tool de entrada.

   | Fonte | Quem | Traz | Comece por |
   |---|---|---|---|
   | Publicações (`buscar_empresas`...) | qualquer empresa com publicação legal | BP 8 linhas, DRE 6 linhas, individual, um exercício por ano, texto das publicações | `buscar_empresas` |
   | CVM (`cvm_*`) | companhias abertas com DFP, 2010+ | consolidado e individual, conta a conta (BPA, BPP, DRE, DRA, DFC, DMPL, DVA), parecer, versões, ranking por exercício | `cvm_analisar_companhia` |
   | BCB (`bcb_*`) | instituições do IF.data, 2000+ | série trimestral, níveis de consolidação, carteira, captações, Basileia, DRE derivada, relatórios | `bcb_analisar_instituicao` |

2. **Roteamento** (nova): regra em quatro passos, por CNPJ.
   1. `buscar_empresas` sempre primeiro: maior cobertura, devolve CNPJ e slug.
   2. Ficha com `natureza_juridica` "Sociedade Anônima Aberta" (ou nome com "S.A." e
      publicações do tipo DFP no índice): `cvm_buscar_companhias(cnpj)`. Achou, números
      vêm da CVM; siga a skill companhia-aberta.
   3. CNAE de instituição financeira (64.21 a 64.24 bancos, caixas e cooperativas de
      crédito, 64.3x bancos de investimento, fomento e financeiras, 64.40 arrendamento
      mercantil, 66.12 corretoras; holdings 64.6x não são) ou `familia: "financeira"` na
      CVM:
      `bcb_buscar_instituicoes(raiz do CNPJ)`. Achou, números de banco vêm do BCB; siga a
      skill instituicao-financeira.
   4. Publicações continuam para texto de notas e para quem não está nas outras duas.

   Precedência quando a empresa está em mais de uma fonte (Banrisul está nas três):
   carteira, captações, Basileia e trimestre no BCB; parecer, DFC, DVA e conta a conta na
   CVM; notas explicativas e relatório da administração no texto da publicação. A resposta
   diz a fonte de cada número.

3. **Fluxo padrão** e **As oito tools**: mantidos, com o título da tabela mudando para
   "As oito tools de publicações". Abaixo, tabela curta "As 21 tools de CVM e BCB" com nome
   e uma linha por tool, apontando para as skills de cada fonte para os detalhes.
4. **Como ler o dado**: mantido para publicações. Item `consolidado` ganha a frase "se a
   companhia está na CVM, o consolidado existe lá; use-o em vez de explicar a holding".
   Item "Controladora com CNAE industrial (Gerdau S.A.)" ganha a mesma remissão.
5. **O que a base não tem**: reescrito em duas listas.
   - Ausente só na fonte publicações (existe na CVM ou no BCB): consolidado, DFC, caixa,
     empréstimos, depreciação, resultado financeiro, EBITDA, dívida líquida, cobertura de
     juros, parecer estruturado, reapresentações, dado trimestral (só bancos), carteira e
     Basileia (só bancos).
   - Ausente em todas: ITR trimestral de companhia aberta, valor de mercado, quadro
     societário e controlador, notas explicativas estruturadas, protestos, rating,
     paginação, filtro por faixa de receita, contagem de empresas por setor.
6. **Erros comuns**: três linhas novas. "Explicar Gerdau como holding quando ela está na
   CVM" → usar o consolidado. "Aplicar liquidez corrente a banco" → skill
   instituicao-financeira. "Buscar banco pelo nome fantasia no BCB" → raiz do CNPJ.

`references/payloads.md` fica com os payloads de publicações. Os das outras famílias vão
nas skills novas.

Tamanho: o SKILL.md hoje tem 170 linhas; a meta é ficar abaixo de 260.

## Seção 2. Skill `companhia-aberta`

### Frontmatter

- `name: companhia-aberta`
- `description`: "Use quando a empresa for companhia aberta (S.A. com DFP na CVM) e o
  pedido envolver consolidado, conta a conta, DFC, DVA, EBITDA, dívida líquida, cobertura
  de juros, parecer do auditor, reapresentação ou ranking de companhias abertas, com o MCP
  do Balanços.AI conectado. Assume a skill balancos-ai."
- `compatibility`: requer o MCP; assume balancos-ai e indicadores-financeiros.

### Conteúdo

1. **Resultado**: o mesmo tipo de entrega da skill que chamou (memo, tabela, relatório),
   com visão e versão declaradas em cada número.
2. **Fluxo**:
   1. `cvm_buscar_companhias(termo ou CNPJ)`: até 20, com `cd_cvm`, `cnpj`, `denominacao`
      e `empresa` (slug e link do balancos.ai).
   2. `cvm_analisar_companhia(chave)`: ficha (denominações anteriores, `familia`,
      primeiro e último exercício, entregas e reapresentações, último parecer, capital
      social com ações em tesouraria), `exercicios[]` com `versoes[]` (id_doc, versão,
      reapresentação, data, parecer, links), `balancos[]` e `dres[]` por exercício e
      `visao`, última versão de cada exercício. Uma chamada; só use `cvm_ficha_companhia`,
      `cvm_dfps_companhia`, `cvm_balancos_companhia` e `cvm_dres_companhia` para uma
      parte.
   3. `cvm_entrega_dfp(id_doc)` quando precisar saber quais visões e demonstrações a
      entrega tem antes de pedir o conta a conta.
   4. `cvm_demonstracoes_dfp(id_doc, demonstracao, visao)`: uma demonstração por chamada;
      sem `demonstracao` a resposta é grande. Padrão da tool: consolidado, ou individual
      quando não há consolidado.
   5. `cvm_parecer_dfp(id_doc)`: tipo, texto integral, declarações dos diretores e parecer
      do conselho fiscal.
   6. `cvm_ranking_companhias(metrica, ano, visao, familia, limite)`: ano obrigatório.
3. **Visão**: consolidado é o padrão para tamanho, operação e comparação. Individual só
   quando a pergunta é sobre a entidade (dividendos, capital, obrigação própria) ou quando
   não há consolidado (lista `visoes` em `cvm_entrega_dfp`). A visão vai no cabeçalho de
   toda tabela. A regra de holding da base não se aplica quando há consolidado.
4. **Família**: `comercial` usa o plano de contas padrão e o mapa de códigos desta skill.
   `financeira` e `seguradora` têm plano próprio: o mapa não vale, comparar só dentro da
   família, e banco vai para a skill instituicao-financeira.
5. **Versões e reapresentações**: a última versão de um exercício é a que vale, e
   `cvm_analisar_companhia` já a escolhe. Reapresentação é sinal para due diligence, mas
   pode ser só a inclusão do parecer (Gerdau 2024: v1 sem parecer, v2 "Sem Ressalva").
   Para dizer o que mudou, comparar `valor_atual` das duas versões pelo conta a conta.
6. **Comparativo**: `valor_anterior` é o comparativo republicado na mesma DFP e pode
   divergir do `valor_atual` da entrega anterior. Série usa a última versão de cada
   exercício e declara divergências acima de 1%.
7. **Parecer**: `tipo` é estruturado ("Sem Ressalva", "Com Ressalva", "Adverso",
   "Negativa de Opinião"). Ênfase, incerteza de continuidade e outros assuntos só lendo o
   texto: procurar "ênfase", "continuidade operacional", "incerteza relevante". Principais
   assuntos de auditoria não são ressalva. Citar auditor e data, que vêm no fim do texto.
8. **Ranking**: ano obrigatório; `visao` e `familia` explícitas; grupos duplicam (JBS S.A. e
   JBS N.V.): dedupe pelo `slug` ou pelo nome e diga. Não há filtro por UF nem setor: para
   setor, cruzar com `ficha_empresa` (CNAE) das publicações.
9. **Indicadores computáveis com o conta a conta** (proveniência 1, com o código da conta na
   apresentação):

   | Indicador | Fórmula | Ressalva obrigatória |
   |---|---|---|
   | EBITDA | 3.05 + \|7.04.01\| (DVA) | depreciação da DVA, que inclui exaustão |
   | Dívida bruta | 2.01.04 + 2.02.01 | dizer se arrendamento (2.01.04.03, 2.02.01.03) entrou |
   | Dívida líquida | dívida bruta − 1.01.01 − 1.01.02 | aplicações de longo prazo (1.02.01.01 a .03) fora, por padrão |
   | Cobertura de juros | 3.05 / \|3.06.02\| | 3.06.02 inclui variação cambial e perdas com derivativos |
   | Caixa operacional | 6.01 | método na resposta (`metodo`) |
   | Caixa operacional sobre dívida | 6.01 / dívida bruta | |
   | Juros pagos | linha "juros" em 6.01.03 ou 6.03 | não padronizada; citar a descrição |
   | Lucro dos controladores | 3.11.01 | para ROE, com PL sem não controladores (2.03 − 2.03.09) |
   | Equivalência no resultado | 3.04.06 | sinaliza dependência de coligadas |
   | Não recorrentes | 3.04.03 (impairment), 3.10 (descontinuadas) | |
   | Contas a receber, estoques, fornecedores | 1.01.03, 1.01.04, 2.01.02 | prazos médios possíveis |
   | Capex | adições de imobilizado e intangível em 6.02 | não padronizada; citar a descrição |

   Contas `padronizada: false` variam por companhia: citar a descrição e o código.
10. **O que a CVM não tem**: ITR trimestral, notas explicativas em campo estruturado
    (continuam no `texto_documento` da publicação), valor de mercado, companhias fechadas,
    exercícios antes de 2010.
11. **Ao apresentar**: visão, versão e `id_doc` da entrega; link do documento no
    balancos.ai (`link_documento`) e na CVM (`link_cvm`); código da conta ao lado de cada
    indicador derivado; `dados_atualizados_em` da família CVM (difere do das publicações).

### Referências

- `references/payloads.md`: campos de cada tool `cvm_*`, no formato do arquivo da base.
- `references/contas-dfp.md`: mapa dos códigos padronizados usados nas fórmulas (BPA 1.x,
  BPP 2.x, DRE 3.x, DFC 6.x, DVA 7.x), com descrição, nível e observação de onde varia.

## Seção 3. Skill `instituicao-financeira`

### Frontmatter

- `name: instituicao-financeira`
- `description`: "Use quando a empresa for banco, cooperativa de crédito, financeira,
  corretora ou outra instituição do IF.data do Banco Central, e o pedido envolver carteira
  de crédito, captações, Basileia, conglomerado, série trimestral ou ranking de
  instituições, com o MCP do Balanços.AI conectado. Assume a skill balancos-ai."
- `compatibility`: requer o MCP; assume balancos-ai.

### Conteúdo

1. **Resultado**: o mesmo tipo de entrega da skill que chamou, com nível de consolidação,
   data-base e era contábil em cada número.
2. **Fluxo**:
   1. `bcb_buscar_instituicoes(termo, uf, tipo, consolidado_bancario)`: raiz do CNPJ
      primeiro. Nome só com `tipo` (8 banco múltiplo, 9 cooperativa de crédito) e sabendo
      que fundos poluem e nome fantasia não casa com o oficial. Se o usuário deu o nome
      fantasia, obter o CNPJ por `buscar_empresas` das publicações ou pelo MCP do cnpj.ai.
   2. `bcb_analisar_instituicao(chave)`: ficha (tipo, consolidado bancário, segmento
      prudencial, sede, conglomerados, níveis com CodInst e qual é o padrão, resumo da
      última data-base), série trimestral do nível padrão e DRE anual derivada. Uma
      chamada.
   3. `bcb_trimestres_instituicao(chave, nivel, desde, ate)` para outro nível ou janela.
   4. `bcb_resultados_instituicao(chave, nivel, periodo)` para trimestre isolado.
   5. `bcb_estrutura_relatorios(data_base)` e depois `bcb_relatorios_instituicao(chave,
      nivel, data_base, relatorio)`: um relatório por chamada.
   6. `bcb_conglomerado(codinst, nivel)` para os membros e os links de empresa.
   7. `bcb_ranking_instituicoes(metrica, data_base, nivel, uf, tipo,
      consolidado_bancario, limite)`.
   8. `bcb_data_bases()` para saber a última data-base e a era.
3. **Níveis**: individual, financeiro, prudencial. Banco grande reporta pelo prudencial,
   que é o `nivel_padrao`; cooperativa singular e instituição independente reportam pelo
   individual. Comparar instituições no nível padrão de cada uma (`nivel="padrao"` no
   ranking). Linhas prudenciais do ranking vêm com `cnpj` e `empresa` nulos: para o link,
   `bcb_conglomerado(codinst)` lista os membros com CNPJ e link.
4. **Tempo**: data-base AAAAMM em 03, 06, 09 e 12. O IF.data publica lucro acumulado no
   semestre (`lucro_liquido_acumulado_semestre`): T1 = mar, T2 = jun − mar, T3 = set,
   T4 = dez − set, anual = jun + dez. A DRE derivada já desmonta e marca `completo`.
   Era contábil `cosif_2000` até 202412 e `cosif_2025` de 202503 em diante: ano contra ano
   só dentro da mesma era; `comparavel` na resposta de relatórios diz se dá. Campos nulos
   em trimestres antigos (`tvm` antes de 2025, índices antes de 2015, `rede`) ficam em
   branco, não zero.
5. **Índices**: vêm em fração (0,159 é 15,9%). `unidade` no ranking diz se `valor` é
   reais ou fração. Basileia se compara com o mínimo regulatório vigente, que é
   conhecimento geral e vai rotulado; imobilização e alavancagem idem.
6. **Indicadores próprios** (sem liquidez corrente, margem bruta, giro):

   | Indicador | Fórmula | Leitura |
   |---|---|---|
   | ROE | lucro anual (DRE derivada, `completo`) / PL de dezembro | |
   | Carteira sobre ativo | carteira_credito / ativo_total | perfil de crédito |
   | Captações sobre ativo | captacoes / ativo_total | funding |
   | Crescimento de carteira | carteira(t) / carteira(t − 4 trimestres) − 1 | mesma era |
   | Basileia, imobilização, alavancagem | `indices` | fração; mínimo regulatório rotulado |
   | Lucro semestral | `lucro_liquido_acumulado_semestre` em jun e dez | sazonal |
   | Rede | agências e postos | quando existir |

   A DRE derivada tem `receita_liquida` (receitas de intermediação e serviços), `custo`
   (despesas de intermediação) e `lucro_bruto` (resultado de intermediação): explicar antes
   de qualquer margem, e chamar de "margem de intermediação".
7. **Relatórios**: ids por era; reconferir com `bcb_estrutura_relatorios(data_base)` antes
   de pedir. Na era COSIF 2025: Resumo 121/119/120, Ativo 105/107/106, Passivo
   108/110/109, DRE 116/118/117 (prudencial/financeiro/individual), Capital 115, carteira
   123 a 130, Segmentação 131. Carteira por CNAE (129), por porte (127) e por região (126)
   respondem "para quem o banco empresta".
8. **Cooperativas e sistemas**: cooperativa singular é `b3S`, tipo 9, nível individual.
   Sistemas (Sicredi, Sicoob) são muitos CNPJs; a central e o banco do sistema aparecem
   como conglomerado. Dizer qual entidade foi analisada.
9. **O que o BCB não tem**: parecer do auditor (CVM ou texto da publicação), notas
   explicativas, DFC, valor de mercado, instituições fora do IF.data (instituições de
   pagamento entram só de 2020 em diante).
10. **Ao apresentar**: nível, data-base, era; `link_documento` quando houver (dezembro) ou
    `link_ifdata`; link da empresa no balancos.ai; `dados_atualizados_em` da família.

### Referências

- `references/payloads.md`: campos de cada tool `bcb_*`.
- `references/relatorios-ifdata.md`: os 22 relatórios da era COSIF 2025 (id, nome, grupo,
  níveis), códigos de tipo de instituição (TI) e de consolidado bancário (TCB) que
  apareceram nos testes (8 banco múltiplo, 9 cooperativa de crédito, 15 corretora de TVM,
  41 instituição de pagamento; b1, b3S, n1, n2, n4), e a instrução de reconferir por
  data-base.

## Seção 4. Desvios nas seis skills existentes

Cada skill ganha um bloco curto "Quando a empresa está na CVM ou no BCB", sem reescrever o
resto. Os desvios:

- **indicadores-financeiros**: a tabela "Incomputável com o dado estruturado" ganha a coluna
  "Na CVM" com o código da conta e a remissão à skill companhia-aberta; um parágrafo diz que
  em instituição financeira a tabela de fórmulas não se aplica e remete à skill
  instituicao-financeira. A seção "Campos disponíveis" diz que `cvm_balancos_companhia` e
  `cvm_dres_companhia` têm os mesmos nomes de campo com `visao` a mais, e que
  `bcb_resultados_instituicao` usa os mesmos nomes com semântica de intermediação.
- **investigar-empresa**: passo 2 vira "roteie pela skill balancos-ai"; a seção 2 do memo
  ("Natureza do dado") ganha fonte, família, visão ou nível; em companhia aberta a seção 5
  acrescenta EBITDA, dívida líquida, caixa operacional e o tipo do parecer, e a seção 4
  usa o consolidado; em banco, o memo troca as seções 3 a 5 por tamanho (ativo, carteira,
  captações, PL, Basileia na última data-base), trajetória trimestral (8 trimestres) e
  rentabilidade (ROE anual, lucro semestral, crescimento de carteira). O modelo em
  `references/modelo-memo.md` ganha as duas variantes.
- **comparar-empresas**: regra "mesma fonte, mesma família e mesma visão na tabela"; a
  linha "Natureza do dado" passa a trazer isso; companhia aberta ganha as linhas dívida
  líquida e EBITDA; banco só compara com banco, com as linhas da skill
  instituicao-financeira; pares de companhia aberta pelo `cvm_ranking_companhias` (por
  família e visão, e a skill diz que não há UF nem setor) e pares de banco pelo
  `bcb_ranking_instituicoes` (por UF, tipo e consolidado bancário).
- **due-diligence-financeira**: seção 5 começa por `cvm_parecer_dfp` quando a contraparte é
  companhia aberta (tipo, ênfase, continuidade, auditor, data), antes do texto da
  publicação; reapresentações da linha do tempo de entregas entram na seção 4; dívida
  bruta, caixa, juros pagos e caixa operacional entram na tabela da seção 3; em banco, a
  seção 3 usa os indicadores da skill instituicao-financeira e o trimestre mais recente
  substitui o pedido de balancete na seção 7. O `references/roteiro-notas.md` ganha uma
  linha por item dizendo se ele vem estruturado na CVM.
- **originacao-ma**: para alvos entre companhias abertas, `cvm_ranking_companhias` por
  família e visão, cruzando CNAE e UF pela `ficha_empresa`; para instituições financeiras,
  `bcb_ranking_instituicoes` por UF, tipo e consolidado bancário, que é o único ranking
  com filtro geográfico real além do de publicações; compradores bancários ordenados por
  PL e Basileia. Orçamento de chamadas mantido.
- **ler-publicacao**: "tem ressalva do auditor" em companhia aberta vai direto em
  `cvm_parecer_dfp`; DFP com "texto ainda não extraído" tem o conta a conta em
  `cvm_demonstracoes_dfp`; notas explicativas continuam no `texto_documento`.

Cada descrição de skill que menciona "MCP do Balanços.AI conectado" fica como está.

## Seção 5. Infraestrutura, docs e testes

- `scripts/check.py`: `TOOLS_DO_MCP` com as 29 tools; `RE_TOOL` ganha os prefixos `cvm_` e
  `bcb_` (regex por prefixo `(?:cvm|bcb)_[a-z_]+` além dos radicais atuais).
- `README.md`: tabela com nove skills; nova seção "Três fontes" antes de "Instalar";
  "Limitações conhecidas" reescrita por fonte; "O que as skills não fazem" ajustada (EBITDA,
  dívida líquida e DFC existem para companhia aberta).
- `.claude-plugin/plugin.json`: descrição cita companhias abertas e instituições
  financeiras; keywords ganham `cvm`, `bcb`, `bancos`, `dfp`, `ifdata`.
- `evals/`: `companhia-aberta.md` (cenários: consolidado vs individual da Gerdau, EBITDA e
  dívida líquida com código, parecer com ênfase, reapresentação, ranking com grupo
  duplicado) e `instituicao-financeira.md` (cenários: achar o Banrisul, nível prudencial vs
  individual, lucro semestral vs anual, quebra de era, ranking de cooperativas por UF,
  para quem o banco empresta). Nas existentes, três cenários novos cada onde couber:
  empresa nas três fontes, companhia aberta, banco.
- `metadata.version` sobe para "0.2" em todas as skills.
- Commits: um por task, em português, na ordem: checker e base; companhia-aberta;
  instituicao-financeira; um por skill existente; README, plugin e evals. Branch
  `feat/tres-fontes`, merge commit normal.

## Fora de escopo

- Reescrever as skills existentes por fonte.
- Tools que o MCP não tem (ITR, valor de mercado, quadro societário).
- Automatizar os evals; continuam manuais contra produção.
