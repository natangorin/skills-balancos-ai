# Evals

Um arquivo por skill, com os cenários usados para testá-la. Cada cenário tem o pedido
do cliente (o prompt), o que um agente **sem** a skill fez de errado no baseline e o
comportamento esperado **com** a skill.

Como rodar: dê o prompt a um agente com o MCP do Balanços.AI conectado, primeiro sem
a skill e depois com ela, e compare com o esperado. É manual, contra a base de
produção; os números mudam a cada carga, o comportamento não deve mudar.

## Achados sobre a base (2026-09-17)

Problemas do MCP ou dos dados que os evals revelaram e que as skills não resolvem:

- `buscar_empresas("Banrisul")` devolve só subsidiárias e fundos; o banco só aparece
  por trecho do nome oficial. Nome fantasia não indexado.
- Link de empresa com slug errado: Sicredi Dexis (CNPJ 79.342.069) aponta para
  `edital-de-leilao-extrajudicial-de-imovel-alienacao-fiduciaria`; Schulz S.A. (CNPJ
  84.693.183) aponta para `064-21-diario-oficial-do-estado-de-santa-catarina-...`.
- Gerdau Aços Longos (CNPJ 07.358.761): todas as DREs de 2015 a 2025 com
  `escala_publicada: "unidade"` e valores mil vezes menores que o BP; `ativo_circulante`,
  `ativo_nao_circulante` e `passivo_total` nulos em 2025.
- Tupy S.A. aparece sob dois CNPJs (matriz SP rotulada "Comércio", CNAE 46.85-1; filial
  SC rotulada "Indústrias de Transformação") com os mesmos valores.
- Nas reapresentações da CVM, a v1 costuma vir sem demonstrações (`visoes: []`), o que
  impede comparar versões conta a conta.
- `bcb_ranking_instituicoes` com `nivel="padrao"` rotula cooperativas e independentes
  como `prudencial` com `cnpj` e `empresa` nulos, e `bcb_conglomerado` devolve zero
  membros para elas.
- O CodInst do conglomerado (em `niveis[]` e `conglomerados`) não é aceito como `chave`
  em nenhuma tool `bcb_*`.
- Cooperativa dos empregados do Banrisul: `tvm` em 202606 vem como R$ 10.750 contra
  R$ 10,0 mi no trimestre anterior; Basileia errática entre 200812 e 201012.
