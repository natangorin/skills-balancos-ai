# Evals

Um arquivo por skill, com os cenários usados para testá-la. Cada cenário tem o pedido
do cliente (o prompt), o que um agente **sem** a skill fez de errado no baseline e o
comportamento esperado **com** a skill.

Como rodar: dê o prompt a um agente com o MCP do Balanços.AI conectado, primeiro sem
a skill e depois com ela, e compare com o esperado. É manual, contra a base de
produção; os números mudam a cada carga, o comportamento não deve mudar.
