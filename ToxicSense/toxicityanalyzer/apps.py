from django.apps import AppConfig

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
import logging

logger = logging.getLogger(__name__)
global loaded_model
global char_map


def read_in_keras_model(mjson_file, weights_file, char_file):
    json_file = open(mjson_file, 'r')
    loaded_model_json = json_file.read()
    json_file.close()
    loaded_model = model_from_json(loaded_model_json)
    loaded_model.load_weights(weights_file)
    char_map = char_map = json.loads(open(char_file).read())
    return loaded_model, char_map


class ToxicityanalyzerConfig(AppConfig):
    name = 'toxicityanalyzer'

    def ready(self):

        path = os.path.dirname(os.path.realpath(__file__))
        model_json_file = path + '/resources/model-ascii.json'
        model_h5_file = path + "/resources/model-ascii.h5"
        char_to_index = path + "/resources/ascii-char-map.json"


        self.loaded_model, self.char_map = read_in_keras_model(model_json_file, 
model_h5_file,char_to_index)










