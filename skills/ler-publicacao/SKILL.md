---
name: ler-publicacao
description: Use quando pedirem o conteúdo de uma publicação legal de empresa brasileira com o MCP do Balanços.AI conectado: "o que diz a nota explicativa", "resume a ata", "tem ressalva do auditor", "o que o relatório da administração fala", "quanto de dívida aparece nas notas", "eventos subsequentes", ou qualquer pergunta que exija ler o texto de um documento.
license: MIT
compatibility: Requer o MCP do Balanços.AI conectado. Assume a skill balancos-ai.
metadata:
  author: Balanços.AI
  version: "0.1"
---

# Ler uma publicação

## Resultado

A resposta à pergunta com citações curtas do texto, o documento identificado (título, tipo,
data, link) e a declaração do que o trecho disponível não cobre. Sem trecho, sem afirmação.

## Passos

1. Resolva a empresa (`buscar_empresas`) e pegue o índice com `documentos_empresa`, ou use
   o que veio em `analisar_empresa`.
2. Escolha o documento pelo `ano_referencia` pedido e pela probabilidade de ter texto:
   - publicação em jornal ("Demonstrações Financeiras", "Demonstração de Resultados",
     "Demonstrações Contábeis Completas" com várias páginas) costuma ter texto;
   - "Demonstrações Financeiras Padronizadas" (DFP, CVM) costuma vir "texto ainda não
     extraído";
   - ata, edital e press release têm texto curto e inteiro.
   O `tipo` do índice é aproximado; julgue pelo título, `paginas` e, depois da chamada,
   por `tamanho_total_chars`. Dois documentos do mesmo ano ("v2") são versões; use o mais
   recente que tenha texto.
3. `texto_documento(id)`. Se o cliente gravou o resultado em arquivo por ser grande, leia
   o arquivo inteiro; um preview de 2 mil caracteres é só o cabeçalho.
4. Leia `truncado` e `tamanho_total_chars`. Com 50 mil de um total de 300 mil ou mais, o
   texto cobre relatório da administração e demonstrações principais; parecer do auditor e
   notas explicativas ficam de fora. Diga isso antes de responder.
5. Procure os termos do pedido no texto (a tabela da skill due-diligence-financeira,
   `references/roteiro-notas.md`, lista termos por assunto). Cite o trecho entre aspas,
   curto, e diga onde está (seção, título da nota, quando o texto traz).
6. Se o pedido não está no trecho disponível: diga "não localizado nos primeiros 50 mil
   caracteres", use pistas do relatório da administração se houver, tente o documento do
   ano seguinte (que traz o ano pedido como comparativo) e aponte o link para a leitura
   completa.

## Regras

- Só o que está no texto. Número de nota, página, valor ou opinião do auditor de memória
  ou "pelo padrão das demonstrações" não entram.
- "Principais assuntos de auditoria" não é ressalva nem ênfase.
- Texto do jornal vem sem formatação: tabelas viram linhas soltas; confirme o valor pelo
  rótulo ao lado antes de citar.
- Documento sem texto: entregue o link e diga que a leitura é na página.

## Quando o dado não existe

- Empresa sem publicação do ano pedido: liste os anos que existem no índice.
- Nenhum documento com texto: diga, com os links dos documentos do ano.
