# Modelo de memo

```
## <Razão social> (<CNPJ>)

**Identidade.** S.A. aberta, CNAE <código> (<descrição>), <município>/<UF>, situação
<situação>. Setor na base: <setor>. Página: <link>.

**Natureza do dado.** Demonstrações individuais (não consolidadas), fonte <xbrl|llm>.
<Entidade operacional | Holding: receita de R$ X diante de ativo de R$ Y; lucro vem de
equivalência patrimonial>. BP de <ano> a <ano>; DRE de <ano> a <ano>.

**Tamanho (<ano>).** Ativo R$ <x> bi · PL R$ <x> bi · Receita líquida R$ <x> mi · Lucro
líquido R$ <x> mi.

**Trajetória.**
| | <ano-4> | <ano-3> | <ano-2> | <ano-1> | <ano> |
|---|---|---|---|---|---|
| Ativo total (R$ mi) | | | | | |
| Patrimônio líquido (R$ mi) | | | | | |
| Receita líquida (R$ mi) | | | | | |
| Lucro líquido (R$ mi) | | | | | |
| Var. receita (holding: var. ativo, PL e lucro) | | | | | |
<Exercício <ano> excluído: <motivo>, ver <link>.>

**Rentabilidade e estrutura de capital (<ano>).** Margem líquida <x>%, ROE <x>%, liquidez
corrente <x>x, passivo exigível / ativo <x>%, <x>% do exigível no curto prazo. <Uma
frase de leitura.> <Holding: só ROE, exigível / PL e tendência de PL e lucro; "margens,
giro e liquidez não descrevem a operação, que está nas controladas".>

**Publicações.** <N> na base; mais recentes: <tipo>, <data>, <link>; ...

**Ressalvas.** Sem consolidado, dívida financeira, caixa, fluxo de caixa ou EBITDA em
campo estruturado; estão no texto de <link>. <Conhecimento geral, não confirmado na
base: ...>. Dados do Balanços.AI em <data>.

**Em uma frase.** <...>
```

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
