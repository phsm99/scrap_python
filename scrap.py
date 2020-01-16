from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
import json

print('Abrindo arquivo credentials.json')

try:
    with open('credentials.json','r') as arquivo:
        dados = json.load(arquivo)
        login = dados['login']
        senha = dados['senha']
except:
    print('Erro ao abrir arquivo!')
    raise 


print('Arquivo lido com sucesso!')
browser = webdriver.Chrome('chromedriver.exe')
browser.get(
    'https://www.sistemas.pucminas.br/sgaaluno4/SilverStream/Pages/pgAln_LoginSSL.html')

# matricula
campo_matricula = browser.find_element_by_name('S48_')
campo_matricula.send_keys(login)
# senha
campo_senha = browser.find_element_by_name('S62_')
campo_senha.send_keys(senha)
# Origem
Select(browser.find_element_by_name('S76_')).select_by_value('9')
# botão Entrar
browser.find_element_by_name('S122_').click()

delay = 20  # seconds
myElem = WebDriverWait(browser, delay).until(
    EC.title_is('SGA - Página Inicial'))

if browser.current_url == 'https://www.sistemas.pucminas.br/sco/SilverStream/Pages/pgALN_AreaNoticia.html':

    dropdown = browser.find_element_by_xpath(
        '/html/body/form/table/tbody/tr[1]/td/header/font/nav[2]/aside/section/div/ul/li[1]/a')
    dropdown.click()
    hist = browser.find_element_by_xpath(
        '/html/body/form/table/tbody/tr[1]/td/header/font/nav[2]/aside/section/div/ul/li[1]/ul/li[5]/a')
    hist.click()

    myElem = WebDriverWait(browser, delay).until(
        EC.title_is('SGA - Histórico'))

    if browser.current_url == 'https://www.sistemas.pucminas.br/sga4/SilverStream/Pages/pgAln_Historico.html':
        tabelas_materias = browser.find_elements_by_class_name('smc-grid')

        print('Tentando abrir arquivo de saída')
        try:
            file = open('saida.txt','w',encoding='utf-8')
        except:
            print('Erro abrir arquivo de saída')
            raise
        print('Sucesso ao abrir arquivo de saída')

        for index, semestre in enumerate(tabelas_materias):
            pai = semestre.find_element(By.XPATH, './..')
            string = "{0} - {1} Período \n".format(pai.find_element_by_tag_name('span').text,index+1)
            print(string)
            file.write(string)
            linhas_semestre = semestre.find_elements_by_tag_name('tr')
            if len(linhas_semestre) > 0:
                if linhas_semestre[0].text == 'Disciplina\nAulas\nFaltas\n%Freq.\nNota':
                    count = 0
                    soma = 0
                    for materia in linhas_semestre:
                        if materia.text == 'Disciplina\nAulas\nFaltas\n%Freq.\nNota':
                            continue
                        linha_materia = materia.find_elements_by_tag_name('td')
                        nota_materia = float(
                            linha_materia[4].text.replace(',', '.'))
                        soma += nota_materia
                        count += 1
                        string = '  {0}: {1:.2f} \n'.format(linha_materia[0].text.strip(),nota_materia)
                        print(string)
                        file.write(string)
                    string = '  Média semestre: {0:.2f} \n'.format((soma/count))
                    print(string)
                    file.write(string)
        file.close()
        print('Fim programa')

    else:
        print('você não está na pagina correta!')
        print('Página atual:', browser.current_url)


else:
    print('você não está na pagina correta!')
    print('Página atual:', browser.current_url)
