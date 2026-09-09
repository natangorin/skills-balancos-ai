---
name: originacao-ma
description: Use quando pedirem para mapear alvos de aquisição, empresas à venda em potencial, consolidação de um setor, ou possíveis compradores estratégicos para uma empresa ("quem poderia comprar a X", "mapeia alvos de energia no Sul", "empresas de saúde entre 100 mi e 1 bi de receita") com o MCP do Balanços.AI conectado.
license: MIT
compatibility: Requer o MCP do Balanços.AI conectado. Assume as skills balancos-ai e indicadores-financeiros.
metadata:
  author: Balanços.AI
  version: "0.1"
---

# Originação de M&A

## Resultado

**Alvos**: longlist em tabela (empresa, UF da sede, CNAE, último exercício, receita
líquida, lucro líquido, PL, alavancagem, fonte, link) com uma linha de tese por empresa,
separada em "dentro do corte", "borda" e "descartadas com motivo". **Compradores**:
shortlist ordenada por capacidade (PL, liquidez, crescimento de ativo) e encaixe
(mesmo setor ou adjacente, mesma região), com o porquê. Nas duas, uma seção "o que a base
não tem" e uma "de conhecimento geral, não confirmado na base".

## Passos para alvos

1. Traduza o pedido em filtros: rótulo de `setor` (tabela em
   `references/setores.md` da skill balancos-ai; "energia" é "Eletricidade"), UFs,
   faixa de receita, sinais desejados (margem, tendência, estresse).
2. Para cada UF, `ranking_empresas` com `metrica="receita"` e depois `metrica="ativo"`,
   `setor` pelo rótulo certo, `limite=50`. Ativo pega quem ficou fora por receita
   (holding, ano sem DRE). Junte e dedupe pelo slug. Se o setor tiver rótulos herdados
   ("Energia Elétrica"), rode com os dois e junte.
3. Corte de receita do lado do agente com `receita_em_reais` e `exercicio` de cada linha.
   Descarte receita zero ou irrisória (holding, extração parcial) e exercícios anteriores
   a 3 anos atrás vão para "dado defasado", nunca para a longlist principal.
4. `ficha_empresa` (ou `analisar_empresa` só para a shortlist) para CNAE, situação
   cadastral, município e anos disponíveis. Tire "Baixada" e "Inapta"; separe por CNAE o
   que passou no corte só por volume (comercializadoras, tradings, holdings).
5. Sinais para a tese, com a skill indicadores-financeiros: prejuízo recorrente, PL em
   queda, liquidez apertada e alavancagem alta apontam candidato a venda ou
   reestruturação; margem alta e PL crescente apontam ativo caro. Uma frase por empresa,
   só com o que os números mostram.
6. Complete o universo com `buscar_empresas` por nomes que você conhece do setor, e diga
   que a base não cobre todo o setor. Empresa citada e não encontrada entra numa lista
   "fora da base".

## Passos para compradores

1. `analisar_empresa` do alvo: setor, UF, tamanho, alavancagem.
2. `ranking_empresas` por `ativo` e por `lucro` no setor do alvo (sem UF, depois com as
   UFs vizinhas), `limite=50`; `metrica="crescimento"` com `ativo_base` acima de
   R$ 500 milhões para achar quem está expandindo o ativo (é o sinal mais próximo de
   "aquisitiva" que a base oferece).
3. Para cada candidato, PL e liquidez corrente do último exercício (capacidade), setor e
   CNAE (encaixe), UF (região). Ordene e diga o critério.
4. Grupo econômico, controlador, apetite declarado e transações passadas são
   conhecimento seu ou do MCP do cnpj.ai (se disponível): seção própria, rotulada.

## Regras

- UF é a da sede. Usina, planta ou linha pode ficar em outro estado; se classificar por
  localização do ativo, diga que veio de conhecimento seu.
- Crescimento é de ativo total, e percentuais de milhares por cento vêm de bases
  minúsculas: filtre `ativo_base`.
- Não há filtro por faixa de receita, porte econômico, controle acionário nem paginação:
  o teto é 50 por chamada, e quem não está no top 50 por receita nem por ativo na UF não
  aparece. Diga isso.
- Coluna "último exercício" é obrigatória; dado de 2021 não sustenta tese em 2026.
- Valores em R$ mi ou bi com unidade; sem "em milhares".
- Não recomende preço, múltiplo ou "vale a pena": falta dívida líquida, EBITDA e mercado.

## Quando o dado não existe

- Ranking vazio para setor e UF: teste o outro rótulo (`references/setores.md`), depois
  rode sem `setor` e leia a coluna `setor` das linhas. Se continuar vazio, a base não
  cobre; diga e liste o que existe nas UFs vizinhas.
- Alvo sem pares no ranking: compradores vêm de setores adjacentes; diga a adjacência.
