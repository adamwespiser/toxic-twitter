import numpy as np
import logging
import sys
import os
import json

from keras.preprocessing.text import Tokenizer
from keras.preprocessing.sequence import pad_sequences
from keras.models import model_from_json
from keras.models import load_model
from keras import backend
import tensorflow as tf
import pickle

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
logger = logging.getLogger(__name__)

# set tensorflow to run on only the CPU
# https://stackoverflow.com/questions/37660312/how-to-run-tensorflow-on-cpu
config = tf.ConfigProto(
    device_count = {'GPU': 1}
)
config.gpu_options.allow_growth = True
backend.set_session(tf.Session(config=config))
logger.info("Set Tensorflow backend")
# Set our model resources, and character -> int map
path = os.path.dirname(os.path.realpath(__file__)) + "/resources/"
model_json_file = path + 'model.json'
model_h5_file = path + "weights.best.hdf5"
tokenizer_file = path + "tokenizer.pickle"



def read_in_keras_model(mjson_file, weights_file, tokenizer_file):
    json_file = open(mjson_file, 'r')
    loaded_model_json = json_file.read()
    json_file.close()
    loaded_model = model_from_json(loaded_model_json)
    loaded_model.load_weights(weights_file)
    with open(tokenizer_file, 'rb') as handle:
        tokenizer = pickle.load(handle)
    return loaded_model, tokenizer

# Set the global model variable
global loaded_model
global tokenizer
loaded_model = None
tokenizer = None
loaded_model, char_map = read_in_keras_model(model_json_file,
                                             model_h5_file,
                                             tokenizer_file)


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

def glove_preprocess(text):
    """
    adapted from https://nlp.stanford.edu/projects/glove/preprocess-twitter.rb

    """
    # Different regex parts for smiley faces
    eyes = "[8:=;]"
    nose = "['`\-]?"
    text = re.sub("https?:* ", "<URL>", text)
    text = re.sub("www.* ", "<URL>", text)
    text = re.sub("\[\[User(.*)\|", '<USER>', text)
    text = re.sub("<3", '<HEART>', text)
    text = re.sub("[-+]?[.\d]*[\d]+[:,.\d]*", "<NUMBER>", text)
    text = re.sub(eyes + nose + "[Dd)]", '<SMILE>', text)
    text = re.sub("[(d]" + nose + eyes, '<SMILE>', text)
    text = re.sub(eyes + nose + "p", '<LOLFACE>', text)
    text = re.sub(eyes + nose + "\(", '<SADFACE>', text)
    text = re.sub("\)" + nose + eyes, '<SADFACE>', text)
    text = re.sub(eyes + nose + "[/|l*]", '<NEUTRALFACE>', text)
    text = re.sub("/", " / ", text)
    text = re.sub("[-+]?[.\d]*[\d]+[:,.\d]*", "<NUMBER>", text)
    text = re.sub("([!]){2,}", "! <REPEAT>", text)
    text = re.sub("([?]){2,}", "? <REPEAT>", text)
    text = re.sub("([.]){2,}", ". <REPEAT>", text)
    pattern = re.compile(r"(.)\1{2,}")
    text = pattern.sub(r"\1" + " <ELONG>", text)

    return text


def format_tweet(tweet, tokenizer):
    ''' Format the Tweet to input to the model'''
    tweet_pre = glove_preprocess(tweet)
    tweet_seq = tokenizer.texts_to_sequences([tweet_pre])
    array = pad_sequences(tweet_seq, maxlen = MAXLEN)

    return array


def get_toxicity(text):
    # char_map is a set global var
    # if the text is longer than 500, just look at the end
    if len(text) > 500:
        text = text[(len(text)-500):len(text)]
    # use the globally defined char_map for
    # Tweet :: Unicode -> Tweet :: Int
    global tokenizer
    # Globally defined model
    global loaded_model
    tweet_input = format_tweet(text, tokenizer)
    # bug: https://github.com/keras-team/keras/issues/2397
    with backend.get_session().graph.as_default() as g:
        model = loaded_model
        pred = loaded_model.predict(tweet_input)
        predlist = pred.tolist()[0]
        # we can use any combination of the 5 different labels
        # here, I am just using the max of 'toxic' and 'severe_toxic'
        # we should probably look at some tweets and see what works best...
        output = max(predlist[0],predlist[1])
        return float(output)