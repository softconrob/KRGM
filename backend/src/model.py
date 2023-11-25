from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from typing import List, Optional

class Player(BaseModel):
    sofifa_id: int
    player_url: str
    short_name: str
    player_positions: str
    overall: int
    age: int
    gender: str
    nationality_name: str
    pace: float
    shooting: float
    passing: float
    dribbling: float
    defending: float
    physic: int
    player_face_url: str
    nation_flag_url: str
    attacking: int
    skill: int
    movement: int
    power: int
    mentality: int
    goalkeeping: int
    def to_json(self):
        return jsonable_encoder(self, exclude_none=True)

class PlayerRank(BaseModel):
    sofifa_id: int
    short_name: str
    overall: int
    def to_json(self):
        return jsonable_encoder(self, exclude_none=True)

