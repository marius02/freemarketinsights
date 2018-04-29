import requests
import bs4
from bs4 import BeautifulSoup
import warnings
import time
import datetime
import json
import pandas as pd
import io
import re
import psycopg2
import quandl
from mmduprem import mmduprem


###########################################################
##########################################################
######## Used QUANDL Functions #########################

quandl.ApiConfig.api_key = 'omQiMysF2NQ1B-xZEJBk'

def quandl_stocks(symbol, start_date=(2017, 1, 1), end_date=None):
    query_list = ['WIKI' + '/' + symbol + '.' + str(k) for k in range(11, 12)]
    start_date = datetime.date(*start_date)
    if end_date:
        end_date = datetime.date(*end_date)
    else:
        end_date = datetime.date.today()
    return quandl.get(query_list,
            returns='pandas',
            start_date=start_date,
            end_date=end_date,
            collapse='daily',
            order='asc'
            )

def quandl_adj_close(ticker):
	if len(ticker)<10:
		data=pd.DataFrame(quandl_stocks(ticker))
		#data=data[len(data)-1:]
		data=data.tail(1)
		data=str(data.max()).split(' ')[7:8]
		data=re.split(r'[`\-=;\'\\/<>?]', str(data))
		data=data[1]
		try:
			data=float(data)
		except:
			data=int(0)
		price=round(data,2)
		if price>1:
			return price

def barchart(ticker):
    with requests.Session() as c:
        u='https://www.barchart.com/stocks/quotes/'+ticker
        x=c.get(u)
        x=BeautifulSoup(x.content, "html.parser")
        titles=x.find_all()
        titles=str(titles)
        s=titles[titles.find("dailyLastPrice")+17:titles.find("dailyLastPrice")+17+20].replace('"','').split(",")
        s=float(s[0])
        return s

print(barchart("AAPL"))


#############################################################################
############## Pull Current Portfolio and Obtain Tickers  ###################
conn = psycopg2.connect("dbname='postgres' user='postgres' password='postgres' host='localhost' port='5432'")
cur = conn.cursor()
cur.execute("""SELECT ticker,shares,target_price FROM fmi.portfolio where ticker<>'CASH';""")
portfolio=cur.fetchall()

####################################################
###Pull Quandl Price information for each ticker and send it to database#########
###################################################
for ticker,shares,target_price in portfolio:
    price=quandl_adj_close(ticker)
    value=round(shares*float(price),2)
    cur.execute("""UPDATE fmi.portfolio set price=%s,value=%s where ticker=%s;""", (price, value, ticker))
    conn.commit()
    #Insert calculated expected return
    exp_return=round((target_price-price)/float(price),2)
    exp_value=(target_price*shares)
    cur.execute("""UPDATE fmi.portfolio set exp_return=%s,exp_value=%s where ticker=%s;""", (exp_return,exp_value,ticker))
    conn.commit()

cur.close()
conn.close()
