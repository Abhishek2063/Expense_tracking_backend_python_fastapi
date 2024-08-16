from fastapi import FastAPI
from config.database import get_db

app = FastAPI()
get_db()

@app.get("/")
def read_root():
    return {"Hello": "World"}
