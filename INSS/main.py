import pandas as pd
import mysql.connector

# Leitura do arquivo Excel
df = pd.read_excel("INSS.xlsx")

# Substituir valores nulos ou vazios por 0
df = df.fillna(value=0)

# Processamento da coluna comp_ini_desconto
df['comp-ini-desconto'] = pd.to_datetime(df['comp-ini-desconto'], format='%Y%m')
# Processamento da coluna comp_fim_desconto
df['comp-fim-desconto'] = pd.to_datetime(df['comp-fim-desconto'], format='%Y%m')



# Conexão com o banco de dados
mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    database="portaldados"
)

mycursor = mydb.cursor()

# Inserir dados na tabela
for row in df.itertuples(index=False):
    sql = "INSERT INTO INSS (nb, nome_segurado, dt_nascimento, IDADE, nu_CPF, esp, dib, ddb, vl_beneficio, id_banco_pagto, id_agencia_banco, id_orgao_pagador, nu_conta_corrente, aps_benef, cs_meio_pagto, id_banco_empres, id_contrato_empres, vl_empres, comp_ini_desconto, comp_fim_desconto, quant_parcelas, vl_parcela, tipo_empres, endereco, bairro, municipio, uf, cep, situacao_empres, dt_averbacao_consig, FONE1, FONE2, FONE3, FONE4, SOMA_PARC, NOVO_BENEFICIO, MARGEM) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
    val = row
    mycursor.execute(sql, val)

mydb.commit()

print(mycursor.rowcount, "registros inseridos com sucesso!")
