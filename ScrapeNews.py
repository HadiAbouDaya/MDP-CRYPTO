import csv
import pandas as pd
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
from dateutil.parser import parse


driver = webdriver.Chrome("/usr/bin/chromedriver")  
driver.maximize_window()  
driver.get("https://cryptonews.com/news")
time.sleep(3)
for i in range(int(20)):
    button=driver.find_element(By.XPATH, '//*[@id="load_more"]')
    driver.execute_script("arguments[0].click();", button)
    time.sleep(3)

soup = BeautifulSoup(driver.page_source, 'lxml')
driver.close()

category=[]
divTag = soup.find_all("a", {"class":"article__badge article__badge--sm"})
for tag in divTag:
    category.append(tag.text[1:-1])

newstitle=[]
newslink=[]
divTag = soup.find_all("a", {"class":"article__title article__title--md article__title--featured"})
for tag in divTag:
    newslink.append(str("https://cryptonews.com"+tag['href']))
    for element in tag.find_all("h4"):
        newstitle.append(element.text)

date=[]
divTag = soup.find_all("div", {"class":"article__badge-date d-none d-md-inline-block"})
for tag in divTag:
    date.append(tag['data-utctime'])

dict = {'Category': category, 'Date': date, 'Link': newslink, 'News': newstitle} 
    
df = pd.DataFrame(dict)
print(df.head())
print(df.tail())
df.to_csv('/home/hadi/Desktop/MDP/NewsScraper/news.csv')