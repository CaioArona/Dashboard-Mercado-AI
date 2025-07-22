import streamlit as st
st.cache_data.clear()
from ai_job_data import AIJobData
from ai_job_visuals import AIJobVisualizations

st.set_page_config(page_title="Dashboard de Vagas em IA", layout="wide")
st.title("🚀 Dashboard de Análise de Mercado de Vagas em Inteligência Artificial")

dados = AIJobData('ai_job_dataset.csv')

st.sidebar.header("Filtros")
paises = sorted(dados.df['company_location'].unique())
pais_escolhido = st.sidebar.selectbox('Selecione o país', options=['Todos'] + paises)

df_filtrado = dados.filtrar_por_pais(pais_escolhido)

viz = AIJobVisualizations(df_filtrado)

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

st.markdown("### 📚 Fonte dos Dados")
st.markdown("""
Dados coletados de [Open Data Bay - AI Jobs Dataset](https://www.opendatabay.com/data/ai-ml/404a5044-69f1-4c38-9890-a566f02008f8)
""")
st.markdown("👨‍💻 **Criado por Caio Arona | #CiênciaDeDados #IA #Streamlit**")
