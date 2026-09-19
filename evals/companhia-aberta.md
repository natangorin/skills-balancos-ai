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

**Esperado**: `cvm_demonstracoes` de `dre`, `dva`, `bpa` e `bpp` (uma por chamada),
EBITDA = 3.05 + |7.04.01|, dívida bruta = 2.01.04 + 2.02.01, dívida líquida descontando
1.01.01 e 1.01.02, cobertura = 3.05 / |3.06.02| com a ressalva de variação cambial; cada
número com o código ao lado e o link da entrega.

## Cenário 3: parecer com ênfase

**Prompt**: "O auditor da <companhia com ênfase> fez alguma ressalva ou ênfase?"

**Baseline**: leu o preview do texto da publicação, disse "não localizado".

**Esperado**: `cvm_parecer` do `id_doc` da DFP do último exercício; cita o tipo
estruturado, procura "ênfase" e "continuidade" no texto, cita a firma e a data; diz que
PAA não é ressalva.

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

## Cenário 6: dado mais recente

**Prompt**: "Como está a Gerdau este ano? Quanto faturou nos últimos doze meses?"

**Baseline (skill 0.3)**: respondia com a DFP do exercício anterior, dizendo que a base não
tem ITR.

**Esperado**: `cvm_analisar_companhia` e, se preciso, `cvm_trimestres_companhia`; responde
com a data de referência mais recente (jun/26, não "2T26"), receita e lucro de doze meses
prontos (sem somar trimestres), o trimestre contra o mesmo trimestre do ano anterior,
visão consolidada e o link do ITR; marca "derivado" no trimestre de fechamento se o citar.

## Resultados registrados

Os registros de 2026-09-17 usam os nomes de tool do MCP 0.3 (`*_dfp`); no 0.4 eles viraram
`cvm_entregas_companhia`, `cvm_entrega`, `cvm_demonstracoes` e `cvm_parecer`.

- 2026-09-17, cenário 1, com skill: passou. `buscar_empresas("Gerdau")` →
  `cvm_buscar_companhias` pelo CNPJ → `cvm_analisar_companhia`, sem `analisar_empresa`.
  Respondeu com o consolidado de 2025 (receita R$ 69,86 bi, ativo R$ 81,69 bi), visão,
  `id_doc` 154830 e versão declarados, parecer "Sem Ressalva", individual apresentado
  como "controladora sozinha", links da empresa e das entregas, `dados_atualizados_em`
  da fonte CVM separado do de publicações.
- 2026-09-17, cenários 2 a 5, com skill: todos passaram.
  - 2 (EBITDA e dívida líquida): uma demonstração por chamada, cada número com código,
    ressalva de variação cambial, e percebeu que a Gerdau lança arrendamento em "Outras
    Obrigações" (2.01.05.02.05 e 2.02.02.02.04), fora de 2.01.04.03; a skill passou a
    mandar procurar "arrendamento" nas descrições.
  - 3 (parecer, Americanas S.A.): tipo "Sem Ressalva" com duas ênfases (recuperação
    judicial e investigações), PAA separado, firma e data, resultado de 49 KB lido
    inteiro do arquivo; a skill ganhou a nota de arquivo grande.
  - 4 (reapresentação): listou as quatro reapresentações; descobriu que as v1 estão na
    base como casca vazia (`visoes: []`) e comparou o
    comparativo da DFP 2025 com a v2 de 2024. A skill passou a mandar conferir `visoes`
    da v1 e comparar pelo comparativo da DFP seguinte.
  - 5 (ranking): deduplicou JBS S.A. e JBS N.V., achou Metalúrgica Gerdau e Gerdau S.A.
    também duplicadas, marcou ano fiscal não-calendário da Raízen e a reapresentação da
    Vale; a skill passou a citar duplicidade por controladora e controlada.
