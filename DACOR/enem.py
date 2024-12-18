# importar as bibliotecas
import streamlit as st
from mapa import carregar_dados
import altair as alt

# enem 2010 - 2022
dados = carregar_dados('Base_ENEM')
#print(dados_enem.head())

# Calcular total de estudantes por ano, disciplina e raça/cor antes do filtro
dados_totais = (
    dados.groupby(['ano', 'disciplina', 'raca_cor'])['cont_nota']
    .sum()
    .reset_index()
    .rename(columns={'cont_nota': 'total_estudantes'})
)

#filtros
anos = st.slider(
    "Selecione o Intervalo de Anos",
    min_value=int(dados['ano'].min()),
    max_value=int(dados['ano'].max()),
    value=(int(dados['ano'].min()), int(dados['ano'].max()))
)
disciplinas = st.selectbox("Selecione a Disciplina", dados['disciplina'].unique())
notas = st.selectbox("Selecione a faixa de Notas", dados['nota'].unique())

dados_filtrados = dados.query(
    "ano >= @anos[0] and ano <= @anos[1] and "
    "disciplina in @disciplinas and nota in @notas"
)

# Juntar com o total de estudantes correspondente
dados_merged = dados_filtrados.merge(
    dados_totais, 
    on=['ano', 'disciplina', 'raca_cor'], 
    how='left'
)
#st.write(dados_totais.head())
# Calcular percentual
# Garantir que o percentual seja calculado corretamente
dados_merged['percentual'] = (
    dados_merged['cont_nota'] / dados_merged['total_estudantes'] * 100
)

# Verificar se a coluna foi criada corretamente
#st.write(dados_merged.head())

# criar gráficos
grafico_evolucao = alt.Chart(dados_merged).mark_line(point=True).encode(
    x='ano:O',
    y=alt.Y('percentual:Q', title='Percentual de Estudantes (%)'),
    color='raca_cor:N',
    tooltip=['ano', 'disciplina', 'raca_cor', 'nota', 'percentual']
).properties(title="Evolução das Notas por Raça/Cor")

st.altair_chart(grafico_evolucao, use_container_width=True)

notas_selecionadas = st.multiselect("Selecione as Notas", dados['nota'].unique(), default=dados['nota'].unique())

# Filtrar os dados
dados_notas = dados.query(
    "disciplina == @disciplinas and nota in @notas_selecionadas"
)

# Calcular o percentual por raca_cor e nota
dados_notas['total_por_nota'] = dados_notas.groupby('nota')['cont_nota'].transform('sum')
dados_notas['percentual'] = (dados_notas['cont_nota'] / dados_notas['total_por_nota']) * 100

# Ordem personalizada para o eixo X
ordem_notas = [
    "Sem nota", 
    "Abaixo de 400", 
    "Entre 500 e 400", 
    "Entre 600 e 500", 
    "Entre 700 e 600", 
    "Entre 800 e 700", 
    "Acima de 800"
]

# Gráfico de barras empilhadas com percentual
grafico_notas_raca = alt.Chart(dados_notas).mark_bar().encode(
    x=alt.X('nota:N', 
            title='Nota',
            sort=ordem_notas),  # Definir a ordem personalizada
    y=alt.Y('sum(percentual):Q', title='Percentual (%)'),
    color=alt.Color('raca_cor:N', title='Raça/Cor'),
    tooltip=['nota', 'raca_cor', 'sum(percentual):Q']
).properties(
    title=f"Comparação Percentual de Notas por Raça/Cor ({disciplinas})"
)

st.altair_chart(grafico_notas_raca, use_container_width=True)
