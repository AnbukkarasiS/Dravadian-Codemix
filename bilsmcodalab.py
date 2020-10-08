# -*- coding: utf-8 -*-
"""BiLSmCodalab

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1zjjtMtPpbpeCNCk_JLoKJ_l9L3oJ5nqX
"""

from google.colab import files
import pandas as pd
import io
uploaded = files.upload()
#df = pd.read_csv('tamil_test1.csv')
df= pd.read_csv('test.csv', sep=',')
df.head(3)

df = df[['text','category']]
df.head(10)

# convert airline_seentiment to numeric
sentiment_label = df.category.factorize()
sentiment_label

from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences


mytext = df.text.values
tokenizer = Tokenizer(num_words=5000)
tokenizer.fit_on_texts(mytext)

vocab_size = len(tokenizer.word_index) + 1
encoded_docs = tokenizer.texts_to_sequences(mytext)
padded_sequence = pad_sequences(encoded_docs, maxlen=200)

# Build the model
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM,Dense, Dropout
from tensorflow.keras.layers import SpatialDropout1D
from tensorflow.keras.layers import Embedding
embedding_vector_length = 32
model = Sequential()
model.add(Embedding(vocab_size, embedding_vector_length,     
                                     input_length=200) )
model.add(SpatialDropout1D(0.25))
model.add(LSTM(50, dropout=0.5, recurrent_dropout=0.5))
model.add(Dropout(0.2))
model.add(Dense(5, activation='softmax'))
model.compile(loss='sparse_categorical_crossentropy',optimizer='adam', 
                           metrics=['accuracy'])
print(model.summary())

#Bi directional example
import tensorflow
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM,Dense, Dropout, SpatialDropout1D
from tensorflow.keras.layers import Embedding

# Input for variable-length sequences of integers
inputs = tensorflow.keras.Input(shape=(None,), dtype="int32")
# Embed each integer in a 128-dimensional vector
x = tensorflow.keras.layers.Embedding(vocab_size, 128)(inputs)
# Add 2 bidirectional LSTMs
x = tensorflow.keras.layers.Bidirectional(tensorflow.keras.layers.LSTM(64, return_sequences=True))(x)
x = tensorflow.keras.layers.Bidirectional(tensorflow.keras.layers.LSTM(64))(x)
# Add a classifier
outputs = tensorflow.keras.layers.Dense(5, activation="sigmoid")(x)
model = tensorflow.keras.Model(inputs, outputs)
model.compile(loss='sparse_categorical_crossentropy',optimizer='adam', metrics=['accuracy'])  
print(model.summary()) 
#model.summary()

history = model.fit(padded_sequence,sentiment_label[0],epochs=5,batch_size=128,validation_split=0.2)

from google.colab import files
import pandas as pd
import io
uploaded = files.upload()
#df = pd.read_csv('tamil_test1.csv')
df= pd.read_csv('tamil_test1.csv', sep=',')
df.head(3)

df = df[['text']]
df.head(10)

import numpy as np
tweet = df.text.values

for test_word in tweet:
  seq = tokenizer.texts_to_sequences([test_word])
  padded = pad_sequences(seq,maxlen=200)
  pred = model.predict(padded)
  labels = ['Positive', 'Negative', 'Mixed_feelings', 'unknown_state','not-Tamil'] 
  #print(pred)
  #print(np.argmax(pred))
  print(labels[np.argmax(pred)-1])

tweet = df.text.values
#tokenizer = Tokenizer(num_words=5000)
tokenizer.fit_on_texts(tweet)

vocab_size = len(tokenizer.word_index) + 1
encoded_docs = tokenizer.texts_to_sequences(tweet)
padded_sequence1 = pad_sequences(encoded_docs, maxlen=200)

from sklearn.metrics import classification_report
import numpy as np

y_pred = model.predict(padded_sequence, batch_size=64, verbose=1)
y_pred_bool = np.argmax(y_pred, axis=1)

print(classification_report(sentiment_label[0], y_pred_bool))

from tensorflow.keras.utils import plot_model
plot_model(model, to_file='model.png')

history = model.fit(padded_sequence,sentiment_label[0],epochs=5,batch_size=128,validation_split=0.2)

tokenizer.word_index.get("Trailer", "word not in the vocabulary")

tokenizer.num_words

tokenizer.oov_token

test_word ="enna padam mass"
tw = tokenizer.texts_to_sequences([test_word])
tw = pad_sequences(tw,maxlen=200)
tw

prediction = int(model.predict(tw).round().item())
sentiment_label[1][prediction]