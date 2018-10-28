import sys, os, re, csv, codecs, numpy as np, pandas as pd
import matplotlib.pyplot as plt
from keras.preprocessing.text import Tokenizer
from keras.preprocessing.sequence import pad_sequences
from keras.layers import Dense, Input, LSTM, Embedding, Dropout, Activation, GRU,Conv1D,MaxPooling1D
from keras.layers import Bidirectional, GlobalMaxPool1D,Bidirectional
from keras.models import Model
from keras import initializers, regularizers, constraints, optimizers, layers
from keras.callbacks import EarlyStopping, ModelCheckpoint
import gc
from sklearn.model_selection import train_test_split
from keras.models import load_model
import tensorflow as tf
import tensorflowjs as tfjs
from keras.models import model_from_json
import unidecode
import keras.backend
import json
import tensorflow as tf
from keras.backend.tensorflow_backend import set_session

config = tf.ConfigProto(
    device_count = {'GPU': 0}
)
config.gpu_options.allow_growth = True
set_session(tf.Session(config=config))

tfjs_directory = 'ascii-3-model'
model_json_file = 'ascii-3-model/model-ascii.json'
model_h5_file = "ascii-3-model/model-ascii.h5"
char_to_index = "ascii-3-model/ascii-char-map.json"

if len(sys.argv) > 1:
    tweet = sys.argv[1]
    print(tweet)
else:
    print("please provide a tweet as arg 1")

def read_in_keras_model(mjson_file, weights_file):
    json_file = open(model_json_file, 'r')
    loaded_model_json = json_file.read()
    json_file.close()
    loaded_model = model_from_json(loaded_model_json)
    loaded_model.load_weights(model_h5_file)
    char_map = char_map = json.loads(open(char_to_index).read())
    return loaded_model, char_map

def format_tweet(tweet, char_map):
    tweet_array = list(unidecode.unidecode(tweet.lower()))
    tweet_int = [char_map.get(x) for x in tweet_array]
    if (len(tweet_int) < 500):
        tweet_int = list([0]*(500 - len(tweet_int))) + tweet_int

    array = np.array(tweet_int).astype(int).reshape(1,500)
    return array


def run_main():
    loaded_model, char_map = read_in_keras_model(model_json_file, 
                                             model_h5_file)
    tweet_input = format_tweet(tweet, char_map)

    labels = ["toxic", "severe_toxic", "obscene", "threat", "insult", "identity_hate"]
    pred = loaded_model.predict(tweet_input)
    print(pred.tolist())
    for i,p in enumerate(pred[0]):
        print(f'{labels[i]}: {p}')

if __name__ == '__main__':
     run_main()

