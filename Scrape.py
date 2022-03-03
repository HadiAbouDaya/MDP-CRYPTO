import csv
import pandas as pd
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup

coin = input('Please enter the name of the coin you would like to scrape: ')

driver = webdriver.Chrome("/usr/bin/chromedriver")  
driver.maximize_window()  
driver.get("https://coinmarketcap.com/currencies/{}/historical-data/".format(coin))
time.sleep(3)
for i in range(2):
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
        Date = values[0]
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
print(df.tail())

df["open"]=df["open"].astype(float)
df["high"]=df["high"].astype(float)
df["low"]=df["low"].astype(float)
df["close"]=df["close"].astype(float)
df["volume"]=df["volume"].astype(float)
print(df.tail())
#print("_"*40)
df.to_csv ('{}.csv'.format(coin), index = False, header=True)

import matplotlib.pyplot as plt
import numpy as np
import math

#x = np.arange(0,len(df))
#fig, ax = plt.subplots(1, figsize=(12,6))
#for idx, val in df.iterrows():
#    plt.plot([x[idx], x[idx]], [val['Low'], val['High']])
#plt.show()

x = np.arange(0,len(df))
fig, (ax, ax2) = plt.subplots(2, figsize=(12,8), gridspec_kw={'height_ratios': [4, 1]})
for idx, val in df.iterrows():
    color = '#2CA453'
    if val['open'] > val['close']: color= '#F04730'
    ax.plot([x[idx], x[idx]], [val['low'], val['high']], color=color)
    ax.plot([x[idx], x[idx]-0.1], [val['open'], val['open']], color=color)
    ax.plot([x[idx], x[idx]+0.1], [val['close'], val['close']], color=color)
    
# ticks top plot
ax2.set_xticks(x)#[::3])
ax2.set_xticklabels(df.date)#.dt.date[::3])
ax.set_xticks(x, minor=True)
# labels
ax.set_ylabel('USD')
ax2.set_ylabel('Volume')
# grid
ax.xaxis.grid(color='black', linestyle='dashed', which='both', alpha=0.1)
ax2.set_axisbelow(True)
ax2.yaxis.grid(color='black', linestyle='dashed', which='both', alpha=0.1)
# remove spines
ax.spines['right'].set_visible(False)
ax.spines['left'].set_visible(False)
ax.spines['top'].set_visible(False)
ax2.spines['right'].set_visible(False)
ax2.spines['left'].set_visible(False)
# plot volume
ax2.bar(x, df['volume'], color='lightgrey')
# get max volume + 10%
mx = df['volume'].max()*1.1
# define tick locations - 0 to max in 4 steps
yticks_ax2 = np.arange(0, mx+1, mx/4)
# create labels for ticks. Replace 1.000.000 by 'mi'
yticks_labels_ax2 = ['{:.2f} mi'.format(i/1000000) for i in yticks_ax2]
ax2.yaxis.tick_right() # Move ticks to the left side
# plot y ticks / skip first and last values (0 and max)
plt.yticks(yticks_ax2[1:-1], yticks_labels_ax2[1:-1])
plt.ylim(0,mx)
 
# title
ax.set_title('{} Price\n'.format(coin), loc='left', fontsize=20)
# no spacing between the subplots
plt.subplots_adjust(wspace=0, hspace=0)
plt.show()