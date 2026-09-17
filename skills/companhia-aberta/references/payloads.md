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

## cvm_dfps_companhia(chave, ano?)

```
companhia {cnpj, cd_cvm, denominacao, empresa}
exercicios[]: exercicio, data_referencia,
  versoes[]: id_doc, versao, reapresentacao (bool), recebida_em, parecer (tipo | null),
             link_cvm, link_documento
```

Exercícios decrescentes; versões crescentes. A última versão de um exercício é a que vale.

## cvm_entrega_dfp(id_doc) → entrega

```
id_doc, exercicio, data_referencia, versao, link_documento, companhia,
reapresentacao, recebida_em, link_cvm, escala_publicada, moeda,
visoes[] (consolidado, individual),
demonstracoes_disponiveis {consolidado[], individual[]}  (bpa, bpp, dre, dra, dfc, dmpl, dva),
parecer (tipo), capital_social, versoes[] (igual a cvm_dfps_companhia)
```

## cvm_balancos_companhia(chave, ano?, visao?) → balancos[]

```
exercicio, data_referencia, visao, versao, id_doc, familia, escala_publicada,
eq_ativo_passivo (bool),
valores_em_reais: ativo_total, ativo_circulante, ativo_nao_circulante,
                  passivo_circulante, passivo_nao_circulante, passivo_total,
                  patrimonio_liquido, passivo_e_pl_total
```

Mesmos nomes de campo da fonte publicações, com `visao` a mais. `passivo_total` é o
exigível, sem PL.

## cvm_dres_companhia(chave, ano?, visao?) → dres[]

```
exercicio, data_referencia, data_inicio, periodo_tipo, visao, versao, id_doc, familia,
escala_publicada,
valores_em_reais: receita_bruta (null na CVM), receita_liquida, custo (negativo),
                  lucro_bruto, lucro_operacional (EBIT, conta 3.05), lucro_liquido
```

## cvm_analisar_companhia(chave)

```
companhia (igual à ficha)
exercicios[] (igual a cvm_dfps_companhia)
balancos[] (igual a cvm_balancos_companhia, as duas visões, última versão)
dres[] (igual a cvm_dres_companhia)
nota
```

## cvm_demonstracoes_dfp(id_doc, demonstracao?, visao?)

```
entrega {id_doc, exercicio, data_referencia, versao, link_documento}
visao (a usada), visao_solicitada
demonstracoes[]: demonstracao, nome, metodo (dfc: direto | indireto), escala_publicada,
  moeda, exercicio_atual {inicio, fim}, exercicio_anterior {inicio, fim},
  contas[]: codigo, descricao, nivel, padronizada (bool), coluna, valor_atual, valor_anterior
```

`valor_anterior` é o comparativo republicado nesta DFP. Resposta grande sem
`demonstracao`: clientes como o Claude Code gravam em arquivo; leia o arquivo inteiro.

## cvm_parecer_dfp(id_doc)

```
entrega {id_doc, exercicio, data_referencia, versao, link_documento}
auditor {tipo, texto}
declaracoes[]: tipo, texto
```

Tipos de `declaracoes`: "Declaração dos Diretores sobre as Demonstrações Financeiras",
"Declaração dos Diretores sobre o Relatório do Auditor Independente", "Parecer do
Conselho Fiscal ou Órgão Equivalente".

## cvm_ranking_companhias(metrica, ano, visao?, familia?, limite?)

```
metrica, exercicio, visao, familia
companhias[]: posicao, cnpj, cd_cvm, denominacao, valor_em_reais, versao, id_doc, empresa
nota
```

`metrica` = `ativo` | `patrimonio` | `receita` | `lucro`. Limite até 50, padrão 20.
