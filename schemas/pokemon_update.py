from pydantic import BaseModel
from typing import Optional

class PokemonStatsUpdate(BaseModel):
    hp: Optional[int]
    attack: Optional[int]
    defense: Optional[int]
    sp_attack: Optional[int]
    sp_defense: Optional[int]
    speed: Optional[int]