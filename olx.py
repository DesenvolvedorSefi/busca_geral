import pandas as pd
import numpy as np
from bs4 import BeautifulSoup
import json 
from difflib import SequenceMatcher 
from selenium import webdriver 
import time 
from datetime import datetime
import requests
import re
from urllib.parse import urlencode
import mysql.connector
from mysql.connector import Error
def busca_olx(qtd_pag):
  def json_from_url(url):
      headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
      params = {'api_key': '8ba5241ee1f0ceaf5b70a77d0db209ca', 'url': url}
      #page = requests.get('http://api.scraperapi.com/', params=urlencode(params))
      page = requests.get(url, headers=headers)
      soup = BeautifulSoup(page.text, 'html.parser')
      data_json = soup.find(id='initial-data').get('data-json')
      return json.loads(data_json)
  def Convert(a):  
      init = iter(a)  
      res_dct = dict(zip(init, init))  
      return res_dct  
  # Função que recebe url do anúncio
  # e mostra nome do vendedor, telefone,
  # descrição do produto e preço
  df=pd.DataFrame(columns=['Carro','Vendedor','Dia','Hora','Telefone','Telefone Descrição','Preço','Cidade','CEP','Descrição','Link'])

  def mostra_dados_do_anuncio(url):
      a0=0
      k=''
      carro=''
      data = json_from_url(url)
      
      prop=data['ad']['properties']
      prop1=prop[1]['value']
      a=0
      b=""
      n_descri=""
      cep = data['ad']['location']['zipcode']
      cidade=data['ad']['location']['municipality']
      cidades=['Sobral','Massapê','Senador Sá','Pires Ferreira','Santana do Acaraú','Forquilha','Coreaú','Moraújo','Groaíras','Reriutaba', 'Varjota', 'Cariré', 'Pacujá', 'Graça', 'Frecheirinha', 'Mucambo', 'Meruoca', 'Alcântaras']
      #print(cep[0:4])
      carro=prop1
      #Municípios de Massapê, Senador Sá, Pires Ferreira, Santana do Acaraú, Forquilha, Coreaú, Moraújo, Groaíras, Reriutaba, Varjota, Cariré, Pacujá, Graça, Frecheirinha, Mucambo, Meruoca e Alcântaras, além de Sobra
      for x in cidades:
        if(cidade==x):
            descricao = data['ad']['body']
            phone =  data['ad']['phone']['phone']
            user = data['ad']['user']['name']
            preco = data['ad']['price']
            data0=data['ad']['listTime']
            dia=data0[0:10]
            hora=data0[11:19]
            n_descri0=re.findall(r'[\+\(]?[1-9][0-9 .\-\(\)]{8,}[0-9]', descricao)
            for y in n_descri0:
                y=re.sub('[^0-9]', '', y)
                n_descri=y+" "+n_descri

            
          #   while (a<len(descricao)-1):
          #     b=descricao[a]+descricao[a+1]
          #     if(b=="88" or b=="85"):
          #         n_descri=descricao[a:a+15]+""+n_descri
          #     a=a+1
            df.loc[len(df)]=[carro,user,dia,hora,phone,n_descri,preco,cidade,cep,descricao,url]
            
            #print("Carro",carro)
            #print('Vendedor=',user)
            #print('Telefone=',phone)
            #print('Descrição=',descricao)
            #print('Numero descrição=',n_descri)
            #print('preco=',preco)
            #print('CEP=',cep)
            #print('CIDADE=',cidade)
  for x in range(0,qtd_pag):
    print(x)
    # Pega a lista de produtos da área de eletrônicos
    url_eletronicos="https://www.olx.com.br/autos-e-pecas/carros-vans-e-utilitarios/estado-ce/regiao-de-juazeiro-do-norte-e-sobral?o="+str(x+1)
    data = json_from_url(url_eletronicos)

    # Entra em cada anúncio e mostra o telefone
    adList = data['listingProps']['adList']
    for anuncio in adList:
        subject = anuncio.get('subject')
        if subject: 
            #print('------------------------')
            #descricao = anuncio.get('subject')        
            url = anuncio.get('url')
            #print('Descricao do produto:',descricao)
            #print('URL do produto=',url)
            mostra_dados_do_anuncio(url)
  data_e_hora_atuais = datetime.now()
  data_e_hora_em_texto = data_e_hora_atuais.strftime('%d_%m_%Y')  
  arquivo=str(data_e_hora_em_texto)
  df.to_excel("O_"+arquivo+'.xlsx')







