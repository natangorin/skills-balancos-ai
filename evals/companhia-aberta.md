# Eval: companhia-aberta

## Cenário 1: consolidado versus individual

**Prompt**: "Que tamanho tem a Gerdau S.A. e quanto ela faturou em 2025?"

**Baseline (sem skill)**: usou `analisar_empresa` (publicações), viu receita de R$ 4,8 bi
e lucro operacional acima do bruto, chamou de holding e explicou equivalência.

**Esperado com a skill**: roteia pela natureza jurídica, chama `cvm_analisar_companhia`
com o CNPJ, responde com o consolidado de 2025 (receita de R$ 69,9 bi, ativo de
R$ 81,7 bi), diz a visão e o `id_doc`, e menciona o individual só como "entidade".

## Cenário 2: EBITDA e dívida líquida com código

**Prompt**: "Qual o EBITDA, a dívida líquida e a cobertura de juros da Gerdau em 2025?"

**Baseline**: disse que a base não tem depreciação e mandou ler o texto.

**Esperado**: `cvm_demonstracoes_dfp` de `dre`, `dva`, `bpa` e `bpp` (uma por chamada),
EBITDA = 3.05 + |7.04.01|, dívida bruta = 2.01.04 + 2.02.01, dívida líquida descontando
1.01.01 e 1.01.02, cobertura = 3.05 / |3.06.02| com a ressalva de variação cambial; cada
número com o código ao lado e o link da entrega.

## Cenário 3: parecer com ênfase

**Prompt**: "O auditor da <companhia com ênfase> fez alguma ressalva ou ênfase?"

**Baseline**: leu o preview do texto da publicação, disse "não localizado".

**Esperado**: `cvm_parecer_dfp` do `id_doc` do último exercício; cita o tipo estruturado,
procura "ênfase" e "continuidade" no texto, cita a firma e a data; diz que PAA não é
ressalva.

## Cenário 4: reapresentação

**Prompt**: "A Gerdau reapresentou alguma DFP nos últimos anos? O que mudou?"

**Baseline**: não sabia dizer.

**Esperado**: lê `exercicios[].versoes[]`, lista 2024 (v1 sem parecer, v2 cinco dias
depois "Sem Ressalva"), 2017, 2013 e 2011; diz que a v2 de 2024 pode ser só a inclusão do
parecer; para dizer se número mudou, compara `valor_atual` das duas versões pelo conta a
conta ou diz que não comparou.

## Cenário 5: ranking com grupo duplicado

**Prompt**: "Quais as cinco maiores companhias abertas por receita em 2025?"

**Baseline**: usou `ranking_empresas` de publicações, misturando individual e fechadas.

**Esperado**: `cvm_ranking_companhias(receita, 2025)`; percebe JBS S.A. e JBS N.V. com a
mesma receita, deduplica e diz; declara visão consolidada, família e que o teto é 50.
