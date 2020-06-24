#libs ultilizadas:
# requests2
# pandas
# lxml
# beautifulsoup4
# selenium
# html5lib

# importar libs
import time
import requests
import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import json
import html5lib
import re

# 1. Pegar conteúdo Html a partir da url
url = "https://www.saraiva.com.br/livros?promo_id=livros&promo_name=livros-menuexp-livros&promo_creative=linkdep&promo_position=slot1"

option = Options()
option.headless = True
driver = webdriver.Chrome()

driver.get(url)
'''
driver.implicitly_wait(10)
busca = driver.find_element_by_xpath("//div[@class='linx-impulse-autocomplete']//form[@id='search-form']//input[@class='impulse-input search-input default']")
busca.send_keys('alice')
busca.send_keys(Keys.ENTER)
'''

element = driver.find_element_by_xpath("//div[@class='slider slider--products slider--buttons-centered-touching']//div[@class='slider__clip']//div[@class='prateleira']//ul[@class='slider__slides slick-initialized slick-slider slick-dotted']//div[@class='slick-list draggable']//div[@class='slick-track']")
html_content = element.get_attribute('outerHTML')


# 2. Parsear o conteudo Htlm - Beaultifulsoup
soup = BeautifulSoup(html_content, 'html.parser')
table = soup.find_all('a', tabindex='-1')
preco = soup.find_all('strong', class_="product__price")
tabela = []
tbpreco = []

for x in table:
    clear = re.compile('<.*?>')
    limpo = (re.sub(clear, '', str(x)))
    limpo = limpo.replace('Saiba Mais', '')
    if limpo != '':
        dicLista = {
            'Titulo': limpo,
        }
        tabela.append(dicLista)


for x in preco:
    clear = re.compile('<.*?>')
    limpo = (re.sub(clear, '', str(x)))
    if limpo != '':
        dicLista = {
            'valor': limpo
        }
        tbpreco.append(dicLista)



# 3. Estruturar um conteudo em um Data Frame - Pandas
btabela = filter(None, tabela)
dfpreco = pd.DataFrame(tbpreco)
dftitulos = pd.DataFrame(tabela)
frames = dftitulos.join(dfpreco)
frames.columns = ['Titulo' , 'valor']
print(frames)

# 4. Transformar os dados em um dicionario de dados próprio
Tblp = {}
Tblp['tabela'] = frames.to_dict('records')


driver.quit()


# 5. Converter e salvar em um arquivo JSON
js = json.dumps(Tblp)
fp = open('tabela.json', 'w')
fp.write(js)
fp.close()

