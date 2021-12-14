from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
import tensorflow as tf
from tqdm import tqdm
import pickle
import csv


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
    model = buildModel()
    model.load_weights('checkpoints/tf_weights')

dataset = []

for stars in tqdm(range(1,1401)):
	for acc in range(1,100):
		dataset.append([
            acc/100,
            stars/100,
            model.predict([[acc/100,stars/100]])
        ])

with open('collected/new_dataset.csv', 'wb') as file:
    pickle.dump(dataset,file)

with open('collected/new_dataset.csv', 'w',newline='') as csvfile:
    writer = csv.writer(csvfile, delimiter=';')
    writer.writerow(["stars","acc","pp"])
    for data in dataset:
        writer.writerow(data)