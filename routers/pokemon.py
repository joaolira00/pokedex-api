from fastapi import APIRouter, Depends, HTTPException, Path, Body
from fastapi.responses import JSONResponse, HTMLResponse
from typing import Annotated, List
from sqlalchemy.orm import Session
from database.database import SessionLocal
from schemas.pokemon_schema import PokemonSchema
from schemas.pokemon_schema_output import PokemonDTO
from starlette import status
from models.pokemon_model import Pokemon
from httpx import AsyncClient
from schemas.pokemon_update import PokemonStatsUpdate

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
async def get_pokemon_by_id(db: db_dependency,
                      pokemon_id: int = Path(gt=0)):
    pokemon = db.query(Pokemon).filter(Pokemon.national_number == pokemon_id).first()

    if pokemon is None:
        raise HTTPException(status_code=404, detail="No pokemon found with this id :(")
    
    image_url = f"https://www.pokemon.com/static-assets/content-assets/cms2/img/pokedex/full/{pokemon_id:03d}.png"

    async with AsyncClient() as client:
        response = await client.get(image_url)
        if response.status_code != 200:
            raise HTTPException(status_code=404, detail="Pokemon image not found.")
    
    pokemon.image = image_url

    return pokemon


@router.get("/get-all-legendary-pokemons")
def get_all_legendary_pokemons(db: db_dependency):
    legendary_pokemons = db.query(Pokemon).filter(Pokemon.is_legendary == True).all()

    if legendary_pokemons is None:
        raise HTTPException(status_code=404, detail="No legendary pokemons found.")
    
    return legendary_pokemons


@router.post("/add-new-pokemon",
             status_code=status.HTTP_201_CREATED)
async def add_new_pokemon(db: db_dependency,
                          pokemon_request: PokemonSchema):
    pokemon_model = Pokemon(**pokemon_request.model_dump())

    existing_pokemon = db.query(Pokemon).filter(Pokemon.national_number == pokemon_model.national_number).first()

    if existing_pokemon:
        raise HTTPException(status_code=400,
                            detail="Pokemon with this id already exists!")

    db.add(pokemon_model)
    db.commit()

    return JSONResponse(status_code=status.HTTP_201_CREATED, content="Pokemon added succesfully!")



@router.patch("/update-pokemon-stats/{pokemon_id}",
              status_code=status.HTTP_200_OK)
async def update_pokemon_stats(db: db_dependency,
                               stats: PokemonStatsUpdate,
                               pokemon_id: int = Path(gt=0)):
    
    pokemon = db.query(Pokemon).filter(Pokemon.national_number == pokemon_id).first()

    if not pokemon:
        raise HTTPException(status_code=404, detail="No pokemons found with this Id :(")

    for field, value in stats.model_dump(exclude_unset=True).items():
        setattr(pokemon, field, value)

    db.commit()
    db.refresh(pokemon)

    return JSONResponse({"message": "Pokemon stats updated successfully", "pokemon_id": pokemon.national_number})


@router.delete("/delete-pokemon/{pokemon_id}",
               status_code=status.HTTP_200_OK)
async def delete_pokemon(db: db_dependency,
                         pokemon_id: int = Path(gt=0)):
    pokemon_to_delete = db.query(Pokemon).filter(Pokemon.national_number == pokemon_id).first()

    if not pokemon_to_delete:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="No pokemon found with this id.")
    
    db.delete(pokemon_to_delete)
    db.commit()

    return JSONResponse(status_code=status.HTTP_200_OK,
                        content="Pokemon deleted succesfully.")