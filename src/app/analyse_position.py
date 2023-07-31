import chess
from app.stockfish_wrapper import StockfishWrapper


def generate_line(fen, line):
    board = chess.Board()
    board.set_fen(fen)
    moves = []
    for coord_move in line:
        move = chess.Move.from_uci(coord_move)
        san_move = board.san(move)
        board.push(move)
        moves.append(san_move)

    return moves


def run_analyse_position(fen):
    stockfish = StockfishWrapper()
    stockfish.set_fen_position(fen_position=fen)
    stockfish.set_depth(16)
    top_lines = []
    for move in stockfish.get_top_moves(5):
        top_lines.append({
           "move": move["Move"],
           "centipawn": move["Centipawn"],
           "mate": move["Mate"],
           "line": generate_line(fen, move["Line"])
        })

    return top_lines
