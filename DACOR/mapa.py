# importar as bibliotecas
import streamlit as st
import pandas as pd
import altair as alt


@st.cache_data
def carregar_dados(base):
    """Load data from local CSV files in the 'data' folder."""
    try:
        file_path = f"mapadedados/DACOR/data/{base}.csv"  # Assuming files are named like 'Base_SAEB.csv'
        df = pd.read_csv(file_path)
        return df
    except FileNotFoundError:
        st.error(f"File '{base}.csv' not found in the 'data' folder.")
        return pd.DataFrame()
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return pd.DataFrame()


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

