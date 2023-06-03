from datetime import datetime
from datetime import timedelta
import pandas as pd
from datetime import datetime
def duplo():
    data_e_hora_atuais = datetime.now()
    data_e_hora_em_texto = data_e_hora_atuais.strftime('%d_%m_%Y')  
    data=datetime.today()
    data=data-timedelta(minutes=60)
    # agora=datetime(0,0,0,12,0) 
    # data-agora
    arquivo=str(data_e_hora_em_texto)
    # lendo arquivos
    df3=pd.read_excel("F_"+arquivo+'.xlsx')
    df_sem_duplicatas = df3.drop_duplicates(subset=['Link'])
    df_sem_duplicatas.to_excel("F_"+arquivo+'.xlsx')
    df4=pd.read_excel("O_"+arquivo+'.xlsx')
    df2_sem_duplicatas = df4.drop_duplicates(subset=['Link'])
    df2_sem_duplicatas.to_excel("O_"+arquivo+'.xlsx')
