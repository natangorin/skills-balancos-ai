---
name: investigar-empresa
description: Use quando pedirem um retrato de uma empresa brasileira específica ("me conta sobre a X", "o que sabemos da X", "como está a X financeiramente", "perfil da empresa X") com o MCP do Balanços.AI conectado, ou quando o usuário citar um CNPJ ou razão social e quiser entender tamanho, tendência e saúde financeira.
license: MIT
compatibility: Requer o MCP do Balanços.AI conectado. Assume as skills balancos-ai e indicadores-financeiros.
metadata:
  author: Balanços.AI
  version: "0.1"
---

# Investigar uma empresa

## Resultado

Um memo com seções fixas, nesta ordem, que cabe em uma tela e separa o que a base mostra do
que é interpretação:

1. **Identidade**: razão social, CNPJ, natureza jurídica, CNAE, UF e município, situação
   cadastral, setor da base, link da empresa.
2. **Natureza do dado**: se é entidade operacional ou holding, e por quê (CNAE, receita
   diante do ativo). Fonte por exercício (xbrl ou llm). Anos disponíveis de BP e DRE.
3. **Tamanho**: ativo total, patrimônio líquido, receita líquida e lucro líquido do último
   exercício, em R$ mi ou bi, com o ano. Em holding, acrescente o que o relatório da
   administração diz do grupo (EBITDA, lucro, dívida líquida consolidados), citado e
   rotulado "segundo a companhia".
4. **Trajetória**: tabela de 3 a 5 exercícios com ativo, PL, receita líquida, lucro líquido
   e a variação anual. Em holding, variação de ativo, PL e lucro no lugar de receita.
   Anomalias excluídas e declaradas; anomalia fora da janela vai numa linha da seção 7.
5. **Rentabilidade e estrutura de capital**: margens, ROE, liquidez corrente,
   endividamento e composição, com a leitura da skill indicadores-financeiros.
6. **Publicações**: as 3 a 5 mais recentes com tipo, data e link; total no índice.
7. **Ressalvas**: tudo que ficou fora (consolidado, dívida, fluxo de caixa), com o caminho
   pelo texto da publicação. `dados_atualizados_em`.
8. **Uma frase**: o que a empresa é e como chega ao último exercício.

## Passos

1. `buscar_empresas` com termo curto. Se vier mais de uma, escolha pelo CNPJ ou pela
   ficha e diga qual escolheu e quais descartou (homônimos, coligadas).
2. `analisar_empresa` com o slug. Uma chamada; não repita `ficha_empresa`,
   `balancos_empresa` e `dres_empresa` para a mesma empresa.
3. Classifique a natureza do dado antes de qualquer número: CNAE 64.62-0 ou 64.63-8,
   "participações" ou "holding" na descrição, receita líquida abaixo de 1% do ativo, ou
   lucro operacional acima do lucro bruto indicam holding ou controladora. Nesse caso a
   seção 5 mostra só ROE, alavancagem e tendência de PL e lucro, e a seção 7 diz que o
   número do grupo está no consolidado da publicação.
4. Monte a série pelo `exercicio`, pareando BP e DRE do mesmo ano. Exclua exercícios com
   ativo de R$ 1.000, receita negativa ou salto de mil vezes, e liste-os na seção 7 com o
   link do documento.
5. Calcule os indicadores com as fórmulas da skill indicadores-financeiros.
6. Se o pedido incluir "o que publicou" ou "o que aconteceu", leia o texto da publicação
   mais recente com `texto_documento` (a publicação em jornal costuma ter texto; a DFP
   costuma não ter). Se o resultado vier gravado em arquivo, leia o arquivo inteiro. Cite
   só o que está no texto, entre aspas curtas, com o link.
7. Escreva o memo.

## Regras

- Três proveniências (skill balancos-ai): base, texto citado, conhecimento geral. Tudo
  que não veio do MCP nem do texto lido é conhecimento seu: história do grupo,
  controlador, eventos de mercado, motivo de uma queda. Vai em frase separada, rotulada
  "de conhecimento geral, não confirmado na base", ou fica de fora.
- Não atribua causa a variações (covenant, aquisição, crise) sem trecho do texto.
- Não escreva "em milhares". Valores já estão em reais.
- Se o MCP do cnpj.ai estiver disponível, a seção 1 pode ganhar sócios e vínculos; se
  não, diga que quadro societário não está na base.

## Quando o dado não existe

- Empresa não encontrada: diga que a base não a cobre ainda, sugira a busca por CNPJ e
  aponte https://balancos.ai para acompanhar.
- Empresa sem BP nem DRE (só publicações): entregue as seções 1, 2, 6 e 7 e diga que os
  demonstrativos ainda não foram extraídos, com o link dos documentos.

Modelo do memo em [references/modelo-memo.md](references/modelo-memo.md).
