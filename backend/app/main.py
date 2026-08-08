from fastapi import FastAPI
from routers import players
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "https://main.d3cb2hde0hbx30.amplifyapp.com",
    ],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(players.router)

from routers import leagues
app.include_router(leagues.router)

from routers import auth
app.include_router(auth.router)


@app.get("/")
def root():
    return {"status": "ok"}