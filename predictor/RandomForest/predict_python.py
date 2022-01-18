import sklearn.ensemble
from sklearn.ensemble import RandomForestRegressor
from flask import Flask
from flask_restful import Resource, Api, reqparse
import pickle
import pprint

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
        return {"pp": str(round(model.predict([[args["stars"],args["acc"]]])[0],2)) + 'pp'}
    
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('stars', required=True)
        parser.add_argument('acc', required=True)
        args = parser.parse_args()
        return {"pp": str(round(model.predict([[args["stars"],args["acc"]]])[0],2)) + 'pp'}

class Locations(Resource):
    def get(self):
        return {"/predict": "prediction endpoint"}

class LoggingMiddleware(object):
    def __init__(self, app):
        self._app = app

    def __call__(self, env, resp):
        errorlog = env['wsgi.errors']
        pprint.pprint(('REQUEST', env), stream=errorlog)

        def log_response(status, headers, *args):
            pprint.pprint(('RESPONSE', status, headers), stream=errorlog)
            return resp(status, headers, *args)

        return self._app(env, log_response)

api.add_resource(Predict,'/predict')
api.add_resource(Locations,'/')

if __name__ == '__main__':
    app.wsgi_app = LoggingMiddleware(app.wsgi_app)
    app.run()