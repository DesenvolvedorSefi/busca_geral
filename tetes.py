import pandas as pd
from datetime import datetime
def teste():
    #pegando data atual
    data_e_hora_atuais = datetime.now()
    data_e_hora_em_texto = data_e_hora_atuais.strftime('%d_%m_%Y')  
    arquivo=str(data_e_hora_em_texto)
    # lendo arquivos
    df3=pd.read_excel("F_"+arquivo+'.xlsx')
    df2=pd.read_excel('O_'+arquivo+'.xlsx')
    #separando os que tem telefone na descrição e os que não tem
    telefone = df2.loc[df2['Telefone'].notnull()]
    telefone_descri = df2.loc[df2['Telefone'].isnull() & df2['Telefone Descrição'].notnull()]
    telefone_n = df2.loc[df2['Telefone'].isnull() & df2['Telefone Descrição'].isnull()]
    telefonef = df3.loc[df3['Telefone'].notnull()]
    telefone_descrif= df3.loc[df3['Telefone'].isnull()]
    #

   
    #exportnado resultados
    telefonef.to_excel('./saidas/facebook/F_T_O_'+arquivo+'.xlsx')
    telefone_descrif.to_excel('./saidas/facebook/F_T_D_'+arquivo+'.xlsx')
    telefone.to_excel('./saidas/olx/T_O_'+arquivo+'.xlsx')
    telefone_descri.to_excel('./saidas/olx/T_D_'+arquivo+'.xlsx')
    telefone_n.to_excel('./saidas/olx/T_N_'+arquivo+'.xlsx')
