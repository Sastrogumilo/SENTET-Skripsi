from twython import Twython
import time
import collections
import pandas as pd

import numpy as np
import re
from tqdm import tqdm
from os import path
#from PIL import Image
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator
#from sqlalchemy import create_engine
from bs4 import BeautifulSoup
from nltk.corpus import stopwords

from .functional_sa import Helper as helper
from .data_helper import *
from .GrafGenerator import Grap_Generate
from .cleantweet import CleanTweet as ct
from .TwitterConfig import *
from .TwitterConfig import login

import chart_studio.plotly as py
import plotly.graph_objs as go
import networkx as nx
import matplotlib.pyplot as plt

"""
Main Program yang berfungsi mencrawl data twitter 
dan menjadikan 2 data besar Tweet dan Retweet 

Note: model dapat ditraining, atau di-load, atau di retrain 

an = Analiser(training_data='data/coba_train.csv')

#Training :
filename='model'
an.train(filename)

#Load:
filename = 'model'
an.load_model(filename)

#Retrain:
filename = 'model'
an.retrain(filename)

#Contoh Print Hasil Sentimen :
kata1 = input() 
print (an.testFromTrained([an.tfidf_data.transform(kata1)])) #float
print (an.testFromTrained([an.tfidf_data.transform(kata2)])) #Pos, Net, Neg
"""

#twitter = login() #load TwitterConfig 

#Memanggil Class Analiser untuk load data set


twitter = login()
level = helper.load_level()
main = helper.load_main()
target = helper.load_target()
tipe = helper.load_tipe()   

"""
Mencrawl twitter Data
"""

def MineData(apiobj, query, pagestocollect = 10):

    results = apiobj.search(q=query, include_entities='true',
                            tweet_mode='extended',count='450',
                            result_type='recent',
                            include_retweets=True)

    data = results['statuses']
    i=0
    ratelimit=1
    
    while results['statuses'] and i<pagestocollect: 
        
        if ratelimit < 1: 
            print(str(ratelimit)+'Rate limit!')
            break
        
        mid = results['statuses'][len(results['statuses']) -1]['id']-1

        print(mid)
        print('Jumlah Tweet Per-page : '+str(len(results['statuses'])))
        
        results = apiobj.search(q=query, max_id=str(mid)
                            ,include_entities='true',
                            tweet_mode='extended',count='450',
                            result_type='recent',
                            include_retweets=True)
        
        data+=results['statuses']
        i+=1
        ratelimit = int(apiobj.get_lastfunction_header('x-rate-limit-remaining'))

    #print(data)
    return data

"""
ProcessHashtags berfungsi mengambil hanya 
hashtag
"""

def ProcessHashtags(data):
    HashtagData = pd.DataFrame(columns=['HT','ID','Date','RAWDATA_INDEX'])
    
    for index,twit in enumerate(data):
        HashtagData = HashtagData.append(pd.DataFrame({'ID':twit['id'],
                        'Date':pd.to_datetime(twit['created_at']),
                        'RAWDATA_INDEX':index,
                        'HT':[hashtag['text'] for hashtag 
                                in twit['entities']['hashtags']]})
                            , ignore_index=True)

    return HashtagData
"""
ProcessTimestamp berfungsi mengambil data timestamp 
untuk data pada Class Grap_Generate
"""
def ProcessTimestamp(data):
    TimestampData = pd.DataFrame(columns=['ID','Date','RAWDATA_INDEX'])
    
    for index,twit in enumerate(data):
        TimestampData = TimestampData.append(pd.DataFrame({'ID':[twit['id']],
                        'Date':[pd.to_datetime(twit['created_at'])],
                        'RAWDATA_INDEX':[index]})
                            , ignore_index=True)

    return TimestampData

"""
clean_tweet berfungsi normalisasi tweet sebelum masuk ke DataFrame
"""


"""
ProcessSentiment mengolah data sentimen berdasarkan crawl tweet,
kemudian data sentiment tersebut digunakan pada 
Class Graph_Generate  
"""

"""
ProsesStoreData berfungsi sebagai mengubah data crawl menjadi DataFrame,
dan membagi 2 besar data menjadi Data tweet, dan data Retweet
"""

def ProsesStoreData(data):

    #Note (Penting:)
    #jika terjadi : "TypeError: clean_tweet() missing 1 required positional argument: 'tweet'"
    #atau NameError: name 'an' is not defined
    #kemungkinan class belum diload, atau sudah diload
    
    
    
    df1 = pd.DataFrame(columns=['IDrts', 'ID', 'Username', 'Date', 'Original', 'Tweet', 'Hashtags', 'RT', 'SA',])
    df2 = pd.DataFrame(columns=['ID', 'Username', 'Date', 'Original', 'Tweet', 'Hashtags', 'RT', 'SA',])

    #NLP.an = Analiser(training_data='data/coba_train.csv')
    
    for twit in tqdm(data):
        a = ''
        b = ''
        c = ''
        hasil = helper.sentiment_analisis(twit['full_text'], level, main, target, tipe)
        hasil = str(hasil)[1:-1]
        hasil = re.sub("'", "", hasil)
        
        for hashtag in twit['entities']['hashtags']:
            if hashtag['text'] is None:
                a = ' '
            else:
                a = a + str(hashtag['text'] + ' ')
                a = a.lower()
        if 'retweeted_status' in twit:
        
            df1 = df1.append(pd.DataFrame({
                'IDrts':[(twit['retweeted_status'])],
                'ID':[(twit['id'])],
                'Username':[twit['user']['screen_name']],
                'Date':[pd.to_datetime(twit['created_at'])],
                'Original':[twit['full_text']],
                'Tweet':[ct.clean_tweet_2(twit['full_text'])],
                'Hashtags':[a],
                'RT':[twit['retweet_count']],
                'SA':[hasil],
                #'Float':[float(NLP.an.testFromTrained([NLP.an.tfidf_data.transform(twit['full_text'])]))]
            }))
                
            #b = clean_tweet(twit['full_text'])
        else:
        
            df2 = df2.append(pd.DataFrame({
                'ID':[(twit['id'])],
                'Username':[twit['user']['screen_name']],
                'Date':[pd.to_datetime(twit['created_at'])],
                'Original':[twit['full_text']],
                'Tweet':[ct.clean_tweet_2(twit['full_text'])],
                'Hashtags':[a],
                'RT':[twit['retweet_count']],
                'SA':[hasil],
                #'Float':[float(NLP.an.testFromTrained([NLP.an.tfidf_data.transform(twit['full_text'])]))]
            }))

    #DataJoin = df1[['ID','Username', 'Date', 'Tweet', 'Hashtags', 'RT', 'SA', 'Float']].concat(df2[['ID','Username', 'Date', 'Tweet', 'Hashtags', 'RT', 'SA', 'Float'], on = 'ID')
    #DataJoin = pd.merge(df1, df2, how='inner', left_on = 'ID', right_on = 'ID') 
    DataJoin = pd.concat([df1, df2], sort=False)
    StoreData = [df1, df2, DataJoin]
    df1.to_csv('./Lib/export/RT.csv')
    df2.to_csv('./Lib/export/T.csv')
    DataJoin.to_csv('./Lib/export/total.csv')
    print(StoreData)
    print(DataJoin)
    print("Proses Crawl Data Selesai! \n")
    return StoreData
"""
########
#Contoh Pengunaan
########

cari = 'NurhadiAldo'

NLP = NLP()
dataaccum = NLP.MineData(twitter, cari ,2)

#print(dataaccum)

dp = NLP.ProsesStoreData(dataaccum)
df = NLP.ProcessSentiment(dataaccum)
dfs = NLP.ProcessHashtags(dataaccum)
dft = NLP.ProcessTimestamp(dataaccum)

print("===================================================================== \n")

#Proses Memasukan Data ke dalam Database sql

from create_db import input_database as ID

ID.masuk_tweet(dp[1]) #tabel tweet
ID.masuk_retweet(dp[0]) #tabel retweet
ID.sambungan(dp[1]) #tabel_cari

#Export Grap dari Class Grap_Generate

#from GrafGenerator import Grap_Generate

#gg = Grap_Generate
#gg.PieChart(dp)
#gg.Graf(df, dfs, dft)
#gg.Word(dp)
#gg.Node(dp)
"""