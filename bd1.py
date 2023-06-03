import mysql.connector
from mysql.connector import Error
import pandas as pd
import datetime
from datetime import datetime
data_e_hora_atuais = datetime.now()
data_e_hora_em_texto = data_e_hora_atuais.strftime('%d_%m_%Y')  
arquivo=str(data_e_hora_em_texto)
# lendo arquivos
import os
# diretório onde estão os arquivos
diretorio = r'C:\Users\alex1\OneDrive\Documentos\Estagio data\busca geral'

# listas para os arquivos que começam com "F" e "O"
arquivos_F = []
arquivos_O = []

# loop pelos arquivos no diretório
for arquivo in os.listdir(diretorio):
    # se o arquivo é do mês de março e começa com "F" ou "O"
    if "_03_" in arquivo and (arquivo.startswith("F") or arquivo.startswith("O")):
        # separa o nome do arquivo e sua extensão
        nome_arquivo, extensao_arquivo = os.path.splitext(arquivo)
        # adiciona o nome do arquivo na lista correspondente
        if nome_arquivo.startswith("F"):
            arquivos_F.append(nome_arquivo)
        elif nome_arquivo.startswith("O"):
            arquivos_O.append(nome_arquivo)

# imprime as listas de arquivos
print("Arquivos que começam com F:", arquivos_F)
print("Arquivos que começam com O:", arquivos_O)

def fb_db(alex):
    df3=pd.read_excel(alex+".xlsx")
    df3 = df3.drop_duplicates(subset=['Link'])
    a, b=df3.shape
    # print(df3.s)
    df3.fillna(0)
    df3=df3.replace("nan",0)
    print(a)
    i=0
    
    while(i<a):
        dfloop=df3.loc[i]
        try:
            con=mysql.connector.connect(host='localhost',database='portaldados',user='root',password='')
            dia=datetime.strptime(str(dfloop['Dia']), '%d_%m_%Y').date()
            inserir_user="INSERT INTO carro_olx  (`indice`, `Origem`, `Carro`, `Vendedor`, `Dia`, `Hora`, `Telefone`, `Telefone_Descricao`, `Preço`, `Cidade`, `CEP`, `Descricao`, `Link`,`status`,`cliente`,`nomeiki`) VALUES (%s,%s,%s, %s,%s,%s,%s,%s, %s,%s,%s,%s,%s,%s,%s,%s)"
            val=("","FB",str(dfloop['Carro']),str(dfloop['Vendedor']),dia,str(dfloop['Hora']),str(dfloop['Telefone'])," ",str(dfloop['Preço']),str(dfloop['Local']),"",str(dfloop['Descrição']),str(dfloop['Link']),1,0,"")


            cursor=con.cursor()
            cursor.execute(inserir_user,val)
            print(con)
            con.commit()
            cursor.close()
        except Error as erro:
            print(erro)
        finally:
            if(con.is_connected()):
                #cursor.close()
                con.close()
        i=i+1
def olx_db(alex):
    df2=pd.read_excel(alex+".xlsx")
    df2 = df2.drop_duplicates(subset=['Link'])
    a, b=df2.shape
    df2.fillna(0)
    df2=df2.replace("nan",0)
    i=0
    while(i<a):
        dfloop=df2.loc[i]
        try:
            con=mysql.connector.connect(host='localhost',database='portaldados',user='root',password='')
            inserir_user="INSERT INTO carro_olx  (`indice`, `Origem`, `Carro`, `Vendedor`, `Dia`, `Hora`, `Telefone`, `Telefone_Descricao`, `Preço`, `Cidade`, `CEP`, `Descricao`, `Link`,`status`,`cliente`,`nomeiki`) VALUES (%s,%s,%s, %s,%s,%s,%s,%s, %s,%s,%s,%s,%s,%s,%s,%s)"
            val=("","OLX",str(dfloop['Carro']),str(dfloop['Vendedor']),str(dfloop['Dia']),str(dfloop['Hora']),str(dfloop['Telefone']),str(dfloop['Telefone Descrição']),str(dfloop['Preço']),str(dfloop['Cidade']),str(dfloop['CEP']),str(dfloop['Descrição']),str(dfloop['Link']),1,0,"")


            cursor=con.cursor()
            cursor.execute(inserir_user,val)
            con.commit()
            cursor.close()
        except Error as erro:
            print(erro)
        finally:
            if(con.is_connected()):
                #cursor.close()
                con.close()
        i=i+1
def reepetidos():
        try:
            con=mysql.connector.connect(host='localhost',database='portaldados',user='root',password='')
            inserir_user="DELETE a FROM carro_olx AS a, carro_olx AS b WHERE a.Link=b.Link AND a.indice < b.indice"
            cursor=con.cursor()
            cursor.execute(inserir_user)
            con.commit()
            print(cursor.rowcount)
            #cursor.close()
        except Error as erro:
            print(erro)
        finally:
            if(con.is_connected()):
                #cursor.close()
                con.close()
def main():
    for i in arquivos_O:
        olx_db(i)
    for j in arquivos_F:
        fb_db(j)
    reepetidos()
main()
