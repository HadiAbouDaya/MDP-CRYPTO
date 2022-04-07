import csv
import pandas as pd
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
from dateutil.parser import parse

coin = input('Please enter the name of the coin you would like to scrape: ')
tp = float(input('How many years do you want to scrape: '))

driver = webdriver.Chrome("/usr/bin/chromedriver")  
driver.maximize_window()  
driver.get("https://coinmarketcap.com/currencies/{}/historical-data/".format(coin))
time.sleep(3)
for i in range(int(10*tp)):
    button=driver.find_element(By.XPATH, '//button[text()="Load More"]')
    driver.execute_script("arguments[0].click();", button)
    time.sleep(3)

soup = BeautifulSoup(driver.page_source, 'lxml')
driver.close()

data = []
table = soup.find('table', id='')
for row in table.find_all('tr'):
    cells = row.findChildren('td')
    values = []
    for cell in cells:
        value = cell.string
        values.append(value)
    try:
        Date = parse(values[0]).date()
        Open = values[1][1:].replace(',', '')
        High = values[2][1:].replace(',', '')
        Low =  values[3][1:].replace(',', '')
        Close = values[4][1:].replace(',', '')
        Volume = values[5][1:].replace(',', '')
        MarketCap = values[6][1:].replace(',', '')
    except IndexError:
        continue
    data.append([Date, Open, High, Low, Close, Volume, MarketCap])
df = pd.DataFrame(data, columns = ['date', 'open', 'high', 'low', 'close', 'volume', 'marketCap'])

df["open"]=df["open"].astype(float)
df["high"]=df["high"].astype(float)
df["low"]=df["low"].astype(float)
df["close"]=df["close"].astype(float)
df["volume"]=df["volume"].astype(float)
print(df.tail())
df.to_csv ('{}.csv'.format(coin), index = False, header=True)


import mplfinance as mpf
df_plot = df.copy()
df_plot['date'] = pd.to_datetime(df_plot['date'])
df_plot = df_plot.set_index('date')
df_plot=df_plot[::-1]
mpf.plot(df_plot,type='candle',mav=(20, 60),volume=True, title='{} to USD Chart'.format(coin.capitalize()))
