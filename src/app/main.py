import io

import chess.pgn
from fastapi import FastAPI
from pydantic import BaseModel
from stockfish import Stockfish

stockfish = Stockfish('/src/Stockfish/src/stockfish', parameters={"Threads": 4})

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

    return {"analysis": {"data": "here"}}


# +++++++GAME ANALYSIS +++++++

def run_game_analysis(pgn):
    game = chess.pgn.read_game(io.StringIO(pgn))
    print(get_headers(game))

    stockfish.set_depth(16)
    board = game.board()

    moves = []

    for i, move in enumerate(game.mainline_moves()):
        is_white_move = board.turn
        san = board.san(move)
        board.push(move)
        fen = board.fen()
        stockfish.set_fen_position(fen_position=fen)
        evaluation = stockfish.get_evaluation()
        normalised_evaluation = float(evaluation["value"]) / 1530
        normalised_evaluation if evaluation["type"] != "mate" \
            else mate_value(normalised_evaluation, is_white_move)
        moves.append({
            "san": san,
            "fen": fen,
            "evaluation": normalised_evaluation
        })

    return {
        "moves": moves,
    }


def get_headers(game):
    time_control = game.headers['TimeControl'] if 'TimeControl' in game.headers else ''
    termination = game.headers['Termination'] if 'Termination' in game.headers else ''
    return f"{game.headers['Date']} {time_control}\n" \
           f"{game.headers['White']} ({game.headers['WhiteElo']}) vs. " \
           f"{game.headers['Black']} ({game.headers['BlackElo']})\n" \
           f"{game.headers['Result']} {termination}"


def mate_value(eval_value, is_white_move):
    if eval_value == 0:
        return -1 if not is_white_move else 1
    return -1 if eval_value < 0 else 1


def get_san(fen, coord_move):
    board = chess.Board()
    board.set_fen(fen)
    move = chess.Move.from_uci(coord_move)
    return board.san(move)


def get_move_counts_dict():
    return {
        "blunders": 0,
        "mistakes": 0,
        "inaccuracies": 0,
        "best_moves": 0,
        "excellent_moves": 0,
        "great_moves": 0,
        "good_moves": 0,
    }
