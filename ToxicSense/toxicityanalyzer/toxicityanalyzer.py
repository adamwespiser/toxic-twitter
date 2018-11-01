import random
import numpy as np
import unidecode
import logging
import sys, os, re, csv, codecs
import numpy as np
import unidecode
import json

from keras.preprocessing.text import Tokenizer
from keras.preprocessing.sequence import pad_sequences
from keras.models import model_from_json
from keras import backend
import keras.backend
from keras.backend.tensorflow_backend import set_session
import gc
from keras.models import load_model
import tensorflow as tf


logger = logging.getLogger(__name__)

config = tf.ConfigProto(
# set tensorflow to run on only the CPU
# https://stackoverflow.com/questions/37660312/how-to-run-tensorflow-on-cpu
        device_count = {'GPU': 0}
)
config.gpu_options.allow_growth = True
set_session(tf.Session(config=config))


global loaded_model
global char_map

loaded_model = None
char_map = None

# Set our model resources, and character -> int map
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
loaded_model, char_map = read_in_keras_model(model_json_file,
                                             model_h5_file,
                                             char_to_index)

labels = ["toxic",
          "severe_toxic",
          "obscene",
          "threat",
          "insult",
          "identity_hate"]

def format_tweet(tweet, char_map):
    default_char = 1 # corresponds to ' ' (space)
    tweet_array = list(unidecode.unidecode(tweet.lower()))
    tweet_int = [char_map.get(x,1) for x in tweet_array]
    # the model (as is) only works for 500 char arrays
    if (len(tweet_int) < 500):
        tweet_int = list([0]*(500 - len(tweet_int))) + tweet_int
    logger.warn(tweet_int)
    array = np.array(tweet_int).astype(int).reshape(1,500)
    return array


def get_toxicity(text):
    # char_map is a set global var
    logger.warn(text)
    # if the text is longer than 500, just look at the end
    if len(text) > 500:
        text = text[(len(text)-500):len(text)]
    global char_map
    global loaded_model
    tweet_input = format_tweet(text, char_map)
    # bug: https://github.com/keras-team/keras/issues/2397
    with backend.get_session().graph.as_default() as g:
        model = loaded_model
        pred = loaded_model.predict(tweet_input)
        output = np.max(pred)
        return float(output)

