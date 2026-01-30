import streamlit as st
import pandas as pd
import plotly.express as px

# --- Configuração da Página ---
st.set_page_config(
    page_title="Dashboard de Salários - Data Analyst",
    page_icon="📊",
    layout="wide",
)

# --- Carregamento dos dados ---
df = pd.read_csv(
    "https://raw.githubusercontent.com/vqrca/dashboard_salarios_dados/refs/heads/main/dados-imersao-final.csv"
)

# --- Barra Lateral (Filtros) ---
st.sidebar.header("🔍 Filtros")

# Filtro de Ano
anos_disponiveis = sorted(df['ano'].unique())
anos_selecionados = st.sidebar.multiselect(
    "Ano", anos_disponiveis, default=anos_disponiveis
)

# Filtro de Senioridade
senioridades_disponiveis = sorted(df['senioridade'].unique())
senioridades_selecionadas = st.sidebar.multiselect(
    "Senioridade", senioridades_disponiveis, default=senioridades_disponiveis
)

# Filtro por Tipo de Contrato
contratos_disponiveis = sorted(df['contrato'].unique())
contratos_selecionados = st.sidebar.multiselect(
    "Tipo de Contrato", contratos_disponiveis, default=contratos_disponiveis
)

# Filtro por Tamanho da Empresa
tamanhos_disponiveis = sorted(df['tamanho_empresa'].unique())
tamanhos_selecionados = st.sidebar.multiselect(
    "Tamanho da Empresa", tamanhos_disponiveis, default=tamanhos_disponiveis
)

# --- Filtragem do DataFrame ---
df_filtrado = df[
    (df['ano'].isin(anos_selecionados)) &
    (df['senioridade'].isin(senioridades_selecionadas)) &
    (df['contrato'].isin(contratos_selecionados)) &
    (df['tamanho_empresa'].isin(tamanhos_selecionados))
]

# ==========================
# 🔴 FOCO NO CARGO
# ==========================
df_cargo = df_filtrado[df_filtrado['cargo'] == 'Data Analyst']

# --- Conteúdo Principal ---
st.title("📊 Dashboard de Salários – Data Analyst")
st.markdown(
    "Análise completa dos salários para o cargo de **Data Analyst**, "
    "considerando ano, senioridade, tipo de contrato e empresa."
)

# --- Métricas Principais ---
st.subheader("Métricas gerais (Salário anual em USD)")

if not df_cargo.empty:
    salario_medio = df_cargo['usd'].mean()
    salario_maximo = df_cargo['usd'].max()
    total_registros = df_cargo.shape[0]
else:
    salario_medio = salario_maximo = total_registros = 0

cargo_mais_frequente = df_cargo['cargo'].mode()[0] if not df_cargo.empty else ""

col1, col2, col3, col4 = st.columns(4)

col1.metric("Salário médio", f"${salario_medio:,.0f}")
col2.metric("Cargo mais frequente", cargo_mais_frequente)
col3.metric("Salário máximo", f"${salario_maximo:,.0f}")
col4.metric("Total de registros", f"{total_registros:,}")


st.markdown("---")

# --- Gráficos ---
st.subheader("Gráficos de Data Analyst")

col_graf1, col_graf2 = st.columns(2)

with col_graf1:
    if not df_cargo.empty:
        salario_senioridade = (
            df_cargo
            .groupby('senioridade')['usd']
            .mean()
            .reset_index()
            .sort_values('usd')
        )

        grafico_senioridade = px.bar(
            salario_senioridade,
            x='usd',
            y='senioridade',
            orientation='h',
            title="Salário médio por senioridade",
            labels={'usd': 'Salário médio (USD)', 'senioridade': ''}
        )
        grafico_senioridade.update_layout(title_x=0.1)
        st.plotly_chart(grafico_senioridade, use_container_width=True)
    else:
        st.warning("Sem dados para Data Analyst.")

with col_graf2:
    if not df_cargo.empty:
        grafico_hist = px.histogram(
            df_cargo,
            x='usd',
            nbins=30,
            title="Distribuição de salários",
            labels={'usd': 'Faixa salarial (USD)', 'count': ''}
        )
        grafico_hist.update_layout(title_x=0.1)
        st.plotly_chart(grafico_hist, use_container_width=True)

col_graf3, col_graf4 = st.columns(2)

with col_graf3:
    if not df_cargo.empty:
        remoto = df_cargo['remoto'].value_counts().reset_index()
        remoto.columns = ['tipo_trabalho', 'quantidade']

        grafico_remoto = px.pie(
            remoto,
            names='tipo_trabalho',
            values='quantidade',
            hole=0.5,
            title="Modelo de trabalho"
        )
        grafico_remoto.update_traces(textinfo='percent+label')
        st.plotly_chart(grafico_remoto, use_container_width=True)

with col_graf4:
    if not df_cargo.empty:
        media_pais = (
            df_cargo
            .groupby('residencia_iso3')['usd']
            .mean()
            .reset_index()
        )

        grafico_paises = px.choropleth(
            media_pais,
            locations='residencia_iso3',
            color='usd',
            color_continuous_scale='rdylgn',
            title="Salário médio de Data Analyst por país",
            labels={'usd': 'Salário médio (USD)', 'residencia_iso3': 'País'}
        )
        grafico_paises.update_layout(title_x=0.1)
        st.plotly_chart(grafico_paises, use_container_width=True)

# --- Tabela ---
st.subheader("Dados detalhados – Data Analyst")
st.dataframe(df_cargo)

# --- Exportação ---
df.to_csv("dados-imersao-final.csv", index=False)
