# Eval: due-diligence-financeira

## Cenário 1: fornecedor avaliando cliente

**Prompt**: "Vou fechar um contrato de fornecimento de 3 anos com a CEEE-G (geradora
de energia do RS), com pagamento a 60 dias. Faz uma due diligence financeira dela pra
mim: posso confiar que ela paga? Que risco eu corro?"

**Esperado com a skill**:
- Não dá nota, rating nem "pode confiar"; entrega evidência organizada e perguntas.
- Indicadores de liquidez e alavancagem em 3 exercícios, com tendência.
- Lê pelo menos uma publicação (`texto_documento`) atrás de parecer do auditor,
  empréstimos, contingências, partes relacionadas e eventos subsequentes; diz o que
  não achou.
- Checa situação cadastral e data da última publicação.
- Lista o que a base não tem (fluxo de caixa, dívida líquida) e o que pedir à
  contraparte.
