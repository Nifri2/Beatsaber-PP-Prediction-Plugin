from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from matplotlib import pyplot as plt
from tqdm import tqdm
import tensorflow as tf
import requests
import time
import json


pdata = []

def buildModel():
    model = Sequential()
    model.add(Dense(50, input_dim=2, kernel_initializer='uniform', activation='relu'))
    model.add(Dense(100, kernel_initializer='uniform', activation='relu'))
    model.add(Dense(100, kernel_initializer='uniform', activation='relu'))
    model.add(Dense(100, kernel_initializer='uniform', activation='relu'))
    model.add(Dense(1, kernel_initializer='uniform', activation='linear'))
    model.compile(loss='mse', optimizer='adam', metrics=['accuracy'])
    return model

with tf.device("/gpu:0"):
    model = tf.keras.models.load_model('checkpoints/model.h5')

now = time.time()
for j in range(1,15):
	g = []
	for i in tqdm(range(0,100)):
		g.append(model.predict([[j,i/100]])[0][0])
	pdata.append(g)
done = time.time() 

print(f"[>] 100 requests took {done - now}s")
print(f"[>] Thats {(done - now) / 100}s per iteration ")
print(f"[>] That means a song can easily have {60 / ((done - now))} bloqs per second")

for i in pdata:
	plt.plot(i)
plt.show()