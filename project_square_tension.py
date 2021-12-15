import chess  # python-chess.readthedocs.io
import chess.pgn
from collections import defaultdict
from visualize_board import plot_color_sum_per_square, PlotType, ScaleType
from argparse import ArgumentParser

parser = ArgumentParser()
parser.add_argument('-g', '--games', help="Either 'first' to analyze only the first game or 'all' for an aggregate", default='first')
parser.add_argument('-d', '--debug', help="Whether to debug", action='store_true', default=False)
args = parser.parse_args()

class Piece:
    def __init__(self, piece, square):
        self.orig_square = square
        self.color = piece.color
        self.curr_square = square
        self.tension_turns = 0
        self.name = piece.symbol()
        self.ded = False

def opposite_color(color):
    return chess.BLACK if color == chess.WHITE else chess.WHITE

total_color_sum_per_square = defaultdict(int)

# Obtained from http://smallchess.com/Games/
with open("Magnus_Carlsen.pgn") as pgn:

    number_of_games = 0
    while True:
        game = chess.pgn.read_game(pgn)
        if not game:
            break
        number_of_games += 1
        if number_of_games % 100 == 0:
            print('Number of games loaded: ', number_of_games)

        board = game.board()
        pieces_stats = []
        piece_map = board.piece_map()
        for square, piece in piece_map.items():
            pieces_stats.append(Piece(piece, square))

        color_sum_per_square = defaultdict(int)
        for move in game.mainline_moves():
            is_capture = False
            if board.is_capture(move):
                is_capture = True

            pieces_attacked = defaultdict(int)
            for piece in pieces_stats:
                is_piece_attacked = board.is_attacked_by(opposite_color(piece.color), piece.curr_square)
                can_piece_be_captured = (board.turn == opposite_color(piece.color) and is_piece_attacked)
                is_piece_captured = (move.to_square == piece.curr_square and is_capture)
                if not piece.ded and can_piece_be_captured and not is_piece_captured:
                    piece.tension_turns += 1
                    if args.debug:
                        print('piece at ', chess.square_name(piece.curr_square), ' is in tension: ', piece.name)
            board.push(move)
            if args.debug:
                print(board)
                input()

            # A piece died! Update it.
            if is_capture:
                for piece in pieces_stats:
                    if move.to_square == piece.curr_square and not piece.ded:
                        piece.ded = True
                        break

            for piece in pieces_stats:
                # Update the moved piece.
                if move.from_square == piece.curr_square and not piece.ded:
                    piece.curr_square = move.to_square
                    break

        for square in range(64):
            if square >= 16 and square < (64-16):
                color_sum_per_square[square] = -1
                total_color_sum_per_square[square] = -1
            else:
                for piece in pieces_stats:
                    if square == piece.orig_square:
                        color_sum_per_square[square] = piece.tension_turns
                        total_color_sum_per_square[square] += piece.tension_turns
                        break


        if args.games == 'first':
            plot_color_sum_per_square(color_sum_per_square, title='Piece tension', zname='Turns in tension', cmap='viridis', plot_type=PlotType.Absolute, scale_type=ScaleType.Log)
            exit()
    
    plot_color_sum_per_square(total_color_sum_per_square, title='Piece tension', zname='Turns in tension', cmap='viridis', plot_type=PlotType.Absolute, scale_type=ScaleType.Log)
    