import pandas as pd


#lendo novos e antigos arquivos
def compare_olx():
    data_e_hora_atuais = datetime.now()
    data_e_hora_em_texto = data_e_hora_atuais.strftime('%d_%m_%Y')  
    arquivo=str(data_e_hora_em_texto)
    newdf=pd.read_excel('./saidas/olx/T_O_'+arquivo+'.xlsx')
    newdf2=pd.read_excel('./saidas/olx/T_D_'+arquivo+'.xlsx')
    newdf3=pd.read_excel('./saidas/olx/T_N_'+arquivo+'.xlsx')
    data=newdf['Link'].tolist()
    diaanterio=int(arquivo[0:2])-3
    arquivo_old=arquivo[3:len(arquivo)]
    arquivo_old=str(diaanterio)+"_"+arquivo_old
    olddf=pd.read_excel('./saidas/olx/T_O_'+arquivo_old+'.xlsx')
    olddf2=pd.read_excel('./saidas/olx/T_D_'+arquivo_old+'.xlsx')
    olddf3=pd.read_excel('./saidas/olx/T_N_'+arquivo_old+'.xlsx')
    #comparando
    m = pd.merge(newdf, olddf, how = 'inner', on = 'Link')
    m1= pd.merge(newdf2, olddf2, how = 'inner', on = 'Link')
    m2= pd.merge(newdf3, olddf3, how = 'inner', on = 'Link')
    o=m['Unnamed: 0_x'].tolist()
    o1=m1['Unnamed: 0_x'].tolist()
    o2=m2['Unnamed: 0_x'].tolist()
    newdf_ex=pd.read_excel('./saidas/olx/T_O_'+arquivo+'.xlsx',index_col='Unnamed: 0')
    newdf2_ex=pd.read_excel('./saidas/olx/T_D_'+arquivo+'.xlsx',index_col='Unnamed: 0')
    newdf3_ex=pd.read_excel('./saidas/olx/T_N_'+arquivo+'.xlsx',index_col='Unnamed: 0')
    for x in o:
        newdf_ex.drop(x,inplace=True)
    for x in o1:
        newdf2_ex.drop(x,inplace=True)
    for x in o2:
        newdf3_ex.drop(x,inplace=True)


    newdf_ex.to_excel('./saidas/olx/T_O_'+arquivo+'.xlsx')
    newdf2_ex.to_excel('./saidas/olx/T_D_'+arquivo+'.xlsx')
    newdf3_ex.to_excel('./saidas/olx/T_N_'+arquivo+'.xlsx')
