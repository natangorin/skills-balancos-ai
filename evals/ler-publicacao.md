# Eval: ler-publicacao

## Cenário 1: parecer do auditor e contingências

**Prompt**: "O auditor independente da Gerdau S.A. fez alguma ressalva ou ênfase nas
demonstrações de 2024? E tem alguma contingência relevante (processos, provisões) nas
notas explicativas? Me aponta onde está no documento."

**Baseline (sem skill)**: filtrou por ano, reconheceu `truncado: true` (50 mil de 731 mil
caracteres) e não inventou o parecer, mas citou numeração de notas "de memória" (17 a
19), tentou as DFPs sem texto antes do jornal e usou o `tipo` do índice como se fosse
exato.

**Esperado com a skill**:
- Escolhe o documento pelo `tipo` e `ano_referencia` em `documentos_empresa`,
  preferindo demonstrações completas ou notas explicativas de 2024.
- Busca por `termo` ("ressalva", "ênfase", "auditor", "conting", "provis"), um por
  chamada, e lê o entorno com `inicio` quando o trecho não basta; não pede o documento
  inteiro para uma pergunta pontual.
- Responde com citações curtas, a posição ou a nota onde está, o link do documento; não
  inventa o parecer, e só diz "não está" depois de dois termos sem ocorrência.

## Cenário 3: resumo do relatório da administração

**Prompt**: "Resume o relatório da administração da publicação de 2024 da Gerdau: o que
a empresa destacou do ano?"

**Esperado**: `texto_documento(id, inicio=0)` e leitura do pedaço inteiro (arquivo, se o
cliente gravou); o relatório da administração fica no começo, então não precisa do laço
até o fim; diz quantos caracteres leu de `tamanho_total_chars` e que o restante do
documento (demonstrações, notas, parecer) não entrou no resumo.

## Cenário 4: evento subsequente

**Prompt**: "Aconteceu algo relevante depois do fechamento de 2024 na Gerdau? Procura
eventos subsequentes nas notas."

**Esperado**: `termo="subsequente"` direto; cita o trecho com a posição; se não há
ocorrência, tenta "posterior" ou "após o encerramento" antes de dizer que a nota não
existe; não lê o documento inteiro.

## Cenário 2: parecer de companhia aberta

**Prompt**: "Tem ressalva do auditor na DFP 2025 da Gerdau?"

**Esperado**: `cvm_parecer_dfp` do `id_doc` de 2025, sem tentar `texto_documento` da DFP;
tipo, firma e data; PAA não é ressalva.

## Resultados registrados

- 2026-09-17, cenário "parecer de companhia aberta" (Gerdau, DFP 2025), com skill:
  passou. Quatro chamadas, direto em `cvm_parecer_dfp`, sem tentar `texto_documento`
  da DFP; tipo, firma, data, PAA separado de ressalva.
