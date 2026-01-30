import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px

# ==============================
# 1. Carregar dados
# ==============================
df = pd.read_csv(
    "https://raw.githubusercontent.com/guilhermeonrails/data-jobs/refs/heads/main/salaries.csv"
)

# ==============================
# 2. Renomear colunas
# ==============================
df.rename(columns={
    'work_year': 'ano_trabalho',
    'experience_level': 'senioridade',
    'employment_type': 'tipo_contrato',
    'job_title': 'cargo',
    'salary': 'salario',
    'salary_currency': 'moeda_salario',
    'salary_in_usd': 'USD',
    'employee_residence': 'residencia_funcionario',
    'remote_ratio': 'modelo_trabalho',
    'company_location': 'localizacao_empresa',
    'company_size': 'tamanho_empresa'
}, inplace=True)

# ==============================
# 3. Traduzir senioridade
# ==============================
rename_senioridade = {
    'EN': 'Júnior',
    'MI': 'Pleno',
    'SE': 'Sênior',
    'EX': 'Executivo',
}

df['senioridade'] = df['senioridade'].replace(rename_senioridade)

# ==============================
# 4. Remover nulos críticos
# ==============================
df = df.dropna(subset=['ano_trabalho'])

# ==============================
# 5. Padronizar categorias
# ==============================
df['modelo_trabalho'] = df['modelo_trabalho'].replace({
    0: 'presencial',
    50: 'hibrido',
    100: 'remoto'
})

# ==============================
# 6. Ajustar tipos
# ==============================
df['ano_trabalho'] = df['ano_trabalho'].astype(int)

# ==============================
# 7. Gráfico 1 — Distribuição de senioridade (Matplotlib)
# ==============================
plt.figure(figsize=(8,5))
df['senioridade'].value_counts().plot(kind='bar')
plt.title("Distribuição de Senioridade")
plt.xlabel("Senioridade")
plt.ylabel("Quantidade")
plt.tight_layout()
plt.show()

# ==============================
# 8. Gráfico 2 — Salário médio por senioridade (Seaborn)
# ==============================
ordem = (
    df.groupby('senioridade')['USD']
    .mean()
    .sort_values(ascending=False)
    .index
)

plt.figure(figsize=(8,5))
sns.barplot(data=df, x='senioridade', y='USD', order=ordem)
plt.title('Salário médio por senioridade')
plt.xlabel('Senioridade')
plt.ylabel('Salário Médio Anual (USD)')
plt.tight_layout()
plt.show()

# ==============================
# 9. Gráfico 3 — Histograma de salários (Seaborn)
# ==============================
plt.figure(figsize=(8,4))
sns.histplot(df['USD'], bins=50, kde=True)
plt.title('Distribuição dos salários anuais')
plt.xlabel('Salário (USD)')
plt.ylabel('Frequência')
plt.tight_layout()
plt.show()

# ==============================
# 10. Gráfico 4 — Pizza modelo de trabalho (Plotly)
# ==============================
remoto_contagem = (
    df['modelo_trabalho']
    .value_counts()
    .reset_index()
)

remoto_contagem.columns = ['tipo_trabalho', 'quantidade']

fig = px.pie(
    remoto_contagem,
    names='tipo_trabalho',
    values='quantidade',
    title='Proporção do modelo de trabalho'
)

fig.update_traces(textinfo='percent+label')
fig.update_layout(title_x=0.5)
fig.show()

# ==============================
# 11. Verificação final
# ==============================
print("\nValores nulos por coluna:")
print(df.isnull().sum())

print("\nInfo da base:")
print(df.info())

print("\nAmostra dos dados:")
print(df.head())

print("\nOrdem de senioridade por salário:")
print(ordem)
