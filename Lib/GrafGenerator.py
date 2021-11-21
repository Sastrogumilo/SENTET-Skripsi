from os import path
from PIL import Image
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator
import pandas as pd
import matplotlib.pyplot as plt
import chart_studio.plotly as py
import plotly.graph_objs as go
import networkx as nx
import numpy as np
import nltk
from nltk.corpus import stopwords
import seaborn as sns
from plotly.offline import plot
import plotly.graph_objs as go
from flask import Markup


"""
Class Grap_Generate berfungsi untuk meng-export 
data yang telah dicrawl sebelumnya menjadi :
Grap Batang (Total hashtag)
Grap PieChart (Sentiment Analysis)
WordCloud
dan Node
"""

class Grap_Generate:
  
    def VisualLabel(data, jumlah_data):
        data = nltk.FreqDist(data)
        data_df = pd.DataFrame({"Label":list(data.keys()), 'Jumlah':list(data.values())})

        plt.style.use('ggplot')
        g = data_df.nlargest(columns = 'Jumlah', n=20)
        plt.figure(figsize=(10, 8))
        plt.title("Distribusi Graf Dengan Jumlah Data Sebanyak {} Tweet".format(jumlah_data))
        ax = sns.barplot(data=g, x='Jumlah', y='Label')
        
        #rects = ax.patches
        #for rect, label in zip(rects, g):
        #    height = rect.get_height()
        #    ax.text(rect.get_x() + rect.get_width()/2, height + 5, label, ha='center', va='bottom', fontsize=18)
            
        ax.set(ylabel='Label')
        plt.savefig("./static/asset/sentiment/sentiment.png")
        plt.savefig('./Lib/export/bar_graph.png', dpi = 320)
        plt.gcf().clear()
        print("==== NOTICE: Graph Telah Diexport !")
        
    def plot_Visual_Label(data, jumlah_data):
        
        data = nltk.FreqDist(data)
        data_df = pd.DataFrame({"Label":list(data.keys()), 'Jumlah':list(data.values())})
        x = data_df.nlargest(columns = 'Jumlah', n=20)
        #data['char_length'] = data['Original'].apply(lambda x: len(str(x)))
        #x = data['char_length'] 

        vis_data = [go.Bar(x=x, nbinsx=15 , )]
        
        fig = plot({"data":vis_data,
                    "layout": go.Layout(
                        height=400,
                        width=800,
                        title="Distribusi Graf Dengan Jumlah Data Sebanyak {} Tweet".format(jumlah_data),
                        yaxis_title="Label",
                        xaxis_title="Jumlah",
                        )},
                    output_type="div",
                    show_link=True,
                   )
        
        
        return fig

    def HashtagGraf(data, input):
        hashtagCountData = data['HT'].value_counts()

        plt.title("Graf Hashtag pada Tweet {}".format(input))

        plt.figure(figsize=(10, 6))
        hashtagCountData.head(15).plot.bar()
        plt.tight_layout()

        #Save hashtag data plot 
        plt.savefig("./static/asset/hashtags/hashtags.png")
        plt.savefig('./Lib/export/test_graph_hashtags.png')
        plt.gcf().clear()
        print("==== NOTICE: Hastags graph telah diexport !")

    def Word(StoreData):

        dp = StoreData
        text = " ".join(txt for txt in dp['Tweet'])

        stw = set(stopwords.words('indonesian'))
        #custom = open('data/stopword.txt', 'r', encoding='utf-8').readlines()
        #stopwords.update(stw)

        wordcloud = WordCloud(height=1080, stopwords=stw, width=1920, background_color="white").generate(text)

        plt.figure(figsize=(24, 12))
        plt.imshow(wordcloud, interpolation="bilinear")
        plt.axis("off")
        #plt.show()
        wordcloud.to_file("./Lib/export/test_graph_wordclloud.png")
        #tampil web
        wordcloud.to_file("./static/asset/wordcloud/WordCloud.png")
        plt.gcf().clear()
        print("=== NOTICE: WordCloud telah diexport !")


    def panjang_tweet(StoreData, cari):

        data = StoreData
        data['char_length'] = data['Original'].apply(lambda x: len(str(x)))
        x = data['char_length'] 

        vis_data = [go.Histogram(x=x, nbinsx=15 , )]
        
        fig = plot({"data":vis_data,
                    "layout": go.Layout(
                        height=400,
                        width=800,
                        title="Histogram Panjang Tweet untuk Kata Kunci {}".format(cari),
                        yaxis_title="Frekuensi",
                        xaxis_title="Panjang Tweet",
                        )},
                    output_type="div",
                    show_link=True,
                   )
        
        return fig
        
        
    
"""
    def panjang_tweet(StoreData, cari):
        data = StoreData
        data['char_length'] = data['Original'].apply(lambda x: len(str(x)))
        
        #graf = data['char_length'].hist()    
        sns.set(rc={'figure.figsize':(10,6)})
        graf = data['char_length'].hist()
        graf.set_title("Panjang Tweet Untuk Kata Kunci {}".format(cari))
        graf.set_xlabel("Panjang Tweet")
        graf.set_ylabel("Jumlah Tweet")
        
        #graf.tight_layout()
        #web
        plt.savefig("./static/asset/panjang_tweet/panjang_tweet.png")
        #test
        plt.savefig('./Lib/export/test_panjang_tweet.png')
        
        plt.gcf().clear()
        print("=== NOTICE: Graf Panjang Tweet telah diexport !")



def Node(StoreData):

        G = nx.Graph()
        G.clear()
        dp = StoreData

        hashtags = []
        for hash_list in dp.values[:,5]:
            hashtags.extend(hash_list[2:-2].split('; '))
        from collections import OrderedDict
        hashtags = list(OrderedDict.fromkeys(hashtags))
        for hashtag in hashtags:
            G.add_node(hashtag.lower(), name=hashtag.lower())

        edges = []
        for hash_list in dp.values[:,5]:
            hash_list = hash_list[2:-2].split('; ')
            if len(hash_list) > 1:
                for i in range(0,len(hash_list)):
                    for j in range(i+1,len(hash_list)):
                        edges.append([hash_list[i].lower(), hash_list[j].lower()])
        for edge in edges:
            G.add_edge(edge[0], edge[1])

        G.remove_nodes_from([d[0] for d in G.degree if d[1] <= 10 ])

        nx.draw(G, node_size=1600, cmap=plt.cm.Reds,
                node_color=range(len(G)), pos=nx.random_layout(G), with_labels=True)

        plt.savefig("./Lib/export/node.png", format='PNG')
        nx.write_gexf(G, "node-hashtag.gexf")
        print("Node Telah Diexport")

      
def PieChart(StoreData):
        
    pos_tweet = StoreData['SA'].value_counts()

    colors = ['yellowgreen','gray','lightcoral']
    pos_tweet.plot.pie(
            shadow=False,
            colors=colors, 
            explode=(0.1, 0.1, 0.1),
            startangle=90,
            autopct='%1.1f%%'
            )

    plt.tight_layout()
    plt.savefig('export/test_graph_pie.png', dpi = 96)
    print("Graph Pie Chart Telah Diexport")
    plt.gcf().clear()
    
 def Graf(SentimentData, HashtagData, TimestampData):

        df = SentimentData

        df = df.astype({'Polarity': 'float64'})

        SentimentbyDate = df.groupby([df['Date'].dt.date, 
                                df['Date'].dt.hour, 
                                df['Date'].dt.minute])['Polarity'].mean()
        df = TimestampData

        TwittbyDate = df.groupby([df['Date'].dt.date, 
                                df['Date'].dt.hour, 
                                df['Date'].dt.minute]).size()
        df = HashtagData
        
        hashtagCountData = df['HT'].value_counts()

        x = np.arange(TwittbyDate.size)

        fit = np.polyfit(x, TwittbyDate, 1)
        fit_fn = np.poly1d(fit)
        #Plot data
        TwittbyDate.plot()
        plt.plot(x, fit_fn(x), 'r-')
        plt.plot(x, TwittbyDate, 'g-', ms=4)
        plt.xticks(rotation=90)

        plt.xlabel('Tanggal, Jam, Menit')
        plt.ylabel('Twitter disebut per menit')
        plt.legend(["NLP Sentiment Polarity antara 0 to 1",
                    "Liner regression untuk rata - rata di mention"])
        #plt.title("Query text: ")

        ax2=plt.twinx()
        ax2.set_ylim(0,1)

        ColorMap = SentimentbyDate > 0
        SentimentbyDate.plot.bar(color=ColorMap.map({True: 'b', False: 'r'}),ax=ax2 )

        plt.ylabel('Sentimet polarity')
        plt.tight_layout()

        #plt.savefig('export/test_graph.png')
        #print("Sentimen Graph Telah diexport")
        plt.gcf().clear()

        hashtagCountData.head(20).plot.bar()
        plt.tight_layout()

        #Save hashtag data plot 
        plt.savefig('export/test_graph_hashtag.png')
        print("Hastags graph telah diexport")
        plt.gcf().clear()
"""