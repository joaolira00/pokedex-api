from fastapi import APIRouter, Depends, HTTPException, Path
from fastapi.responses import JSONResponse
from typing import Annotated, List
from sqlalchemy.orm import Session
from database.database import SessionLocal
from schemas.pokemon_schema import PokemonSchema
from schemas.pokemon_schema_output import PokemonDTO
from starlette import status
from models.pokemon_model import Pokemon

router = APIRouter(
    prefix="/pokemon",
    tags=["pokemon"]
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]


@router.get("/get-all-pokemons",
            status_code=status.HTTP_200_OK,
            summary="Gotta catch 'em all!")
def get_all_pokemons(db: db_dependency):
    all_pokemons = db.query(Pokemon).limit(50).all()

    if len(all_pokemons) < 1:
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND,
                             content={"message": "No pokemons found... :("})
    
    return all_pokemons


@router.get("/get-pokemon-by-id/{pokemon_id}")
def get_pokemon_by_id(db: db_dependency,
                      pokemon_id: int = Path(gt=0)):
    pokemon = db.query(Pokemon).filter(Pokemon.national_number == pokemon_id).all()

    if pokemon is None:
        raise HTTPException(status_code=404, detail="No pokemon found with this id :(")
    
    return pokemon


@router.get("/get-all-legendary-pokemons")
def get_all_legendary_pokemons(db: db_dependency):
    legendary_pokemons = db.query(Pokemon).filter(Pokemon.is_legendary == True).all()

    if legendary_pokemons is None:
        raise HTTPException(status_code=404, detail="No legendary pokemons found.")
    
    return legendary_pokemons