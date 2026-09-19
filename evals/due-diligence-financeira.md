# Eval: due-diligence-financeira

## Cenário 1: fornecedor avaliando cliente

**Prompt**: "Vou fechar um contrato de fornecimento de 3 anos com a CEEE-G (geradora
de energia do RS), com pagamento a 60 dias. Faz uma due diligence financeira dela pra
mim: posso confiar que ela paga? Que risco eu corro?"

**Baseline (sem skill)**: deu veredito e nota ("risco médio-baixo", "pode confiar, sim,
com alta probabilidade"), atribuiu causa à reclassificação de dívida (covenant,
vencimento) sem ler a nota, afirmou o controlador (CSN) por conhecimento prévio, e
dedicou metade da resposta a cláusulas contratuais.

**Esperado com a skill**:
- Não dá nota, rating nem "pode confiar"; entrega evidência organizada e perguntas.
- Indicadores de liquidez e alavancagem em 3 exercícios, com tendência.
- Lê pelo menos uma publicação (`texto_documento`) atrás de parecer do auditor,
  empréstimos, contingências, partes relacionadas e eventos subsequentes; diz o que
  não achou.
- Checa situação cadastral e data da última publicação.
- Lista o que a base não tem (fluxo de caixa, dívida líquida) e o que pedir à
  contraparte.

## Cenário novo: contraparte aberta

**Prompt**: "Vou vender a prazo para a Gerdau S.A.; que risco eu corro?"

**Esperado**: seção 5 abre com `cvm_parecer` da DFP (tipo, firma, data, ênfase) e diz
se a revisão do ITR mais recente trouxe algo novo; seção 3 com dívida bruta, caixa e
caixa operacional com código, e uma coluna com o BP do ITR e os resultados de doze meses; seção 4 lista as reapresentações
da linha do tempo; nada de nota ou semáforo.

## Cenário novo: contraparte banco

**Prompt**: "Vou deixar um depósito grande no <banco médio>; como ele está?"

**Esperado**: indicadores da skill instituicao-financeira, trimestre mais recente na
seção 3 (sem pedir balancete), Basileia com mínimo rotulado; sem "pode confiar".

## Resultados registrados

- 2026-09-17, cenário "contraparte aberta" (Gerdau S.A.), com skill: passou. Parecer
  estruturado de dois exercícios antes do texto, conta a conta com código na seção 3,
  reapresentações na seção 4, texto de dois anos lido inteiro, oito perguntas, sem nota
  nem semáforo.
- 2026-09-17, cenário "contraparte banco" (Banco Daycoval), com skill: passou. Capital
  regulatório, funding por instrumento, carteira e inadimplência pelos relatórios,
  trimestre mais recente na seção 3; tropeçou no CodInst do conglomerado como chave, agora corrigido na skill
  instituicao-financeira.
