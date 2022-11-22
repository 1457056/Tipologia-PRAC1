import numpy as np
from pip._vendor import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
import pandas as pd
import datetime

url = 'https://www.instant-gaming.com/es/'
driver = webdriver.Firefox(executable_path=r'./driver/geckodriver.exe')
bs = BeautifulSoup(driver.page_source,"lxml")

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:106.0) Gecko/20100101 Firefox/106.0'
}
response = requests.get(url, headers = headers)
soup = BeautifulSoup(response.content, 'html.parser')
driver.get(url)
productstitle = []
productsprice = []
productdicount = []
productdicountprice = []
productsdevelop = []
productsreleasedate = []
productdate = []


# Mètode per avançar a la pàgina següent
def getPage(page):
    url_page = 'https://www.instant-gaming.com/es/busquedas/?page='+str(page)
    driver.get(url_page)
    ul = driver.find_element(By.CSS_SELECTOR,"a[class='arrow']")
    driver.implicitly_wait(3)
    ul.click()
    content = driver.page_source
    soup = BeautifulSoup(content, 'html.parser')

# Mètode per obtenir les dades de cada un dels jocs de cada pàgina
def getData():

    content = driver.page_source
    soup = BeautifulSoup(content, 'html.parser')
    items = soup.findAll('div', {'class': 'item force-badge'})

    for item in items:
        try:
            url_item = item.find('a').get('href')
            driver.get(url_item)
            content = driver.page_source
            soup = BeautifulSoup(content, 'html.parser')

            item_infoprice = soup.find('div', {'class': 'main-content'})
            item_infogame = soup.find('div', {'class': 'specifics'})

            productstitle.append(item_infoprice.find('h1').text)
            if type(item_infoprice.find('div', {'class': 'total'}) == "NoneType"):
                productsprice.append(None)
            else:
                productsprice.append(item_infoprice.find('div', {'class': 'total'}).text)

            if type(item_infoprice.find('div', {'class': 'retail'}) == "NoneType"):
                productdicountprice.append(None)
                productdicount.append(None)
            else:
                productdicountprice.append(item_infoprice.find('div', {'class': 'retail'}).text.replace("\n", ""))
                productdicount.append(item_infoprice.find('div', {'class': 'discounted'}).text)

            if type(item_infogame.find('div', {'class': 'table-cell release-date'}) == "NoneType"):
                productsreleasedate.append(None)
            else:
                productsreleasedate.append(item_infogame.find('div', {'class': 'table-cell release-date'}).text.replace("\n", ""))

            if type(item_infogame.find('a', {'class': 'limiter'}) == 'NoneType'):
                productsdevelop.append(None)
            else:
                productsdevelop.append(item_infogame.find('a', {'class': 'limiter'}).text.replace("\n", ""))
            productdate.append(datetime.datetime.now())
        except:
            print(item_infogame.find('a', {'class': 'limiter'}).text)
            print(item_infogame.find('div', {'class': 'table-cell release-date'}).text)

    return

def main():
    ul = driver.find_element(by=By.LINK_TEXT, value = "Tendencias")
    driver.implicitly_wait(3)
    ul.click()
    content = driver.page_source
    soup = BeautifulSoup(content, 'html.parser')

    pages = soup.findAll('li')
    pages = pages[3].text

    for i in range(int(pages)-120):
        getData()
        getPage(i+1)
        content = driver.page_source
        soup = BeautifulSoup(content, 'html.parser')
        print(i)


    dict = {'title': productstitle, 'not discounted price':productdicountprice, 'discount': productdicount, 'price':productsprice, 'developer':productsdevelop ,'release date':productsreleasedate, 'extraction date': productdate}
    df = pd.DataFrame(dict)
    df.to_csv("products.csv",  header=True, index = False, sep=',',encoding='utf-8-sig')

main()











