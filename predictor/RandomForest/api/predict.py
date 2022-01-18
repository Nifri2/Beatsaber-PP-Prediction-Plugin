from sklearn.ensemble import RandomForestRegressor
from bottle import run,route,request

import sklearn.ensemble
import requests
import pickle
import pprint
import zlib


model_version = 'v1.2.0'
url = f'https://github.com/Nifri2/Beatsaber-PP-Prediction-Plugin/releases/download/{model_version}-model/model.pkl'

model = RandomForestRegressor()


def download_file(url):
    fn = url.split('/')[-1]
    with requests.get(url, stream=True) as r:
        r.raise_for_status()
        with open(fn, 'wb') as f:
            for chunk in r.iter_content(chunk_size=8192): 
                f.write(chunk)
    return fn

try:
    with open('model.pkl', 'rb') as file:
        d = zlib.decompress(file.read())
        model = pickle.loads(d)
except Exception as e:
    print('Model not found ',e)
    done = download_file(url)
    if done:
        print('Downloaded: ',done)

@route('/predict', method='GET')
def predict():
    try:
        stars = float(request.GET.getall('stars')[0])
        acc   = float(request.GET.getall('acc')[0])
        pp = str(round(model.predict([[stars,acc]])[0],2)) + 'pp'
        return{'pp':pp}
    except Exception as e:
        return{"Error":"500 Internal Server Error: Cringe detected oωo","message":str(e)}


run(reloader=True, debug=True)