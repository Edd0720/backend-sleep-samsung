from typing import Union

from fastapi import FastAPI

app = FastAPI()

async def get_db()->AsyncSession:
    async with session_local() as session:
        yield session


@app.get("/")
async def read_root():
    return {"Hello": "World"}

@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}