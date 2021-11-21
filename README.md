![alt text](https://raw.githubusercontent.com/Sarewes2310/SENTET/master/static/asset/Logo/SENTET_2.png?token=AVp8RroIPfI2JxAkhoiin7WnAQvqSRycks5cZA6qwA%3D%3D)
<br><br>
SENTET adalah sebuah RESTful API yang berguna untuk menganalisa sebuah tweet yang berkaitan dengan pemilu. Tweet akan di kelompokan menjadi tiga kriteria, yaitu: postif, negatif, netral dengan ekstraksi fitur TF-IDF 
# Getting Started
Buat terlebih dahulu api pada halaman developer twitter https://apps.twitter.com. Registrasi aplikasi yang telah anda buat.
Setelah berhasil simpan ```Consumer Key```, ```Consumer Secret```, ```Api Key ```, dan ```Api Secret Key``` yang didapat tab Apps.
Kemudian isikan di file TwitterConfig.py

### Prerequisites
Dalam menggunakan RESTful API SENTET memerlukan beberapa library tambahan:
```
twython, pandas, matplotlib, numpy, keras, tensorflow, scikit-learn, nltk, networkx, plotly, pymyql
```

### Instalation
1. Install requirement nya dulu 
2. Download semua model di : https://drive.google.com/drive/folders/10YHKfQ2VNgMOc2QSAs1bNWjl2P35QEkG?usp=sharing
3. Masukan model pada folder Lib/model


### Usage 

1. langsung run file ```template.py```
2. buka browser url : ```127.0.0.1:5000```


