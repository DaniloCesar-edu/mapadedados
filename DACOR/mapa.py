# importar as bibliotecas
import streamlit as st
import pandas as pd
import altair as alt
import gspread
from google.oauth2 import service_account


# criar as funções de carregamento de dados
# Configuração de autenticação
credentials = service_account.Credentials.from_service_account_file(
    'credentials.json',
    scopes=["https://www.googleapis.com/auth/spreadsheets",
            "https://www.googleapis.com/auth/drive"]
)

# Acessando a planilha
gc = gspread.authorize(credentials)
planilha = gc.open("Bases_Mapa_de_Dados")

@st.cache_data
def carregar_dados(base):
    aba = planilha.worksheet(base)
    df = pd.DataFrame(aba.get_all_records())
    return df


st.title("""
Mapa de Dados
""")

# criar a interface do streamlit
paginas = st.navigation(
    {
        'Início': [st.Page('dacor.py', title='DACOR'), st.Page('mapadedados.py', title='Mapa de Dados')],
        'Indicadores': [st.Page('saeb.py', title='SAEB'), st.Page('enem.py', title='ENEM')],
        'Relatórios': []
    }
)

paginas.run()

