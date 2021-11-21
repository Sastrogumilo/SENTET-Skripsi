import tensorflow as tf
from tensorflow import keras
import pickle
import re
import pandas as pd
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory
from keras.preprocessing.text import one_hot, Tokenizer
from keras.preprocessing.sequence import pad_sequences
from tensorflow.compat.v1.keras.backend import set_session

"""
Fungsi untuk membantu penanganan session mesin pada saat memberikan 
klasifikasi pada tweet yang di crawlling dan fungsi untuk mempercantik hasil 
klasifikasi
"""

#Tensorflow Sessions ===================================================
config = tf.compat.v1.ConfigProto()
config.gpu_options.allow_growth = True  # dynamically grow the memory used on the GPU
config.log_device_placement = True  # to log device placement (on which device the operation ran)
                                    # (nothing gets printed in Jupyter, only if you run it standalone)
sess = tf.compat.v1.Session(config=config)
set_session(sess)  # set this TensorFlow session as the default session for Keras

#Load Model ============================================================

class Helper:
    

    def load_level():
        print("==== Notif: Level Model Loaded ! =====\n")
        return keras.models.load_model("Lib/model/Level.h5",)

    def load_main():
        print("==== Notif: Main Model Loaded ! =====\n")
        return keras.models.load_model("Lib/model/Main.h5",)

    def load_target():
        print("==== Notif: Target Model Loaded ! =====\n")
        return keras.models.load_model("Lib/model/Target.h5",)

    def load_tipe():
        print("==== Notif: Type Model Loaded ! =====\n")
        return keras.models.load_model("Lib/model/Type.h5",)

    #Contoh
    #level = load_level()
    #main = load_main()
    #target = load_target()
    #tipe = load_tipe()

    #Preprocess Text =========================================================

    
    def lowercase(text):
        return text.lower()

    def remove_unnecessary_char(text):
        #\xf0\x9f\x98\x84\xf0\x9f\x98\x84\xf0\x9f\x98\x84'
        text = re.sub('\n',' ',text) # Remove every '\n'
        text = re.sub('rt',' ',text) # Remove every retweet symbol
        text = re.sub('xf0',' ',text) # Remove every retweet symbol
        text = re.sub('x9f',' ',text) # Remove every retweet symbol
        text = re.sub('x98',' ',text) # Remove every retweet symbol
        text = re.sub('x82',' ',text) # Remove every retweet symbol
        text = re.sub('x84',' ',text) # Remove every retweet symbol
        text = re.sub('xe2',' ',text) # Remove every retweet symbol
        text = re.sub('x80',' ',text) # Remove every retweet symbol
        text = re.sub('amp',' ',text) # Remove every retweet symbolxa6
        text = re.sub('xa6',' ',text) # Remove every retweet symbol xa4
        text = re.sub('xa4',' ',text) # Remove every retweet symbol

        text = re.sub('user',' ',text) # Remove every username
        text = re.sub('((www\.[^\s]+)|(https?://[^\s]+)|(http?://[^\s]+))',' ',text) # Remove every URL
        text = re.sub('  +', ' ', text) # Remove extra spaces
        return text
        
    def remove_nonaplhanumeric(text):
        text = re.sub('[^0-9a-zA-Z]+', ' ', text) 
        return text

       
    def normalize_alay(text):
        alay_dict = pd.read_csv('./Lib/fungsi/new_kamusalay.csv', encoding='latin-1', header=None)
        alay_dict = alay_dict.rename(columns={0: 'original', 
                                                1: 'replacement'}) #change into function
        
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

    #print("remove_nonaplhanumeric: ", remove_nonaplhanumeric("Halooo,,,,, duniaa!!"))
    #print("lowercase: ", lowercase("Halooo, duniaa!"))
    #print("stemming: ", stemming("Perekonomian Indonesia sedang dalam pertumbuhan yang membanggakan"))
    #print("remove_unnecessary_char: ", remove_unnecessary_char("Hehe\n\n RT USER USER apa kabs www.google.com\n  hehe"))
    #print("normalize_alay: ", normalize_alay("aamiin adek abis"))
    #print("remove_stopword: ", remove_stopword("ada hehe adalah huhu yang hehe"))

    def preprocess(text):
        text = Helper.lowercase(text) # 1
        text = Helper.remove_nonaplhanumeric(text) # 2
        text = Helper.remove_unnecessary_char(text) # 2
        text = Helper.normalize_alay(text) # 3
        text = Helper.stemming(text) # 4
        text = Helper.remove_stopword(text) # 5
        return text

    #Convert Model to Label ==================================================
    
    '''
    #Contoh Multi-class prediction
    def pred_to_label_main(prediction):
    categories = []
    
    
    '''

    def prediction_to_label_main(prediction):
        categories = ["HS", "Abusive"]
        tag_prob = [(categories[i], prob) for i, prob in enumerate(prediction.tolist())]
        return dict(sorted(tag_prob, key=lambda kv: kv[1], reverse=False))

    def prediction_to_label_target(prediction):
        categories = ["HS_Individu", "HS_Group"]
        tag_prob = [(categories[i], prob) for i, prob in enumerate(prediction.tolist())]
        return dict(sorted(tag_prob, key=lambda kv: kv[1], reverse=False))

    def prediction_to_label_type(prediction):
        categories = ['HS_Religion', 'HS_Race', 'HS_Physical', 'HS_Gender', 'HS_Other']
        tag_prob = [(categories[i], prob) for i, prob in enumerate(prediction.tolist())]
        return dict(sorted(tag_prob, key=lambda kv: kv[1], reverse=False))

    def prediction_to_label_level(prediction):
        categories = ['HS_Weak', 'HS_Moderate', "HS_Strong"]
        tag_prob = [(categories[i], prob) for i, prob in enumerate(prediction.tolist())]
        return dict(sorted(tag_prob, key=lambda kv: kv[1], reverse=False))

    def get_features(text_series):
        """
        transforms text data to feature_vectors that can be used in the ml model.
        tokenizer must be available.
        """
        maxlen = 200
        tokenizer = Tokenizer(10700)

        with open('./Lib/fungsi/tokenizer.pickle', 'rb') as handle:
            tokenizer = pickle.load(handle)
        sequences = tokenizer.texts_to_sequences(text_series)
        return pad_sequences(sequences, maxlen=maxlen, padding='pre')

    #Main Test Feature ============================================================
    
    '''
        #Contoh fungsi multi-class 
        def sentiment_analisis_multi_class(text, model):
            
            labels = ["","",""]
            
            sentiment = []
            f = Helper.preprocess(text) #preprocess kata
            #print(f)
            f =  Helper.get_features([f]) #pad_sequence kata
            
            hasil = model.predict(f)
            
            label = labels[np.argmax(hasil)]
            
            sentiment.append(label) 
            
            return sentiment
                    
            
    '''

    def sentiment_analisis(text, level_model, main_model, target_model, tipe_target):
        

        sentiment = []
        f = Helper.preprocess(text)
        #print(f)
        f =  Helper.get_features([f])
        #print(f)


        def sa():
            pred_main = Helper.prediction_to_label_main(main_model.predict(f)[0])
            for label, nilai in pred_main.items():
                if nilai >= 0.5:
                    sentiment.append(label)

                    pred_target = Helper.prediction_to_label_target(target_model.predict(f)[0])
                    for label_target, nilai_target in pred_target.items():
                        if nilai_target >= 0.5:
                            sentiment.append(label_target)
                        else:
                            None

                    pred_type = Helper.prediction_to_label_type(tipe_target.predict(f)[0])
                    for label_tipe, nilai_tipe in pred_type.items():
                        if nilai_tipe >= 0.5:
                            sentiment.append(label_tipe)
                        else:
                            None

                    pred_level = Helper.prediction_to_label_level(level_model.predict(f)[0])
                    for label_level, nilai_level in pred_level.items():
                        if nilai_level >= 0.5:
                            sentiment.append(label_level)
                        else:
                            None      
                else:
                    sentiment.append("Normal")
        
            return sentiment

        def double_check(temp1):
            res = [] 
        
            [res.append(x) for x in temp1 if x not in res] 
            return res
            
        def triple_check(temp1):
            if len(temp1) <= 1:
                new_list = temp1
            else:
                new_list = list(filter(lambda x : x != "Normal", temp1))
            return new_list

        hasil = sa()
        hasil = double_check(hasil)
        hasil = triple_check(hasil)
        return hasil

    #=================================================================================

    #Contoh: 

    #level = load_level()
    #main = load_main()
    #target = load_target()
    #tipe = load_tipe()

    #hasil = sentiment_analisis(teks, level_model=level, main_model=main, target_model=target, tipe_target=tipe)
    #print(hasil)