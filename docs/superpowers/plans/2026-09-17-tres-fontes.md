# Skills sobre três fontes: plano de implementação

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Fazer as skills do Balanços.AI usarem as famílias `cvm_*` e `bcb_*` do MCP: a base vira mapa e roteador, entram as skills `companhia-aberta` e `instituicao-financeira`, e as seis existentes ganham desvios.

**Architecture:** Skills são arquivos Markdown em `skills/<nome>/SKILL.md` com frontmatter YAML e material pesado em `references/`. O único teste automatizado é `python3 scripts/check.py` (`make check`), que valida frontmatter, tamanho, tools citadas em crase e links. Evals são cenários manuais em `evals/<nome>.md`. Cada task termina com `make check` verde e um commit.

**Tech Stack:** Markdown (formato Agent Skills), Python 3 (`scripts/check.py`), git.

**Spec:** `docs/superpowers/specs/2026-09-17-tres-fontes-design.md`

## Global Constraints

- Tudo em português do Brasil: conteúdo das skills, commits, docs.
- `SKILL.md` com no máximo 500 linhas; `description` com no máximo 1024 caracteres e sem `: ` (dois-pontos seguido de espaço) fora de aspas.
- `name` igual ao nome da pasta, só `[a-z0-9-]`.
- Toda tool citada em crase precisa existir na lista `TOOLS_DO_MCP` de `scripts/check.py` (Task 1 a atualiza).
- Links só para domínios permitidos em `check.py` (`balancos.ai`, `mcp.balancos.ai`, `api.balancos.ai`, `github.com`, `agentskills.io`, `code.claude.com`, `claude.ai`, `support.claude.com`, `modelcontextprotocol.io`, `registry.modelcontextprotocol.io`). O IF.data (`www3.bcb.gov.br`) e a CVM (`rad.cvm.gov.br`) **não** estão na lista: nas skills, cite "link do IF.data" e "link na CVM" como campos da resposta (`link_ifdata`, `link_cvm`), nunca a URL.
- Referências a arquivos em `references/` só na forma `(references/arquivo.md)` e o arquivo precisa existir.
- `metadata.version` das skills tocadas sobe para `"0.2"`.
- Valores sempre em reais; nunca escrever "em milhares".
- Um commit por task, mensagem em português, terminando com `Co-Authored-By: Claude Fable 5.1 <noreply@anthropic.com>`.
- Nunca squash merge.

---

## Mapa de arquivos

| Arquivo | Task | Responsabilidade |
|---|---|---|
| `scripts/check.py` | 1 | reconhecer as 29 tools |
| `skills/balancos-ai/SKILL.md` | 2 | três fontes, roteamento, tabela das 21 tools, "o que não tem" por fonte |
| `skills/companhia-aberta/SKILL.md` | 3 | fluxo CVM, visão, família, versões, parecer, ranking, indicadores com código |
| `skills/companhia-aberta/references/payloads.md` | 3 | campos das tools `cvm_*` |
| `skills/companhia-aberta/references/contas-dfp.md` | 3 | mapa de códigos padronizados |
| `skills/instituicao-financeira/SKILL.md` | 4 | fluxo BCB, níveis, tempo, índices, indicadores próprios, relatórios |
| `skills/instituicao-financeira/references/payloads.md` | 4 | campos das tools `bcb_*` |
| `skills/instituicao-financeira/references/relatorios-ifdata.md` | 4 | ids de relatórios, códigos TI e TCB |
| `skills/indicadores-financeiros/SKILL.md` | 5 | coluna "Na CVM" e ressalva para bancos |
| `skills/investigar-empresa/SKILL.md` e `references/modelo-memo.md` | 6 | roteamento, variantes de memo |
| `skills/comparar-empresas/SKILL.md` | 7 | mesma fonte/família/visão, pares por ranking novo |
| `skills/due-diligence-financeira/SKILL.md` e `references/roteiro-notas.md` | 8 | parecer estruturado, DFC, banco |
| `skills/originacao-ma/SKILL.md` | 9 | rankings CVM e BCB |
| `skills/ler-publicacao/SKILL.md` | 10 | parecer e conta a conta pela CVM |
| `README.md`, `.claude-plugin/plugin.json`, `evals/*.md` | 11 | docs, plugin, evals |

---

### Task 1: `check.py` reconhece as 29 tools

**Files:**
- Modify: `scripts/check.py:22-31` (`TOOLS_DO_MCP`) e `scripts/check.py:45-48` (`RE_TOOL`)

**Interfaces:**
- Produces: `TOOLS_DO_MCP` com 29 nomes; `RE_TOOL` casando `cvm_*` e `bcb_*`. As tasks 2 a 10 dependem disso para passar no `make check`.

- [ ] **Step 1: Criar uma skill temporária que cita uma tool nova válida e uma inválida**

```bash
mkdir -p skills/zz-teste
cat > skills/zz-teste/SKILL.md <<'EOF'
---
name: zz-teste
description: Skill temporária para testar o checker.
---

Cita `cvm_analisar_companhia` (existe) e `cvm_inexistente` (não existe).
EOF
```

- [ ] **Step 2: Rodar o checker e confirmar que ele NÃO pega o erro (comportamento atual)**

Run: `python3 scripts/check.py; echo "exit=$?"`
Expected: linha `ok  zz-teste` e `exit=0`. O regex atual ignora nomes com prefixo `cvm_`, então `cvm_inexistente` passa. Esse é o buraco.

- [ ] **Step 3: Atualizar `TOOLS_DO_MCP` e `RE_TOOL`**

Substituir o bloco `TOOLS_DO_MCP = {...}` por:

```python
TOOLS_DO_MCP = {
    # publicações
    "buscar_empresas",
    "ficha_empresa",
    "balancos_empresa",
    "dres_empresa",
    "documentos_empresa",
    "texto_documento",
    "ranking_empresas",
    "analisar_empresa",
    # CVM (companhias abertas, DFP)
    "cvm_buscar_companhias",
    "cvm_ficha_companhia",
    "cvm_analisar_companhia",
    "cvm_dfps_companhia",
    "cvm_entrega_dfp",
    "cvm_balancos_companhia",
    "cvm_dres_companhia",
    "cvm_demonstracoes_dfp",
    "cvm_parecer_dfp",
    "cvm_ranking_companhias",
    # BCB (instituições financeiras, IF.data)
    "bcb_buscar_instituicoes",
    "bcb_ficha_instituicao",
    "bcb_analisar_instituicao",
    "bcb_trimestres_instituicao",
    "bcb_resultados_instituicao",
    "bcb_relatorios_instituicao",
    "bcb_estrutura_relatorios",
    "bcb_conglomerado",
    "bcb_ranking_instituicoes",
    "bcb_data_bases",
}
```

Substituir `RE_TOOL = re.compile(...)` por:

```python
RE_TOOL = re.compile(
    r"`((?:cvm|bcb)_[a-z_]+|"
    r"(?:buscar|ficha|balancos|dres|documentos|texto|ranking|analisar|listar|comparar|"
    r"pares|novidades|contar|filtrar|empresas|setores)_[a-z_]+)(?:\([^)]*\))?`"
)
```

Atualizar a docstring do topo: a linha "nome com cara de tool citado em crase (`buscar_x`, `ranking_y`...) que não existe no MCP" vira "nome com cara de tool citado em crase (`buscar_x`, `cvm_x`, `bcb_x`...) que não existe no MCP".

- [ ] **Step 4: Rodar o checker e confirmar que agora pega só a inválida**

Run: `python3 scripts/check.py; echo "exit=$?"`
Expected: `ERRO zz-teste`, uma linha `  - zz-teste/SKILL.md: tool `cvm_inexistente` não existe no MCP`, nenhuma linha sobre `cvm_analisar_companhia`, `exit=1`.

- [ ] **Step 5: Remover a skill temporária e confirmar verde**

Run: `rm -rf skills/zz-teste && python3 scripts/check.py; echo "exit=$?"`
Expected: `7 skills, 0 erros`, `exit=0`.

- [ ] **Step 6: Commit**

```bash
git add scripts/check.py
git commit -m "chore(check): reconhece as 29 tools do MCP (cvm_* e bcb_*)

Co-Authored-By: Claude Fable 5.1 <noreply@anthropic.com>"
```

---

### Task 2: skill `balancos-ai` vira mapa e roteador

**Files:**
- Modify: `skills/balancos-ai/SKILL.md`

**Interfaces:**
- Consumes: Task 1 (tools novas passam no checker).
- Produces: seções "Três fontes" e "Roteamento" que as skills `companhia-aberta` e `instituicao-financeira` (Tasks 3 e 4) e os desvios (Tasks 5 a 10) citam pelo nome "skill balancos-ai".

- [ ] **Step 1: Subir a versão**

Em `metadata:`, trocar `version: "0.1"` por `version: "0.2"`.

- [ ] **Step 2: Ajustar os "três fatos" para dizer que valem para a fonte publicações**

Trocar:

```
Três fatos que mudam toda leitura:

- **Um exercício por ano, sempre o individual.** Para cada ano fiscal a base escolhe um
  período vencedor. Não há versão consolidada. Holding e controladora mostram a receita e
  a dívida da própria entidade, não do grupo.
```

por:

```
Três fatos que mudam toda leitura da fonte publicações (as outras duas fontes, abaixo,
não têm essas limitações):

- **Um exercício por ano, sempre o individual.** Para cada ano fiscal a base escolhe um
  período vencedor. Não há versão consolidada nesta fonte. Holding e controladora mostram
  a receita e a dívida da própria entidade, não do grupo. Se a companhia é aberta, o
  consolidado está na fonte CVM.
```

E trocar:

```
- **BP tem 8 linhas e DRE tem 6.** Não há caixa, empréstimos, estoques, depreciação,
  resultado financeiro nem fluxo de caixa em campo estruturado.
```

por:

```
- **BP tem 8 linhas e DRE tem 6.** Não há caixa, empréstimos, estoques, depreciação,
  resultado financeiro nem fluxo de caixa em campo estruturado nesta fonte. Na CVM o
  conta a conta existe; no BCB existe carteira, captações e Basileia.
```

- [ ] **Step 3: Inserir a seção "Três fontes e roteamento" antes de "## Fluxo padrão"**

Inserir este bloco logo acima da linha `## Fluxo padrão`:

```
## Três fontes e roteamento

O MCP reúne três fontes com famílias de tools próprias. Todas aceitam CNPJ como chave.

| Fonte | Quem está | O que traz | Comece por |
|---|---|---|---|
| Publicações (`buscar_empresas`, `analisar_empresa`...) | qualquer empresa com publicação legal | BP de 8 linhas, DRE de 6, individual, um exercício por ano, texto das publicações, ranking por UF e setor | `buscar_empresas` |
| CVM (`cvm_*`) | companhias abertas com DFP, exercícios de 2010 em diante | consolidado e individual, conta a conta (BPA, BPP, DRE, DRA, DFC, DMPL, DVA), parecer do auditor, versões e reapresentações, ranking por exercício e família | `cvm_analisar_companhia` |
| BCB (`bcb_*`) | instituições financeiras do IF.data, desde 2000 | série trimestral, níveis individual, financeiro e prudencial, carteira de crédito, captações, Basileia, DRE derivada, relatórios conta a conta, conglomerados, ranking por data-base, UF e tipo | `bcb_analisar_instituicao` |

Roteamento, sempre nesta ordem:

1. `buscar_empresas` primeiro. É a maior cobertura e devolve CNPJ e slug.
2. Ficha com `natureza_juridica` "Sociedade Anônima Aberta", ou índice com publicações do
   tipo "Demonstrações Financeiras Padronizadas": `cvm_buscar_companhias` com o CNPJ.
   Achou, os números vêm da CVM; siga a skill companhia-aberta.
3. CNAE de instituição financeira (64.21 a 64.24 bancos, caixas e cooperativas de
   crédito; 64.3x bancos de investimento, fomento e financeiras; 64.40 arrendamento;
   66.12 corretoras; holdings 64.6x **não** são) ou `familia: "financeira"` na CVM:
   `bcb_buscar_instituicoes` com a raiz do CNPJ (8 dígitos). Achou, os números de banco
   vêm do BCB; siga a skill instituicao-financeira.
4. Publicações continuam valendo para texto de notas e relatório da administração, e para
   quem não está nas outras duas.

A ficha de publicações **não** diz se a empresa está na CVM ou no BCB; a regra acima é o
único caminho. Uma empresa pode estar nas três (um banco listado). Precedência por
pergunta: carteira, captações, Basileia e dado trimestral no BCB; parecer, DFC, DVA e conta
a conta na CVM; notas explicativas e relatório da administração no texto da publicação. A
resposta diz a fonte de cada número. Cada fonte tem o próprio `dados_atualizados_em`.
```

- [ ] **Step 4: Renomear a tabela de tools e acrescentar a das 21 novas**

Trocar o título `## As oito tools` por `## As oito tools de publicações`.

Logo depois do parágrafo que termina em `[references/payloads.md](references/payloads.md).`, inserir:

```
## As 21 tools de CVM e BCB

Detalhes, campos e regras nas skills companhia-aberta e instituicao-financeira.

| Tool | Quando |
|---|---|
| `cvm_buscar_companhias(termo)` | achar CNPJ, código CVM e slug de companhia aberta |
| `cvm_ficha_companhia(chave)` | denominações, família, exercícios, entregas, último parecer, capital |
| `cvm_analisar_companhia(chave)` | retrato: ficha, linha do tempo de entregas, BPs e DREs consolidado e individual |
| `cvm_dfps_companhia(chave, ano?)` | entregas por exercício e versão, com `id_doc` |
| `cvm_entrega_dfp(id_doc)` | visões e demonstrações que a entrega tem |
| `cvm_balancos_companhia(chave, ano?, visao?)` | só os BPs |
| `cvm_dres_companhia(chave, ano?, visao?)` | só as DREs |
| `cvm_demonstracoes_dfp(id_doc, demonstracao?, visao?)` | conta a conta de uma demonstração |
| `cvm_parecer_dfp(id_doc)` | tipo e texto do parecer, declarações dos diretores |
| `cvm_ranking_companhias(metrica, ano, visao?, familia?, limite?)` | maiores companhias abertas num exercício |
| `bcb_buscar_instituicoes(termo?, uf?, tipo?, consolidado_bancario?)` | achar CodInst e CNPJ de instituição |
| `bcb_ficha_instituicao(chave)` | cadastro, níveis, resumo da última data-base |
| `bcb_analisar_instituicao(chave)` | retrato: ficha, série trimestral, DRE anual derivada |
| `bcb_trimestres_instituicao(chave, nivel?, desde?, ate?)` | série trimestral por nível e janela |
| `bcb_resultados_instituicao(chave, nivel?, periodo?)` | DRE derivada por trimestre e ano |
| `bcb_relatorios_instituicao(chave, nivel?, data_base?, relatorio?)` | conta a conta de um relatório |
| `bcb_estrutura_relatorios(data_base, relatorio?)` | dicionário dos relatórios de uma data-base |
| `bcb_conglomerado(codinst, nivel?)` | membros de um conglomerado, com links |
| `bcb_ranking_instituicoes(metrica, data_base?, nivel?, uf?, tipo?, consolidado_bancario?, limite?)` | maiores instituições numa data-base |
| `bcb_data_bases()` | data-bases disponíveis e era contábil |
```

- [ ] **Step 5: Remeter holding e controladora ao consolidado da CVM**

No item `**`consolidado`**` da seção "Como ler o dado", trocar o final `Diga isso em
vez de concluir "receita despencou" ou "margem de 90%".` por `Diga isso em vez de
concluir "receita despencou" ou "margem de 90%". Se a companhia é aberta, o consolidado
está na CVM: use-o (skill companhia-aberta) em vez de explicar a holding.`

No item `**Controladora com CNAE industrial** (Gerdau S.A.)`, acrescentar no fim:
`Gerdau S.A. é companhia aberta: na CVM o consolidado de 2025 tem receita de R$ 69,9 bi,
e é ele que responde "que tamanho tem".`

- [ ] **Step 6: Reescrever "O que a base não tem"**

Substituir a seção inteira `## O que a base não tem` (até antes de `## Ao apresentar`) por:

```
## O que cada fonte não tem

Ausente só na fonte publicações, mas presente na CVM (companhias abertas) ou no BCB
(instituições financeiras): consolidado, DFC, caixa, empréstimos, depreciação, resultado
financeiro, EBITDA, dívida líquida, cobertura de juros, parecer do auditor estruturado,
reapresentações explícitas, dado trimestral (só bancos), carteira de crédito e Basileia
(só bancos). Quando pedirem um desses para uma empresa que não está na CVM nem no BCB,
responda o que existe, diga que não existe nesta fonte, leia o texto da publicação quando
ele tiver o número (proveniência 2) e aponte o link. Não estime.

Ausente em todas as fontes: ITR trimestral de companhia aberta, valor de mercado, quadro
societário e controlador, notas explicativas estruturadas, protestos, rating, paginação,
filtro por faixa de receita, contagem de empresas por setor.

"Quantas empresas do setor X": não há contagem. O mais perto é `ranking_empresas` com
`limite=50` nas quatro métricas; se voltar menos de 50, esse é o total com balanço
carregado, e diga que é só isso. Para bancos, `bcb_ranking_instituicoes` com `uf` e
`tipo` chega mais perto de uma contagem por região.
```

- [ ] **Step 7: Acrescentar três erros comuns**

Acrescentar ao fim da tabela `## Erros comuns`:

```
| Explicar a Gerdau como holding quando ela está na CVM | Usar o consolidado da CVM |
| Aplicar liquidez corrente e margem bruta a banco | Skill instituicao-financeira |
| Buscar banco pelo nome fantasia no BCB ("Banrisul") | Raiz do CNPJ; o nome oficial é outro e fundos poluem a busca |
```

- [ ] **Step 8: Rodar o checker e conferir tamanho**

Run: `python3 scripts/check.py && wc -l skills/balancos-ai/SKILL.md`
Expected: `7 skills, 0 erros`; menos de 260 linhas.

- [ ] **Step 9: Commit**

```bash
git add skills/balancos-ai/SKILL.md
git commit -m "feat(balancos-ai): três fontes, roteamento por CNPJ e tabela das 21 tools novas

Co-Authored-By: Claude Fable 5.1 <noreply@anthropic.com>"
```

---

### Task 3: skill `companhia-aberta`

**Files:**
- Create: `skills/companhia-aberta/SKILL.md`
- Create: `skills/companhia-aberta/references/payloads.md`
- Create: `skills/companhia-aberta/references/contas-dfp.md`

**Interfaces:**
- Consumes: Task 1 (checker), Task 2 (seção "Três fontes e roteamento" da base).
- Produces: a skill que as Tasks 5 a 10 citam como "skill companhia-aberta"; a tabela "Indicadores com o conta a conta" com os códigos que a Task 5 copia na coluna "Na CVM".

- [ ] **Step 1: Criar `skills/companhia-aberta/SKILL.md`**

```markdown
---
name: companhia-aberta
description: Use quando a empresa for companhia aberta (S.A. com DFP na CVM) e o pedido envolver consolidado, conta a conta, DFC, DVA, EBITDA, dívida líquida, cobertura de juros, parecer do auditor, reapresentação ou ranking de companhias abertas, com o MCP do Balanços.AI conectado. Assume a skill balancos-ai.
license: MIT
compatibility: Requer o MCP do Balanços.AI conectado. Assume as skills balancos-ai e indicadores-financeiros.
metadata:
  author: Balanços.AI
  version: "0.2"
---

# Companhia aberta pela CVM

## Resultado

O mesmo tipo de entrega da skill que chamou (memo, tabela, relatório), com **visão**
(consolidado ou individual), **versão** e `id_doc` da entrega declarados em cada número, e
o código da conta ao lado de cada indicador derivado do conta a conta.

## Fluxo

1. `cvm_buscar_companhias(termo)`: trecho da denominação ou CNPJ. Até 20, com `cnpj`,
   `cd_cvm`, `denominacao` e `empresa` (slug e link do balancos.ai, quando está lá).
   Vindo da skill balancos-ai, use o CNPJ da ficha de publicações.
2. `cvm_analisar_companhia(chave)`, chave = CNPJ ou código CVM. Uma chamada traz a ficha
   (denominações anteriores, `familia`, primeiro e último exercício, número de entregas e
   de reapresentações, último parecer, capital social com ações em tesouraria), a linha do
   tempo `exercicios[]` com `versoes[]` (`id_doc`, versão, `reapresentacao`, data,
   parecer, links) e `balancos[]` e `dres[]` por exercício e `visao`, na última versão de
   cada exercício. Só use `cvm_ficha_companhia`, `cvm_dfps_companhia`,
   `cvm_balancos_companhia` e `cvm_dres_companhia` para uma parte.
3. `cvm_entrega_dfp(id_doc)` quando precisar saber quais visões e demonstrações a entrega
   tem (`visoes`, `demonstracoes_disponiveis`) antes de pedir o conta a conta.
4. `cvm_demonstracoes_dfp(id_doc, demonstracao, visao)`: **uma demonstração por chamada**
   (`bpa`, `bpp`, `dre`, `dra`, `dfc`, `dmpl`, `dva`). Sem `demonstracao` a resposta é
   grande. Padrão da tool: consolidado, ou individual quando não há consolidado. Cada conta
   traz `codigo`, `descricao`, `nivel`, `padronizada`, `valor_atual` e `valor_anterior`.
5. `cvm_parecer_dfp(id_doc)`: `auditor.tipo`, `auditor.texto` integral e `declaracoes[]`
   (diretores sobre as demonstrações, diretores sobre o parecer, conselho fiscal).
6. `cvm_ranking_companhias(metrica, ano, visao, familia, limite)`: `ano` obrigatório.

Campos de cada resposta em [references/payloads.md](references/payloads.md).

## Visão

- **Consolidado é o padrão** para tamanho, operação, margens e comparação. É o que
  responde "que tamanho tem" e "quanto fatura".
- **Individual** só quando a pergunta é sobre a entidade (dividendos, capital social,
  obrigação própria, garantia dada pela controladora) ou quando não há consolidado (lista
  `visoes` em `cvm_entrega_dfp`; companhia sem controladas entrega só o individual).
- A visão vai no cabeçalho de toda tabela e ao lado de todo número solto.
- A regra de holding e controladora da skill balancos-ai **não se aplica** quando há
  consolidado: Gerdau S.A. tem receita individual de R$ 4,8 bi e consolidada de R$ 69,9 bi
  em 2025; o consolidado é a operação.
- Exercício antigo com receita zero na visão individual (Gerdau 2010) é lacuna da
  entrega, não receita zero: deixe em branco e diga.

## Família

`familia` vem na ficha: `comercial`, `financeira`, `seguradora` ou `desconhecida`.

- `comercial` usa o plano de contas padrão da CVM e o mapa de códigos desta skill.
- `financeira` e `seguradora` têm plano próprio: o mapa **não** vale, o ranking só compara
  dentro da família (`familia` no `cvm_ranking_companhias`), e banco vai para a skill
  instituicao-financeira, que tem carteira, captações e Basileia.

## Versões e reapresentações

- A última versão de um exercício é a que vale, e `cvm_analisar_companhia` já a escolhe
  (`versao` e `id_doc` em cada linha de `balancos[]` e `dres[]`).
- `n_reapresentacoes` na ficha e `reapresentacao: true` na linha do tempo são sinal para
  due diligence, mas uma reapresentação pode ser só a inclusão do parecer (Gerdau 2024:
  v1 com `parecer: null`, v2 cinco dias depois com "Sem Ressalva"). Para dizer o que mudou,
  compare `valor_atual` das duas versões pelo conta a conta; sem isso, diga só que houve
  reapresentação e a data.
- `valor_anterior` é o comparativo **republicado na mesma DFP** e pode divergir do
  `valor_atual` da entrega anterior. Série usa a última versão de cada exercício; quando o
  comparativo diverge mais de 1% do publicado no ano anterior, diga que houve
  reclassificação ou reapresentação do comparativo.

## Parecer

- `auditor.tipo` é estruturado: "Sem Ressalva", "Com Ressalva", "Adverso", "Negativa de
  Opinião". Na linha do tempo, `parecer: null` significa entrega sem parecer carregado.
- Ênfase, incerteza relevante de continuidade e outros assuntos só lendo `auditor.texto`:
  procure "ênfase", "continuidade operacional", "incerteza relevante", "outros assuntos".
- "Principais assuntos de auditoria" não é ressalva nem ênfase.
- Firma e data ficam no fim do texto; cite as duas. Troca de firma entre exercícios é
  sinal: compare pareceres de dois `id_doc`.
- O texto vem sem quebras de linha entre seções; leia por frase.

## Ranking

- `ano` obrigatório; `visao` (padrão consolidado) e `familia` explícitas na resposta.
- Grupos duplicam (JBS S.A. e JBS N.V. com a mesma receita de 2025): dedupe pelo `slug`
  da `empresa` ou pelo nome e diga que deduplicou.
- Não há filtro por UF nem setor: para setor, cruze com `cnae_principal` da
  `ficha_empresa` de publicações; para UF idem. Diga que o corte foi feito do lado do
  agente e que o teto é 50 por chamada.
- `metrica` = `ativo`, `patrimonio`, `receita` ou `lucro`. Valores em reais da última
  versão de cada companhia no exercício.

## Indicadores com o conta a conta

Proveniência 1 (da base), com o código da conta ao lado na apresentação. Mapa completo em
[references/contas-dfp.md](references/contas-dfp.md). Use valor absoluto de contas que
vêm negativas (custo, despesas, depreciação).

| Indicador | Fórmula | Ressalva obrigatória |
|---|---|---|
| EBITDA | 3.05 + \|7.04.01\| (DVA) | depreciação da DVA inclui amortização e exaustão |
| Dívida bruta | 2.01.04 + 2.02.01 | dizer se arrendamento (2.01.04.03 e 2.02.01.03) entrou; padrão: entra, porque está dentro da conta |
| Dívida líquida | dívida bruta − 1.01.01 − 1.01.02 | aplicações de longo prazo (1.02.01.01 a 1.02.01.03) ficam fora por padrão; diga |
| Cobertura de juros | 3.05 / \|3.06.02\| | 3.06.02 inclui variação cambial e perdas com derivativos; se a companhia abre 3.06.02.01 "Despesas Financeiras", use-a e diga |
| Caixa operacional | 6.01 | método em `metodo` (direto ou indireto) |
| Caixa operacional sobre dívida bruta | 6.01 / dívida bruta | |
| Juros pagos | linha com "juros" em 6.01.03 ou em 6.03 | não padronizada; cite a descrição |
| Capex | linhas de adição de imobilizado e intangível em 6.02 | não padronizada; cite a descrição |
| Lucro dos controladores | 3.11.01 | para ROE, com PL sem não controladores: 2.03 − 2.03.09 |
| Equivalência no resultado | 3.04.06 | dependência de coligadas e controladas em conjunto |
| Não recorrentes | 3.04.03 (impairment), 3.10 (descontinuadas) | |
| Prazos médios | contas a receber 1.01.03, estoques 1.01.04, fornecedores 2.01.02 sobre receita 3.01 e custo 3.02, vezes 365 | saldo de fim de exercício |

Contas com `padronizada: false` variam por companhia: cite código e descrição.
Indicadores da skill indicadores-financeiros (liquidez, endividamento, margens, ROE)
continuam valendo com os campos de `balancos[]` e `dres[]`, agora na visão escolhida.

## O que a CVM não tem

ITR trimestral, notas explicativas em campo estruturado (continuam no `texto_documento`
da publicação), valor de mercado, companhias fechadas, exercícios anteriores a 2010.
Quando pedirem, diga e aponte a fonte publicações ou o link.

## Ao apresentar

- Visão, versão e `id_doc` da entrega usada; `link_documento` (balancos.ai) e `link_cvm`
  de cada entrega citada; link da `empresa`.
- Código da conta ao lado de cada indicador derivado.
- `dados_atualizados_em` da família CVM, que difere do das publicações.
- Ranking é dentro das companhias com DFP no exercício; diga o N e a família.
```

- [ ] **Step 2: Criar `skills/companhia-aberta/references/payloads.md`**

```markdown
# Campos de cada resposta das tools `cvm_*`

Toda resposta traz `dados_atualizados_em`. `chave` aceita CNPJ (com ou sem pontuação) ou
código CVM. Valores em reais; `escala_publicada` é só proveniência.

## cvm_buscar_companhias(termo)

```
companhias[]: cnpj, cd_cvm, denominacao, empresa {razao_social, slug, link} | null
total
```

## cvm_ficha_companhia(chave) → companhia

```
cnpj, cd_cvm, denominacao, empresa, denominacoes_anteriores[],
familia (comercial | financeira | seguradora | desconhecida),
primeiro_exercicio, ultimo_exercicio, n_entregas, n_reapresentacoes,
ultimo_parecer {exercicio, tipo},
capital_social {exercicio, versao, integralizado {ordinarias, preferenciais, total},
                tesouraria {ordinarias, preferenciais, total}}
```

## cvm_dfps_companhia(chave, ano?)

```
companhia {cnpj, cd_cvm, denominacao, empresa}
exercicios[]: exercicio, data_referencia,
  versoes[]: id_doc, versao, reapresentacao (bool), recebida_em, parecer (tipo | null),
             link_cvm, link_documento
```

Exercícios decrescentes; versões crescentes. A última versão de um exercício é a que vale.

## cvm_entrega_dfp(id_doc) → entrega

```
id_doc, exercicio, data_referencia, versao, link_documento, companhia,
reapresentacao, recebida_em, link_cvm, escala_publicada, moeda,
visoes[] (consolidado, individual),
demonstracoes_disponiveis {consolidado[], individual[]}  (bpa, bpp, dre, dra, dfc, dmpl, dva),
parecer (tipo), capital_social, versoes[] (igual a cvm_dfps_companhia)
```

## cvm_balancos_companhia(chave, ano?, visao?) → balancos[]

```
exercicio, data_referencia, visao, versao, id_doc, familia, escala_publicada,
eq_ativo_passivo (bool),
valores_em_reais: ativo_total, ativo_circulante, ativo_nao_circulante,
                  passivo_circulante, passivo_nao_circulante, passivo_total,
                  patrimonio_liquido, passivo_e_pl_total
```

Mesmos nomes de campo da fonte publicações, com `visao` a mais. `passivo_total` é o
exigível, sem PL.

## cvm_dres_companhia(chave, ano?, visao?) → dres[]

```
exercicio, data_referencia, data_inicio, periodo_tipo, visao, versao, id_doc, familia,
escala_publicada,
valores_em_reais: receita_bruta (null na CVM), receita_liquida, custo (negativo),
                  lucro_bruto, lucro_operacional (EBIT, conta 3.05), lucro_liquido
```

## cvm_analisar_companhia(chave)

```
companhia (igual à ficha)
exercicios[] (igual a cvm_dfps_companhia)
balancos[] (igual a cvm_balancos_companhia, as duas visões, última versão)
dres[] (igual a cvm_dres_companhia)
nota
```

## cvm_demonstracoes_dfp(id_doc, demonstracao?, visao?)

```
entrega {id_doc, exercicio, data_referencia, versao, link_documento}
visao (a usada), visao_solicitada
demonstracoes[]: demonstracao, nome, metodo (dfc: direto | indireto), escala_publicada,
  moeda, exercicio_atual {inicio, fim}, exercicio_anterior {inicio, fim},
  contas[]: codigo, descricao, nivel, padronizada (bool), coluna, valor_atual, valor_anterior
```

`valor_anterior` é o comparativo republicado nesta DFP. Resposta grande sem
`demonstracao`: clientes como o Claude Code gravam em arquivo; leia o arquivo inteiro.

## cvm_parecer_dfp(id_doc)

```
entrega {id_doc, exercicio, data_referencia, versao, link_documento}
auditor {tipo, texto}
declaracoes[]: tipo, texto
```

Tipos de `declaracoes`: "Declaração dos Diretores sobre as Demonstrações Financeiras",
"Declaração dos Diretores sobre o Relatório do Auditor Independente", "Parecer do
Conselho Fiscal ou Órgão Equivalente".

## cvm_ranking_companhias(metrica, ano, visao?, familia?, limite?)

```
metrica, exercicio, visao, familia
companhias[]: posicao, cnpj, cd_cvm, denominacao, valor_em_reais, versao, id_doc, empresa
nota
```

`metrica` = `ativo` | `patrimonio` | `receita` | `lucro`. Limite até 50, padrão 20.
```

- [ ] **Step 3: Criar `skills/companhia-aberta/references/contas-dfp.md`**

```markdown
# Mapa de contas padronizadas da DFP

Códigos com `padronizada: true` no plano de contas da CVM para a família `comercial`.
Os valores vêm em reais em `cvm_demonstracoes_dfp`. Contas abaixo do nível 3 costumam
variar por companhia (`padronizada: false`): cite código e descrição ao usá-las.

## BPA (`demonstracao="bpa"`)

| Código | Conta | Uso |
|---|---|---|
| 1 | Ativo Total | |
| 1.01 | Ativo Circulante | |
| 1.01.01 | Caixa e Equivalentes de Caixa | dívida líquida |
| 1.01.02 | Aplicações Financeiras | dívida líquida |
| 1.01.03 | Contas a Receber | prazo médio de recebimento |
| 1.01.04 | Estoques | prazo médio de estoque |
| 1.01.06 | Tributos a Recuperar | |
| 1.02 | Ativo Não Circulante | |
| 1.02.01 | Ativo Realizável a Longo Prazo | |
| 1.02.01.01 a 1.02.01.03 | Aplicações Financeiras de longo prazo | fora da dívida líquida por padrão |
| 1.02.01.07 | Tributos Diferidos | qualidade do lucro |
| 1.02.01.09 | Créditos com Partes Relacionadas | due diligence |
| 1.02.02 | Investimentos | equivalência |
| 1.02.03 | Imobilizado | |
| 1.02.04 | Intangível | |
| 1.02.04.02 | Goodwill | impairment |

## BPP (`demonstracao="bpp"`)

| Código | Conta | Uso |
|---|---|---|
| 2 | Passivo Total (inclui PL) | |
| 2.01 | Passivo Circulante | |
| 2.01.02 | Fornecedores | prazo médio de pagamento |
| 2.01.04 | Empréstimos e Financiamentos (curto prazo) | dívida bruta |
| 2.01.04.01 | Empréstimos e Financiamentos | |
| 2.01.04.02 | Debêntures | |
| 2.01.04.03 | Financiamento por Arrendamento | dizer se entrou na dívida |
| 2.01.05.01 | Passivos com Partes Relacionadas | due diligence |
| 2.01.06 | Provisões | contingências |
| 2.02 | Passivo Não Circulante | |
| 2.02.01 | Empréstimos e Financiamentos (longo prazo) | dívida bruta |
| 2.02.01.01 / .02 / .03 | Empréstimos, Debêntures, Arrendamento | |
| 2.02.02.01 | Passivos com Partes Relacionadas | |
| 2.02.04 | Provisões | contingências |
| 2.02.04.01 | Provisões Fiscais, Previdenciárias, Trabalhistas e Cíveis | |
| 2.03 | Patrimônio Líquido (Consolidado) | |
| 2.03.01 | Capital Social Realizado | |
| 2.03.04 | Reservas de Lucros | |
| 2.03.05 | Lucros/Prejuízos Acumulados | |
| 2.03.09 | Participação dos Acionistas Não Controladores | PL dos controladores = 2.03 − 2.03.09 |

`passivo_total` de `balancos[]` (exigível) = 2.01 + 2.02, sem 2.03.

## DRE (`demonstracao="dre"`)

| Código | Conta | Uso |
|---|---|---|
| 3.01 | Receita de Venda de Bens e/ou Serviços | = `receita_liquida` |
| 3.02 | Custo dos Bens e/ou Serviços Vendidos | negativo |
| 3.03 | Resultado Bruto | |
| 3.04 | Despesas/Receitas Operacionais | |
| 3.04.01 | Despesas com Vendas | |
| 3.04.02 | Despesas Gerais e Administrativas | |
| 3.04.03 | Perdas pela Não Recuperabilidade de Ativos | impairment, não recorrente |
| 3.04.04 / 3.04.05 | Outras Receitas / Outras Despesas Operacionais | |
| 3.04.06 | Resultado de Equivalência Patrimonial | |
| 3.05 | Resultado Antes do Resultado Financeiro e dos Tributos | EBIT = `lucro_operacional` |
| 3.06 | Resultado Financeiro | |
| 3.06.01 | Receitas Financeiras | |
| 3.06.02 | Despesas Financeiras | cobertura de juros; inclui variação cambial |
| 3.07 | Resultado Antes dos Tributos sobre o Lucro | |
| 3.08 | Imposto de Renda e Contribuição Social | 3.08.01 corrente, 3.08.02 diferido |
| 3.09 | Resultado Líquido das Operações Continuadas | |
| 3.10 | Resultado Líquido de Operações Descontinuadas | não recorrente |
| 3.11 | Lucro/Prejuízo (Consolidado) do Período | = `lucro_liquido` |
| 3.11.01 | Atribuído a Sócios da Empresa Controladora | ROE dos controladores |
| 3.11.02 | Atribuído a Sócios Não Controladores | |
| 3.99 | Lucro por Ação | em reais por ação, não em milhares |

## DFC (`demonstracao="dfc"`)

| Código | Conta | Uso |
|---|---|---|
| 6.01 | Caixa Líquido Atividades Operacionais | geração de caixa |
| 6.01.01 | Caixa Gerado nas Operações | abaixo, linhas não padronizadas: lucro, depreciação, juros |
| 6.01.02 | Variações nos Ativos e Passivos | capital de giro |
| 6.01.03 | Outros | juros e IR pagos costumam estar aqui |
| 6.02 | Caixa Líquido Atividades de Investimento | capex nas linhas não padronizadas |
| 6.03 | Caixa Líquido Atividades de Financiamento | captações, amortizações, dividendos |
| 6.04 | Variação Cambial sobre Caixa e Equivalentes | |
| 6.05 | Aumento (Redução) de Caixa e Equivalentes | 6.05.01 inicial, 6.05.02 final |

Depreciação na DFC é linha não padronizada dentro de 6.01.01: use a DVA (7.04.01) para
EBITDA e cite a DFC só como conferência.

## DVA (`demonstracao="dva"`)

| Código | Conta | Uso |
|---|---|---|
| 7.01 | Receitas | 7.01.01 vendas, 7.01.02 outras, 7.01.04 PCLD |
| 7.02 | Insumos Adquiridos de Terceiros | |
| 7.03 | Valor Adicionado Bruto | |
| 7.04.01 | Depreciação, Amortização e Exaustão | EBITDA (valor absoluto) |
| 7.06.01 | Resultado de Equivalência Patrimonial | |
| 7.06.02 | Receitas Financeiras | |
| 7.08.01 | Pessoal | |
| 7.08.02 | Impostos, Taxas e Contribuições | |
| 7.08.03 | Remuneração de Capitais de Terceiros | 7.08.03.01 juros, quando preenchido |
| 7.08.04 | Remuneração de Capitais Próprios | JCP, dividendos, lucros retidos |

## DRA e DMPL

`dra` (resultado abrangente) e `dmpl` (mutações do PL) existem; use a DMPL para
dividendos declarados e movimentação de reservas, citando a descrição da linha.
```

- [ ] **Step 4: Rodar o checker e conferir tamanho**

Run: `python3 scripts/check.py && wc -l skills/companhia-aberta/SKILL.md`
Expected: `8 skills, 0 erros`; SKILL.md abaixo de 200 linhas.

- [ ] **Step 5: Commit**

```bash
git add skills/companhia-aberta
git commit -m "feat(companhia-aberta): skill da fonte CVM com visão, versões, parecer e indicadores por código de conta

Co-Authored-By: Claude Fable 5.1 <noreply@anthropic.com>"
```

---

### Task 4: skill `instituicao-financeira`

**Files:**
- Create: `skills/instituicao-financeira/SKILL.md`
- Create: `skills/instituicao-financeira/references/payloads.md`
- Create: `skills/instituicao-financeira/references/relatorios-ifdata.md`

**Interfaces:**
- Consumes: Task 1, Task 2.
- Produces: a skill que as Tasks 5 a 10 citam como "skill instituicao-financeira"; a tabela "Indicadores próprios" que a Task 6 usa no memo de banco e a Task 7 nas linhas da comparação.

- [ ] **Step 1: Criar `skills/instituicao-financeira/SKILL.md`**

```markdown
---
name: instituicao-financeira
description: Use quando a empresa for banco, cooperativa de crédito, financeira, corretora ou outra instituição do IF.data do Banco Central, e o pedido envolver carteira de crédito, captações, Basileia, conglomerado, série trimestral ou ranking de instituições, com o MCP do Balanços.AI conectado. Assume a skill balancos-ai.
license: MIT
compatibility: Requer o MCP do Balanços.AI conectado. Assume a skill balancos-ai.
metadata:
  author: Balanços.AI
  version: "0.2"
---

# Instituição financeira pelo IF.data

## Resultado

O mesmo tipo de entrega da skill que chamou, com **nível de consolidação**, **data-base**
e **era contábil** declarados em cada número. Sem liquidez corrente, margem bruta nem giro:
banco tem vocabulário próprio (abaixo).

## Fluxo

1. `bcb_buscar_instituicoes(termo, uf, tipo, consolidado_bancario)`. **Raiz do CNPJ
   (8 dígitos) primeiro.** Nome só com `tipo` (8 banco múltiplo, 9 cooperativa de crédito)
   e sabendo de dois problemas: fundos de investimento poluem a busca ("Banrisul" devolve
   20 fundos e não o banco) e nome fantasia não casa com o oficial ("Banrisul" com tipo 8
   devolve zero; o oficial é "Banco do Estado do Rio Grande do Sul"). Se o usuário deu nome
   fantasia, obtenha o CNPJ por `buscar_empresas` das publicações ou pelo MCP do cnpj.ai
   se disponível, e busque pela raiz.
2. `bcb_analisar_instituicao(chave)`, chave = CodInst, CNPJ ou raiz. Uma chamada: ficha
   (`tipo`, `consolidado_bancario`, `segmento_prudencial`, sede, `conglomerados`,
   `niveis[]` com o CodInst de cada um e `padrao`, `ultima_data_base_resumo`), série
   `trimestres[]` do nível padrão e `resultados_anuais[]` (DRE derivada).
3. `bcb_trimestres_instituicao(chave, nivel, desde, ate)` para outro nível ou janela.
4. `bcb_resultados_instituicao(chave, nivel, periodo)` para trimestre isolado
   (`periodo="trimestre"`).
5. `bcb_estrutura_relatorios(data_base)` para achar o `relatorio`, depois
   `bcb_relatorios_instituicao(chave, nivel, data_base, relatorio)`: **um relatório por
   chamada**; sem `relatorio` a resposta é grande.
6. `bcb_conglomerado(codinst, nivel)` para os membros de um conglomerado, cada um com CNPJ
   e link de empresa.
7. `bcb_ranking_instituicoes(metrica, data_base, nivel, uf, tipo, consolidado_bancario,
   limite)`.
8. `bcb_data_bases()` para a última data-base e a era de cada uma.

Campos de cada resposta em [references/payloads.md](references/payloads.md).

## Níveis de consolidação

- `individual`, `financeiro` e `prudencial`, cada um com o próprio CodInst em
  `niveis[]`. Banco grande reporta pelo **prudencial**, que é o `nivel_padrao`; cooperativa
  singular e instituição independente reportam pelo individual.
- Compare instituições no nível padrão de cada uma: `nivel="padrao"` no ranking dá uma
  linha por grupo. Nunca some o individual ao prudencial do mesmo grupo.
- Linhas prudenciais do ranking vêm com `cnpj` e `empresa` nulos ("ITAU - PRUDENCIAL"):
  para chegar à empresa e ao link, `bcb_conglomerado(codinst)` lista os membros em ordem
  de ativo, com CNPJ e link.
- Diga qual nível usou e o CodInst, em toda tabela.

## Tempo

- Data-base `AAAAMM` com mês 03, 06, 09 ou 12. A última vem em `ultima_data_base` da
  ficha e em `bcb_data_bases`.
- O IF.data publica **lucro acumulado no semestre** (`lucro_liquido_acumulado_semestre`):
  março traz janeiro a março, junho traz janeiro a junho, setembro traz julho a setembro,
  dezembro traz julho a dezembro. Trimestre isolado: T1 = mar, T2 = jun − mar, T3 = set,
  T4 = dez − set; anual = jun + dez. A DRE derivada (`resultados`) já faz isso e marca
  `completo`; use-a em vez de recalcular. Não compare lucro de junho com lucro de setembro
  como se fossem o mesmo período.
- Era contábil: `cosif_2000` até 202412 e `cosif_2025` de 202503 em diante. Comparação
  ano contra ano só dentro da mesma era; `bcb_relatorios_instituicao` devolve
  `comparavel` e `valor_ano_anterior` já respeitando isso. Numa série que cruza a
  fronteira, marque a quebra e não atribua a ela variação de negócio.
- Campos nulos em trimestres antigos (`tvm` antes de 2025, `indices` antes de 2015,
  `rede` em toda a série de alguns bancos) ficam em branco, nunca zero.
- `link_documento` só existe em trimestres de dezembro (publicação anual); nos demais,
  aponte `link_ifdata`.

## Índices

- `indices.basileia`, `imobilizacao` e `alavancagem` vêm em **fração** (0,159 é 15,9%).
  No ranking, `unidade` diz se `valor` é reais ou fração.
- Basileia se compara com o mínimo regulatório vigente; o mínimo é conhecimento geral e vai
  rotulado "de conhecimento geral, não confirmado na base". Idem imobilização e
  alavancagem.
- `patrimonio_referencia` e `rwa` em reais; Basileia = PR / RWA.

## Indicadores próprios

| Indicador | Fórmula | Leitura |
|---|---|---|
| ROE anual | `lucro_liquido` anual (`resultados_anuais`, `completo: true`) / `patrimonio_liquido` de dezembro | PL de fim de ano; diga |
| Carteira sobre ativo | `carteira_credito` / `ativo_total` | quanto do balanço é crédito |
| Captações sobre ativo | `captacoes` / `ativo_total` | dependência de funding |
| Crescimento de carteira | carteira(t) / carteira(t − 4 trimestres) − 1 | mesma era |
| Crescimento de captações | idem | |
| Basileia, imobilização, alavancagem | `indices` | fração; mínimo rotulado |
| Lucro semestral | `lucro_liquido_acumulado_semestre` em junho e em dezembro | sazonal; não some com março |
| Rede | `rede.agencias`, `rede.postos` | quando existir |
| TVM sobre ativo | `tvm` / `ativo_total` | só a partir de 2025 |

A DRE derivada tem `receita_liquida` (receitas de intermediação financeira e de serviços),
`custo` (despesas de intermediação) e `lucro_bruto` (resultado de intermediação). Explique
isso antes de qualquer razão e chame de "margem de intermediação", nunca "margem bruta".
`lucro_operacional` e `lucro_liquido` seguem o sentido usual.

## Relatórios conta a conta

Ids mudam por era: **reconfira com `bcb_estrutura_relatorios(data_base)`** antes de pedir.
Na era COSIF 2025 (202503 em diante): Resumo 121 (prudencial), 119 (financeiro), 120
(individual); Ativo 105/107/106; Passivo 108/110/109; Demonstração de Resultado
116/118/117; Informações de Capital 115; carteira de crédito 123 a 130; Segmentação 131.
Lista completa em [references/relatorios-ifdata.md](references/relatorios-ifdata.md).

"Para quem o banco empresta" responde-se com carteira PJ por atividade econômica (129),
por porte do tomador (127) e por região (126); "que tipo de crédito" com PF (123) e PJ
(128) por modalidade e prazo; "risco" com por instrumento (130) e por indexador (125).
Cada linha traz `formato` (`mil` = reais, `pct` = fração, `inteiro` = contagem),
`valor` e `valor_ano_anterior`.

## Cooperativas e sistemas

Cooperativa singular é `consolidado_bancario` `b3S`, tipo 9, nível individual. Sistemas
(Sicredi, Sicoob, Unicred) são centenas de CNPJs; a central e o banco do sistema aparecem
como conglomerado. Diga qual entidade analisou e não some cooperativas por conta própria.
Ranking de cooperativas por UF: `tipo="9"` ou `consolidado_bancario="b3S"` com `uf`.

## O que o BCB não tem

Parecer do auditor (CVM, se listado, ou texto da publicação), notas explicativas, DFC,
valor de mercado, instituições fora do IF.data (instituições de pagamento só de 2020 em
diante), fundos de investimento com série útil (aparecem na busca com uma ou poucas
data-bases: ignore-os).

## Ao apresentar

- Nível, CodInst, data-base e era em cada tabela; `link_documento` quando houver ou
  `link_ifdata`; link da `empresa` no balancos.ai.
- Valores em R$ mi ou bi com a unidade escrita; índices em porcentagem com uma casa.
- `dados_atualizados_em` da família BCB.
- Ranking é dentro do IF.data na data-base; diga o N e o nível.
```

- [ ] **Step 2: Criar `skills/instituicao-financeira/references/payloads.md`**

```markdown
# Campos de cada resposta das tools `bcb_*`

Toda resposta traz `dados_atualizados_em`. `chave` aceita CodInst, CNPJ (14 dígitos) ou
raiz do CNPJ (8 dígitos). Valores em reais; índices em fração.

## Objeto `instituicao` (ficha), presente em quase toda resposta

```
codinst, nome, cnpj, cnpj_raiz,
tipo {codigo, nome} | null, consolidado_bancario {codigo, nome} | null,
segmento_prudencial (S1..S5) | null, sede {uf, municipio},
conglomerados {financeiro (codinst | null), prudencial (codinst | null)},
primeira_data_base, ultima_data_base, n_data_bases,
empresa {razao_social, slug, link} | null
```

`bcb_ficha_instituicao` e `bcb_analisar_instituicao` acrescentam:

```
receita {razao_social, situacao, cnae}
niveis[]: nivel (individual | financeiro | prudencial), codinst, nome, padrao (bool)
nivel_padrao
ultima_data_base_resumo {data_base, data_referencia, nivel, ativo_total, carteira_credito,
                         captacoes, patrimonio_liquido, indice_basileia}
link_ifdata
```

## bcb_buscar_instituicoes(termo?, uf?, tipo?, consolidado_bancario?)

```
instituicoes[] (objeto instituicao, até 20)
total, dica (quando vazio)
```

Fundos de investimento aparecem com `tipo: null` e poucas data-bases.

## bcb_analisar_instituicao(chave)

```
instituicao (ficha completa)
nivel {nivel, codinst, nome, padrao}
trimestres[]: data_base, data_referencia, ano, trimestre, era (cosif_2000 | cosif_2025),
  nivel_padrao,
  valores_em_reais {ativo_total, carteira_credito, tvm, captacoes, patrimonio_liquido,
                    lucro_liquido_acumulado_semestre, patrimonio_referencia, rwa},
  indices {basileia, imobilizacao, alavancagem},
  rede {agencias, postos},
  link_documento (só em dezembro) | null
resultados_anuais[]: periodo ("anual"), ano, trimestre (null), data_inicio, data_referencia,
  era, completo (bool),
  valores_em_reais {receita_bruta (null), receita_liquida, custo, lucro_bruto,
                    lucro_operacional, lucro_liquido}
nota
```

## bcb_trimestres_instituicao(chave, nivel?, desde?, ate?)

```
instituicao, nivel, trimestres[] (igual a bcb_analisar_instituicao)
```

## bcb_resultados_instituicao(chave, nivel?, periodo?)

```
instituicao, nivel
resultados[]: periodo (trimestre | anual), ano, trimestre (1..4 | null), data_inicio,
  data_referencia, era, completo, valores_em_reais (igual a resultados_anuais)
```

## bcb_relatorios_instituicao(chave, nivel?, data_base?, relatorio?)

```
instituicao, nivel, data_base, data_referencia, era, data_base_anterior, comparavel (bool)
relatorios[]: id, nome, grupo, cabecalho,
  linhas[]: id, lid, nome, descricao, profundidade, grupo (bool), formato (mil | pct | inteiro),
            valor, valor_ano_anterior
```

`formato: "mil"` é só o cabeçalho da fonte: `valor` está em reais.

## bcb_estrutura_relatorios(data_base, relatorio?)

Sem `relatorio` (`resumido: true`):

```
data_base, era
relatorios[]: id, nome, grupo (demonstracoes | capital | carteira | segmentacao),
  niveis[], cabecalho, notas, n_colunas
nota
```

Com `relatorio`: o mesmo relatório com a árvore de colunas (id, lid, nome, descricao,
pai, profundidade, formato).

## bcb_conglomerado(codinst, nivel?)

```
conglomerado {nivel, codinst, nome, primeira_data_base, ultima_data_base, n_data_bases, n_membros}
membros[]: codinst, nome, cnpj, ativo_total, data_base, empresa
```

## bcb_ranking_instituicoes(metrica, data_base?, nivel?, uf?, tipo?, consolidado_bancario?, limite?)

```
data_base, data_referencia, nivel, metrica, unidade (reais | fracao)
instituicoes[]: posicao, nivel, codinst, nome, cnpj | null, tipo, consolidado_bancario,
  uf, valor, empresa | null
nota
```

`metrica` = `ativo` | `carteira` | `captacoes` | `patrimonio` | `lucro` | `basileia`.
Linhas de nível prudencial vêm com `cnpj` e `empresa` nulos.

## bcb_data_bases()

```
data_bases[]: data_base, data_referencia, ano, trimestre, era, n_instituicoes, derivada_em
```
```

- [ ] **Step 3: Criar `skills/instituicao-financeira/references/relatorios-ifdata.md`**

```markdown
# Relatórios do IF.data e códigos de tipo

Ids de relatório valem por era contábil. A lista abaixo é da era COSIF 2025 (data-bases
202503 em diante), conferida em 202606. Antes de chamar `bcb_relatorios_instituicao`
para outra data-base, rode `bcb_estrutura_relatorios(data_base)` e confira o id.

## Relatórios (era COSIF 2025)

| Id | Nome | Grupo | Nível |
|---|---|---|---|
| 121 | Resumo | demonstracoes | prudencial |
| 119 | Resumo | demonstracoes | financeiro |
| 120 | Resumo | demonstracoes | individual |
| 105 | Ativo | demonstracoes | prudencial |
| 107 | Ativo | demonstracoes | financeiro |
| 106 | Ativo | demonstracoes | individual |
| 108 | Passivo | demonstracoes | prudencial |
| 110 | Passivo | demonstracoes | financeiro |
| 109 | Passivo | demonstracoes | individual |
| 116 | Demonstração de Resultado | demonstracoes | prudencial |
| 118 | Demonstração de Resultado | demonstracoes | financeiro |
| 117 | Demonstração de Resultado | demonstracoes | individual |
| 115 | Informações de Capital | capital | prudencial |
| 123 | Carteira de crédito ativa Pessoa Física, modalidade e prazo de vencimento | carteira | prudencial |
| 128 | Carteira de crédito ativa Pessoa Jurídica, modalidade e prazo de vencimento | carteira | prudencial |
| 129 | Carteira de crédito ativa Pessoa Jurídica, por atividade econômica (CNAE) | carteira | prudencial |
| 127 | Carteira de crédito ativa Pessoa Jurídica, por porte do tomador | carteira | prudencial |
| 124 | Carteira de crédito ativa, quantidade de clientes e de operações | carteira | prudencial |
| 130 | Carteira de crédito ativa, por carteiras de instrumentos financeiros | carteira | prudencial |
| 125 | Carteira de crédito ativa, por indexador | carteira | prudencial |
| 126 | Carteira de crédito ativa, por região geográfica | carteira | prudencial |
| 131 | Segmentação | segmentacao | prudencial |

O Resumo (121) traz, numa chamada, ativo total, carteira de crédito, TVM, passivo
exigível, captações, PL, lucro líquido, patrimônio de referência, Basileia e imobilização,
com `valor_ano_anterior` quando a era é a mesma.

Os relatórios de carteira e capital existem só no nível prudencial (ou individual, para
quem não tem conglomerado). A DRE (116) tem 60 colunas: receitas e despesas de
intermediação abertas por natureza, resultado de serviços, despesas de pessoal e
administrativas, provisões.

## Códigos de tipo de instituição (`tipo`, TI)

Os que apareceram nos testes; a lista do IF.data é maior.

| Código | Tipo |
|---|---|
| 8 | Banco múltiplo |
| 9 | Cooperativa de crédito |
| 15 | Sociedade corretora de TVM |
| 41 | Instituição de pagamento |
| 199 | Conglomerado prudencial (aparece no ranking, `nome` nulo) |

## Códigos de consolidado bancário (`consolidado_bancario`, TCB)

| Código | Grupo |
|---|---|
| b1 | Banco comercial ou múltiplo com carteira comercial |
| b2 | Banco múltiplo sem carteira comercial ou banco de investimento |
| b3S | Cooperativa de crédito singular |
| b3C | Cooperativa de crédito central |
| b4 | Banco de desenvolvimento |
| n1 | Não bancário de crédito |
| n2 | Não bancário de mercado de capitais |
| n4 | Instituição de pagamento |

`segmento_prudencial` vai de S1 (bancos sistêmicos) a S5 (menor porte).
```

- [ ] **Step 4: Rodar o checker e conferir tamanho**

Run: `python3 scripts/check.py && wc -l skills/instituicao-financeira/SKILL.md`
Expected: `9 skills, 0 erros`; SKILL.md abaixo de 200 linhas.

- [ ] **Step 5: Commit**

```bash
git add skills/instituicao-financeira
git commit -m "feat(instituicao-financeira): skill da fonte BCB com níveis, tempo, índices e relatórios do IF.data

Co-Authored-By: Claude Fable 5.1 <noreply@anthropic.com>"
```

---

### Task 5: desvio em `indicadores-financeiros`

**Files:**
- Modify: `skills/indicadores-financeiros/SKILL.md`

**Interfaces:**
- Consumes: Task 3 (códigos das contas), Task 4 (vocabulário de banco).

- [ ] **Step 1: Subir a versão**

`version: "0.1"` → `version: "0.2"`.

- [ ] **Step 2: Dizer de onde mais os campos podem vir**

Depois do parágrafo `Pareie BP e DRE pelo mesmo `exercicio`. Um ano sem BP ou sem DRE
entra na tabela com o indicador em branco, nunca com o ano vizinho no lugar.` acrescentar:

```
Os mesmos nomes de campo voltam em `cvm_balancos_companhia` e `cvm_dres_companhia` (skill
companhia-aberta), com `visao` a mais: as fórmulas valem, e o cabeçalho diz a visão.
`bcb_resultados_instituicao` também usa esses nomes, mas com semântica de intermediação
financeira: não aplique esta skill a banco; use a skill instituicao-financeira.
```

- [ ] **Step 3: Trocar a tabela de incomputáveis por uma com a coluna "Na CVM"**

Substituir a tabela da seção `## Incomputável com o dado estruturado` (do cabeçalho
`| Pedido | Por que não | Caminho |` até a linha `| ROIC, múltiplos | ... |`) por:

```
| Pedido | Na fonte publicações | Na CVM (companhia aberta, skill companhia-aberta) |
|---|---|---|
| EBITDA | não há depreciação; "EBITDA ajustado" do relatório da administração, ou EBIT + depreciação da DVA no texto, rotulado aproximado | 3.05 + \|7.04.01\| da DVA, proveniência 1 |
| Dívida bruta e líquida | nota de empréstimos e nota de caixa no texto | 2.01.04 + 2.02.01, menos 1.01.01 e 1.01.02 |
| Cobertura de juros | DRE completa no texto; encargos de empréstimos na DVA | 3.05 / \|3.06.02\| |
| Fluxo de caixa | DFC no texto (depois da DMPL, antes das notas) | 6.01, 6.02, 6.03 da DFC |
| Prazo médio de recebimento, estoque, pagamento | notas explicativas | 1.01.03, 1.01.04, 2.01.02 sobre 3.01 e 3.02 |
| ROIC, múltiplos | fora da base | falta valor de mercado; fora |
```

Logo abaixo da tabela, acrescentar:

```
Em instituição financeira nenhuma linha desta tabela se aplica; o vocabulário é carteira,
captações, Basileia e resultado de intermediação (skill instituicao-financeira).
```

- [ ] **Step 4: Rodar o checker**

Run: `python3 scripts/check.py`
Expected: `9 skills, 0 erros`.

- [ ] **Step 5: Commit**

```bash
git add skills/indicadores-financeiros/SKILL.md
git commit -m "feat(indicadores-financeiros): incomputáveis por fonte, com código de conta na CVM

Co-Authored-By: Claude Fable 5.1 <noreply@anthropic.com>"
```

---

### Task 6: desvio em `investigar-empresa`

**Files:**
- Modify: `skills/investigar-empresa/SKILL.md`
- Modify: `skills/investigar-empresa/references/modelo-memo.md`

**Interfaces:**
- Consumes: Task 2 (roteamento), Task 3, Task 4.

- [ ] **Step 1: Subir a versão e a compatibilidade**

`version: "0.1"` → `version: "0.2"`. Em `compatibility`, trocar `Assume as skills
balancos-ai e indicadores-financeiros.` por `Assume as skills balancos-ai e
indicadores-financeiros; companhia-aberta e instituicao-financeira quando a empresa está
na CVM ou no BCB.`

- [ ] **Step 2: Roteamento nos passos**

Trocar o passo 2:

```
2. `analisar_empresa` com o slug. Uma chamada; não repita `ficha_empresa`,
   `balancos_empresa` e `dres_empresa` para a mesma empresa.
```

por:

```
2. `analisar_empresa` com o slug. Uma chamada; não repita `ficha_empresa`,
   `balancos_empresa` e `dres_empresa` para a mesma empresa. Depois, roteie pela skill
   balancos-ai: S.A. aberta, `cvm_analisar_companhia` com o CNPJ e siga a skill
   companhia-aberta; instituição financeira, `bcb_analisar_instituicao` com a raiz do
   CNPJ e siga a skill instituicao-financeira. Os números do memo vêm da fonte que achou;
   as publicações continuam para a seção 6.
```

Trocar o passo 3 inteiro por:

```
3. Classifique a natureza do dado antes de qualquer número. Na fonte publicações: CNAE
   64.62-0 ou 64.63-8, "participações" ou "holding" na descrição, receita líquida abaixo
   de 1% do ativo, ou lucro operacional acima do lucro bruto indicam holding ou
   controladora; a seção 5 mostra só ROE, alavancagem e tendência de PL e lucro, e a
   seção 7 diz que o número do grupo está no consolidado da publicação. Na CVM: use a visão
   consolidada e a regra de holding não se aplica. No BCB: use o nível padrão.
```

- [ ] **Step 3: Seção 2 do memo ganha fonte, visão e nível; seções 3 a 5 ganham variantes**

Trocar o item 2 da lista "Resultado":

```
2. **Natureza do dado**: se é entidade operacional ou holding, e por quê (CNAE, receita
   diante do ativo). Fonte por exercício (xbrl ou llm). Anos disponíveis de BP e DRE.
```

por:

```
2. **Natureza do dado**: fonte (publicações, CVM ou BCB); na CVM, família e visão; no
   BCB, nível e CodInst; nas publicações, se é entidade operacional ou holding e por quê
   (CNAE, receita diante do ativo) e a fonte por exercício (xbrl ou llm). Anos disponíveis.
```

Depois do item 5 (`**Rentabilidade e estrutura de capital**...`), acrescentar:

```
   Em companhia aberta, a seção 5 acrescenta EBITDA, dívida líquida, cobertura de juros e
   caixa operacional com o código da conta (skill companhia-aberta), e uma linha com o
   tipo do último parecer. Em instituição financeira, as seções 3, 4 e 5 viram: tamanho
   (ativo, carteira, captações, PL e Basileia na última data-base), trajetória (oito
   trimestres de ativo, carteira, captações, PL e lucro semestral, com a era) e
   rentabilidade (ROE anual, crescimento de carteira, Basileia, imobilização), tudo da
   skill instituicao-financeira.
```

- [ ] **Step 4: Acrescentar as variantes ao `references/modelo-memo.md`**

Acrescentar ao fim do arquivo:

````markdown

## Variante: companhia aberta (fonte CVM)

Substitui as seções "Natureza do dado", "Rentabilidade e estrutura de capital" e
"Ressalvas":

```
**Natureza do dado.** Companhia aberta (código CVM <n>), família <comercial>, visão
consolidada, última versão de cada exercício. DFP de <ano> a <ano>; <n> reapresentações.
Último parecer: <tipo> (<firma>, <data>).

**Rentabilidade e estrutura de capital (<ano>, consolidado, id_doc <n>).** Margem líquida
<x>%, ROE <x>% (3.11.01 / (2.03 − 2.03.09)), liquidez corrente <x>x, dívida bruta
R$ <x> bi (2.01.04 + 2.02.01), dívida líquida R$ <x> bi, EBITDA R$ <x> bi
(3.05 + |7.04.01|), dívida líquida / EBITDA <x>x, cobertura de juros <x>x
(3.05 / |3.06.02|, inclui variação cambial), caixa operacional R$ <x> bi (6.01).

**Ressalvas.** Sem ITR, valor de mercado ou notas estruturadas; notas no texto de <link>.
<Conhecimento geral, não confirmado na base: ...>. Dados do Balanços.AI (CVM) em <data>.
```

## Variante: instituição financeira (fonte BCB)

Substitui as seções "Natureza do dado", "Tamanho", "Trajetória", "Rentabilidade e
estrutura de capital" e "Ressalvas":

```
**Natureza do dado.** <Banco múltiplo | Cooperativa de crédito singular | ...>,
consolidado bancário <b1>, segmento <S2>. Nível <prudencial> (CodInst <n>), padrão da
instituição. Série de <AAAAMM> a <AAAAMM>; era COSIF 2025 a partir de 202503.

**Tamanho (<AAAAMM>).** Ativo R$ <x> bi · Carteira de crédito R$ <x> bi · Captações
R$ <x> bi · PL R$ <x> bi · Basileia <x>%.

**Trajetória (oito trimestres).**
| | <AAAAMM> | ... | <AAAAMM> |
|---|---|---|---|
| Ativo total (R$ bi) | | | |
| Carteira de crédito (R$ bi) | | | |
| Captações (R$ bi) | | | |
| Patrimônio líquido (R$ bi) | | | |
| Lucro acumulado no semestre (R$ mi) | | | |
| Basileia | | | |
<Quebra de era em 202503: variações contra 2024 não são comparáveis.>

**Rentabilidade e capital (<ano>).** ROE <x>% (lucro anual / PL de dezembro), carteira
<x>% do ativo, captações <x>% do ativo, crescimento de carteira em 12 meses <x>%,
Basileia <x>% (mínimo regulatório: de conhecimento geral, não confirmado na base),
imobilização <x>%.

**Ressalvas.** Sem parecer do auditor, notas explicativas ou DFC no IF.data; <se companhia
aberta: parecer na CVM>; demais no texto de <link>. Dados do Balanços.AI (BCB) em <data>.
```
````

- [ ] **Step 5: Rodar o checker**

Run: `python3 scripts/check.py`
Expected: `9 skills, 0 erros`.

- [ ] **Step 6: Commit**

```bash
git add skills/investigar-empresa
git commit -m "feat(investigar-empresa): roteamento por fonte e variantes de memo para companhia aberta e banco

Co-Authored-By: Claude Fable 5.1 <noreply@anthropic.com>"
```

---

### Task 7: desvio em `comparar-empresas`

**Files:**
- Modify: `skills/comparar-empresas/SKILL.md`

**Interfaces:**
- Consumes: Task 3 (ranking CVM, dívida líquida, EBITDA), Task 4 (ranking BCB, indicadores próprios).

- [ ] **Step 1: Subir a versão e a compatibilidade**

`version: "0.1"` → `version: "0.2"`. Em `compatibility`, trocar `Assume as skills
balancos-ai e indicadores-financeiros.` por `Assume as skills balancos-ai e
indicadores-financeiros; companhia-aberta e instituicao-financeira quando as empresas
estão na CVM ou no BCB.`

- [ ] **Step 2: Pares pelos rankings novos e retrato pela fonte certa**

No passo 1, depois de `Diga quantas empresas a base
   devolveu e que o teto é 50 por chamada.` acrescentar:

```
   Se a empresa-alvo é companhia aberta, os pares abertos vêm de
   `cvm_ranking_companhias` no exercício, com a mesma `familia` e `visao` (não há UF nem
   setor: corte por CNAE e UF pela `ficha_empresa`, e diga). Se é instituição financeira,
   os pares vêm de `bcb_ranking_instituicoes` com `uf`, `tipo` ou `consolidado_bancario`
   iguais, no nível padrão.
```

Trocar o passo 2:

```
2. `analisar_empresa` para cada uma, em paralelo.
```

por:

```
2. Retrato de cada uma, em paralelo, pela fonte que o roteamento da skill balancos-ai
   indicar: `analisar_empresa`, `cvm_analisar_companhia` ou `bcb_analisar_instituicao`.
```

- [ ] **Step 3: Regra de mesma fonte, família e visão**

Trocar o passo 4:

```
4. Classifique a natureza de cada dado (skill balancos-ai): holding, controladora ou
   operacional; fonte xbrl ou llm. Empresas do mesmo grupo (controladora e controlada)
   não somam nem competem: diga que são andares da mesma operação.
```

por:

```
4. Classifique a natureza de cada dado (skill balancos-ai): fonte (publicações, CVM ou
   BCB), família e visão na CVM, nível no BCB, holding ou operacional e xbrl ou llm nas
   publicações. **Na mesma tabela, mesma fonte, mesma família e mesma visão**: consolidado
   com consolidado, nunca consolidado de uma com individual de outra. Se uma está só nas
   publicações (individual) e a outra na CVM (consolidado), mostre a individual da CVM
   para igualar e diga o que se perde. Banco compara só com banco, pelas linhas da skill
   instituicao-financeira. Empresas do mesmo grupo (controladora e controlada) não somam
   nem competem: diga que são andares da mesma operação.
```

- [ ] **Step 4: Linhas novas na tabela**

Na tabela `## Tabela`, trocar a linha `| Natureza do dado | xbrl, individual, operacional | xbrl, individual, holding | llm, individual, operacional |` por
`| Natureza do dado | CVM, consolidado, comercial | CVM, consolidado, comercial | publicações, llm, individual, operacional |`.

Depois da linha `| Exigível no curto prazo | | | |` acrescentar:

```
| Dívida líquida (só CVM, com código) | | | não disponível |
| EBITDA (só CVM, 3.05 + \|7.04.01\|) | | | não disponível |
```

Depois do parágrafo `Valores em R$ mi ou bi, unidade no rótulo...` acrescentar:

```
Tabela de bancos: ativo total, carteira de crédito, captações, PL, lucro anual, ROE,
carteira sobre ativo, Basileia, na mesma data-base e no nível padrão de cada um, com a
era no cabeçalho (skill instituicao-financeira).
```

- [ ] **Step 5: Rodar o checker**

Run: `python3 scripts/check.py`
Expected: `9 skills, 0 erros`.

- [ ] **Step 6: Commit**

```bash
git add skills/comparar-empresas/SKILL.md
git commit -m "feat(comparar-empresas): mesma fonte, família e visão; pares pelos rankings da CVM e do BCB

Co-Authored-By: Claude Fable 5.1 <noreply@anthropic.com>"
```

---

### Task 8: desvio em `due-diligence-financeira`

**Files:**
- Modify: `skills/due-diligence-financeira/SKILL.md`
- Modify: `skills/due-diligence-financeira/references/roteiro-notas.md`

**Interfaces:**
- Consumes: Task 3 (parecer, DFC, reapresentações), Task 4 (trimestre recente).

- [ ] **Step 1: Subir a versão e a compatibilidade**

`version: "0.1"` → `version: "0.2"`. Em `compatibility`, trocar `Assume as skills
balancos-ai, indicadores-financeiros e ler-publicacao.` por `Assume as skills
balancos-ai, indicadores-financeiros e ler-publicacao; companhia-aberta e
instituicao-financeira quando a contraparte está na CVM ou no BCB.`

- [ ] **Step 2: Seção 3 ganha dívida e caixa; seção 4 ganha reapresentações; seção 5 começa pelo parecer**

No item 3 do "Resultado", depois de `variação de receita e
   lucro)` inserir `; em companhia aberta, também dívida bruta, dívida líquida, caixa
   operacional e juros pagos, com o código da conta; em banco, os indicadores da skill
   instituicao-financeira`.

No item 4, trocar `ausência de publicação recente.` por `ausência de publicação recente,
reapresentação de DFP (linha do tempo de entregas da CVM, com data e se o parecer mudou).`

No item 5, trocar `**O que o texto da publicação diz**: parecer do auditor (opinião,
   ênfase, ressalva),` por `**O que o parecer e o texto dizem**: em companhia aberta, o
   parecer vem estruturado de `cvm_parecer_dfp` (tipo, ênfase e continuidade lidas no
   texto, firma, data, e se a firma mudou entre exercícios); nas demais, parecer do
   auditor no texto da publicação (opinião, ênfase, ressalva);`.

No item 6, trocar `dado intra-ano. Se o
   último exercício tem mais de seis meses, diga quantos e inclua na seção 7 o pedido de
   balancete ou ITR recente.` por `dado intra-ano (exceto banco: o IF.data tem o
   trimestre mais recente, e ele entra na seção 3). Se o último exercício tem mais de
   seis meses, diga quantos e inclua na seção 7 o pedido de balancete ou ITR recente.`

- [ ] **Step 3: Passos**

Trocar o passo 2:

```
2. `analisar_empresa`. Classifique natureza do dado (holding ou operacional) e monte a
   série com a skill indicadores-financeiros, excluindo anomalias com nota.
```

por:

```
2. `analisar_empresa`, e depois o roteamento da skill balancos-ai: companhia aberta,
   `cvm_analisar_companhia` e o conta a conta de BPP, DRE e DFC do último exercício
   (skill companhia-aberta); banco, `bcb_analisar_instituicao` (skill
   instituicao-financeira). Classifique a natureza do dado e monte a série com a skill
   indicadores-financeiros, excluindo anomalias com nota.
```

Trocar o passo 4 (`4. Leia texto: ...`) para começar com:

```
4. Em companhia aberta, `cvm_parecer_dfp` da última entrega e da anterior antes de
   qualquer texto. Depois, leia texto: no índice de documentos, escolha a publicação mais
   recente com texto (jornal antes de DFP) e siga a skill ler-publicacao, com o roteiro em
```

mantendo o restante do passo como está.

- [ ] **Step 4: Coluna "Na CVM" no roteiro de notas**

Em `references/roteiro-notas.md`, trocar o cabeçalho da tabela
`| Item | Termos de busca | O que registrar |` e a linha separadora por
`| Item | Termos de busca | O que registrar | Na CVM (companhia aberta) |` e
`|---|---|---|---|`, e acrescentar a quarta coluna em cada linha:

| Item | Quarta coluna |
|---|---|
| Parecer do auditor | `cvm_parecer_dfp`: tipo estruturado; ênfase e continuidade no texto |
| Empréstimos e financiamentos | BPP 2.01.04 e 2.02.01 (saldo e parcela em 12 meses); DFC 6.03 (captações e pagamentos); covenant só no texto |
| Caixa | BPA 1.01.01 e 1.01.02 |
| Contingências | BPP 2.01.06 e 2.02.04 (provisionado); perda possível só no texto |
| Partes relacionadas | BPA 1.02.01.09, BPP 2.01.05.01 e 2.02.02.01 (saldos); garantias só no texto |
| Eventos subsequentes | só no texto |
| Reapresentação | linha do tempo de entregas (`reapresentacao`, data, parecer) |
| Não recorrentes | DRE 3.04.03, 3.04.04, 3.04.05, 3.10 |
| Continuidade | parecer (texto) e BP; plano só no texto |
| EBITDA e fluxo de caixa | DRE 3.05 + DVA 7.04.01; DFC 6.01; juros pagos em 6.01.03 ou 6.03 |

Acrescentar ao fim do arquivo:

```
Em companhia aberta, o que a quarta coluna aponta é proveniência 1 (da base): não precisa
do texto nem do rótulo "segundo a publicação". O que ela marca como "só no texto" segue o
roteiro normal.
```

- [ ] **Step 5: Rodar o checker**

Run: `python3 scripts/check.py`
Expected: `9 skills, 0 erros`.

- [ ] **Step 6: Commit**

```bash
git add skills/due-diligence-financeira
git commit -m "feat(due-diligence-financeira): parecer estruturado, dívida e caixa da CVM, trimestre do BCB

Co-Authored-By: Claude Fable 5.1 <noreply@anthropic.com>"
```

---

### Task 9: desvio em `originacao-ma`

**Files:**
- Modify: `skills/originacao-ma/SKILL.md`

**Interfaces:**
- Consumes: Task 3 (ranking CVM), Task 4 (ranking BCB).

- [ ] **Step 1: Subir a versão e a compatibilidade**

`version: "0.1"` → `version: "0.2"`. Em `compatibility`, trocar `Assume as skills
balancos-ai e indicadores-financeiros.` por `Assume as skills balancos-ai e
indicadores-financeiros; companhia-aberta e instituicao-financeira para alvos e
compradores abertos ou financeiros.`

- [ ] **Step 2: Rankings novos nos passos para alvos**

Depois do passo 2 dos "Passos para alvos" (o que termina em `rode
   por ativo também.`), inserir:

```
   Companhias abertas do setor: `cvm_ranking_companhias` por `receita` e por `ativo` no
   último exercício, `familia="comercial"`, `visao="consolidado"`, `limite=50`; não há
   UF nem setor, então cruze CNAE e UF pela `ficha_empresa` e diga que o corte foi do lado
   do agente. Instituições financeiras: `bcb_ranking_instituicoes` por `ativo` e por
   `carteira` com `uf`, `tipo` ou `consolidado_bancario`, no nível padrão; é o único
   ranking além do de publicações com filtro geográfico real, e cooperativas por UF saem
   com `tipo="9"`.
```

- [ ] **Step 3: Compradores bancários**

Depois do passo 3 dos "Passos para compradores" (`Ordene e diga o critério.`), inserir:

```
   Comprador financeiro (banco ou cooperativa central comprando carteira, financeira ou
   cooperativa): `bcb_ranking_instituicoes` por `patrimonio` e por `basileia` na UF e nas
   vizinhas; capacidade é PL e folga de Basileia (skill instituicao-financeira). Comprador
   aberto: `cvm_ranking_companhias` por `patrimonio`, e caixa 1.01.01 mais dívida líquida
   do conta a conta como capacidade (skill companhia-aberta).
```

- [ ] **Step 4: Regras**

Na seção `## Regras`, depois da regra que começa com `Não há filtro por faixa de receita`,
acrescentar:

```
- Alvo companhia aberta: a tese ganha EBITDA, dívida líquida e caixa operacional do conta
  a conta (skill companhia-aberta), com o código; "vale a pena" continua fora, porque
  falta valor de mercado.
```

- [ ] **Step 5: Rodar o checker**

Run: `python3 scripts/check.py`
Expected: `9 skills, 0 erros`.

- [ ] **Step 6: Commit**

```bash
git add skills/originacao-ma/SKILL.md
git commit -m "feat(originacao-ma): alvos e compradores pelos rankings da CVM e do BCB

Co-Authored-By: Claude Fable 5.1 <noreply@anthropic.com>"
```

---

### Task 10: desvio em `ler-publicacao`

**Files:**
- Modify: `skills/ler-publicacao/SKILL.md`

**Interfaces:**
- Consumes: Task 3 (parecer e conta a conta).

- [ ] **Step 1: Subir a versão e a compatibilidade**

`version: "0.1"` → `version: "0.2"`. Em `compatibility`, trocar `Assume a skill
balancos-ai.` por `Assume a skill balancos-ai; companhia-aberta quando a empresa está na
CVM.`

- [ ] **Step 2: Atalhos pela CVM no passo 2**

No passo 2, trocar o sub-item:

```
   - "Demonstrações Financeiras Padronizadas" (DFP, CVM) costuma vir "texto ainda não
     extraído";
```

por:

```
   - "Demonstrações Financeiras Padronizadas" (DFP, CVM) costuma vir "texto ainda não
     extraído". Se a empresa é companhia aberta, o que a DFP tem de estruturado não
     precisa de texto: parecer do auditor em `cvm_parecer_dfp` (tipo, texto integral,
     declarações dos diretores) e demonstrações conta a conta em `cvm_demonstracoes_dfp`
     (skill companhia-aberta). Notas explicativas e relatório da administração continuam
     só no texto da publicação em jornal;
```

- [ ] **Step 3: Regra**

Na seção `## Regras`, acrescentar antes de `- "Principais assuntos de auditoria" não é
ressalva nem ênfase.`:

```
- "Tem ressalva do auditor" em companhia aberta vai direto em `cvm_parecer_dfp` do
  `id_doc` do exercício; o texto integral vem inteiro, sem o corte de 50 mil caracteres.
```

- [ ] **Step 4: Rodar o checker**

Run: `python3 scripts/check.py`
Expected: `9 skills, 0 erros`.

- [ ] **Step 5: Commit**

```bash
git add skills/ler-publicacao/SKILL.md
git commit -m "feat(ler-publicacao): parecer e conta a conta pela CVM quando a DFP não tem texto

Co-Authored-By: Claude Fable 5.1 <noreply@anthropic.com>"
```

---

### Task 11: README, plugin e evals

**Files:**
- Modify: `README.md`
- Modify: `.claude-plugin/plugin.json`
- Create: `evals/companhia-aberta.md`
- Create: `evals/instituicao-financeira.md`
- Modify: `evals/balancos-ai.md`, `evals/investigar-empresa.md`, `evals/comparar-empresas.md`, `evals/due-diligence-financeira.md`, `evals/originacao-ma.md`, `evals/ler-publicacao.md`, `evals/indicadores-financeiros.md`

**Interfaces:**
- Consumes: Tasks 2 a 10 (nomes das skills e regras que os evals testam).

- [ ] **Step 1: README, tabela de skills**

Na tabela `## Skills`, acrescentar depois da linha da `balancos-ai`:

```
| [`companhia-aberta`](skills/companhia-aberta/) | Empresa é S.A. aberta: consolidado, conta a conta, DFC, EBITDA, dívida líquida, parecer, reapresentação, ranking de abertas. |
| [`instituicao-financeira`](skills/instituicao-financeira/) | Empresa é banco, cooperativa ou financeira: carteira, captações, Basileia, trimestre, conglomerado, ranking do IF.data. |
```

- [ ] **Step 2: README, seção "Três fontes" antes de "## Instalar"**

Inserir:

```
## Três fontes num MCP só

| Fonte | Tools | Quem | O que traz |
|---|---|---|---|
| Publicações | `buscar_empresas`, `analisar_empresa`, `texto_documento`, `ranking_empresas`... | qualquer empresa com publicação legal | BP de 8 linhas, DRE de 6, individual, texto das publicações |
| CVM | `cvm_*` | companhias abertas com DFP (2010 em diante) | consolidado e individual, conta a conta com DFC e DVA, parecer do auditor, reapresentações |
| BCB | `bcb_*` | instituições financeiras do IF.data (2000 em diante) | série trimestral, carteira, captações, Basileia, conglomerados |

A skill `balancos-ai` ensina a rotear pelo CNPJ; `companhia-aberta` e
`instituicao-financeira` ensinam cada fonte; as skills de tarefa usam a fonte certa.
```

- [ ] **Step 3: README, "O que as skills não fazem" e "Limitações conhecidas"**

Trocar o segundo item de "O que as skills não fazem":

```
- Não inventam o que a base não tem. Fluxo de caixa, EBITDA, dívida líquida e
  cobertura de juros não vêm em campo estruturado; as skills ensinam a buscar isso
  no texto das publicações e a declarar quando não encontrou.
```

por:

```
- Não inventam o que a base não tem. Para companhia aberta, fluxo de caixa, EBITDA,
  dívida líquida e cobertura de juros vêm do conta a conta da CVM, com o código da conta;
  para as demais, as skills ensinam a buscar isso no texto das publicações e a declarar
  quando não encontrou.
```

Substituir a seção `## Limitações conhecidas` inteira por:

```
## Limitações conhecidas

As skills são escritas em cima do que o MCP entrega hoje, e dizem isso ao usuário.

Fonte publicações:

- Balanço com 8 linhas e DRE com 6, sempre da entidade individual (sem consolidado).
- Texto de publicação limitado aos primeiros 50 mil caracteres; parecer do auditor e
  notas explicativas costumam ficar fora, e a skill aponta o link do documento.
- Ranking com até 50 empresas por chamada, sem filtro por faixa de receita.
- Rótulo de setor por seção CNAE, com alguns rótulos herdados.

Fonte CVM:

- Só companhias abertas com DFP, de 2010 em diante; sem ITR trimestral.
- Ranking por exercício e família, sem filtro por UF ou setor.
- Notas explicativas continuam só no texto da publicação.

Fonte BCB:

- Busca por nome sofre com fundos de investimento e nomes fantasia; a raiz do CNPJ
  resolve.
- Lucro publicado acumulado no semestre; quebra de era contábil em março de 2025.
- Sem parecer, notas ou DFC.

Em todas: valor de mercado, quadro societário, notas estruturadas, paginação.
```

- [ ] **Step 4: plugin.json**

Trocar a `description` por: `"Skills para investigar empresas brasileiras, comparar
concorrentes, fazer due diligence financeira, originar M&A, ler publicações e analisar
companhias abertas (CVM) e instituições financeiras (BCB) com o MCP do Balanços.AI."`

Em `keywords`, acrescentar `"cvm"`, `"bcb"`, `"dfp"`, `"ifdata"`, `"bancos"`.

- [ ] **Step 5: Criar `evals/companhia-aberta.md`**

```markdown
# Eval: companhia-aberta

## Cenário 1: consolidado versus individual

**Prompt**: "Que tamanho tem a Gerdau S.A. e quanto ela faturou em 2025?"

**Baseline (sem skill)**: usou `analisar_empresa` (publicações), viu receita de R$ 4,8 bi
e lucro operacional acima do bruto, chamou de holding e explicou equivalência.

**Esperado com a skill**: roteia pela natureza jurídica, chama `cvm_analisar_companhia`
com o CNPJ, responde com o consolidado de 2025 (receita de R$ 69,9 bi, ativo de
R$ 81,7 bi), diz a visão e o `id_doc`, e menciona o individual só como "entidade".

## Cenário 2: EBITDA e dívida líquida com código

**Prompt**: "Qual o EBITDA, a dívida líquida e a cobertura de juros da Gerdau em 2025?"

**Baseline**: disse que a base não tem depreciação e mandou ler o texto.

**Esperado**: `cvm_demonstracoes_dfp` de `dre`, `dva`, `bpa` e `bpp` (uma por chamada),
EBITDA = 3.05 + |7.04.01|, dívida bruta = 2.01.04 + 2.02.01, dívida líquida descontando
1.01.01 e 1.01.02, cobertura = 3.05 / |3.06.02| com a ressalva de variação cambial; cada
número com o código ao lado e o link da entrega.

## Cenário 3: parecer com ênfase

**Prompt**: "O auditor da <companhia com ênfase> fez alguma ressalva ou ênfase?"

**Baseline**: leu o preview do texto da publicação, disse "não localizado".

**Esperado**: `cvm_parecer_dfp` do `id_doc` do último exercício; cita o tipo estruturado,
procura "ênfase" e "continuidade" no texto, cita a firma e a data; diz que PAA não é
ressalva.

## Cenário 4: reapresentação

**Prompt**: "A Gerdau reapresentou alguma DFP nos últimos anos? O que mudou?"

**Baseline**: não sabia dizer.

**Esperado**: lê `exercicios[].versoes[]`, lista 2024 (v1 sem parecer, v2 cinco dias
depois "Sem Ressalva"), 2017, 2013 e 2011; diz que a v2 de 2024 pode ser só a inclusão do
parecer; para dizer se número mudou, compara `valor_atual` das duas versões pelo conta a
conta ou diz que não comparou.

## Cenário 5: ranking com grupo duplicado

**Prompt**: "Quais as cinco maiores companhias abertas por receita em 2025?"

**Baseline**: usou `ranking_empresas` de publicações, misturando individual e fechadas.

**Esperado**: `cvm_ranking_companhias(receita, 2025)`; percebe JBS S.A. e JBS N.V. com a
mesma receita, deduplica e diz; declara visão consolidada, família e que o teto é 50.
```

- [ ] **Step 6: Criar `evals/instituicao-financeira.md`**

```markdown
# Eval: instituicao-financeira

## Cenário 1: achar o banco

**Prompt**: "Como está o Banrisul?"

**Baseline (sem skill)**: `bcb_buscar_instituicoes("Banrisul")` devolveu 20 fundos;
tentou com tipo 8 e não achou; desistiu ou usou só as publicações.

**Esperado com a skill**: obtém o CNPJ (por `buscar_empresas` ou conhecimento) e busca
pela raiz 92702067; `bcb_analisar_instituicao`; memo de banco com ativo, carteira,
captações, PL, Basileia na última data-base, nível prudencial e CodInst declarados.

## Cenário 2: nível prudencial versus individual

**Prompt**: "Qual o ativo total do Banrisul, o banco só, sem as controladas?"

**Baseline**: deu o número do prudencial.

**Esperado**: `bcb_trimestres_instituicao` com `nivel="individual"`; diz que o padrão da
instituição é o prudencial e que o individual exclui a corretora e a instituição de
pagamento (membros em `bcb_conglomerado`).

## Cenário 3: lucro semestral versus anual

**Prompt**: "Quanto o Banrisul lucrou em 2025?"

**Baseline**: somou os quatro `lucro_liquido_acumulado_semestre` ou usou só dezembro.

**Esperado**: usa `resultados_anuais` de 2025 com `completo: true`; explica que o IF.data
publica acumulado no semestre e que anual = junho + dezembro.

## Cenário 4: quebra de era

**Prompt**: "A carteira de crédito do Banrisul cresceu quanto de março de 2024 para março
de 2026?"

**Baseline**: calculou a variação sem ressalva.

**Esperado**: calcula, mas marca a quebra de era (COSIF 2000 até 202412, COSIF 2025
depois) e diz que parte da variação pode ser reclassificação contábil; `comparavel` do
relatório é a referência.

## Cenário 5: cooperativas por UF

**Prompt**: "Quais as maiores cooperativas de crédito do Paraná?"

**Baseline**: usou `ranking_empresas` com setor "Atividades Financeiras" e UF PR,
misturando bancos e holdings.

**Esperado**: `bcb_ranking_instituicoes(ativo, uf="PR", tipo="9")` no nível padrão; diz
a data-base, o N e que sistemas (Sicredi, Sicoob) aparecem por cooperativa singular.

## Cenário 6: para quem o banco empresta

**Prompt**: "Para que setores o Banrisul mais empresta?"

**Baseline**: não sabia.

**Esperado**: `bcb_estrutura_relatorios` da última data-base para confirmar o id, depois
`bcb_relatorios_instituicao` com `relatorio=129` (PJ por CNAE); tabela com as maiores
linhas, valor em reais, `valor_ano_anterior` quando comparável, nível e data-base.
```

- [ ] **Step 7: Cenários novos nos evals existentes**

Acrescentar ao fim de cada arquivo:

`evals/balancos-ai.md`:

```
## Cenário novo: empresa nas três fontes

**Prompt**: "Me dá um panorama do Banco do Estado do Rio Grande do Sul."

**Esperado**: `buscar_empresas`, percebe S.A. aberta e CNAE 64.22, busca na CVM pelo CNPJ e
no BCB pela raiz; diz qual fonte responde o quê (BCB para carteira e trimestre, CVM para
parecer, publicações para texto); cita o `dados_atualizados_em` de cada fonte.
```

`evals/investigar-empresa.md`:

```
## Cenário novo: companhia aberta

**Prompt**: "Me conta sobre a Gerdau S.A."

**Esperado**: memo na variante CVM: natureza do dado com código CVM, família e visão
consolidada; tamanho e trajetória consolidados; seção 5 com EBITDA, dívida líquida,
cobertura e caixa operacional com código; tipo do último parecer.

## Cenário novo: banco

**Prompt**: "Me conta sobre a Cooperativa de Economia e Crédito Mútuo dos Empregados do
Banrisul."

**Esperado**: memo na variante BCB, nível individual (cooperativa singular, b3S), oito
trimestres, ROE anual, Basileia com o mínimo rotulado como conhecimento geral.
```

`evals/comparar-empresas.md`:

```
## Cenário novo: aberta com fechada

**Prompt**: "Compara a Gerdau S.A. com a Gerdau Aços Longos."

**Esperado**: percebe que são andares do mesmo grupo; se comparar, iguala a visão
(individual da CVM contra individual das publicações) e diz o que se perde; não põe
consolidado de uma contra individual da outra.

## Cenário novo: bancos

**Prompt**: "Banrisul versus Banco do Brasil: quem é maior e mais rentável?"

**Esperado**: tabela de bancos (ativo, carteira, captações, PL, lucro anual, ROE, Basileia)
na mesma data-base e no nível padrão; BB via `bcb_conglomerado` para o link; sem liquidez
corrente nem margem bruta.
```

`evals/due-diligence-financeira.md`:

```
## Cenário novo: contraparte aberta

**Prompt**: "Vou vender a prazo para a Gerdau S.A.; que risco eu corro?"

**Esperado**: seção 5 abre com `cvm_parecer_dfp` (tipo, firma, data, ênfase); seção 3
com dívida bruta, caixa e caixa operacional com código; seção 4 lista as reapresentações
da linha do tempo; nada de nota ou semáforo.

## Cenário novo: contraparte banco

**Prompt**: "Vou deixar um depósito grande no <banco médio>; como ele está?"

**Esperado**: indicadores da skill instituicao-financeira, trimestre mais recente na
seção 3 (sem pedir balancete), Basileia com mínimo rotulado; sem "pode confiar".
```

`evals/originacao-ma.md`:

```
## Cenário novo: cooperativas alvo

**Prompt**: "Mapeia cooperativas de crédito no Rio Grande do Sul que podem ser alvo de
incorporação."

**Esperado**: `bcb_ranking_instituicoes` por ativo e carteira com `uf="RS"` e `tipo="9"`;
tese por PL, Basileia e crescimento de carteira; diz o N e a data-base.

## Cenário novo: compradores abertos

**Prompt**: "Quem poderia comprar a <companhia aberta do setor X>?"

**Esperado**: `cvm_ranking_companhias` por patrimônio na família comercial, cruzando CNAE
pela ficha; capacidade por caixa e dívida líquida do conta a conta.
```

`evals/ler-publicacao.md`:

```
## Cenário novo: parecer de companhia aberta

**Prompt**: "Tem ressalva do auditor na DFP 2025 da Gerdau?"

**Esperado**: `cvm_parecer_dfp` do `id_doc` de 2025, sem tentar `texto_documento` da DFP;
tipo, firma e data; PAA não é ressalva.
```

`evals/indicadores-financeiros.md`:

```
## Cenário novo: EBITDA de companhia aberta

**Prompt**: "Calcula o EBITDA e a dívida líquida / EBITDA da Gerdau nos últimos três
anos."

**Esperado**: reconhece que na CVM é computável, remete à skill companhia-aberta, usa
3.05 + |7.04.01| e dívida bruta − caixa − aplicações, um `id_doc` por exercício, visão
consolidada.

## Cenário novo: banco

**Prompt**: "Qual a liquidez corrente e a margem bruta do Banrisul?"

**Esperado**: diz que esses indicadores não se aplicam a banco, oferece carteira sobre
ativo, captações, Basileia e margem de intermediação (skill instituicao-financeira).
```

- [ ] **Step 8: Rodar o checker**

Run: `python3 scripts/check.py`
Expected: `9 skills, 0 erros`.

- [ ] **Step 9: Commit**

```bash
git add README.md .claude-plugin/plugin.json evals
git commit -m "docs: três fontes no README, plugin e evals das skills novas

Co-Authored-By: Claude Fable 5.1 <noreply@anthropic.com>"
```

---

## Verificação final

- [ ] `python3 scripts/check.py` → `9 skills, 0 erros`.
- [ ] `grep -rn "version: \"0.1\"" skills/` → vazio.
- [ ] `grep -rln "bcb.gov.br\|rad.cvm.gov.br" skills/` → vazio.
- [ ] `git log --oneline main..HEAD` → 12 commits (spec, plano e um por task).
- [ ] Rodar manualmente os cenários 1 e 2 de `evals/companhia-aberta.md` e 1 e 3 de
      `evals/instituicao-financeira.md` com o MCP conectado e registrar o resultado no
      próprio arquivo de eval.
