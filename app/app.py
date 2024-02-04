from models import db
from flask_cors import CORS
from flask import Flask, jsonify, request, session, make_response
from flask_restful import Api, Resource
from flask_migrate import Migrate

from datetime import timedelta
from flask_session import Session

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mydb.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JSONIFY_PRETTYPRINT_REGULAR']= True

db.init_app(app)
api = Api(app)
migrate = Migrate(app, db)
Session(app)

class Index(Resource):
    def get(self):
        response_body = '<h1>Hello World</h1>'
        status = 200
        headers = {}
        return make_response(response_body,status,headers)
    
api.add_resource(Index,'/', endpoint='landing')

if __name__ == '__main__':
    app.run(port=5555, debug=True)