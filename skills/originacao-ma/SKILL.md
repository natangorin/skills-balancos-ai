---
name: originacao-ma
description: Use quando pedirem para mapear alvos de aquisição, empresas à venda em potencial, consolidação de um setor, ou possíveis compradores estratégicos para uma empresa ("quem poderia comprar a X", "mapeia alvos de energia no Sul", "empresas de saúde entre 100 mi e 1 bi de receita") com o MCP do Balanços.AI conectado.
license: MIT
compatibility: Requer o MCP do Balanços.AI conectado. Assume as skills balancos-ai e indicadores-financeiros; companhia-aberta e instituicao-financeira para alvos e compradores abertos ou financeiros.
metadata:
  author: Balanços.AI
  version: "0.4"
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
   ("Energia Elétrica"), rode o herdado por receita em cada UF; se voltar alguém, rode
   por ativo também.
   Companhias abertas do setor: `cvm_ranking_companhias` por `receita` e por `ativo` no
   último exercício, `familia="comercial"`, `visao="consolidado"`, `limite=50`, e por
   `receita` com `periodo="12m"` para o corte de receita mais atual; não há
   UF nem setor, então cruze CNAE e UF pela `ficha_empresa` e diga que o corte foi do lado
   do agente. Instituições financeiras: `bcb_ranking_instituicoes` por `ativo` e por
   `carteira` com `uf`, `tipo` ou `consolidado_bancario`, no nível padrão; é o único
   ranking além do de publicações com filtro geográfico real, e cooperativas por UF saem
   com `tipo="9"`.
3. Corte de receita do lado do agente com `receita_em_reais` e `exercicio` de cada linha.
   Descarte receita zero ou irrisória (holding, extração parcial). Exercício anterior a
   (ano atual − 3) vai para "dado defasado", nunca para a longlist principal; em 2026,
   2023 ainda entra. Ano fiscal não-calendário (`exercicio` igual ao ano corrente, data
   de referência em junho) é o mais recente da empresa; diga a data.
4. `analisar_empresa` para quem passou no corte (a tabela precisa de BP e DRE; `ficha`
   não basta), até uns 15; acima disso, `ficha_empresa` primeiro e `analisar` só na
   shortlist. Tire "Baixada" e "Inapta"; separe por CNAE o que passou no corte só por
   volume (comercializadoras, tradings, holdings). Orçamento: o mapa inteiro cabe em
   30 a 40 chamadas; passou disso, pare de ampliar o universo e feche a lista.
5. Sinais para a tese, com a skill indicadores-financeiros: prejuízo recorrente, PL em
   queda, liquidez apertada e alavancagem alta apontam candidato a venda ou
   reestruturação; margem alta e PL crescente apontam ativo caro. Uma frase por empresa,
   só com o que os números mostram.
6. Complete o universo com `buscar_empresas` por até dez nomes que você conhece do
   setor (razão social curta; nome fantasia de cooperativa costuma não casar), e diga que
   a base não cobre todo o setor. Empresa citada e não encontrada entra numa lista "fora
   da base".

## Passos para compradores

1. `analisar_empresa` do alvo: setor, UF, tamanho, alavancagem.
2. `ranking_empresas` por `ativo` e por `lucro` no setor do alvo (sem UF, depois com as
   UFs vizinhas), `limite=50`; `metrica="crescimento"` com `ativo_base` acima de
   R$ 500 milhões para achar quem está expandindo o ativo (é o sinal mais próximo de
   "aquisitiva" que a base oferece).
3. Para cada candidato, PL e liquidez corrente do último exercício (capacidade), setor e
   CNAE (encaixe), UF (região). Ordene e diga o critério.
   Comprador financeiro (banco ou cooperativa central comprando carteira, financeira ou
   cooperativa): `bcb_ranking_instituicoes` por `patrimonio` e por `basileia` na UF e nas
   vizinhas; capacidade é PL e folga de Basileia (skill instituicao-financeira). Comprador
   aberto: `cvm_ranking_companhias` por `patrimonio`, e caixa 1.01.01 mais dívida líquida
   do conta a conta como capacidade (skill companhia-aberta).
4. Grupo econômico, controlador, apetite declarado e transações passadas são
   conhecimento seu ou do MCP do cnpj.ai (se disponível): seção própria, rotulada.

## Regras

- UF é a da sede. Usina, planta ou linha pode ficar em outro estado. Mantenha na
  longlist pela sede e acrescente uma coluna "ativo físico" preenchida por conhecimento
  geral, rotulada como tal; o leitor decide se conta.
- Crescimento é de ativo total, e percentuais de milhares por cento vêm de bases
  minúsculas: filtre `ativo_base`.
- Não há filtro por faixa de receita, porte econômico, controle acionário nem paginação:
  o teto é 50 por chamada, e quem não está no top 50 por receita nem por ativo na UF não
  aparece. Diga isso.
- Alvo companhia aberta: a tese ganha EBITDA, dívida líquida e caixa operacional do conta
  a conta (skill companhia-aberta), com o código; "vale a pena" continua fora, porque
  falta valor de mercado.
- Coluna "último exercício" é obrigatória; dado de 2021 não sustenta tese em 2026.
- Valores em R$ mi ou bi com unidade; sem "em milhares".
- Não recomende preço, múltiplo ou "vale a pena": falta dívida líquida, EBITDA e mercado.

## Quando o dado não existe

- Ranking vazio para setor e UF: teste o outro rótulo (`references/setores.md`), depois
  rode sem `setor` e leia a coluna `setor` das linhas. Se continuar vazio, a base não
  cobre; diga e liste o que existe nas UFs vizinhas.
- Alvo sem pares no ranking: compradores vêm de setores adjacentes; diga a adjacência.
