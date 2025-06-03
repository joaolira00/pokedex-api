from pydantic import BaseModel
from typing import Optional

class PokemonDTO(BaseModel):
    national_number: int
    gen: str
    pokemon_name: str
    primary_type: str
    secondary_type: Optional[str]
    classification: str
    height_m: float
    weight_kg: float
    hp: int
    attack: int
    defense: int
    sp_attack: int
    sp_defense: int
    speed: int
    abilities_0: str
    abilities_1: str
    is_sublegendary: bool
    is_legendary: bool
    is_mythical: bool
    evochain_1: str
    evochain_2: str
    evochain_3: str
    evochain_4: str
    mega_evolution: Optional[str]
    description: str
    image: Optional[str]