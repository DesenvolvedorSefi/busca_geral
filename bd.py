import mysql.connector
from mysql.connector import Error
import pandas as pd
import datetime
from datetime import datetime
data_e_hora_atuais = datetime.now()
data_e_hora_em_texto = data_e_hora_atuais.strftime('%d_%m_%Y')  
arquivo=str(data_e_hora_em_texto)
# lendo arquivos


def fb_db():
    df3=pd.read_excel("F_"+arquivo+'.xlsx')
    df3 = df3.drop_duplicates(subset=['Link'])
    a, b=df3.shape
    df3.fillna(0)
    df3=df3.replace("nan",0)
    print(a)
    i=0
    while(i<a):
        dfloop=df3.loc[i]
        try:
            con=mysql.connector.connect(host='localhost',database='portaldados',user='root',password='')
            dia=datetime.strptime(str(dfloop['Dia']), '%d-%m-%Y').date()
            inserir_user="INSERT INTO carro_olx  (`indice`, `Origem`, `Carro`, `Vendedor`, `Dia`, `Hora`, `Telefone`, `Telefone_Descricao`, `Preço`, `Cidade`, `CEP`, `Descricao`, `Link`,`status`,`cliente`,`nomeiki`) VALUES (%s,%s,%s, %s,%s,%s,%s,%s, %s,%s,%s,%s,%s,%s,%s,%s)"
            val=(0,"FB",str(dfloop['Carro']),str(dfloop['Vendedor']),dia,str(dfloop['Hora']),str(dfloop['Telefone'])," ",str(dfloop['Preço']),str(dfloop['Local']),"",str(dfloop['Descrição']),str(dfloop['Link']),1,0,"")
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
def olx_db():
    df2=pd.read_excel('O_'+arquivo+'.xlsx')
    df2 = df2.drop_duplicates(subset=['Link'])
    a, b=df2.shape
    df2.fillna(0)
    df2=df2.replace("nan",0)
    i=0
    while(i<a-1):
        dfloop=df2.loc[i]
        try:
            con=mysql.connector.connect(host='localhost',database='portaldados',user='root',password='')
            inserir_user="INSERT INTO carro_olx  (`indice`, `Origem`, `Carro`, `Vendedor`, `Dia`, `Hora`, `Telefone`, `Telefone_Descricao`, `Preço`, `Cidade`, `CEP`, `Descricao`, `Link`,`status`,`cliente`,`nomeiki`) VALUES (%s,%s,%s, %s,%s,%s,%s,%s, %s,%s,%s,%s,%s,%s,%s,%s)"
            val=(0,"OLX",str(dfloop['Carro']),str(dfloop['Vendedor']),str(dfloop['Dia']),str(dfloop['Hora']),str(dfloop['Telefone']),str(dfloop['Telefone Descrição']),str(dfloop['Preço']),str(dfloop['Cidade']),str(dfloop['CEP']),str(dfloop['Descrição']),str(dfloop['Link']),1,0,"")
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
    olx_db()
    fb_db()
    reepetidos()

