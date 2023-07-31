from fastapi import FastAPI
from pydantic import BaseModel

from app.analyse_game import run_game_analysis
from app.analyse_position import run_analyse_position

app = FastAPI()


class ItemPgn(BaseModel):
    pgn: str


class ItemFen(BaseModel):
    fen: str


@app.get("/health-check")
def analyse_game():
    return {"message": "ok"}


@app.post("/analyse-game")
def analyse_game(item: ItemPgn):
    print(item)

    return run_game_analysis(item.pgn)


@app.post("/analyse-position")
def analyse_position(item: ItemFen):
    print(item)

    return run_analyse_position(item.fen)
