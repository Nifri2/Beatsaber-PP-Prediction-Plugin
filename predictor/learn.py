import matplotlib.pyplot as plt
from sklearn.ensemble import RandomForestRegressor
import pandas as pd
import pickle

data = pd.read_csv("collected/dataset.csv",delimiter=';')

x = []
y = []

for s,a in zip(data.stars,data.acc):
    x.append([s,a])

for pp in data.pp:
    y.append(pp)

regr = RandomForestRegressor(n_estimators=10, max_features=2)
regr.fit(x, y)

with open("model.pkl", "wb") as file:
    pickle.dump(regr,file)

def plot(stars,model):
    stardata = [model.predict([[stars,i / 100]])[0] for i in range(40,100)]
    plt.ylabel("PP")
    plt.xlabel("Accuracy")
    plt.plot(stardata)
    plt.show()