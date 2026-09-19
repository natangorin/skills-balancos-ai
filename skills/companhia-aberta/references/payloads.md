# Campos de cada resposta das tools `cvm_*`

Toda resposta traz `dados_atualizados_em`. `chave` aceita CNPJ (com ou sem pontuação) ou
código CVM. Valores em reais; `escala_publicada` é só proveniência.

## cvm_buscar_companhias(termo)

```
companhias[]: cnpj, cd_cvm, denominacao, empresa {razao_social, slug, link} | null
total
```

## cvm_ficha_companhia(chave) → companhia

```
cnpj, cd_cvm, denominacao, empresa, denominacoes_anteriores[],
familia (comercial | financeira | seguradora | desconhecida),
primeiro_exercicio, ultimo_exercicio, n_entregas, n_reapresentacoes,
ultimo_parecer {exercicio, tipo},
capital_social {exercicio, versao, integralizado {ordinarias, preferenciais, total},
                tesouraria {ordinarias, preferenciais, total}}
```

Derivada das entregas de DFP.

## cvm_entregas_companhia(chave, tipo?, ano?)

```
companhia {cnpj, cd_cvm, denominacao, empresa}
tipo (dfp | itr)
exercicios[]: exercicio, data_referencia,
  versoes[]: id_doc, versao, reapresentacao (bool), recebida_em, parecer (tipo | null),
             link_cvm, link_documento
```

`tipo` padrão `dfp`. No ITR há um item por data de referência, três por exercício, com o
mesmo `exercicio`. Datas decrescentes; versões crescentes. A última versão de uma data é
a que vale.

## cvm_entrega(id_doc) → entrega

```
id_doc, exercicio, data_referencia, versao, link_documento, companhia,
reapresentacao, recebida_em, link_cvm, escala_publicada, moeda,
visoes[] (consolidado, individual),
demonstracoes_disponiveis {consolidado[], individual[]}  (bpa, bpp, dre, dra, dfc, dmpl, dva),
parecer (tipo), capital_social, versoes[] (igual a cvm_entregas_companhia)
tipo (dfp | itr)   ← fora de `entrega`, no topo da resposta
```

## cvm_balancos_companhia(chave, ano?, visao?) → balancos[]

```
exercicio, data_referencia, visao, versao, id_doc, familia, escala_publicada,
eq_ativo_passivo (bool),
valores_em_reais: ativo_total, ativo_circulante, ativo_nao_circulante,
                  passivo_circulante, passivo_nao_circulante, passivo_total,
                  patrimonio_liquido, passivo_e_pl_total
```

Só DFP. Mesmos nomes de campo da fonte publicações, com `visao` a mais. `passivo_total`
é o exigível, sem PL.

## cvm_dres_companhia(chave, ano?, visao?) → dres[]

```
exercicio, data_referencia, data_inicio, periodo_tipo, visao, versao, id_doc, familia,
escala_publicada,
valores_em_reais: receita_bruta (null na CVM), receita_liquida, custo (negativo),
                  lucro_bruto, lucro_operacional (EBIT, conta 3.05), lucro_liquido
```

Só DFP.

## cvm_trimestres_companhia(chave, desde?, ate?, visao?)

```
companhia {cnpj, cd_cvm, denominacao, empresa}
visao (a usada), visao_solicitada
trimestres[]: data_referencia, inicio_exercicio, trimestre_exercicio (1 a 4),
  origem (itr | dfp), familia, link_documento,
  balanco_em_reais: (mesmos 8 campos de cvm_balancos_companhia)
  resultado:
    trimestre | acumulado | doze_meses:
      valores_em_reais: (mesmos 6 campos de cvm_dres_companhia)
      derivado (bool), consistente (bool), ranqueavel (bool | null),
      documentos_origem[] (links das entregas que compõem o número)
nota, aviso (quando cortou nas 12 datas mais recentes), dica (quando vazio)
```

Do mais recente para o mais antigo, última versão de cada entrega. O ponto do fechamento
do exercício tem `origem: dfp`, `trimestre.derivado: true` e `doze_meses` igual ao
`acumulado`. `trimestre_exercicio` conta do início do exercício social da companhia.

## cvm_resultados_companhia(chave, periodo?, desde?, ate?, visao?)

```
companhia, periodo, visao, visao_solicitada
resultados[]: data_referencia, inicio_exercicio, trimestre_exercicio, periodo, visao,
  familia, valores_em_reais (6 campos), derivado, consistente, ranqueavel,
  documentos_origem[]
nota, aviso, dica
```

`periodo` = `trimestre`, `acumulado`, `12m` ou `anual`; sem valor, todos (linhas
repetidas por data, uma por período).

## cvm_analisar_companhia(chave)

```
companhia (igual à ficha)
exercicios[] (DFPs, igual a cvm_entregas_companhia)
balancos[] (igual a cvm_balancos_companhia, as duas visões, última versão)
dres[] (igual a cvm_dres_companhia)
trimestral {visao, mais_recente (um item de trimestres[] ou null), nota}
nota
```

## cvm_demonstracoes(id_doc, demonstracao?, visao?)

```
entrega {id_doc, exercicio, data_referencia, versao, link_documento}
visao (a usada), visao_solicitada, tipo (dfp | itr)
demonstracoes[]: demonstracao, nome, metodo (dfc: direto | indireto), escala_publicada,
  moeda, exercicio_atual {inicio, fim}, exercicio_anterior {inicio, fim},
  trimestre_atual {inicio, fim} | null, trimestre_anterior {inicio, fim} | null,
  contas[]: codigo, descricao, nivel, padronizada (bool), coluna, valor_atual,
            valor_anterior, valor_trimestre_atual, valor_trimestre_anterior
nota (no ITR)
```

Na DFP, `valor_anterior` é o comparativo republicado nesta entrega e os campos de
trimestre vêm nulos. No ITR:

| Demonstração | `valor_atual` / `valor_anterior` | `valor_trimestre_*` |
|---|---|---|
| DRE, DRA | acumulado no exercício / mesmo período do ano anterior | trimestre isolado, atual e do ano anterior |
| DFC, DVA, DMPL | acumulado no exercício / mesmo período do ano anterior | null |
| BPA, BPP | saldo na data / fechamento do exercício anterior | null |

Resposta grande sem `demonstracao`: clientes como o Claude Code gravam em arquivo; leia o
arquivo inteiro.

## cvm_parecer(id_doc)

```
entrega {id_doc, exercicio, data_referencia, versao, link_documento}
tipo (dfp | itr)
auditor {tipo, texto}
declaracoes[]: tipo, texto
nota (no ITR: relatório de revisão especial), dica (quando não há parecer)
```

Tipos de `declaracoes`: "Declaração dos Diretores sobre as Demonstrações Financeiras",
"Declaração dos Diretores sobre o Relatório do Auditor Independente", "Parecer do
Conselho Fiscal ou Órgão Equivalente".

## cvm_ranking_companhias(metrica, ano?, periodo?, data_referencia?, visao?, familia?, limite?)

`periodo="anual"` (padrão):

```
metrica, exercicio, visao, familia
companhias[]: posicao, cnpj, cd_cvm, denominacao, valor_em_reais, versao, id_doc, empresa
nota
```

`periodo="12m"`:

```
metrica, data_referencia, visao, familia, periodo ("12m")
companhias[]: posicao, cnpj, denominacao, familia, valor_em_reais, consistente, empresa
nota
```

`metrica` = `ativo` | `patrimonio` | `receita` | `lucro` no anual; `receita` | `lucro` no
12m. Limite até 50, padrão 20.
