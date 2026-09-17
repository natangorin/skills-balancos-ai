# Campos de cada resposta das tools `bcb_*`

Toda resposta traz `dados_atualizados_em`. `chave` aceita CodInst, CNPJ (14 dígitos) ou
raiz do CNPJ (8 dígitos). Valores em reais; índices em fração.

## Objeto `instituicao` (ficha), presente em quase toda resposta

```
codinst, nome, cnpj, cnpj_raiz,
tipo {codigo, nome} | null, consolidado_bancario {codigo, nome} | null,
segmento_prudencial (S1..S5) | null, sede {uf, municipio},
conglomerados {financeiro (codinst | null), prudencial (codinst | null)},
primeira_data_base, ultima_data_base, n_data_bases,
empresa {razao_social, slug, link} | null
```

`bcb_ficha_instituicao` e `bcb_analisar_instituicao` acrescentam:

```
receita {razao_social, situacao, cnae}
niveis[]: nivel (individual | financeiro | prudencial), codinst, nome, padrao (bool)
nivel_padrao
ultima_data_base_resumo {data_base, data_referencia, nivel, ativo_total, carteira_credito,
                         captacoes, patrimonio_liquido, indice_basileia}
link_ifdata
```

## bcb_buscar_instituicoes(termo?, uf?, tipo?, consolidado_bancario?)

```
instituicoes[] (objeto instituicao, até 20)
total, dica (quando vazio)
```

Fundos de investimento aparecem com `tipo: null` e poucas data-bases.

## bcb_analisar_instituicao(chave)

```
instituicao (ficha completa)
nivel {nivel, codinst, nome, padrao}
trimestres[]: data_base, data_referencia, ano, trimestre, era (cosif_2000 | cosif_2025),
  nivel_padrao,
  valores_em_reais {ativo_total, carteira_credito, tvm, captacoes, patrimonio_liquido,
                    lucro_liquido_acumulado_semestre, patrimonio_referencia, rwa},
  indices {basileia, imobilizacao, alavancagem},
  rede {agencias, postos},
  link_documento (só em dezembro) | null
resultados_anuais[]: periodo ("anual"), ano, trimestre (null), data_inicio, data_referencia,
  era, completo (bool),
  valores_em_reais {receita_bruta (null), receita_liquida, custo, lucro_bruto,
                    lucro_operacional, lucro_liquido}
nota
```

## bcb_trimestres_instituicao(chave, nivel?, desde?, ate?)

```
instituicao, nivel, trimestres[] (igual a bcb_analisar_instituicao)
```

## bcb_resultados_instituicao(chave, nivel?, periodo?)

```
instituicao, nivel
resultados[]: periodo (trimestre | anual), ano, trimestre (1..4 | null), data_inicio,
  data_referencia, era, completo, valores_em_reais (igual a resultados_anuais)
```

## bcb_relatorios_instituicao(chave, nivel?, data_base?, relatorio?)

```
instituicao, nivel, data_base, data_referencia, era, data_base_anterior, comparavel (bool)
relatorios[]: id, nome, grupo, cabecalho,
  linhas[]: id, lid, nome, descricao, profundidade, grupo (bool), formato (mil | pct | inteiro),
            valor, valor_ano_anterior
```

`formato: "mil"` é só o cabeçalho da fonte: `valor` está em reais.

## bcb_estrutura_relatorios(data_base, relatorio?)

Sem `relatorio` (`resumido: true`):

```
data_base, era
relatorios[]: id, nome, grupo (demonstracoes | capital | carteira | segmentacao),
  niveis[], cabecalho, notas, n_colunas
nota
```

Com `relatorio`: o mesmo relatório com a árvore de colunas (id, lid, nome, descricao,
pai, profundidade, formato).

## bcb_conglomerado(codinst, nivel?)

```
conglomerado {nivel, codinst, nome, primeira_data_base, ultima_data_base, n_data_bases, n_membros}
membros[]: codinst, nome, cnpj, ativo_total, data_base, empresa
```

## bcb_ranking_instituicoes(metrica, data_base?, nivel?, uf?, tipo?, consolidado_bancario?, limite?)

```
data_base, data_referencia, nivel, metrica, unidade (reais | fracao)
instituicoes[]: posicao, nivel, codinst, nome, cnpj | null, tipo, consolidado_bancario,
  uf, valor, empresa | null
nota
```

`metrica` = `ativo` | `carteira` | `captacoes` | `patrimonio` | `lucro` | `basileia`.
Linhas de nível prudencial vêm com `cnpj` e `empresa` nulos.

## bcb_data_bases()

```
data_bases[]: data_base, data_referencia, ano, trimestre, era, n_instituicoes, derivada_em
```
