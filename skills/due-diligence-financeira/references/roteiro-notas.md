# Roteiro de leitura das notas explicativas

O que procurar no texto da publicação, com termos de busca. Cite o trecho curto e o link;
o que não aparecer no trecho disponível fica marcado como não localizado.

| Item | Termos de busca | O que registrar | Na CVM (companhia aberta) |
|---|---|---|---|
| Parecer do auditor | "opini", "ressalva", "ênfase", "principais assuntos", "incerteza relevante", "continuidade operacional", nome da firma de auditoria | tipo de opinião; ênfases e ressalvas literais; PAA não é ressalva; troca de auditor entre anos | `cvm_parecer` da DFP: tipo estruturado; ênfase e continuidade no texto |
| Empréstimos e financiamentos | "empréstim", "inanciament", "debênture", "notas comerciais", "vencimento", "covenant", "cláusulas restritivas" | saldo total, parcela em 12 meses, captações e pagamentos na DFC, covenant citado e se foi cumprido | BPP 2.01.04 e 2.02.01 do ITR mais recente, ou da DFP (saldo e parcela em 12 meses); DFC 6.03 (captações e pagamentos); covenant só no texto |
| Caixa | "caixa e equivalentes", "aplicações financeiras" | saldo; dívida bruta menos caixa, os dois citados, vira "dívida líquida aproximada, segundo a publicação" | BPA 1.01.01 e 1.01.02 |
| Contingências | "conting", "provis", "perda provável", "perda possível", "depósit" | provisionado × possível; natureza (tributária, cível, trabalhista); depósitos judiciais | BPP 2.01.06 e 2.02.04 (provisionado); perda possível só no texto |
| Partes relacionadas | "partes relacionadas", "mútuo", "controladora", "coligada", "grupo econômico" | saldos a receber e a pagar, garantias cruzadas, garantia da controladora | BPA 1.02.01.09, BPP 2.01.05.01 e 2.02.02.01 (saldos); garantias só no texto |
| Eventos subsequentes | "subsequente" | qualquer item; aquisições, dívidas novas, reestruturações | só no texto |
| Reapresentação | "reapresent", "correção de erro" | o que foi reapresentado e o efeito | linha do tempo de entregas (`reapresentacao`, data, parecer) |
| Não recorrentes | "não recorrente", "impairment", "valor recuperável", "reversão de provis", "outras receitas" | valor e se explica o lucro operacional acima do bruto | DRE 3.04.03, 3.04.04, 3.04.05, 3.10 |
| Continuidade | "capital circulante líquido negativo", "plano de capitalização", "recuperação judicial", "obrigações de curto prazo" | citação literal | parecer (texto) e BP; plano só no texto |
| EBITDA e fluxo de caixa | "EBITDA", "geração de caixa", "atividades operacionais", "pagamentos de juros", "depreciação" (DVA) | valor divulgado pela empresa no relatório da administração, na DFC ou na DVA, sempre com "segundo a empresa" | DRE 3.05 + DVA 7.04.01; DFC 6.01; juros pagos em 6.01.03 ou 6.03 |

Use radicais, não expressões fechadas: a extração perde a ligadura "fi" ("inanceiro") e
alterna singular e plural.

O parecer do auditor e as notas ficam no fim do documento (relatório da administração,
BP, DRE, DMPL, DVA, DFC, notas, relatório do auditor). Cada linha da tabela é uma busca
por `termo` em `texto_documento`, um termo por chamada; o entorno de um trecho se lê com
`inicio` na posição devolvida. O relatório da administração traz pistas (itens não
recorrentes, dívida, EBITDA divulgado) e serve como fonte citável. Assunto sem ocorrência
em dois termos fica marcado como não encontrado no documento, com o link.

Em companhia aberta, o que a quarta coluna aponta é proveniência 1 (da base): não precisa
do texto nem do rótulo "segundo a publicação". O que ela marca como "só no texto" segue o
roteiro normal.
