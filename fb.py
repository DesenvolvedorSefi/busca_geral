import selenium
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import NoSuchElementException,TimeoutException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from datetime import timedelta
import pandas as pd
from datetime import datetime
from datetime import date
from time import sleep
import traceback
import getpass
import re
import mysql.connector
from mysql.connector import Error

def busca_fb(qtd_carros):
    print("foi")

    options = Options()
    options.headless = False # Executar o Firefox em modo gráfico (com interface)

# Inicialização do driver do Firefox
    driver = webdriver.Firefox(executable_path=GeckoDriverManager().install(), options=options)

    driver.get("https://www.facebook.com/")
    driver.maximize_window()
    user_id=""
    my_password=""
    carro="carro"

    user_name = driver.find_element(By.XPATH,"//input[@type='text']")
    user_name.send_keys(user_id)

    password = driver.find_element(By.XPATH,"//input[@type='password']")
    password.send_keys(my_password)

    login = driver.find_element(By.XPATH,"//button[@name='login']")
    login.click()
    sleep(5)
    # pular=driver.find_element(By.XPATH,"/html/body/div[1]/div/div[2]/div/div[1]/div/div/div[3]/div[1]/div/div/a")
    # pular.click()
    #pular=driver.find_element(By.XPATH,"/html/body/div[1]/div/div[2]/div/div[1]/div/div/div[3]/div[2]/form/div/button")
    #pular.click()

    driver.get("https://www.facebook.com/marketplace/108076769226284/search?daysSinceListed=1&query=carros&exact=false")
    driver.maximize_window()
    i=1
    j=0
    k=1
    links=[]
    local=[]
    lin=["a","n"]
    #qtd_carros=10
    while(i<qtd_carros):
        print(i)

        
        try:
            #carro1=WebDriverWait(driver, timeout=5).until(lambda d: d.find_element(By.XPATH,"/html/body/div[1]/div/div[1]/div/div[5]/div/div/div[3]/div/div/div[1]/div[1]/div[2]/div/div/div[3]/div/div[2]/div["+str(i)+"]/div/div/span/div/div/a"))
            #driver.execute_script("window.scrollTo(0,"+str(k*500)+")")
            if i>40:
                print("GOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOl")
                print(k)
                carro1 = driver.find_element(By.XPATH,"/html/body/div[1]/div/div[1]/div/div[5]/div/div/div[3]/div/div/div[1]/div[1]/div[2]/div/div/div[3]/div[2]/div[2]/div["+str(k)+"]/div/div/span/div/div/a")
                carro1.location_once_scrolled_into_view
                link=carro1.get_attribute('href')
                print("linnnkoo"+link)
                lo=driver.find_element(By.XPATH,"/html/body/div[1]/div/div[1]/div/div[5]/div/div/div[3]/div/div/div[1]/div[1]/div[2]/div/div/div[3]/div[2]/div[2]/div["+str(k)+"]/div/div/span/div/div/a/div/div[2]/div[3]/span/div/span/span")
                #local.append(lo.text)
                k=k+1
            else:
                carro1_xpath = "/html/body/div[1]/div/div[1]/div/div[3]/div/div/div/div[1]/div[1]/div[2]/div/div/div[3]/div/div[2]/div[" + str(i) + "]/div/div/span/div/div/a"

                # Aguardar até que o elemento esteja visível na página
                wait = WebDriverWait(driver, 10)  # Tempo máximo de espera de 10 segundos
                carro1 = wait.until(EC.visibility_of_element_located((By.XPATH, carro1_xpath)))

                # Aguardar até que o elemento esteja clicável na página
                carro1 = wait.until(EC.element_to_be_clickable((By.XPATH, carro1_xpath)))

                carro1.location_once_scrolled_into_view
                link = carro1.get_attribute('href')
                print("linnnkoo" + link)
                #lin[j]=link
                j=j+1
        # j=""
        # j=link[11:len(link)]
        # j="https://m"+j
        # driver.get(j)
        # driver.maximize_window()
        # descricao=driver.find_element(By.XPATH,"/html/body/div[1]/div/div[4]/div/div/div/div/div[2]/div/div[3]/div[2]/div")
        # print(descricao.text)
            # driver.get("https://www.facebook.com/marketplace/108076769226284/search/?query=carros")
            # driver.maximize_window()
        except (NoSuchElementException, TimeoutException):
            traceback.print_exc()
            print("exception handled")
            if i>40:
                k=k+1
        #driver.execute_script("arguments[0.scrollIntoView();",carro1)
        #print(link)
        links.append(link)
        sleep(2)
        i=i+1

    #print(links)
    print("tamanho local"+str(len(local)))
    i=0
    data1=datetime.today()
    df=pd.DataFrame(columns=['Carro','Vendedor','Local','Dia','Hora','Telefone','Preço','Descrição','Link'])
    while(i<len(links)):
        print(i)
        j=""
        j=links[i][11:len(links[i])]
        j="https://m"+j
        driver.get(links[i])
        driver.maximize_window()
        try:
            try:
                local_data = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, "/html/body/div[1]/div/div[1]/div/div[3]/div/div/div/div[1]/div[1]/div[2]/div/div/div/div/div/div[2]/div/div[2]/div/div[1]/div/div[1]/div[3]/div/div/div/span")))
        
                local_data1=local_data.text
                incio_s=local_data1.find("em")
                final_s=local_data1.find(",")
                local=local_data1[incio_s+2:final_s]
                data=local_data1[0:incio_s-1]
                print(data)
                dataloop=data.split(" ")
                print(dataloop)
                dia=dataloop[len(dataloop)-1]
                print(dia)
                hora=dataloop[len(dataloop)-2]
                datal = None  # Valor padrão
                if(dia=="horas"):
                    datal=data1-timedelta(minutes=int(hora)*60)
                elif(dia=="minutos"):
                    datal=data1-timedelta(minutes=int(hora))
                elif(dia=="hora"):
                    if(hora=="uma"):
                        datal=data1-timedelta(minutes=1*60)
                elif(dia=="dia" or dia=="dias"):
                    if(hora=="um"):
                        datal=data1-timedelta(days=1)

                try:
                    dia1 = datal.strftime('%d-%m-%Y')
                    hora1 = datal.strftime('%H:%M')
                except AttributeError:
                    print("Erro na conversão da data e hora")
                    dia1 = date.today().strftime('%d-%m-%Y')
                    hora1 = datetime.now().strftime('%H:%M')
                print("sdia1"+dia1)
                
            except (NoSuchElementException, TimeoutException):
                print("exception handled")
                dia1=date.today().strftime('%d-%m-%Y')
                hora1=0
        except WebDriverException as e:
            # Verifica se a mensagem de erro contém "Reached error page"
            if "Reached error page" in str(e):
                print("Erro de página alcançada. Recarregando a página...")
                driver.refresh()
            else:
                raise e
        driver.get(j)
        driver.maximize_window()
        # Obter o título da página
        title = driver.title

        # Imprimir o título da página
        print("Título da página:", title)

        try:
            descricao = WebDriverWait(driver, 50).until(EC.presence_of_element_located((By.XPATH, "/html/body/div[1]/div/div[4]/div/div/div/div/div/div[3]/div/div[3]/div[2]")))
            vendedor = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "/html/body/div[1]/div/div[4]/div/div/div/div/div/div[3]/div/div[3]/div[1]")))
            carro = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "/html/body/div[1]/div/div[4]/div/div/div/div/div/div[3]/div/div[1]/div[1]/div/div[1]")))
            preco = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "/html/body/div[1]/div/div[4]/div/div/div/div/div/div[3]/div/div[1]/div[1]/div/div[2]")))
            n_descri=""
            a=0
            b=""
            n_descri=""
            descricao_=descricao.text
            n_descri0=re.findall(r'[\+\(]?[1-9][0-9 .\-\(\)]{8,}[0-9]', descricao_)
            for y in n_descri0:
                y=re.sub('[^0-9]', '', y)
                n_descri=y+" "+n_descri
            # while (a<len(descricao_)-1):
            #                     b=descricao_[a]
            #                     if(b=="9"):
            #                         n_descri=descricao_[a-5:a+15]+""+n_descri
            #                     a=a+1
            df.loc[len(df)]=[carro.text,vendedor.text,local,dia1,hora1,n_descri,preco.text,descricao.text,links[i]]
            
            # print("Carro"+carro.text)
            # print("Preço"+preco.text)
            # print(vendedor.text)
            # print(descricao.text)
        except (NoSuchElementException, TimeoutException):
            print("exception handled")
        i=i+1
    data_e_hora_atuais = datetime.now()
    data_e_hora_em_texto = data_e_hora_atuais.strftime('%d_%m_%Y')  
    arquivo=str(data_e_hora_em_texto)
    
    df.to_excel("F_"+arquivo+'.xlsx')
    # try:
    #     carro1 = driver.find_element(By.XPATH,"/html/body/div[1]/div/div[1]/div/div[5]/div/div/div[3]/div/div/div[1]/div[1]/div[2]/div/div/div[3]/div/div[2]/div[1]/div/div/span/div/div/a")
    # except NoSuchElementException:
    #     print("exception handled")
    # #driver.execute_script("arguments[0.scrollIntoView();",carro1)
    # carro1.location_once_scrolled_into_view
    # link=carro1.get_attribute('href')
    # i=""
    # i=link[11:len(link)]
    # i="https://m"+i
    # driver.get(i)
    # driver.maximize_window()
    # descricao=driver.find_element(By.XPATH,"/html/body/div[1]/div/div[4]/div/div/div/div/div[2]/div/div[3]/div[2]/div")
    # print(descricao.text)


