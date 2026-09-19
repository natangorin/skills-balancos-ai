# Campos de cada resposta do MCP

Toda resposta traz `dados_atualizados_em` (data da última carga). Empresa não encontrada
volta `{"erro": "Empresa não encontrada.", "dica": ...}`. Listas vazias vêm com `dica`.

## buscar_empresas(termo)

```
empresas[]: razao_social, cnpj, slug, link
total
```

## ficha_empresa(chave) → empresa

```
razao_social, nome_fantasia, cnpj, slug, setor, porte, uf, municipio,
cnae_principal, cnae_descricao, natureza_juridica, situacao_cadastral, capital_social,
publicacoes_total, publicacoes_financeiras, ultima_publicacao,
anos_com_balanco[], anos_com_dre[], link
```

## balancos_empresa(chave, ano?) → balancos[]

```
exercicio, data_referencia, fonte (llm|xbrl), consolidado (bool), contexto (ultimo|penultimo|...),
valores_em_reais: ativo_total, ativo_circulante, ativo_nao_circulante,
                  passivo_circulante, passivo_nao_circulante, passivo_total,
                  patrimonio_liquido, passivo_e_pl_total
escala_publicada, link_documento
```

`passivo_total` é o exigível (circulante + não circulante), sem o PL.

## dres_empresa(chave, ano?) → dres[]

```
exercicio, data_referencia, data_inicio, fonte, periodo_tipo (anual|...), consolidado, contexto,
valores_em_reais: receita_bruta, receita_liquida, custo, lucro_bruto,
                  lucro_operacional, lucro_liquido
escala_publicada, link_documento
```

`custo` costuma vir negativo no xbrl e positivo no llm. Use o valor absoluto nas fórmulas.

## documentos_empresa(chave)

```
empresa: razao_social, slug, link
documentos[]: id, tipo, publicado_em, ano_referencia, titulo, paginas, link
total, aviso (quando há mais de 100)
```

Tipos frequentes: "Demonstrações Financeiras Padronizadas" (DFP, CVM), "Informações
Trimestrais" (ITR, CVM, título "ITR dd/mm/aaaa", três por exercício), "Demonstração de
Resultados", "Notas Explicativas", "Ata de AGO", "Ata de AGE", "Press Release",
"Apresentação de Resultados", "Demonstrações Contábeis Completas".

## texto_documento(documento_id, inicio?, tamanho?, termo?)

Dois modos. Sem `termo`, um pedaço do texto: `inicio` (padrão 0), `tamanho` (padrão
100.000, teto 200.000). Com `termo`, só os trechos que contêm o termo, sem o campo `texto`.
Um pedaço é grande: clientes como o Claude Code gravam o resultado em arquivo e mostram só
um preview de 2 mil caracteres; leia o arquivo inteiro.

```
documento: id, titulo, tipo, publicado_em, link
origem_texto ("legado" | "silver"; só proveniência da extração)
tamanho_total_chars

sem termo:
inicio, fim, texto, truncado (bool: o pedaço não chegou ao fim)
proximo_inicio (só quando truncado; igual a fim), aviso (só quando truncado)

com termo:
termo, trechos[] (até 20): inicio, fim, texto (600 caracteres de contexto para cada lado;
    ocorrências vizinhas colapsam num trecho), total_ocorrencias
dica (quando total_ocorrencias = 0), aviso (quando há mais ocorrências que trechos)

erro ("Texto ainda não extraído para este documento — ...") quando não há texto
```

Busca sem distinção de caixa nem acento; as posições valem no texto original. Laço de
leitura integral: `inicio=0`, depois `inicio=proximo_inicio` enquanto `truncado`.

## ranking_empresas(metrica, uf?, setor?, limite?)

`metrica` = `ativo` | `receita` | `lucro` | `crescimento`. Volta `nota` explicando a régua.

```
empresas[] (ativo/receita/lucro): razao_social, slug, uf, setor,
    ativo_total_em_reais | receita_em_reais | lucro_liquido_em_reais, exercicio, link
empresas[] (crescimento): razao_social, slug, uf, setor, crescimento_ativo_total_pct,
    ativo_base, ativo_atual, de_ano, para_ano, link
```

Cada linha traz o próprio `exercicio`: eles diferem entre empresas. Linhas com valor zero
ou irrisório aparecem (holdings, extrações parciais); filtre antes de apresentar.

## analisar_empresa(chave)

```
empresa (igual à ficha)
balancos[] (igual a balancos_empresa)
dres[] (igual a dres_empresa)
documentos[] (100 mais recentes), documentos_total
crescimento_ativo_total: de_ano, para_ano, ativo_base, ativo_atual, pct  (quando existe)
```
