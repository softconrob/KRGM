from flask import Flask, jsonify
from flask_cors import CORS
from flask_restx import Resource, Api
from flask_pymongo import PyMongo
from pymongo.collection import Collection
from .model import Player, PlayerRank
from sklearn.neighbors import NearestNeighbors
import traceback
import pandas as pd
from bson import json_util
import json

app = Flask(__name__)
# allow access from any frontend
cors = CORS()
cors.init_app(app, resources={r"*": {"origins": "*"}})
# add your mongodb URI
app.config["MONGO_URI"] = "mongodb://localhost:27017/fifadatabase"

mongo = PyMongo(app)

players: Collection = mongo.db.players

api = Api(app)

number_of_neighbors = 6
outfield_player_attributes = ['overall', 'pace', 'shooting', 'passing', 'dribbling', 'defending', 'physic', 'attacking', 'skill', 'movement', 'power', 'mentality']
nn = NearestNeighbors(n_neighbors=number_of_neighbors, algorithm='ball_tree')

dict_position = {0: 'GK', 1: 'ST', 2: 'LW', 3: 'RW', 
                4: 'CM', 5: 'LM', 6: 'RM', 7: 'CB', 
                8: 'LB', 9: 'RB'}
try:
    df_fifa = pd.DataFrame(list(players.find()))
    nn.fit(df_fifa[outfield_player_attributes])
except Exception as e:
    app.logger.error(f"Error in Nearest Neighbors setup: {traceback.format_exc()}")
    raise e

def find_similar_players(player_name, df, model, player_attributes):
    if player_name not in df['short_name'].values:
        return {"error": f"Player {player_name} not found."}

    player = df[df['short_name'] == player_name][player_attributes]
    distances, indices = model.kneighbors(player)
    indices = indices[0]
    if df.iloc[indices[0]]['short_name'] == player_name:
        indices = indices[1:]

    similar_players = []
    # return the top 5 similar players with their sofifa_id, short_name
    for i in indices:
        similar_players.append({"sofifa_id": int(df.iloc[i]['sofifa_id']), "short_name": df.iloc[i]['short_name'], "player_face_url": df.iloc[i]['player_face_url']})
    return similar_players

class SimilarPlayers(Resource):
    def get(self, player_name):
        similar_players = find_similar_players(player_name, df_fifa, nn, outfield_player_attributes)
        return jsonify(similar_players)
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
api.add_resource(SimilarPlayers, '/players/similar/<string:player_name>')
