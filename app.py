import streamlit as st
import pandas as pd
import requests
from ai_job_data import AIJobData
from ai_job_visuals import AIJobVisualizations

# --- FUNÇÃO PARA BUSCAR VAGAS NA API ---
@st.cache_data(show_spinner=False)
def buscar_vagas(query="data science", location="brazil", pages=1):
    url = "https://jsearch.p.rapidapi.com/search"
    headers = {
        "X-RapidAPI-Key": "4b38fd911dmsh0ef1ed5de02cff1p1c7613jsn43f872b0da18",
        "X-RapidAPI-Host": "jsearch.p.rapidapi.com"
    }
    params = {
        "query": query,
        "location": location,
        "page": 1,
        "num_pages": pages
    }
    response = requests.get(url, headers=headers, params=params)

    if response.status_code == 200:
        data = response.json().get("data", [])
        if not data:
            return pd.DataFrame()
        df = pd.DataFrame(data)
        df = df[[
            "employer_name", "job_title", "job_city",
            "job_country", "job_posted_at_datetime_utc", "job_apply_link"
        ]]
        df["job_posted_at_datetime_utc"] = pd.to_datetime(df["job_posted_at_datetime_utc"])
        return df
    else:
        st.error(f"Erro ao acessar a API: {response.status_code}")
        return pd.DataFrame()

# --- CONFIG GERAL ---
st.set_page_config(page_title="Dashboard de Vagas em IA", layout="wide")
st.title("🚀 Dashboard de Análise de Mercado de Vagas em Inteligência Artificial")

# --- DADOS ESTÁTICOS (CSV) ---
dados = AIJobData('ai_job_dataset.csv')

st.sidebar.header("Filtros")
paises = sorted(dados.df['company_location'].unique())
pais_escolhido = st.sidebar.selectbox('Selecione o país', options=['Todos'] + paises)

df_filtrado = dados.filtrar_por_pais(pais_escolhido)
viz = AIJobVisualizations(df_filtrado)

# --- VISUALIZAÇÕES DO CSV ---
st.markdown(f"## 📊 Visão Geral ({pais_escolhido})")

col1, col2, col3 = st.columns(3)
col1.metric("Vagas filtradas", len(df_filtrado))
col2.metric("Salário Médio Mensal (US$)", f"US$ {df_filtrado['salario_usd_mensal'].mean():,.2f}")
col3.metric("Vagas Remotas (%)", f"{df_filtrado['remote_ratio'].mean():.1f}%")

st.pyplot(viz.grafico_nivel_experiencia(pais_escolhido))
st.pyplot(viz.grafico_tipo_contrato(pais_escolhido))
st.pyplot(viz.grafico_top_skills(pais_escolhido))
st.pyplot(viz.grafico_top_industrias(pais_escolhido))

st.markdown("---")

st.markdown("## 📈 Análise Temporal")
st.pyplot(viz.grafico_vagas_por_mes(pais_escolhido))

st.markdown("---")

st.markdown("## 💼 Salário médio por Indústria")
st.pyplot(viz.grafico_salario_por_industria(pais_escolhido))

st.markdown("---")

st.markdown("## 🛠️ Demanda por Cluster de Skills")
st.pyplot(viz.grafico_skills_clusters(pais_escolhido))

st.markdown("---")

# --- NOVA SESSÃO: VAGAS EM TEMPO REAL ---
st.markdown("## 🌍 Vagas em Tempo Real (API)")

with st.expander("🔍 Buscar vagas ao vivo"):
    col1, col2 = st.columns(2)
    with col1:
        query = st.text_input("Palavra-chave", value="data science")
    with col2:
        location = st.text_input("Localização", value="brazil")

    if st.button("Buscar vagas"):
        df_vagas = buscar_vagas(query, location)

        if not df_vagas.empty:
            st.success(f"{len(df_vagas)} vagas encontradas.")
            st.dataframe(df_vagas)

            # Gráfico de crescimento diário
            st.subheader("📈 Publicações por Dia")
            df_vagas['data'] = df_vagas['job_posted_at_datetime_utc'].dt.date
            vagas_dia = df_vagas.groupby('data').size()
            st.line_chart(vagas_dia)
        else:
            st.warning("Nenhuma vaga encontrada para esses termos.")

st.markdown("---")

st.markdown("### 📚 Fonte dos Dados")
st.markdown("""
- Dados históricos: [Open Data Bay - AI Jobs Dataset](https://www.opendatabay.com/data/ai-ml/404a5044-69f1-4c38-9890-a566f02008f8)  
- Dados em tempo real: [JSearch API - RapidAPI](https://rapidapi.com/letscrape-6bRBa3QguO5/api/jsearch)
""")
st.markdown("👨‍💻 **Criado por Caio Arona | #CiênciaDeDados #IA #Streamlit**")
