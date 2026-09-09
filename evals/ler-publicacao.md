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
- Reconhece `truncado: true` e diz que o texto veio cortado em 50 mil caracteres;
  procura o trecho em outro documento (parecer separado) ou manda pro link.
- Responde com citações curtas do texto e o link do documento; não inventa o parecer
  quando o trecho não está no texto disponível.
