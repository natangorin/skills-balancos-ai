# Rótulos de setor

O campo `setor` (ficha, ranking) é o nome da seção CNAE da atividade principal. O filtro
`setor` do `ranking_empresas` casa por trecho do nome, sem acento obrigatório, então
"Eletricidade" ou "Transporte" bastam.

| Setor | Seção CNAE |
|---|---|
| Agropecuária | A |
| Indústrias Extrativas | B |
| Indústrias de Transformação | C (siderurgia, alimentos, química, automotivo...) |
| Eletricidade e Gás | D (geração, transmissão, distribuição, comercialização, gás) |
| Água, Esgoto e Resíduos | E |
| Construção | F |
| Comércio | G |
| Transporte e Armazenagem | H |
| Alojamento e Alimentação | I |
| Informação e Comunicação | J |
| Atividades Financeiras | K (bancos, seguradoras e **holdings**) |
| Atividades Imobiliárias | L |
| Atividades Profissionais | M |
| Atividades Administrativas | N |
| Administração Pública | O |
| Educação | P |
| Saúde e Serviços Sociais | Q |
| Artes, Cultura e Recreação | R |
| Outras Atividades de Serviços | S |

Algumas empresas trazem rótulos herdados de fontes antigas ("Energia Elétrica", "Energia",
"Saúde"). Por isso "energia" devolve poucas empresas e "Eletricidade" devolve o setor
inteiro. Na dúvida, rode o ranking sem `setor` para a UF e leia a coluna `setor` das
linhas, ou use os dois rótulos e junte.

Não há setor por subclasse (geração × distribuição, siderurgia × alimentos): o corte fino
é pelo `cnae_principal` e `cnae_descricao` da ficha de cada empresa.
