import pandas as pd

df = pd.read_csv("https://raw.githubusercontent.com/guilhermeonrails/data-jobs/refs/heads/main/salaries.csv")
"""
#print(df.head())

#print(df.info()) 

#print(df.describe()) 

#print(df.shape)

linhas, colunas = df.shape[0], df.shape[1]

print("Linhas: ", linhas)
print("Colunas: ", colunas)


print(df.columns)



"""

renomear_colunas = {
    'work_year': 'ano_trabalho',
    'experience_level': 'nivel_experiencia',
    'employment_type': 'tipo_contrato',
    'job_title': 'cargo',
    'salary': 'salario',
    'salary_currency': 'moeda_salario',
    'salary_in_usd': 'salario_usd',
    'employee_residence': 'residencia_funcionario',
    'remote_ratio': 'remoto',
    'company_location': 'localizacao_empresa',
    'company_size': 'tamanho_empresa'
}

df.rename(columns=renomear_colunas, inplace=True)
print(df.columns)

print(df["nivel_experiencia"].value_counts())
print(df["tipo_contrato"].value_counts())

remoto = {
    0: "remoto",
    100: "presencial",
    50: "hibrido",
}

df["remoto"] = df["remoto"].replace(remoto)
print(df['remoto'].value_counts())

print(df.head())