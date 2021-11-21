"""
Fungsi untuk menghitung data pada hasil crawling tweet

"""
from sklearn.preprocessing import MultiLabelBinarizer
import pandas as pd
from pandas import Series, DataFrame
import re

def hitung_value_main(data):
    list_label = []
    for label in data['SA']:
        list_label.append(re.split(', ', label))
    s = sum(list_label, [])
    return s

