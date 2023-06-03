import selenium
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import NoSuchElementException
from datetime import timedelta
import pandas as pd
from datetime import datetime
from datetime import date
from time import sleep
import getpass
import re
import mysql.connector
from mysql.connector import Error
def busca_fb(qtd_carros):
    option = Options()
    option.add_argument("--disable-infobars")
    option.add_argument("start-maximized")
    option.add_argument("--disable-extensions")

    # Pass the argument 1 to allow and 2 to block
    option.add_experimental_option("prefs", { 
        "profile.default_content_setting_values.notifications": 2 
    })

    from sys import platform

     option = webdriver.ChromeOptions()
    option.add_argument('--disable-infobars')
    option.add_argument('--no-sandbox')
    option.add_argument('--disable-dev-shm-usage')
    option.add_argument('--disable-browser-side-navigation')
    option.add_argument('--disable-gpu')
    option.add_argument('--disable-features=VizDisplayCompositor')
    option.add_argument('--disable-blink-features=AutomationControlled')
    option.add_argument("--remote-debugging-port=9222")
    driver = webdriver.Chrome(ChromeDriverManager().install(), chrome_options=option)
    driver.get("https://www.facebook.com/")
    driver.maximize_window()
    user_id="a.s.rwar@gmail.com"
    my_password="meuirmao07"
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
                carro1 = driver.find_element(By.XPATH,"/html/body/div[1]/div/div[1]/div/div[3]/div/div/div/div[1]/div[1]/div[2]/div/div/div[3]/div/div[2]/div["+str(i)+"]/div/div/span/div/div/a")
                carro1.location_once_scrolled_into_view
                link=carro1.get_attribute('href')
                print("linnnkoo"+link)
                lo=driver.find_element(By.XPATH,"/html/body/div[1]/div/div[1]/div/div[5]/div/div/div[3]/div/div/div[1]/div[1]/div[2]/div/div/div[3]/div[1]/div[2]/div["+str(i)+"]/div/div/span/div/div/a/div/div[2]/div[3]/span/div/span/span")
                #local.append(lo.text)
                if j==2:
                    j=0
                lin[j]=link
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
        except NoSuchElementException:
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
            
            local_data=driver.find_element(By.XPATH,"/html/body/div[1]/div/div[1]/div/div[3]/div/div/div/div[1]/div[1]/div[2]/div/div/div/div/div/div[2]/div/div[2]/div/div[1]/div[1]/div[1]/div[3]/div/div/div/span")
            print(local_data)
            local_data1=local_data.text
            incio_s=local_data1.find("em")
            final_s=local_data1.find(",")
            local=local_data1[incio_s+2:final_s]
            data=local_data1[0:incio_s-1]
            print(data)
            dataloop=data.split(" ")
            print(dataloop)
            dia=dataloop[len(dataloop)-1]
            hora=dataloop[len(dataloop)-2]
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

            dia1=datal.strftime('%d-%m-%Y')
            hora1=datal.strftime('%H:%M')
            print("sdia1"+dia1)
            
        except NoSuchElementException:
            print("exception handled local")
            dia1=date.today().strftime('%d-%m-%Y')
            hora1=0
        driver.get(j)
        driver.maximize_window()
        try:
            descricao=driver.find_element(By.XPATH,"/html/body/div[1]/div/div[4]/div/div/div/div/div[2]/div/div[3]/div[2]/div")
            vendedor=driver.find_element(By.XPATH,"/html/body/div[1]/div/div[4]/div/div/div/div/div[2]/div/div[3]/div[1]/div/div/div/div")
            carro=driver.find_element(By.XPATH,"/html/body/div[1]/div/div[4]/div/div/div/div/div[2]/div/div[1]/div[1]/div[1]/div[1]/div")
            preco=driver.find_element(By.XPATH,"/html/body/div[1]/div/div[4]/div/div/div/div/div[2]/div/div[1]/div[1]/div[1]/div[2]")
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
        except NoSuchElementException:
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

busca_fb(10)
