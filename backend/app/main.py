from fastapi import FastAPI
from routers import players

app = FastAPI()

app.include_router(players.router)


@app.get("/")
def root():
    return {"status": "ok"}