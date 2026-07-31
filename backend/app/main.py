from fastapi import FastAPI
from routers import players
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(players.router)


@app.get("/")
def root():
    return {"status": "ok"}