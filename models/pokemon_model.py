from database.database import Base
from sqlalchemy import Column, Integer, String, Text, Boolean, Float

class Pokemon(Base):
    __tablename__ = "pokemon"

    national_number = Column(Integer, primary_key=True, index=True)
    gen = Column(String(length=4))
    pokemon_name = Column(String(length=50))
    primary_type = Column(String(length=50))
    secondary_type = Column(String(length=50), nullable=True)
    classification = Column(String(length=50))
    height_m = Column(Float)
    weight_kg = Column(Float)
    hp = Column(Integer)
    attack = Column(Integer)
    defense = Column(Integer)
    sp_attack = Column(Integer)
    sp_defense = Column(Integer)
    speed = Column(Integer)
    abilities_0 = Column(String(length=50))
    abilities_1 = Column(String(length=50), nullable=True)
    is_sublegendary = Column(Boolean, default=False)
    is_legendary = Column(Boolean, default=False)
    is_mythical = Column(Boolean, default=False)
    evochain_1 = Column(String(length=50))
    evochain_2 = Column(String(length=50), nullable=True)
    evochain_3 = Column(String(length=50), nullable=True)
    evochain_4 = Column(String(length=50), nullable=True)
    mega_evolution = Column(String(length=50), nullable=True)
    description = Column(Text)
    image = Column(String(length=255), nullable=True)