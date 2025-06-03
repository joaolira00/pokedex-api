from fastapi import FastAPI
import models.pokemon_model as pokemon_model
from database.database import engine
from scalar_fastapi import get_scalar_api_reference
from routers import pokemon

app = FastAPI()

pokemon_model.Base.metadata.create_all(bind=engine)

app.include_router(pokemon.router)

@app.get("/scalar", include_in_schema=False)
async def scalar_html():
    return get_scalar_api_reference(
        openapi_url=app.openapi_url,
        title=app.title
    )