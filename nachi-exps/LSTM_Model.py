import sys, os, re, csv, codecs
import numpy as np
import pandas as pd

from keras.preprocessing.text import Tokenizer
from keras.preprocessing.sequence import pad_sequences
from keras.layers import Dense, Input, GRU, Embedding, Dropout, Activation, Conv1D
from keras.layers import Bidirectional, GlobalMaxPool1D, MaxPooling1D
from keras.models import Model
from keras import initializers, regularizers, constraints, optimizers, layers
from keras.callbacks import EarlyStopping, ModelCheckpoint
import gc
from sklearn.model_selection import train_test_split
from keras.models import load_model
import tensorflow as tf
from keras.models import model_from_json
import keras.backend
import unidecode
import json

# Parameters
EMBEDSIZE = 50
MAXFEATURES = 20000
MAXLEN = 100

train = pd.read_csv('data/train.csv')
test  = pd.read_csv('data/test.csv')

X_train, X_test, y_train, y_test = train_test_split(train,
                                        train[["toxic", "severe_toxic", "obscene", "threat", "insult", "identity_hate"]],
                                        test_size = 0.10, random_state = 42)

list_sentences_train = X_train["comment_text"].apply(unidecode.unidecode)
list_sentences_test = X_test["comment_text"].apply(unidecode.unidecode)

tokenizer = Tokenizer(num_words=MAXFEATURES,char_level=True)
tokenizer.fit_on_texts(list(list_sentences_train))
list_tokenized_train = tokenizer.texts_to_sequences(list_sentences_train)
list_sentences_test = tokenizer.texts_to_sequences(list_sentences_test)

X_t = pad_sequences(list_tokenized_train, maxlen=MAXLEN)
X_te = pad_sequences(list_sentences_test, maxlen=MAXLEN)

def get_model(embedding_matrix, dropout = 0.2):
    inp = Input(shape=(MAXLEN,))
    x = Embedding(MAXFEATURES, EMBEDSIZE, weights=[ embedding_matrix])(inp)
    x = Conv1D(filters = 100, kernel_size = 4, padding = 'same', activation = 'relu' )(x)
    x = MaxPooling1D(pool_size =4)(x)
    x = Bidirectional(GRU(60, return_sequences=True, dropout=dropout, recurrent_dropout=0.2))(x)
    x = GlobalMaxPool1D()(x)
    x = Dense(50, activation="relu")(x)
    x = Dropout(dropout)(x)
    x = Dense(6, activation = "sigmoid")(x)
    model = Model(inputs= inp, outputs = x)
    model.compile(loss = 'binary_crossentropy', optimizers = 'adam', metrics = ['accuracy'])
    return model


def get_coefs(word,*arr): return word, np.asarray(arr, dtype='float32')
embeddings_index = dict(get_coefs(*o.strip().split()) for o in open(EMBEDDING_FILE))

all_embs = np.stack(embeddings_index.values())
emb_mean,emb_std = all_embs.mean(), all_embs.std()

word_index = tokenizer.word_index
nb_words = min(MAXFEATURES, len(word_index))
embedding_matrix = np.random.normal(emb_mean, emb_std, (nb_words, EMBEDSIZE))
for word, i in word_index.items():
    if i >= MAXFEATURES: continue
    embedding_vector = embeddings_index.get(word)
    if embedding_vector is not None: embedding_matrix[i] = embedding_vector

model = get_model(embedding_matrix, dropout=0.2)
model.summary()

model.fit(X_t, y, batch_size=32, epochs=2, validation_split=0.1)