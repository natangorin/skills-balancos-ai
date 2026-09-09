---
name: balancos-ai
description: Use quando o MCP do Balanços.AI estiver conectado e o pedido envolver empresa brasileira, balanço patrimonial, DRE, CNPJ, publicação legal, ranking por setor ou UF, ou qualquer número financeiro de empresa. Base das demais skills do Balanços.AI; leia antes de chamar qualquer tool.
license: MIT
compatibility: Requer o MCP do Balanços.AI (https://mcp.balancos.ai/mcp) conectado no cliente.
metadata:
  author: Balanços.AI
  version: "0.1"
---

# Balanços.AI pelo MCP

## O que a base é

Demonstrações financeiras (balanço patrimonial e DRE) de empresas brasileiras, extraídas
de publicações legais: DFP na CVM (XBRL), demonstrações publicadas em jornal (PDF lido por
LLM) e outras fontes públicas. A base está em beta e cresce a cada carga: nem toda empresa
está lá, nem todo ano de uma empresa, e a cobertura por setor é parcial.

Três fatos que mudam toda leitura:

- **Um exercício por ano, sempre o individual.** Para cada ano fiscal a base escolhe um
  período vencedor. Não há versão consolidada. Holding e controladora mostram a receita e
  a dívida da própria entidade, não do grupo.
- **Valores sempre em reais**, já multiplicados pela escala do documento.
  `escala_publicada` é só proveniência. Nunca escreva "em milhares" ao apresentar.
- **BP tem 8 linhas e DRE tem 6.** Não há caixa, empréstimos, estoques, depreciação,
  resultado financeiro nem fluxo de caixa em campo estruturado.

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

## As oito tools

| Tool | Quando | Teto |
|---|---|---|
| `buscar_empresas(termo)` | achar slug e CNPJ pelo nome ou CNPJ | 20 empresas |
| `ficha_empresa(chave)` | cadastro, setor, anos com BP e DRE, contagem de publicações | |
| `analisar_empresa(chave)` | retrato completo; comece por aqui | 100 documentos no índice |
| `balancos_empresa(chave, ano?)` | só os BPs (todos ou um ano) | |
| `dres_empresa(chave, ano?)` | só as DREs (todas ou um ano) | |
| `documentos_empresa(chave)` | índice de publicações, mais recentes primeiro | 100 |
| `texto_documento(documento_id)` | texto extraído de uma publicação | 50 mil caracteres, sem offset |
| `ranking_empresas(metrica, uf?, setor?, limite?)` | maiores por ativo, receita, lucro ou crescimento | 50 por chamada |

`chave` aceita slug ou CNPJ (com ou sem pontuação). Campos de cada resposta em
[references/payloads.md](references/payloads.md).

## Como ler o dado

- **`consolidado`**: quase sempre `false`. Se a ficha mostra CNAE de holding
  (`64.62-0`, `64.63-8`, "participações") ou a receita é irrisória diante do ativo, o
  número é da entidade individual e o lucro vem de equivalência patrimonial. Diga isso em
  vez de concluir "receita despencou" ou "margem de 90%".
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
  sinalize, sem interpretar.
- **Reapresentação**: dois documentos do mesmo tipo e ano (`v2`) são versões. A base já
  escolheu; você não precisa.
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

- `texto_documento` devolve os primeiros 50 mil caracteres. Uma DF completa tem 300 a
  800 mil. `truncado: true` significa que parecer do auditor e notas explicativas, que
  ficam no fim, provavelmente não vieram. Não há como pedir o resto. Diga isso e aponte
  o link. Texto de jornal vem com o espaçamento das colunas: 50 mil brutos podem ser 20
  mil úteis, e frases de colunas vizinhas se intercalam linha a linha; leia por frase.
  A extração perde a ligadura "fi": procure "inanceir", "inanciament", "iscal".
- `ano_referencia` em publicação de jornal pode ser o ano da publicação, não do
  exercício ("DFs de 2025" com `ano_referencia: 2026`); confira pelo título e pela data.
- DFPs da CVM costumam vir como "texto ainda não extraído". A publicação em jornal do
  mesmo exercício costuma ter texto. Prefira ela.
- O `tipo` do índice é aproximado: "Demonstração de Resultados" com 10 páginas e centenas
  de milhares de caracteres é a DF completa. Julgue pelo título, páginas e tamanho.
- Se o cliente gravou o resultado da tool em arquivo por ser grande, leia o arquivo
  inteiro antes de responder. Um preview de 2 mil caracteres é só o cabeçalho.
- O documento do ano seguinte traz o ano pedido como comparativo nas notas; o do ano
  anterior pode conter um item que o corte de 50 mil deixou fora no ano corrente.

## O que a base não tem

Fluxo de caixa, EBITDA, dívida bruta ou líquida, caixa, cobertura de juros, resultado
financeiro, depreciação, estoques, contas a receber, quadro societário, controlador, ITR
trimestral, contagem de empresas por setor, filtro por faixa de receita, paginação. Quando
pedirem, responda o que existe, diga com todas as letras o que não existe, leia o texto da
publicação quando ele tiver o número (proveniência 2) e aponte o link. Não estime.

"Quantas empresas do setor X": não há contagem. O mais perto é `ranking_empresas` com
`limite=50` nas quatro métricas; se voltar menos de 50, esse é o total com balanço
carregado, e diga que é só isso.

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
| Buscar pela razão social completa | Termo curto; depois CNPJ |
| Usar o ranking de crescimento como "quem cresce" | Filtrar `ativo_base` mínimo e dizer que é ativo total |
| Comparar 2025 de uma com 2023 de outra | Alinhar pelo exercício e declarar buracos |
