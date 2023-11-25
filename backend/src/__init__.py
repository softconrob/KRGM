from flask import Flask
from flask_cors import CORS
from flask_restx import Resource, Api
from flask_pymongo import PyMongo
from pymongo.collection import Collection
from .model import Player, PlayerRank

app = Flask(__name__)
# allow access from any frontend
cors = CORS()
cors.init_app(app, resources={r"*": {"origins": "*"}})
# add your mongodb URI
app.config["MONGO_URI"] = "mongodb://localhost:27017/fifadatabase"

mongo = PyMongo(app)

players: Collection = mongo.db.players

api = Api(app)

dict_position = {0: 'GK', 1: 'ST', 2: 'LW', 3: 'RW', 
                4: 'CM', 5: 'LM', 6: 'RM', 7: 'CB', 
                8: 'LB', 9: 'RB'}

class PlayerDetail(Resource):
    def get(self, sofifa_id):
        doc = players.find_one({"sofifa_id": sofifa_id})
        return Player(**doc).to_json()

class PlayerRankList(Resource):
    def get(self, gender, position):
        # return top 10 players in the same gender
        gender = "female" if gender == 0 else "male"
        cursor = players.find({"gender": gender, "player_positions": {"$regex": dict_position[position]}}).sort("overall", -1).limit(10)
        return [PlayerRank(**doc).to_json() for doc in cursor]

api.add_resource(PlayerDetail, "/players/<int:sofifa_id>")
api.add_resource(PlayerRankList, "/ranks/<int:gender>/<int:position>")
