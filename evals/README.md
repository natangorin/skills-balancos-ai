# Evals

Um arquivo por skill, com os cenários usados para testá-la. Cada cenário tem o pedido
do cliente (o prompt), o que um agente **sem** a skill fez de errado no baseline e o
comportamento esperado **com** a skill.

Como rodar: dê o prompt a um agente com o MCP do Balanços.AI conectado, primeiro sem
a skill e depois com ela, e compare com o esperado. É manual, contra a base de
produção; os números mudam a cada carga, o comportamento não deve mudar.

Cada arquivo termina com "Resultados registrados": data, cenário e o que o agente fez
com a skill na última rodada. Quando um eval revela problema do MCP ou dos dados, e
não da skill, ele é reportado ao Balanços.AI (contato@balancos.ai) e a skill ganha o
contorno enquanto o problema não é corrigido.
