import io

import chess.pgn
from stockfish import Stockfish


def run_game_analysis(pgn):
    stockfish = Stockfish('/src/Stockfish/src/stockfish', parameters={"Threads": 8})

    game = chess.pgn.read_game(io.StringIO(pgn))
    print(get_headers(game))

    stockfish.set_depth(16)
    board = game.board()

    moves = []

    move_data = {
        "white_moves": [],
        "black_moves": [],
        "white_move_counts": get_move_counts_dict(),
        "black_move_counts": get_move_counts_dict()
    }

    last_cp = 0

    for i, move in enumerate(game.mainline_moves()):
        is_white_move = board.turn

        san = board.san(move)
        board.push(move)
        fen = board.fen()
        stockfish.set_fen_position(fen_position=fen)
        evaluation = stockfish.get_evaluation()
        cp = evaluation["value"]

        update_move_data(move_data, san, cp, last_cp, is_white_move)
        last_cp = cp

        normalised_evaluation = float(evaluation["value"]) / 1530
        normalised_evaluation = normalised_evaluation if evaluation["type"] != "mate" \
            else mate_value(normalised_evaluation, is_white_move)

        moves.append({
            "san": san,
            "fen": fen,
            "evaluation": cp,
            "is_mate": evaluation["type"] == "mate",
            "normalised_evaluation": normalised_evaluation
        })

    return {
        "moves": moves,
        "move_data": move_data
    }


def update_move_data(move_data, san, cp, last_cp, is_white_move):
    current_player_moves = move_data['white_moves'] if is_white_move else move_data['black_moves']
    current_player_move_counts = move_data['white_move_counts'] if is_white_move else move_data['black_move_counts']
    if abs(last_cp - cp) > 300:
        current_player_move_counts["blunders"] += 1
        current_player_moves.append({"san": san + '??', "type": "blunder"})
    elif abs(last_cp - cp) > 100:
        current_player_move_counts["mistakes"] += 1
        current_player_moves.append({"san": san + '?', "type": "mistake"})
    elif abs(last_cp - cp) > 50:
        current_player_move_counts["inaccuracies"] += 1
        current_player_moves.append({"san": san + '?!', "type": "inaccuracy"})
    elif abs(last_cp - cp) < 10:
        current_player_move_counts["excellent_moves"] += 1
        current_player_moves.append({"san": san, "type": "excellent"})
    elif abs(last_cp - cp) < 25:
        current_player_move_counts["great_moves"] += 1
        current_player_moves.append({"san": san, "type": "great"})
    else:
        current_player_move_counts["good_moves"] += 1
        current_player_moves.append({"san": san, "type": "good"})


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
        "excellent_moves": 0,
        "great_moves": 0,
        "good_moves": 0,
    }
