# Skills do Balanços.AI

Skills para agentes de IA (Claude, ChatGPT, Codex, Cursor e outros) usarem bem o
[MCP do Balanços.AI](https://balancos.ai/mcp): rotinas prontas para investigar uma
empresa brasileira, comparar concorrentes, fazer due diligence financeira, originar
operações de M&A e ler publicações legais, sempre a partir de balanços e DREs
publicados.

O MCP entrega o dado. As skills ensinam o agente **o que fazer com ele**: em que
ordem chamar as ferramentas, como calcular indicadores com os campos que voltam, que
ressalvas declarar e o que responder quando o dado não existe.

## Skills

| Skill | Use quando |
|---|---|
| [`balancos-ai`](skills/balancos-ai/) | Base: como o MCP funciona, ferramentas, limites, vocabulário. As demais assumem esta. |
| [`indicadores-financeiros`](skills/indicadores-financeiros/) | Precisar calcular liquidez, endividamento, margens, ROE, ROA, CAGR a partir do BP e da DRE. |
| [`investigar-empresa`](skills/investigar-empresa/) | "Me conta sobre a empresa X", "o que sabemos da X". |
| [`comparar-empresas`](skills/comparar-empresas/) | "X versus Y", "compara essas cinco", "como a X fica frente aos pares". |
| [`due-diligence-financeira`](skills/due-diligence-financeira/) | Homologar fornecedor ou cliente, avaliar alvo de aquisição ou investimento. |
| [`originacao-ma`](skills/originacao-ma/) | Mapear alvos de aquisição num setor ou possíveis compradores para uma empresa. |
| [`ler-publicacao`](skills/ler-publicacao/) | Ler uma ata, notas explicativas, parecer de auditoria ou relatório da administração. |

## Instalar

### Claude Code, Codex, Cursor e outros agentes de terminal

Instala todas as skills nos agentes detectados na máquina:

```bash
npx skills add natangorin/skills-balancos-ai
```

No Claude Code também dá para instalar como plugin, que já conecta o MCP (login
OAuth na primeira chamada):

```
/plugin marketplace add natangorin/skills-balancos-ai
/plugin install balancos-ai@balancos-ai
```

Sem o plugin, conecte o MCP diretamente:

```bash
claude mcp add --transport http balancos-ai https://mcp.balancos.ai/mcp
```

Para usar uma chave de API em vez do login (criada em
[Minha conta](https://balancos.ai/conta)):

```bash
claude mcp add --transport http balancos-ai https://mcp.balancos.ai/mcp \
  --header "Authorization: Bearer bal_live_..."
```

### Claude.ai e Claude Desktop

1. Conecte o MCP em Configurações › Conectores › Adicionar conector personalizado,
   com a URL `https://mcp.balancos.ai/mcp`, e faça o login.
2. Gere os arquivos das skills com `make zips` (ou baixe da página de releases) e
   suba cada `dist/<skill>.zip` em Configurações › Capacidades › Skills.

Cada skill funciona sozinha. Suba só as que fizer sentido para o seu uso; a
`balancos-ai` é a única que vale a pena ter sempre.

### Outros clientes MCP

Qualquer cliente que aceite servidores MCP remotos por HTTP conecta em
`https://mcp.balancos.ai/mcp`. O conteúdo das skills é Markdown: cole a
`SKILL.md` que precisar nas instruções do seu agente.

## O que as skills não fazem

- Não substituem o MCP: sem ele conectado, o agente não tem dado.
- Não inventam o que a base não tem. Fluxo de caixa, EBITDA, dívida líquida e
  cobertura de juros não vêm em campo estruturado; as skills ensinam a buscar isso
  no texto das publicações e a declarar quando não encontrou.
- Não emitem nota de crédito, rating ou recomendação de investimento. Entregam
  evidência organizada e perguntas a fazer.

## Atualizações

Nenhum caminho atualiza sozinho por padrão. Para pegar a versão mais nova das skills:

| Instalou por | Como atualizar |
|---|---|
| `npx skills add` | `npx skills update` (todas) ou `npx skills update balancos-ai` (uma). A instalação padrão é por symlink para uma cópia canônica, então o comando atualiza todos os agentes de uma vez. |
| Plugin do Claude Code | `/plugin` › Marketplaces › `balancos-ai` › Update, ou `claude plugin marketplace update balancos-ai` seguido de `/plugin` › Update. No mesmo menu dá para ligar a atualização automática desse marketplace (desligada por padrão para marketplaces de terceiros); com ela ligada, o Claude Code puxa cada novo commit em segundo plano ao iniciar. |
| Zip no Claude.ai | Baixar o zip novo e subir de novo em Configurações › Capacidades › Skills, substituindo o anterior. |

Cada mudança relevante vira uma release no GitHub com o que mudou por skill; siga o repositório
para receber aviso.

## Limitações conhecidas

As skills são escritas em cima do que o MCP entrega hoje, e dizem isso ao usuário:

- Balanço com 8 linhas e DRE com 6, sempre da entidade individual (sem consolidado).
- Texto de publicação limitado aos primeiros 50 mil caracteres; parecer do auditor e
  notas explicativas costumam ficar fora, e a skill aponta o link do documento.
- Ranking com até 50 empresas por chamada, sem filtro por faixa de receita.
- Rótulo de setor por seção CNAE, com alguns rótulos herdados.

Quando o MCP ganhar essas capacidades, as skills mudam junto.

## Desenvolvimento

```bash
make check   # valida frontmatter, tamanho, tools citadas e links
make zips    # gera dist/<skill>.zip
```

Formato: [Agent Skills](https://agentskills.io/specification). Cada skill fica em
`skills/<nome>/SKILL.md`, com material pesado em `references/`. Os cenários de
teste de cada skill estão em `evals/<nome>.md`.

## Licença

MIT. Dados servidos pelo MCP seguem os [termos do Balanços.AI](https://balancos.ai/termos).
