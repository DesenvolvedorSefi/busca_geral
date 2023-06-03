import os
import pandas as pd
import mysql.connector
from mysql.connector import Error
from datetime import datetime
from dateutil.parser import parse

# diretório onde estão os arquivos
diretorio = r'C:\Users\alex1\OneDrive\Documentos\Estagio data\busca geral'

# loop pelos arquivos no diretório
for arquivo in os.listdir(diretorio):
    # se o arquivo é do mês de março e começa com "F" ou "O"
    if "_03_" in arquivo and (arquivo.startswith("F") or arquivo.startswith("O")):
        # separa o nome do arquivo e sua extensão
        nome_arquivo, extensao_arquivo = os.path.splitext(arquivo)
        print(nome_arquivo)
        # verificando se é um arquivo Excel
        if extensao_arquivo == ".xlsx":
            # lendo o arquivo Excel
            df = pd.read_excel(os.path.join(diretorio, arquivo))
            
            # removendo duplicatas
            df = df.drop_duplicates(subset=['Link'])
            
            # preenchendo valores nulos
            df.fillna(0)
            df = df.replace("nan", 0)
            print(df.columns)
            
            # loop pelas linhas do DataFrame
            for row in df.itertuples(index=False):
                try:
                    # estabelecendo conexão com o banco de dados
                    con = mysql.connector.connect(host='localhost', database='portaldados', user='root', password='')
                    
                    # convertendo a data para o formato do banco de dados
                    try:
                        # tenta converter com o formato '%d-%m-%Y'
                            dia = datetime.strptime(str(row.Dia), '%d-%m-%Y').date()
                    except ValueError:
                            try:
                                # tenta converter com o formato '%d_%m_%Y'
                                dia = datetime.strptime(str(row.Dia), '%d_%m_%Y').date()
                            except ValueError:
                                # se nenhum dos formatos funcionar, levanta um erro
                                raise ParserError("Unknown string format: %s", row.Dia)
                    
                    # definindo a coluna de cidade ou local a ser usada
                    cidade_ou_local = "Local" if arquivo.startswith("F") else "Cidade"
                    print( cidade_ou_local)
                    
                    # query SQL para inserir os dados no banco
                    inserir_user = "INSERT INTO carro_olx  ( `Origem`, `Carro`, `Vendedor`, `Dia`, `Hora`, `Telefone`, `Telefone_Descricao`, `Preço`, `Cidade`, `CEP`, `Descricao`, `Link`,`status`,`cliente`,`nomeiki`) VALUES (%s,%s,%s, %s,%s,%s,%s,%s, %s,%s,%s,%s,%s,%s,%s,%s)".format(cidade_ou_local)

                    
                    if cidade_ou_local == "Cidade":
                        cidade_ou_local_idx = 8
                    elif cidade_ou_local == "Local":
                        cidade_ou_local_idx = 3
                    else:
                        raise ValueError("cidade_ou_local deve ser 'Cidade' ou 'Local'")

                    val = ("", "FB" if nome_arquivo == "F" else "OLX", str(row[1]), str(row[2]), dia, str(row[5]), str(row[6]), "", str(row[7]), str(row[3]), "", str(row[cidade_ou_local_idx]), str(row[9]), 1, 0, "")



                    
                    # executando a query
                    cursor = con.cursor()
                    cursor.execute(inserir_user, val)
                    con.commit()
                    cursor.close()
                    
                except Error as erro:
                    print(erro)
                finally:
                    if con.is_connected():
                        con.close()
            
           

            
# removendo registros duplicados no banco de
