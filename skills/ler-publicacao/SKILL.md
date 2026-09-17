---
name: ler-publicacao
description: Use quando pedirem o conteúdo de uma publicação legal de empresa brasileira com o MCP do Balanços.AI conectado, como "o que diz a nota explicativa", "resume a ata", "tem ressalva do auditor", "o que o relatório da administração fala", "quanto de dívida aparece nas notas", "eventos subsequentes", ou qualquer pergunta que exija ler o texto de um documento.
license: MIT
compatibility: Requer o MCP do Balanços.AI conectado. Assume a skill balancos-ai; companhia-aberta quando a empresa está na CVM.
metadata:
  author: Balanços.AI
  version: "0.3"
---

# Ler uma publicação

## Resultado

A resposta à pergunta com citações curtas do texto, o documento identificado (título, tipo,
data, link), o que foi lido (termos buscados ou faixa de caracteres de
`tamanho_total_chars`) e o que não foi encontrado. Sem trecho, sem afirmação.

## Passos

1. Resolva a empresa (`buscar_empresas`) e pegue o índice com `documentos_empresa`, ou use
   o que veio em `analisar_empresa`.
2. Escolha o documento pelo `ano_referencia` pedido e pela probabilidade de ter texto:
   - publicação em jornal ou na Central de Balanços ("Demonstrações Financeiras",
     "Demonstração de Resultados", "Demonstrações Contábeis Completas" com várias páginas)
     tem texto, inteiro;
   - "Demonstrações Financeiras Padronizadas" (DFP, CVM) vem "texto ainda não extraído".
     Se a empresa é companhia aberta, o que a DFP tem de estruturado não precisa de texto:
     parecer do auditor em `cvm_parecer_dfp` (tipo, texto integral, declarações dos
     diretores) e demonstrações conta a conta em `cvm_demonstracoes_dfp` (skill
     companhia-aberta). Notas explicativas e relatório da administração continuam só no
     texto da publicação;
   - ata, edital e press release têm texto curto e inteiro.
   O `tipo` do índice é aproximado e `ano_referencia` pode ser o ano da publicação em
   jornal; julgue pelo título, data, `paginas` e, depois da chamada, por
   `tamanho_total_chars`. Dois documentos do mesmo ano ("v2") são versões; use a mais
   recente; se ela não tem texto, a anterior também não costuma ter.
3. **Pedido com assunto** (ressalva, ênfase, contingência, empréstimo, covenant, partes
   relacionadas, evento subsequente): `texto_documento(id, termo="...")`, sem pedir um
   pedaço antes. Volta até 20 trechos com 600 caracteres de contexto para cada lado,
   `inicio` e `fim` de cada um e `total_ocorrencias`, sem distinção de caixa nem acento;
   ocorrências vizinhas colapsam ou se sobrepõem, então vêm menos trechos que
   ocorrências (22 de "opini" viraram 18 trechos). Um termo por chamada, curto,
   pelo radical ("conting", "provis", "ressalva", "ênfase", "subsequente"; a tabela por
   assunto está em `references/roteiro-notas.md` da skill due-diligence-financeira). Se o
   aviso disser "mostrando 20 de N", refine o termo ou continue a partir do `fim` do
   último trecho. Para ler o entorno de um trecho, `texto_documento(id, inicio=<inicio do
   trecho>, tamanho=20000)`.
4. **Pedido sobre o documento inteiro** (resumo, "o que diz o relatório da
   administração", "o que aconteceu no ano"): `texto_documento(id, inicio=0)` devolve
   100 mil caracteres (teto 200 mil com `tamanho`), `tamanho_total_chars`, `truncado` e
   `proximo_inicio`. Enquanto `truncado` for `true`, repita com `inicio=proximo_inicio`.
   Uma DF completa tem 300 a 800 mil caracteres: até 8 chamadas de 100 mil. Se só o
   relatório da administração interessa, ele fica no começo e termina antes de "BALANÇO
   PATRIMONIAL" (na Gerdau, 113 mil caracteres): `tamanho=200000` numa chamada cobre.
   Diga quantos caracteres leu do total e o que ficou fora.
5. Ordem de uma DF completa: relatório da administração, BP, DRE, DMPL, DVA, DFC, notas
   explicativas, e o relatório do auditor no fim. "Parecer" nem sempre aparece como
   palavra, e um parecer limpo não contém "ressalva" nem "ênfase": zero ocorrências
   desses dois não é ausência de parecer. Localize-o por "opinião" ou "auditor" e leia a
   seção "Opinião"; só então diga se tem ressalva, ênfase ou nenhuma das duas. Para
   notas, busque o assunto, não "nota".
6. Texto de jornal traz o espaçamento das colunas e frases de colunas vizinhas
   intercaladas linha a linha: leia por frase. A extração perde a ligadura "fi"
   ("inanceir", "inanciament", "iscal") e alterna singular e plural: busque radicais.
7. Cite o trecho entre aspas, curto, e diga onde está (seção, título da nota quando o
   texto traz, posição em caracteres quando não). Os trechos por termo não trazem o
   cabeçalho das demonstrações: antes de citar valor, confirme a escala com
   `termo="milhares de reais"` (uma chamada) ou diga "escala não confirmada".
8. "Não está no documento" só depois de dois termos diferentes do assunto com
   `total_ocorrencias: 0`, ou da leitura integral até `truncado: false`. Antes disso é
   "ainda não localizado", e a leitura continua. O documento do ano seguinte traz o ano
   pedido como comparativo nas notas e vale como segunda fonte, dizendo de que ano é.

## Regras

- Só o que está no texto. Número de nota, página, valor ou opinião do auditor de memória
  ou "pelo padrão das demonstrações" não entram.
- "Tem ressalva do auditor" em companhia aberta vai direto em `cvm_parecer_dfp` do
  `id_doc` do exercício, que é estruturado (tipo, firma, data). O texto da publicação
  também tem o relatório do auditor, no fim: `termo="auditor"` chega lá.
- "Principais assuntos de auditoria" não é ressalva nem ênfase.
- Texto do jornal vem sem formatação: tabelas viram linhas soltas; confirme o valor pelo
  rótulo ao lado antes de citar.
- `origem_texto` (`legado` ou `silver`) é só proveniência da extração; não muda a leitura.
- Cliente que grava resultado grande em arquivo (Claude Code: acima de uns 10 mil
  caracteres, com preview de 2 mil): leia o arquivo inteiro antes de responder. A busca
  por termo cabe no preview na maioria das vezes; o pedaço de 100 mil nunca cabe. O
  arquivo é um JSON de uma linha, então ler por linhas não divide o pedaço: para achar um
  marcador dentro dele ("BALANÇO PATRIMONIAL", nome de uma nota), procure no texto com
  grep ou um script, não com paginação por linha.
- Cliente conectado antes da atualização do MCP pode mostrar `texto_documento` só com
  `documento_id` e um teto de 50 mil: o servidor aceita `inicio`, `tamanho` e `termo`
  mesmo assim; passe-os.
- Orçamento: um assunto se resolve com 2 a 4 chamadas (termo, entorno); leitura integral
  de um documento, até 8. Não leia três documentos inteiros para uma pergunta pontual.
- Documento sem texto: entregue o link e diga que a leitura é na página. Depois de três
  documentos sem texto útil (DFP "não extraído", jornal só com a capa do extrato), pare
  de tentar e diga que a empresa não tem texto na base.

## Quando o dado não existe

- Empresa sem publicação do ano pedido: liste os anos que existem no índice.
- Nenhum documento com texto: diga, com os links dos documentos do ano.
