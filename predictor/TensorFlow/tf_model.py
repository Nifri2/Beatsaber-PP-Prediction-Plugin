from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense,Dropout
from tensorflow.keras.optimizers import RMSprop
import tensorflow as tf
import pandas as pd

def buildModel():
    model = Sequential()
    model.add(Dense(50, input_dim=2, kernel_initializer='uniform', activation='relu'))
    model.add(Dense(100, kernel_initializer='uniform', activation='relu'))
    model.add(Dense(100, kernel_initializer='uniform', activation='relu'))
    model.add(Dense(100, kernel_initializer='uniform', activation='relu'))
    model.add(Dense(1, kernel_initializer='uniform', activation='linear'))
    model.compile(loss='mse', optimizer='adam', metrics=['accuracy'])
    return model

data = pd.read_csv("collected/dataset.csv",delimiter=';')

x = []
y = []

for s,a in zip(data.stars,data.acc):
    x.append([s,a])

for pp in data.pp:
    y.append(pp)

with tf.device("/GPU:0"):
    model = buildModel()
    model.fit(x, y, epochs=200, batch_size=10,  verbose=2)
model.save_weights('checkpoints/tf_weights')