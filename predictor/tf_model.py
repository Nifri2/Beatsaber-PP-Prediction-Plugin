from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense,Dropout
from tensorflow.keras.optimizers import RMSprop
import tensorflow as tf
import pandas as pd

def buildModel():
    model = Sequential()
    model.add(Dense(40, activation="tanh", input_dim=2, kernel_initializer="uniform"))
    model.add(Dense(1, activation="linear", kernel_initializer="uniform"))
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
    model.fit(x, y, epochs=50, batch_size=10,  verbose=2)
model.save_weights('tf_weights')