# importar as bibliotecas
import streamlit as st
from mapa import carregar_dados
import altair as alt
import pandas as pd

# saeb 2011 - 2021
dados = carregar_dados('Base_SAEB')

# Garantir que a coluna desempenho_aluno_contagem seja numérica
dados['desempenho_aluno_contagem'] = pd.to_numeric(dados['desempenho_aluno_contagem'], errors='coerce')

st.write('''
# SAEB
''')

#filtros
anos = st.slider(
    "Selecione o Intervalo de Anos",
    min_value=int(dados['ano'].min()),
    max_value=int(dados['ano'].max()),
    value=(int(dados['ano'].min()), int(dados['ano'].max()))  # Default to full range
)

disciplinas = st.selectbox("Selecione a Disciplina", dados['disciplina'].unique())
desempenho = st.selectbox("Selecione a faixa de Desempenho", dados['desempenho_aluno'].unique())
series = st.selectbox("Selecione a serie", dados['serie'].unique())
if isinstance(series, (int, str)):
    series = [series]

#st.write("Anos:", anos)
#st.write("Disciplinas:", disciplinas)
#st.write("Desempenho:", desempenho)
#st.write("Séries:", series)


dados_filtrados = dados.query("serie in @series")

# Calcular total de estudantes por ano, disciplina e raça/cor antes do filtro
dados_totais = (
    dados.groupby(['ano', 'disciplina', 'raca_cor'])['desempenho_aluno_contagem']
    .sum() / 2
    .reset_index()
    .rename(columns={'desempenho_aluno_contagem': 'total_estudantes'})
)

# Verificar alunos únicos vs. registros
st.write("Total de registros:", len(dados))
st.write("Alunos únicos:", dados['id_unico'].nunique())

# Checar totais
st.write("Totais calculados:", dados_totais)

# Agora filtrar pelos outros critérios (ano, disciplina, desempenho)
dados_filtrados = dados_filtrados_serie.query(
    "ano >= @anos[0] and ano <= @anos[1] and "
    "disciplina in @disciplinas and desempenho_aluno in @desempenho"
)

# Juntar com o total de estudantes correspondente
dados_merged = dados_filtrados.merge(
    dados_totais, 
    on=['ano', 'disciplina', 'raca_cor'], 
    how='left'
)

st.write("Contagem de estudantes por filtro:")
st.write(dados_filtrados.groupby(['ano', 'disciplina', 'raca_cor'])['desempenho_aluno_contagem'].sum())

# Calcular percentual
# Garantir que o percentual seja calculado corretamente
dados_merged['percentual'] = (
    dados_merged['desempenho_aluno_contagem'] / dados_merged['total_estudantes'] * 100
)

st.write("Exemplo de linhas mescladas (amostra):")
st.write(dados_merged.sample(5)[['ano', 'disciplina', 'raca_cor', 'desempenho_aluno', 
                               'desempenho_aluno_contagem', 'total_estudantes', 'percentual']])

# Verificar se a coluna foi criada corretamente
st.write("Verificação de consistência:")
st.write("Soma de percentuais por grupo:", 
         dados_merged.groupby(['ano', 'disciplina', 'raca_cor'])['percentual'].sum())


# Criar gráfico corrigido
grafico_evolucao = alt.Chart(dados_merged).mark_line(point=True).encode(
    x='ano:O',
    y=alt.Y('percentual:Q', title='Percentual de Estudantes (%)'),
    color='raca_cor:N',
    tooltip=['ano', 'disciplina', 'raca_cor', 'percentual:Q']
).properties(title="Evolução Percentual das Notas por Raça/Cor")

st.altair_chart(grafico_evolucao, use_container_width=True)
