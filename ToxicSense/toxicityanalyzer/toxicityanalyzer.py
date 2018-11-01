import random
from django.apps import AppConfig
from django.apps import apps
import numpy as np
import unidecode
import logging
import os

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





logger = logging.getLogger(__name__)
global loaded_model
global char_map
loaded_model = None
char_map = None
path = os.path.dirname(os.path.realpath(__file__)) + "/resources/"

model_json_file = path + 'model-ascii.json'
model_h5_file = path + "model-ascii.h5"
char_to_index = path + "ascii-char-map.json"
def read_in_keras_model(mjson_file, weights_file, char_file):
    json_file = open(mjson_file, 'r')
    loaded_model_json = json_file.read()
    json_file.close()
    loaded_model = model_from_json(loaded_model_json)
    loaded_model.load_weights(weights_file)
    char_map = char_map = json.loads(open(char_file).read())
    return loaded_model, char_map
loaded_model, char_map = read_in_keras_model(model_json_file, model_h5_file,char_to_index)

labels = ["toxic",
          "severe_toxic",
          "obscene",
          "threat",
          "insult",
          "identity_hate"]



def get_toxicity(text):
    # char_map is a set global var
    global char_map
    global loaded_model

    tweet_input = format_tweet(text, char_map)
    pred = loaded_model.predict(tweet_input)
    output = pred.tolist()
    return max(output)

def format_tweet(tweet, char_map):
    tweet_array = list(unidecode.unidecode(tweet.lower()))
    if len(tweet_array) > 500:
        tweet_array = tweet_array[0:500]
    tweet_int = [char_map.get(x) for x in tweet_array]
    if (len(tweet_int) < 500):
        tweet_int = list([0]*(500 - len(tweet_int))) + tweet_int

    array = np.array(tweet_int).astype(int).reshape(1,500)
    return array
