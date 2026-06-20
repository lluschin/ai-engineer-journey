from contextlib import asynccontextmanager
from fastapi import FastAPI
from pydantic import BaseModel, TypeAdapter, PositiveFloat, field_validator, ValidationError
from pathlib import Path

class Fruit(BaseModel):
    id: int 
    name: str
    description: str
    price: PositiveFloat

    @field_validator('id', mode='after')
    @classmethod
    def isUniqueInt(cls, value: int) -> int:
        ids = [fruit.id for fruit in app.state.fruits]
        if value in ids:
            raise ValueError('id has already been assigned')
        else:
            return value


@asynccontextmanager
async def lifespan(app: FastAPI):
    print('loading data model.')

    adapter = TypeAdapter(list[Fruit])
    data_filepath = Path(__file__).with_name("fruits.json")
    app.state.fruits = []

    if data_filepath.exists():
        with open(data_filepath, 'r') as fp:
            app.state.fruits = adapter.validate_json(fp.read())

    yield

    print('writing data model to disk.')

    with open(data_filepath, 'w') as fp:
        fp.write(adapter.dump_json(app.state.fruits).decode())


app = FastAPI(lifespan=lifespan)

@app.get("/")
async def root():
    return {"Hello" : "World"}


@app.post("/fruits")
async def createFruit(fruit: Fruit):
    app.state.fruits.append(fruit)
    print("added fruit", fruit)


@app.get("/fruits", response_model=list[Fruit])
async def listFruits() -> list[Fruit]:
    return app.state.fruits


data_filepath = Path('fruits.json')
with open(data_filepath, 'r') as fp:
    print(fp.read())