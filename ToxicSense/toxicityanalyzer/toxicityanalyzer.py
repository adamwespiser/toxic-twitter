import numpy as np
import unidecode
import logging
import sys
import os
import unidecode
import json

from keras.preprocessing.text import Tokenizer
from keras.preprocessing.sequence import pad_sequences
from keras.models import model_from_json
from keras.models import load_model
from keras import backend
import tensorflow as tf
import pickle
import numpy as np


logger = logging.getLogger(__name__)

# set tensorflow to run on only the CPU
# https://stackoverflow.com/questions/37660312/how-to-run-tensorflow-on-cpu
config = tf.ConfigProto(
    device_count = {'GPU': 0}
)
config.gpu_options.allow_growth = True
backend.set_session(tf.Session(config=config))
logger.info("Set Tensorflow backend")

# Set our model resources, and character -> int map
path = os.path.dirname(os.path.realpath(__file__)) + "/resources/"
model_json_file = path + 'model-ascii.json'
model_h5_file = path + "model-ascii.h5"
char_to_index = path + "ascii-char-map.json"
swearWordsDict =pickle.load(open(path + "swearWordDict.pickle", 'rb'))
NUM_WORDS = 1


def read_in_keras_model(mjson_file, weights_file, char_file):
    json_file = open(mjson_file, 'r')
    loaded_model_json = json_file.read()
    json_file.close()
    loaded_model = model_from_json(loaded_model_json)
    loaded_model.load_weights(weights_file)
    char_map = char_map = json.loads(open(char_file).read())
    return loaded_model, char_map

# Set the global model variable
global loaded_model
global char_map
loaded_model = None
char_map = None
loaded_model, char_map = read_in_keras_model(model_json_file,
                                             model_h5_file,
                                             char_to_index)
logger.info("Loaded in Keras model")

# Model Labels:
# The model returns a (0,1) number for each of these classes
# we are going to return the max of the array
labels = [
    "toxic",
    "severe_toxic",
    "obscene",
    "threat",
    "insult",
    "identity_hate"
]


def format_tweet(tweet, char_map):
    # establish a default char for unicode not seen
    # during training
    # (1 corresponds to ' ' or 'space')
    default_char = 1 
    # transform Unicode -> Ascii
    tweet_array = list(unidecode.unidecode(tweet.lower()))
    # map the tweet (in ascii) to ints according to the char map
    tweet_int = [char_map.get(x, 1) for x in tweet_array]
    # the model (as is) only works for 500 char arrays
    if (len(tweet_int) < 500):
        tweet_int = list([0]*(500 - len(tweet_int))) + tweet_int
    array = np.array(tweet_int).astype(int).reshape(1,500)
    return array

def getTextHighlighting(text, baseline = None):
    ''' Method to return the texts to highlight'''
    highlight_idx = []
    words = text.split(' ')
    nWords = len(words)
    for k in range(nWords):
        if words[k] in swearWordsDict:
            highlight_idx.append(k)
    return highlight_idx



def get_toxicity(text, highlight = False):
    # char_map is a set global var
    # if the text is longer than 500, just look at the end
    if len(text) > 500:
        text = text[(len(text)-500):len(text)]
    # use the globally defined char_map for
    # Tweet :: Unicode -> Tweet :: Int
    global char_map
    # Globally defined model
    global loaded_model
    tweet_input = format_tweet(text, char_map)
    # bug: https://github.com/keras-team/keras/issues/2397
    with backend.get_session().graph.as_default() as g:
        pred = loaded_model.predict(tweet_input)
        predlist = pred.tolist()[0]
        # we can use any combination of the 5 different labels
        # here, I am just using the max of 'toxic' and 'severe_toxic'
        # we should probably look at some tweets and see what works best...
        output = max(predlist[0],predlist[1])
        if float(output) > 0.8 and highlight:
            listOfWords = tweet_input.split(' ')
            nWords = len(listOfWords)
            baseline = float(output)
            words_to_highlight = []
            for i in range(nWords - (NUM_WORDS -1)):
                listOfWords = tweet_input.split()
                curWord = ' '.join(listOfWords[i:i+NUM_WORDS])
                for k in range(NUM_WORDS):
                    del listOfWords[i]
                cur_toxic_tweet = ' '.join(listOfWords)
                curValue = get_toxicity(cur_toxic_tweet, highlight=False)
                if curValue < baseline:
                    words_to_highlight.append(i)

        return float(output)
