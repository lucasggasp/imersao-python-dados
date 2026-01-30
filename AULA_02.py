import pandas as pd
import numpy as np

# ==============================
# 1. Carregando a base de dados
# ==============================

# Lê o arquivo CSV diretamente do GitHub
df = pd.read_csv(
    "https://raw.githubusercontent.com/guilhermeonrails/data-jobs/refs/heads/main/salaries.csv"
)

# ==============================
# 2. Análise inicial dos dados
# ==============================

# Exibe quais valores são nulos (True = nulo)
# print(df.isnull())

# Conta quantos valores nulos existem em cada coluna
# print(df.isnull().sum())

# Mostra os valores únicos da coluna 'work_year'
# print(df['work_year'].unique())

# Exibe apenas as linhas que possuem pelo menos um valor nulo
# print(df[df.isnull().any(axis=1)])


# ==============================
# 3. Limpeza dos dados
# ==============================

# Remove todas as linhas que possuem valores nulos (NaN)
df_limpo = df.dropna()

# Verifica novamente se ainda existem valores nulos
# print(df_limpo.isnull().sum())


# ==============================
# 4. Ajuste de tipos de dados
# ==============================

# Converte a coluna 'work_year' para inteiro
# (muito importante para análises e gráficos)
df_limpo = df_limpo.assign(
    work_year=df_limpo['work_year'].astype('int64')
)


# ==============================
# 5. Verificação final
# ==============================

# Exibe informações gerais do DataFrame limpo
print(df_limpo.info())
