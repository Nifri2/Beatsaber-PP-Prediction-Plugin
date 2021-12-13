import sklearn.ensemble
from sklearn.ensemble import RandomForestRegressor
from flask import Flask
from flask_restful import Resource, Api, reqparse
import pickle

app = Flask(__name__)
api = Api(app)

model = RandomForestRegressor()

with open('model.pkl', 'rb') as file:
    model = pickle.load(file)

class Predict(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('stars', required=True)
        parser.add_argument('acc', required=True)
        args = parser.parse_args()

        return {"pp": model.predict([[args["stars"],args["acc"]]])[0]}
    
    def get(self):
        return {"errorMessage": "Only post with stars and acc will yield pp"}

class Locations(Resource):
    def get(self):
        return {"/predict": "prediction endpoint"}

api.add_resource(Predict,'/predict')
api.add_resource(Locations,'/')

if __name__ == '__main__':
    app.run()