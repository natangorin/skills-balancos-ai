# Política de segurança

Este repositório contém só Markdown (skills, referências e cenários de teste) e um
script de validação. Não executa código no seu ambiente nem guarda credenciais. Os
riscos reais estão em outro lugar:

- **O MCP do Balanços.AI** (`mcp.balancos.ai`): problema no serviço, na autenticação
  OAuth, nas chaves de API ou nos dados servidos.
- **Instruções nas skills** que levem o agente a expor dados do usuário, a chamar
  endereços fora do balancos.ai ou a agir fora do pedido.

## Como reportar

Escreva para [contato@balancos.ai](mailto:contato@balancos.ai) com o assunto
"segurança". Não abra issue pública para vulnerabilidade. Resposta em até 5 dias úteis.

Descreva o que encontrou, como reproduzir e o impacto que enxerga. Se envolver o MCP,
inclua a tool e os parâmetros usados, sem a sua chave de API.

## Escopo

Versões suportadas: a última release e a `main`. Skills antigas instaladas por zip não
recebem correção retroativa; atualize pelo caminho descrito no README.
