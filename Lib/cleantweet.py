import re,string
import nltk
import csv
import numpy as np
import pandas as pd
from bs4 import BeautifulSoup
import re
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import string
import nltk
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory

""""
Class clean tweet berfungsi sebagai
normalisasi dataset yang akan di training,
dengan cara regex, dan mengganti kata slang 
di tweet berdasarkan KBBI (data/kbba.txt) dan rootword (data/rootword.txt)

kedua file tersebut dapat di update secara manual
"""

class CleanTweet:

    #DATA_KBBI = []  
        
    #kbba_lama = "dataset/preprosesing/kbba_lama.txt" #Slang word or acronym
    #rootword = "rootword.txt" #rootword
    #stopword = "dataset/preprosesing/stopword.txt" #stopword
    

    def clean_tweet_2(tweet):   
        
        #Delete redundant word in data
        def hapus_katadouble(s):
            pattern = re.compile(r"(.)\1{1,}", re.DOTALL)
            return  pattern.sub(r"\1\1", s)

        
        def normalize_alay(text):
            
            alay_dict = pd.read_csv('./Lib/fungsi/new_kamusalay.csv', encoding='latin-1', header=None)
            alay_dict = alay_dict.rename(columns={0: 'original', 
                                            1: 'replacement'})
            
            alay_dict_map = dict(zip(alay_dict['original'], alay_dict['replacement']))
            return ' '.join([alay_dict_map[word] if word in alay_dict_map else word for word in text.split(' ')])

        def remove_stopword(text):
            
            id_stopword_dict = pd.read_csv('./Lib/fungsi/stopword.csv', header=None)
            id_stopword_dict = id_stopword_dict.rename(columns={0: 'stopword'})
            
            text = ' '.join(['' if word in id_stopword_dict.stopword.values else word for word in text.split(' ')])
            text = re.sub('  +', ' ', text) # Remove extra spaces
            text = text.strip()
            return text
            
            return "".join([""+i if not i.startswith("'") and i not in string.punctuation else i for i in filtered_sentence]).strip()

        def stemming(text):
            factory = StemmerFactory()
            stemmer = factory.create_stemmer()
            return stemmer.stem(text)

        emoji_pattern = re.compile("["
            u"\U0001F600-\U0001F64F"  # emoticons
            u"\U0001F300-\U0001F5FF"  # symbols & pictographs
            u"\U0001F680-\U0001F6FF"  # transport & map symbols
            u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                            "]+", flags=re.UNICODE)

        soup = BeautifulSoup(tweet, 'lxml')
        souped = soup.get_text()
        stripped = souped
        
        try:
            tweet = stripped.decode("utf-8-sig").replace(u"\ufffd", "?")
        except:
            tweet = stripped
        
        unicode_literal = re.compile(r'\\u[0-9a-fA-F]{4}|\\U[0-9a-fA-F]{8}')
        tweet = tweet.lower()
        tweet = re.sub(r'rt', '', tweet, flags=re.S)
        tweet = re.sub(r"#(\w+)", ' ', tweet, flags=re.MULTILINE)
        tweet = re.sub(r"@(\w+)", ' ', tweet, flags=re.MULTILINE)
        tweet = re.sub(r'http.+', '', tweet, flags=re.S)
        tweet = re.sub(r'href.+', '', tweet, flags=re.S)
        tweet = emoji_pattern.sub(r'', tweet)
        tweet = unicode_literal.sub(r'', tweet)
        tweet = re.sub(r'".+', '', tweet, flags=re.S)
        tweet = re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", tweet)
        tweet = re.sub(r'\w*\d\w*', '',tweet).strip()
        tweet = normalize_alay(tweet)
        tweet = stemming(tweet)
        tweet = remove_stopword(tweet)
        tweet = hapus_katadouble(tweet)
        #print(tweet)
        #return ("".join(tweet))
        return tweet

