from fastapi import FastAPI
from seedings.seed import seed_data

seed_data()
app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}
