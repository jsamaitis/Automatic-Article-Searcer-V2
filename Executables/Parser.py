url = ['https://feeds.finance.yahoo.com/rss/2.0/headline?s=',',m&region=US&lang=en-US']
tickers = ['spy','iwm','cvx','bac','eem','bmy','jpm','xlf','jnj','c','cl','wfc','xom','gdx','vz','ge','wmt','abbv','baba','ba','cvs','gd','pg','apd','t']
#Source: http://www.marketwatch.com/tools/screener?exchange=Nyse&report=MostActiveByDollarsTraded

import feedparser
import pandas as pd
import time
import os
from datetime import datetime
from pytz import timezone

def parseRSS( rss_url ):
    return feedparser.parse( rss_url )

def getData (rss_url):
    headlines = []
    links = []
    dates = []
    feed = parseRSS(rss_url)
    for newsitem in feed['items']:
        headlines.append(newsitem['title'])
        links.append(newsitem['link'])
        dates.append(newsitem['published'])
    df = pd.DataFrame(
        {"Headlines": headlines,
         "Dates": dates,
         "Links": links}
    )
    return df

def dateCnvFrom (dataframe):
    for i in range(len(dataframe['Dates'])):
        dataframe['Dates'][i] = time.strptime(dataframe['Dates'][i], '%a, %d %b %Y %H:%M:%S %Z')
    return (dataframe)

def dateCnvTo (dataframe):
    for i in range(len(dataframe['Dates'])):
        dataframe['Dates'][i] = time.strftime('%a, %d %b %Y %H:%M:%S',dataframe['Dates'][i]) + ' GMT'
    return(dataframe)

#----
start = datetime.now(timezone('GMT')).replace(hour = 1, minute = 30, second = 0) #Setting NYSE opening time of 14:30 in GMT
start = start.strftime('%a, %d %b %Y %H:%M:%S %Z', )
start = time.strptime(start, "%a, %d %b %Y %H:%M:%S %Z")
end = datetime.now(timezone('GMT')).replace(hour = 21, minute = 0, second = 0)
end = end.strftime('%a, %d %b %Y %H:%M:%S %Z', )
end = time.strptime(end, "%a, %d %b %Y %H:%M:%S %Z")

for tick in tickers:
    df = getData(rss_url = url[0] + tick + url[1])
    df = dateCnvFrom(df)
    df = df[df['Dates'] <= end]
    df = df[df['Dates'] >= start]
    df = df.drop_duplicates(subset='Links')
    if df.empty == False :
        df = dateCnvTo(df)
        dir_path = os.getcwd()[:-11] + '\Data\Articles\%s.csv' % (tick)
        df.to_csv(dir_path, index = False, index_label = False)
    time.sleep(10)

