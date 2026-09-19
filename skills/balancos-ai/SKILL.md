---
name: balancos-ai
description: Use quando o MCP do Balanços.AI estiver conectado e o pedido envolver empresa brasileira, balanço patrimonial, DRE, CNPJ, publicação legal, ranking por setor ou UF, ou qualquer número financeiro de empresa. Base das demais skills do Balanços.AI; leia antes de chamar qualquer tool.
license: MIT
compatibility: Requer o MCP do Balanços.AI (https://mcp.balancos.ai/mcp) conectado no cliente.
metadata:
  author: Balanços.AI
  version: "0.4"
---

# Balanços.AI pelo MCP

## O que a base é

Demonstrações financeiras (balanço patrimonial e DRE) de empresas brasileiras, extraídas
de publicações legais: DFP na CVM (XBRL), demonstrações publicadas em jornal (PDF lido por
LLM) e outras fontes públicas. A base está em beta e cresce a cada carga: nem toda empresa
está lá, nem todo ano de uma empresa, e a cobertura por setor é parcial.

Três fatos que mudam toda leitura da fonte publicações (as outras duas fontes, abaixo,
não têm essas limitações):

- **Um exercício por ano, sempre o individual.** Para cada ano fiscal a base escolhe um
  período vencedor. Não há versão consolidada nesta fonte. Holding e controladora mostram
  a receita e a dívida da própria entidade, não do grupo. Se a companhia é aberta, o
  consolidado está na fonte CVM.
- **Valores sempre em reais**, já multiplicados pela escala do documento.
  `escala_publicada` é só proveniência. Nunca escreva "em milhares" ao apresentar.
- **BP tem 8 linhas e DRE tem 6.** Não há caixa, empréstimos, estoques, depreciação,
  resultado financeiro nem fluxo de caixa em campo estruturado nesta fonte. Na CVM o
  conta a conta existe; no BCB existe carteira, captações e Basileia.

## Três fontes e roteamento

O MCP reúne três fontes com famílias de tools próprias. Todas aceitam CNPJ como chave.

| Fonte | Quem está | O que traz | Comece por |
|---|---|---|---|
| Publicações (`buscar_empresas`, `analisar_empresa`...) | qualquer empresa com publicação legal | BP de 8 linhas, DRE de 6, individual, um exercício por ano, texto das publicações, ranking por UF e setor | `buscar_empresas` |
| CVM (`cvm_*`) | companhias abertas: DFP de 2010 em diante, ITR de 2011 em diante | consolidado e individual, conta a conta (BPA, BPP, DRE, DRA, DFC, DMPL, DVA) da DFP e do ITR, série trimestral com trimestre, acumulado e últimos doze meses, parecer do auditor, versões e reapresentações, ranking por exercício ou por doze meses e família | `cvm_analisar_companhia` |
| BCB (`bcb_*`) | instituições financeiras do IF.data, desde 2000 | série trimestral, níveis individual, financeiro e prudencial, carteira de crédito, captações, Basileia, DRE derivada, relatórios conta a conta, conglomerados, ranking por data-base, UF e tipo | `bcb_analisar_instituicao` |

Roteamento, sempre nesta ordem:

1. `buscar_empresas` primeiro. É a maior cobertura e devolve CNPJ e slug.
2. Ficha com `natureza_juridica` "Sociedade Anônima Aberta", ou índice com publicações do
   tipo "Demonstrações Financeiras Padronizadas" ou "Informações Trimestrais":
   `cvm_buscar_companhias` com o CNPJ.
   Achou, os números vêm da CVM; siga a skill companhia-aberta.
3. CNAE de instituição financeira (64.21 a 64.24 bancos, caixas e cooperativas de
   crédito; 64.3x bancos de investimento, fomento e financeiras; 64.40 arrendamento;
   66.12 corretoras; holdings 64.6x **não** são) ou `familia: "financeira"` na CVM:
   `bcb_buscar_instituicoes` com a raiz do CNPJ (8 dígitos). Achou, os números de banco
   vêm do BCB; siga a skill instituicao-financeira.
4. Publicações continuam valendo para texto de notas e relatório da administração, e para
   quem não está nas outras duas.

A ficha de publicações **não** diz se a empresa está na CVM ou no BCB; a regra acima é o
único caminho. Uma empresa pode estar nas três (um banco listado). Precedência por
pergunta: carteira, captações, Basileia e trimestre de banco no BCB; trimestre e últimos
doze meses de companhia aberta, parecer, DFC, DVA e conta a conta na CVM; notas
explicativas e relatório da administração no texto da publicação. A resposta diz a fonte
de cada número. Cada fonte tem o próprio `dados_atualizados_em`.

## Fluxo padrão

1. `buscar_empresas` com um termo curto e distintivo (sigla, nome fantasia, "Gerdau").
   Razão social completa com acento costuma devolver zero. Sem resultado, tente o CNPJ.
2. Confira homônimos na lista (CEEE-G, CEEE-D, CEEE-Par são empresas diferentes) e escolha
   pelo CNPJ ou pela descrição da ficha.
3. `analisar_empresa` com o slug ou CNPJ. Traz ficha, todos os BPs e DREs, crescimento de
   ativo e o índice de publicações numa chamada. Só use `ficha_empresa`,
   `balancos_empresa` e `dres_empresa` quando quiser uma parte só.
4. Para conteúdo de uma publicação, `documentos_empresa` (ou o índice que veio no
   `analisar_empresa`) e depois `texto_documento` com o id.
5. Para "maiores de", "quem mais cresce", pares de setor: `ranking_empresas`.

## As oito tools de publicações

| Tool | Quando | Teto |
|---|---|---|
| `buscar_empresas(termo)` | achar slug e CNPJ pelo nome ou CNPJ | 20 empresas |
| `ficha_empresa(chave)` | cadastro, setor, anos com BP e DRE, contagem de publicações | |
| `analisar_empresa(chave)` | retrato completo; comece por aqui | 100 documentos no índice |
| `balancos_empresa(chave, ano?)` | só os BPs (todos ou um ano) | |
| `dres_empresa(chave, ano?)` | só as DREs (todas ou um ano) | |
| `documentos_empresa(chave)` | índice de publicações, mais recentes primeiro | 100 |
| `texto_documento(documento_id, inicio?, tamanho?, termo?)` | texto de uma publicação, em pedaços ou por termo | 200 mil caracteres por pedaço; 20 trechos por termo |
| `ranking_empresas(metrica, uf?, setor?, limite?)` | maiores por ativo, receita, lucro ou crescimento | 50 por chamada |

`chave` aceita slug ou CNPJ (com ou sem pontuação). Campos de cada resposta em
[references/payloads.md](references/payloads.md).

## As 22 tools de CVM e BCB

Detalhes, campos e regras nas skills companhia-aberta e instituicao-financeira.

| Tool | Quando |
|---|---|
| `cvm_buscar_companhias(termo)` | achar CNPJ, código CVM e slug de companhia aberta |
| `cvm_ficha_companhia(chave)` | denominações, família, exercícios, entregas, último parecer, capital |
| `cvm_analisar_companhia(chave)` | retrato: ficha, linha do tempo das DFPs, BPs e DREs anuais consolidado e individual, ponto trimestral mais recente |
| `cvm_trimestres_companhia(chave, desde?, ate?, visao?)` | série trimestral: BP, trimestre, acumulado e últimos doze meses |
| `cvm_resultados_companhia(chave, periodo?, desde?, ate?, visao?)` | DRE da série num período (trimestre, acumulado, 12m, anual) |
| `cvm_entregas_companhia(chave, tipo?, ano?)` | entregas de DFP ou ITR por data e versão, com `id_doc` |
| `cvm_entrega(id_doc)` | visões e demonstrações que a entrega (DFP ou ITR) tem |
| `cvm_balancos_companhia(chave, ano?, visao?)` | só os BPs anuais |
| `cvm_dres_companhia(chave, ano?, visao?)` | só as DREs anuais |
| `cvm_demonstracoes(id_doc, demonstracao?, visao?)` | conta a conta de uma demonstração da DFP ou do ITR |
| `cvm_parecer(id_doc)` | parecer (DFP) ou revisão (ITR) do auditor, declarações dos diretores |
| `cvm_ranking_companhias(metrica, ano?, periodo?, data_referencia?, visao?, familia?, limite?)` | maiores companhias abertas num exercício ou nos últimos doze meses |
| `bcb_buscar_instituicoes(termo?, uf?, tipo?, consolidado_bancario?)` | achar CodInst e CNPJ de instituição |
| `bcb_ficha_instituicao(chave)` | cadastro, níveis, resumo da última data-base |
| `bcb_analisar_instituicao(chave)` | retrato: ficha, série trimestral, DRE anual derivada |
| `bcb_trimestres_instituicao(chave, nivel?, desde?, ate?)` | série trimestral por nível e janela |
| `bcb_resultados_instituicao(chave, nivel?, periodo?)` | DRE derivada por trimestre e ano |
| `bcb_relatorios_instituicao(chave, nivel?, data_base?, relatorio?)` | conta a conta de um relatório |
| `bcb_estrutura_relatorios(data_base, relatorio?)` | dicionário dos relatórios de uma data-base |
| `bcb_conglomerado(codinst, nivel?)` | membros de um conglomerado, com links |
| `bcb_ranking_instituicoes(metrica, data_base?, nivel?, uf?, tipo?, consolidado_bancario?, limite?)` | maiores instituições numa data-base |
| `bcb_data_bases()` | data-bases disponíveis e era contábil |

## Como ler o dado

- **`consolidado`**: quase sempre `false`. Se a ficha mostra CNAE de holding
  (`64.62-0`, `64.63-8`, "participações") ou a receita é irrisória diante do ativo, o
  número é da entidade individual e o lucro vem de equivalência patrimonial. Diga isso em
  vez de concluir "receita despencou" ou "margem de 90%". Se a companhia é aberta, o
  consolidado está na CVM: use-o (skill companhia-aberta) em vez de explicar a holding.
- **`fonte`**: `xbrl` (DFP na CVM, estruturado) ou `llm` (lido do PDF). Em conflito no
  mesmo ano, xbrl vence. Quando comparar empresas ou anos com fontes diferentes, mostre
  a fonte.
- **`contexto`**: `ultimo` é o período corrente da entrega; `penultimo` é o comparativo
  republicado na entrega seguinte. Por isso o link de origem do exercício 2024 pode
  apontar para a DFP de 2025. Isso é normal.
- **`lucro_operacional`**: no xbrl é "resultado antes do resultado financeiro e dos
  tributos" (EBIT). No llm é a linha que o PDF chamou de resultado operacional, que pode
  incluir o financeiro. Não some nem subtraia financeiro a partir dele.
- **Campo `null`**: o documento não trazia a linha ou a extração não a pegou. Só derive
  por identidade contábil (`passivo_total` = circulante + não circulante; `lucro_bruto` =
  receita líquida − custo) e diga que derivou. Nada além disso.
- **Anomalias**: ativo total de R$ 1.000, receita zero ou negativa, custo positivo,
  exercício com escala trocada (receita de R$ 15 milhões e prejuízo de R$ 600 milhões no
  mesmo ano, ou `escala_publicada: "unidade"` com valores mil vezes menores que o BP).
  Exclua o exercício da série, diga que excluiu e por quê, e aponte o link do documento.
  Se a anomalia atinge a série inteira da empresa, diga isso. Nunca corrija o valor por
  conta própria, nem multiplicando por mil. Os valores literais do texto da publicação
  podem substituir os excluídos, rotulados "da publicação, não da base".
- **`consolidado: null`** (fonte llm): não informado; trate como individual salvo o
  texto dizer o contrário.
- **Controladora com CNAE industrial** (Gerdau S.A.): receita abaixo de uns 10% do
  ativo **e** lucro operacional acima do bruto em todos os anos. Trate como holding nas
  margens, mesmo sem CNAE de holding. Lucro operacional acima do bruto num ano só, em
  empresa operacional, não é holding: é outras receitas ou equivalência naquele ano;
  sinalize, sem interpretar. Gerdau S.A. é companhia aberta: na CVM o consolidado de
  2025 tem receita de R$ 69,9 bi, e é ele que responde "que tamanho tem".
- **Reapresentação**: dois documentos do mesmo tipo e ano (`v2`) são versões. A base já
  escolheu; você não precisa.
- **`exercicio` igual ao ano corrente** com `data_referencia` em junho ou setembro é ano
  fiscal não-calendário, não erro. Compare pela `data_referencia` e diga a data.
- **`porte`**: classificação cadastral ("Demais", "ME"), não tamanho econômico.
- **Setor**: nome da seção CNAE ("Eletricidade e Gás", "Indústrias de Transformação",
  "Atividades Financeiras"), com rótulos herdados em algumas empresas ("Energia
  Elétrica", "Energia"); tabela em [references/setores.md](references/setores.md).
  Holdings caem em "Atividades Financeiras". O filtro do ranking é por trecho do nome:
  "energia" pega só os rótulos herdados, "Eletricidade" pega a seção. O rótulo pode estar
  semanticamente errado numa empresa (gás em "Energia Elétrica").
- **Crescimento**: sempre de ativo total, entre dois anos consecutivos. Não é receita.
  Percentuais de milhares por cento vêm de bases pequenas; olhe `ativo_base`.

## Três proveniências

Todo número ou fato da resposta tem uma destas origens, e o leitor precisa saber qual:

1. **Da base**: veio no payload. É o padrão; não precisa rótulo.
2. **Do texto**: citado literalmente de `texto_documento`, com o link. Rotule "segundo a
   publicação" ou "segundo a companhia, no relatório da administração". Vale para
   indicadores que a empresa divulga (EBITDA ajustado, dívida líquida, geração de caixa),
   para linhas da DRE, DFC e DVA publicadas e para controlador citado na nota. Número
   solto de gráfico ou tabela desmontada vai com "~" ou fica fora. Os números do texto
   estão na escala do documento (quase sempre milhares); confira o cabeçalho antes de
   comparar com a base, que está em reais.
3. **De conhecimento geral**: estrutura do grupo, controlador, eventos de mercado,
   localização de usina. Frase separada, rotulada "de conhecimento geral, não confirmado
   na base", ou fica fora. Nunca número de nota, página, valor ou opinião do auditor.

Conta com um valor da base e outro do texto (EBIT sobre despesa financeira, dívida bruta
menos caixa) é permitida se os dois forem citados com link, a escala conferida e o
resultado rotulado "aproximado, com <linha> da publicação de <ano>". Inferir um valor a
partir de uma frase ("caiu 15,7%") não é.

## Texto de publicações

- `texto_documento` entrega o documento inteiro, de dois jeitos. Com `termo`, devolve
  até 20 trechos com 600 caracteres de contexto para cada lado e a posição de cada um,
  sem distinção de caixa nem acento: é o caminho para "tem ressalva", "quanto de dívida
  nas notas", "eventos subsequentes". Sem `termo`, devolve um pedaço de `inicio` até
  `inicio + tamanho` (padrão 100 mil, teto 200 mil) com `tamanho_total_chars`,
  `truncado` e `proximo_inicio`; repita com `inicio=proximo_inicio` até `truncado:
  false`. Uma DF completa tem 300 a 800 mil caracteres, com parecer do auditor e notas
  no fim. Nunca diga que algo não está no documento sem ter buscado por termo ou lido até
  o fim (skill ler-publicacao). Texto de jornal vem com o espaçamento das colunas e
  frases de colunas vizinhas intercaladas linha a linha; leia por frase. A extração
  perde a ligadura "fi": procure "inanceir", "inanciament", "iscal".
- `ano_referencia` em publicação de jornal pode ser o ano da publicação, não do
  exercício ("DFs de 2025" com `ano_referencia: 2026`); confira pelo título e pela data.
- DFPs e ITRs ("Informações Trimestrais") da CVM vêm como "texto ainda não extraído".
  A publicação em jornal do mesmo exercício costuma ter texto. Prefira ela.
- O `tipo` do índice é aproximado: "Demonstração de Resultados" com 10 páginas e centenas
  de milhares de caracteres é a DF completa. Julgue pelo título, páginas e tamanho.
- Se o cliente gravou o resultado da tool em arquivo por ser grande, leia o arquivo
  inteiro antes de responder. Um preview de 2 mil caracteres é só o cabeçalho.
- O documento do ano seguinte traz o ano pedido como comparativo nas notas e serve de
  segunda fonte para um item que a publicação do ano só menciona.

## O que cada fonte não tem

Ausente só na fonte publicações, mas presente na CVM (companhias abertas) ou no BCB
(instituições financeiras): consolidado, DFC, caixa, empréstimos, depreciação, resultado
financeiro, EBITDA, dívida líquida, cobertura de juros, parecer do auditor estruturado,
reapresentações explícitas, dado trimestral e últimos doze meses, carteira de crédito e
Basileia (só bancos). Quando pedirem um desses para uma empresa que não está na CVM nem
no BCB, responda o que existe, diga que não existe nesta fonte, leia o texto da
publicação quando ele tiver o número (proveniência 2) e aponte o link. Não estime.

Ausente em todas as fontes: valor de mercado, quadro societário e controlador, notas
explicativas estruturadas, protestos, rating, paginação, filtro por faixa de receita,
contagem de empresas por setor.

"Quantas empresas do setor X": não há contagem. O mais perto é `ranking_empresas` com
`limite=50` nas quatro métricas; se voltar menos de 50, esse é o total com balanço
carregado, e diga que é só isso. Para bancos, `bcb_ranking_instituicoes` com `uf` e
`tipo` chega mais perto de uma contagem por região.

## Ao apresentar

- Inclua o link da empresa e dos documentos citados (vêm nas respostas).
- Cite `dados_atualizados_em` como "dados do Balanços.AI em <data>".
- Valores em R$ mil, mi ou bi com a unidade escrita; mesmo exercício para tudo que
  estiver na mesma tabela, com o ano no cabeçalho.
- Proveniência visível em cada número e fato (seção acima).
- Ranking é dentro da cobertura da base. "1º do setor" vale com o N de empresas listadas.

## Erros comuns

| Erro | Correção |
|---|---|
| "Receita caiu 99%" numa holding | É o individual; o grupo está no consolidado, que não está na base |
| Multiplicar por mil um exercício com escala estranha | Sinalizar, excluir, apontar o documento |
| Estimar EBITDA a partir de lucro operacional | Dizer que não há depreciação na base |
| Responder com o preview de 2 KB do texto | Ler o arquivo gravado inteiro |
| "Não está no documento" depois de um pedaço do texto | Buscar por `termo` ou ler até `truncado: false` |
| Buscar pela razão social completa | Termo curto; depois CNPJ |
| Usar o ranking de crescimento como "quem cresce" | Filtrar `ativo_base` mínimo e dizer que é ativo total |
| Comparar 2025 de uma com 2023 de outra | Alinhar pelo exercício e declarar buracos |
| Explicar a Gerdau como holding quando ela está na CVM | Usar o consolidado da CVM |
| Tool `cvm_*` desta skill não aparece no cliente, ou aparecem nomes terminados em "_dfp" | O cliente guardou a lista de tools de antes do MCP 0.4: peça para reconectar o MCP |
| Citar a DFP do ano passado como o dado atual de companhia aberta | `trimestral.mais_recente` ou `cvm_trimestres_companhia`, com a data de referência |
| Aplicar liquidez corrente e margem bruta a banco | Skill instituicao-financeira |
| Buscar banco pelo nome fantasia no BCB ("Banrisul") | Raiz do CNPJ; o nome oficial é outro e fundos poluem a busca |
