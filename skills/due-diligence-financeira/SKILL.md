---
name: due-diligence-financeira
description: Use quando pedirem para avaliar o risco financeiro de uma empresa brasileira como contraparte, com o MCP do Balanços.AI conectado. Cobre homologar fornecedor, vender a prazo para um cliente, analisar alvo de aquisição ou de investimento, "posso confiar que paga", "que risco eu corro", "vale a pena comprar".
license: MIT
compatibility: Requer o MCP do Balanços.AI conectado. Assume as skills balancos-ai, indicadores-financeiros e ler-publicacao; companhia-aberta e instituicao-financeira quando a contraparte está na CVM ou no BCB.
metadata:
  author: Balanços.AI
  version: "0.4"
---

# Due diligence financeira

## Resultado

Um relatório de evidências, não um parecer. Seções fixas, nesta ordem:

1. **Contraparte**: razão social, CNPJ, situação cadastral, natureza, homônimos
   descartados, link.
2. **Base da análise**: exercícios usados, fonte, individual ou consolidado, data dos
   dados, o que foi lido em texto.
3. **O que os números mostram**: tabela de 3 a 5 exercícios (liquidez corrente, capital
   de giro, alavancagem, composição do endividamento, margens, ROE, variação de receita e
   lucro; em companhia aberta, também dívida bruta, dívida líquida, caixa operacional e
   juros pagos, com o código da conta; em banco, os indicadores da skill
   instituicao-financeira) e uma leitura por bloco em linguagem de fato: "o passivo de curto prazo cobre
   4,7 vezes o circulante" e não "risco baixo".
4. **Sinais que exigem leitura da nota**: reclassificação de dívida entre circulante e
   não circulante, prejuízo recorrente, PL em queda, margem operacional acima da bruta,
   ausência de publicação recente, reapresentação de DFP ou ITR (linha do tempo de
   entregas da CVM, com data e se o parecer mudou), trimestres que não fecham com o
   acumulado na fonte (`consistente: false` na série da CVM). Um item por linha, com o
   número que o originou.
5. **O que o parecer e o texto dizem**: em companhia aberta, o parecer vem estruturado de
   `cvm_parecer` da DFP (tipo, ênfase e continuidade lidas no texto, firma, data, e se a
   firma mudou entre exercícios), e a revisão do ITR mais recente diz se surgiu ênfase
   depois; nas demais, parecer do auditor no texto da publicação (opinião, ênfase,
   ressalva); empréstimos e vencimentos, contingências, partes relacionadas, eventos
   subsequentes, continuidade operacional. Citação curta e link. Item não encontrado no
   texto disponível fica marcado "não localizado no trecho disponível", com o link.
6. **O que a base não tem** para esta decisão: fluxo de caixa, dívida líquida, caixa,
   prazo médio de pagamento, protestos, rating, quadro societário, dado intra-ano (exceto
   banco e companhia aberta: o IF.data e o ITR têm o trimestre mais recente, e ele entra
   na seção 3 com a data de referência). Se o dado mais recente tem mais de seis meses,
   diga quantos e inclua na seção 7 o pedido de balancete recente.
7. **Perguntas à contraparte** derivadas dos itens 4, 5 e 6: uma pergunta por lacuna.
8. **Modo** (fornecedor e cliente, aquisição, investimento) ajusta o foco, ver abaixo.

Sem nota, sem semáforo, sem "risco baixo/médio/alto", sem probabilidade de pagamento, sem
"pode confiar". A decisão e a estrutura de garantias são do leitor; a skill entrega o que
os números e o texto mostram e o que falta perguntar.

Pergunta direta cujo dado não existe ("quanto de dívida ela tem?") ganha resposta direta
na seção 6: o que a base tem que se aproxima (passivo exigível, como teto, não estimativa),
o que o texto diz, e o que falta. Não a deixe implícita entre as seções.

## Passos

1. `buscar_empresas`; confirme a contraparte pelo CNPJ e liste homônimos.
2. `analisar_empresa`, e depois o roteamento da skill balancos-ai: companhia aberta,
   `cvm_analisar_companhia` e o conta a conta de BPP, DRE e DFC do último exercício; se
   `trimestral.mais_recente` é posterior, a seção 3 ganha uma coluna com o BP do ITR e os
   resultados de doze meses, e a dívida sai do BPP desse ITR (skill companhia-aberta);
   banco, `bcb_analisar_instituicao` (skill instituicao-financeira). Classifique a
   natureza do dado e monte a série com a skill indicadores-financeiros, excluindo
   anomalias com nota.
3. Marque os sinais da seção 4 comparando exercícios.
4. Em companhia aberta, `cvm_parecer` da última DFP e da anterior, e do ITR mais recente
   quando é posterior, antes de qualquer texto. Depois, leia texto: no índice de
   documentos, escolha a publicação mais recente com texto (jornal antes de DFP) e siga a
   skill ler-publicacao, com o roteiro em
   [references/roteiro-notas.md](references/roteiro-notas.md): um `termo` por assunto do
   roteiro em `texto_documento`, depois o entorno com `inicio` quando o trecho não basta.
   Se o texto vier gravado em arquivo, leia o arquivo inteiro. Item ausente só depois de
   dois termos do assunto sem ocorrência. A publicação do ano anterior serve para item
   que este ano só menciona (garantia da controladora, covenant), e aí você diz de que
   ano é.
5. Escreva as seções 6 e 7 a partir do que ficou em aberto.
6. Escreva o relatório.

## Modos

- **Fornecedor e cliente** (vender a prazo, homologar): foco em liquidez corrente,
  capital de giro, composição do endividamento, tendência de receita, publicação recente.
  Uma linha sobre a proporção do contrato diante da receita anual, sem recomendar
  garantia.
- **Alvo de aquisição**: foco em qualidade do lucro (não recorrentes, equivalência),
  tendência de margem, alavancagem, contingências, partes relacionadas, reapresentações,
  ressalvas do auditor. A seção 7 vira a lista de pedidos para o data room.
- **Investimento minoritário**: foco em ROE, consistência de lucro, PL, distribuição
  (atas de AGO no índice), continuidade operacional.

## Regras

- Causa de uma variação só com trecho do texto. Sem texto: "reclassificação de R$ X do
  não circulante para o circulante em 2023; causa não localizada no trecho disponível".
- Controlador, grupo, notícia, privatização, leilão: se está no texto da publicação
  (nota 1, relatório da administração), cite "segundo a publicação"; se não, é
  conhecimento seu, rotulado, ou fica fora.
- Linhas da DRE, DFC e DVA publicadas são texto citável (resultado financeiro, caixa
  gerado, pagamentos de juros). Dívida bruta menos caixa, os dois citados, pode ser
  apresentada como "dívida líquida aproximada, segundo a publicação".
- Passivo exigível não é dívida financeira; escreva "exigível".
- Não converta indicador em veredito por nenhuma escala própria.
- Não redija cláusulas contratuais.

## Quando o dado não existe

Empresa sem BP ou DRE: entregue as seções 1, 2, 5, 6 e 7 a partir das publicações, e diga
que não há demonstrativo extraído. Empresa fora da base: diga e sugira acompanhar em
https://balancos.ai.
