import pandas as pd
from database import conectar_db

df = pd.read_csv("data/consolidado/Cadastro.csv")

conn = conectar_db()


municipios = df[["IBGE", "Municipio", "Uf"]].drop_duplicates()


print(municipios.head())

# inserir no banco
cursor = conn.cursor()

insert_query = """
INSERT INTO municipios (ibge, nome, uf)
VALUES (%s, %s, %s)
ON CONFLICT (ibge) DO NOTHING;
"""

for _, row in municipios.iterrows():
    cursor.execute(insert_query, (row["IBGE"], row["Municipio"], row["Uf"]))

conn.commit()

cursor.close()
conn.close()
