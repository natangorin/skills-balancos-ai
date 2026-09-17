# Contribuindo

Obrigado por querer melhorar as skills. Este guia diz como o repositório funciona e o
que uma contribuição precisa ter para entrar.

## Antes de começar

- Tudo aqui é em **português do Brasil**: skills, referências, evals, commits, PRs e
  issues.
- As skills seguem o formato [Agent Skills](https://agentskills.io/specification):
  `skills/<nome>/SKILL.md` com frontmatter YAML, até 500 linhas, e material pesado em
  `references/`.
- As skills só citam tools que o MCP do Balanços.AI expõe e só linkam domínios da lista
  em `scripts/check.py`. O check reprova o resto.
- Não há segredo no repositório. Chave de API só existe como placeholder
  (`bal_live_...`). Configuração local fica em `.claude/settings.local.json` e
  `.mcp.local.json`, ambos ignorados pelo git.

## Reportar um problema

Use os modelos de issue:

- **Skill respondeu errado**: o agente, com a skill, fez algo que a skill diz para não
  fazer, ou não fez o que ela manda. Traga o prompt, o cliente usado, as tools chamadas
  e o que saiu.
- **Sugestão**: nova skill, novo cenário ou mudança de rotina.

Problema no MCP ou nos dados (tool com erro, valor errado, empresa faltando) não é
daqui: escreva para [contato@balancos.ai](mailto:contato@balancos.ai). Se a skill puder
contornar o problema enquanto ele não é corrigido, aí sim abra issue aqui.

## Mudar uma skill

1. Crie uma branch a partir da `main`.
2. Edite a `SKILL.md` ou as referências. Regras de escrita:
   - a `description` do frontmatter diz **quando** usar a skill, com exemplos de pedido
     entre aspas, e não contém `: ` sem aspas;
   - toda instrução tem motivo verificável no MCP (campo que existe, limite real);
   - o que a base não tem é dito, nunca inventado;
   - nome de tool sempre em crase (`analisar_empresa`), campo de resposta idem.
3. Rode `make check`. Precisa dar `0 erros`.
4. Se a mudança altera comportamento, acrescente ou ajuste um cenário em
   `evals/<skill>.md` e, se rodou contra produção, registre a data e o resultado em
   "Resultados registrados".
5. Suba a `metadata.version` da skill quando a mudança for visível para quem usa.
6. Abra o PR. O CI roda o mesmo `make check`.

## Evals

Os cenários em `evals/` são manuais: o mesmo prompt para um agente com o MCP
conectado, sem a skill e depois com ela, comparado com o esperado. Os números mudam a
cada carga da base; o comportamento não deve mudar. Detalhes em `evals/README.md`.

## Commits e PRs

- Mensagem no formato `tipo(escopo): resumo`, em pt-BR: `feat(comparar-empresas): ...`,
  `fix(check): ...`, `docs(evals): ...`.
- Um assunto por PR. PR pequeno entra mais rápido.
- Merge é sempre por merge commit, nunca squash: o histórico de cada task se preserva.

## Release

Cada mudança visível para quem usa vira uma entrada no `CHANGELOG.md` e uma tag
`vX.Y.Z`. A tag dispara o workflow de release, que roda o check, gera os zips e publica
a release no GitHub com as notas do changelog. Quem instala por zip no Claude.ai baixa
dali.

## Licença

Ao contribuir, você concorda que sua contribuição é licenciada sob a MIT deste
repositório.
