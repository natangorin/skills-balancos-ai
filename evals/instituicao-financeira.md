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
