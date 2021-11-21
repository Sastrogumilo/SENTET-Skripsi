
#============ ROOT PATH ================================

import sys
sys.path.insert(0, r'../SENTET-MASTER')

#============= PYTHON GENERIC ==========================

from flask import Flask,render_template,url_for,Markup
#import sqlalchemy
import json
import pandas as pd
from flask import request
from flask import send_file
from pandas import Timestamp
import numpy as np
from datetime import date, datetime

from plotly.offline import plot
from plotly.graph_objs import Histogram
from flask import Markup

#============= GRAPH LIBRARY ===========================
import networkx as nx
import matplotlib.cm as cmm
import matplotlib.pyplot as plt

#============== MAIN LIBRARY ============================
from Lib.TwitterConfig import *
#from Lib.create_db import input_database as ID
from Lib.GrafGenerator import Grap_Generate as gg
from Lib.SENTET import *
from Lib.data_helper import *

#=============== DATABASE ===============================
"""
import pymysql
pymysql.install_as_MySQLdb() 
import MySQLdb

pymysql.converters.encoders[Timestamp] = pymysql.converters.escape_datetime
pymysql.converters.encoders[np.float64] = pymysql.converters.escape_float
pymysql.converters.encoders[np.int64] = pymysql.converters._escape_table
pymysql.converters.conversions = pymysql.converters.encoders.copy()
pymysql.converters.conversions.update(pymysql.converters.decoders)

con = MySQLdb.connect(user="root",passwd="",host="localhost",db="coba")
cursor = con.cursor(pymysql.cursors.DictCursor)
"""

app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
app.config["CACHE_TYPE"] = "Null" 

global cari
#
# LIST VARIABEL CSS
#
list_css = [
    '<link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.2.1/css/bootstrap.min.css" integrity="sha384-GJzZqFGwb1QTTN6wy59ffF1BuGJpLSa9DkKMp0DgiMDm4iYMj70gZWKYbI706tWS" crossorigin="anonymous">',
]

#
# LIST VARIABEL JS
#
list_js = [
    #'<script src="https://code.jquery.com/jquery-3.3.1.slim.min.js" integrity="sha384-q8i/X+965DzO0rT7abK41JStQIAqVgRVzpbzo5smXKp4YfRvH+8abtTE1Pi6jizo" crossorigin="anonymous"></script>',
    #'<script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.14.6/umd/popper.min.js" integrity="sha384-wHAiFfRlMFy6i5SRaxvfOCifBUQy1xHdJ/yoi7FRNXMRBu5WHdZYu1hA6ZOblgut" crossorigin="anonymous"></script>',
    #'<script src="https://stackpath.bootstrapcdn.com/bootstrap/4.2.1/js/bootstrap.min.js" integrity="sha384-B0UglyR+jN6CkvvICOB2joaf5I4l3gm9GU6Hc1og6Ls7i6U/mkkaduKaBhlAXv9k" crossorigin="anonymous"></script>'
    #'<script src="component/asset/head.js" integrity="sha384-B0UglyR+jN6CkvvICOB2joaf5I4l3gm9GU6Hc1og6Ls7i6U/mkkaduKaBhlAXv9k" crossorigin="anonymous"></script>',
    '<script src="https://cdnjs.cloudflare.com/ajax/libs/Chart.js/2.7.3/Chart.min.js"></script>',
    '<script src="http://d3js.org/d3.v2.min.js?2.9.3"></script>'
    #'<script src="https://cdnjs.cloudflare.com/ajax/libs/Chart.js/2.7.3/Chart.bundle.min.js"></script>'
]

posts = [
    {
        'author'      : 'Corey Schafer',
        'title'       : 'Blog Post 1',
        'content'     : 'First post content',
        'date_posted' : 'April 20, 2019',
        #'css'         : url_for('static', filename='ujicoba.css')
    },
    {
        'author'      : 'Jane Doe',
        'title'       : 'Blog Post 2',
        'content'     : 'Second post content',
        'date_posted' : 'April 21, 2019',
        #'css'         : url_for('static', filename='ujicoba.css')
    }
]

def json_serial(obj):
    """JSON serializer for objects not serializable by default json code"""

    if isinstance(obj, (datetime, date)):
        return obj.isoformat()
    raise TypeError ("Type %s not serializable" % type(obj))

def SENTET(cari):
    twitter = login()
    

    #cari = 'NurhadiAldo'
    #==================== Proses Crawling =========================================
    dataaccum = MineData(twitter, cari, 2)
    #print(dataaccum)

    #=================== Pre-Proses Data ==========================================
    dp = ProsesStoreData(dataaccum)
    #df = ProcessSentiment(dataaccum)
    dfs = ProcessHashtags(dataaccum)
    #dft = ProcessTimestamp(dataaccum)

    #"=========================Proses Pemasukan Database===========================

    #Proses Memasukan Data ke dalam Database sql
    #ID.masuk_tweet(dp[1]) #tabel tweet
    #ID.masuk_retweet(dp[0]) #tabel retweet
    #ID.sambungan(dp[1]) #tabel_cari

    
    #================= Proses Visualisasi Hasil ==================================
    
    dp_main = dp[2]
    
    gg.Word(dp_main)    
    
    gg.HashtagGraf(dfs, cari)    
    
    jumlah_data = hitung_value_main(dp_main)
       
    gg.VisualLabel(jumlah_data, len(dp_main))
    

    return(dp)

def kata_kunci(cari):
    return cari
'''
def getDB(cari):
    sql = " SELECT tweet.Username, tweet.tanggal, tweet.tweet, tweet.SA FROM tweet \
            LEFT JOIN tabel_cari ON tabel_cari.idT = tweet.idT \
            LEFT JOIN hashtag ON hashtag.idH = tabel_cari.idH \
            WHERE hashtag.isi = %s;" #hashtag.isi = %s (nama hashtag)

    cursor.execute(sql,cari)
'''

       
@app.route("/", methods=['GET','POST'])
@app.route("/home")
def home():
    #dump(render_template("home.html"))
    #print(url_for('static', filename='ujicoba.css'))
    return render_template("component/body/home.html",list_css = list_css,list_js = list_js,)


@app.route("/search",methods=['GET','POST'])

def index():
    
    if request.method == 'POST':
        cari = request.form['search']
        #kata_kunci(cari)
        dp = SENTET(cari)
        dpa = dp[2]
        
        #jumlah_data = hitung_value_main(dpa)
        #vis_label = gg.VisualLabel(jumlah_data, len(dpa))
        vis_data = gg.panjang_tweet(dpa, cari)
        kata_kunci(cari)
        #getDB(cari)
        hitung_tweet = len(dpa)
        #return redirect(url_for("component/body/hasil.html",list_css = list_css,list_js = list_js))
        return render_template("component/body/hasil.html",
                               list_css = list_css,
                               list_js = list_js, 
                               hitung_tweet = hitung_tweet, 
                               cari = cari, 
                               div_placeholder=Markup(vis_data),
                               #div_sentiment=Markup(vis_label)
                               )

        return cari

@app.route("/about")
def about():
    return render_template("component/body/about.html")

@app.route("/documentation")
def documentation():
    return render_template("component/body/documentation.html")


@app.route("/user/<username>")
def show_post(username):
    return "User %s" % username


@app.route("/Download/",methods=['GET','POST'])
def download_csv():
    #cari = kata_kunci()
    return send_file(
        'Lib/export/total.csv',
        mimetype='text/csv',
        attachment_filename='dataset.csv',
        as_attachment=True,
    )

@app.route("/subpath/<path:user_path>")
def show_subpath(user_path):
    return "Path %s" % user_path

'''
@app.route("/getApiAll")

def getApi():
    
    hs = cursor.fetchall()
    #print(hs)
    return json.dumps(hs, default=json_serial)
'''             

def prosesApiDate():
    pass

@app.route("/ujicoba")
def uji():
    return json.dumps(Markup.escape(render_template("ujicoba.html")))
    #return json.dumps(posts)


@app.route("/ujiTampilan")
def ujiTampilan():
    return render_template("component/body/coba.html")

@app.route("/ujiTampilan/json")
def ujiTampilanJson():
    df = pd.read_csv('Lib/export/total.csv')
    #print(df)
    hasil = []
    for i in df.loc[:,'Hashtags']:
        if pd.isnull(i) is False:
            for j in str(i).split(" "):
                if j is not "":
                    hasil.append(j.lower())
    
    edge = []

    edge = list(set(hasil))

    #for i in range(0,len(hasil)):
    #    if len(edge) > 0:
    #        length = len(edge)
    #        print(length)
    #        for j in range(0,length):
    #            if hasil[i] is not edge[j]:
    #                edge.append(hasil[i])
    #    else:
    #        edge.append(hasil[i])
    #        print(edge)
    
    #print(edge)
    link = []
    for i in df.loc[:,'Hashtags']:
        if pd.isnull(i) is False:
            for j in str(i).split(" "):
                if j is not "" and len(j) > 2:
                    for k in str(i).split(" "):
                        if k is not "" and len(k) > 2:
                            if j.lower() is not k.lower():
                                link.append({"source" : edge.index(j.lower()), "target": edge.index(k.lower()), "weight" : 1})
    
    hasil = []
    for i in edge:
        hasil.append({"name":i,"group":1})
    a = {
        "nodes":hasil,
        "links":link,
        "length":[len(hasil),len(link)]
    }
    """a = {
        "nodes":[
            {"name":"node1","group":1},
            {"name":"node2","group":2},
            {"name":"node3","group":2},
            {"name":"node4","group":3}
        ],
        "links":[
            {"source":2,"target":1,"weight":3},
            {"source":0,"target":2,"weight":3},
            {"source":0,"target":2,"weight":3}
        ]
    }"""
    return json.dumps(a)

@app.route("/ujiChart/json")
def ujiChartJSON():
    df = pd.read_csv('Lib/export/total.csv')
    #print(df)
    hasil = []
    a = 0
    b = 0
    c = 0 
    #print(df.loc[:,'SA'])
    for i in df.loc[:,'SA']:
        #print(i)
        if i == "Positif":
            a = a + 1
        elif i == "Negatif":
            b = b + 1
        elif i == "Netral":
            c += 1
    hasil = {
        "P" : a,
        "N" : b,
        "L" : c
    }
    print(hasil)
    return json.dumps(hasil)
    

with app.test_request_context():
    print(url_for('show_post',username="Sastrogumilo"))
    print(url_for('about'))

if __name__ == '__main__':
    app.run(debug=True)