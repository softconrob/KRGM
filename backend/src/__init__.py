from flask import Flask
from flask_cors import CORS
from flask_restx import Resource, Api
from flask_pymongo import PyMongo
from pymongo.collection import Collection
from .model import Player

app = Flask(__name__)
# allow access from any frontend
cors = CORS()
cors.init_app(app, resources={r"*": {"origins": "*"}})
# add your mongodb URI
app.config["MONGO_URI"] = "mongodb://localhost:27017/fifadatabase"

mongo = PyMongo(app)

players: Collection = mongo.db.players

api = Api(app)
class Players(Resource):
    def get(self):
        cursor = players.find({})
        return [Player(**document).to_json() for document in cursor]
api.add_resource(Players, "/players")


