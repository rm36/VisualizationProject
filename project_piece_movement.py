import chess  # python-chess.readthedocs.io
import chess.pgn
from collections import defaultdict
from visualize_board import plot_color_sum_per_square, PlotType, ScaleType

DEBUG = False
PLOT_FIRST_GAME_ONLY = True  # Or plot all together.

class Piece:
    def __init__(self, square):
        self.orig_square = square
        self.curr_square = square
        self.squares_moved = 0
        self.traj = []
        self.ded = False

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
            pieces_stats.append(Piece(square))

        color_sum_per_square = defaultdict(int)
        for move in game.mainline_moves():
            is_capture = False
            if board.is_capture(move):
                is_capture = True
            # print(board.san(move))
            board.push(move)

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
                    # Distance in king steps.
                    moved_this_turn = chess.square_distance(move.from_square, move.to_square)
                    piece.squares_moved += moved_this_turn
                    #print(chess.square_name(move.from_square),' moved ', moved_this_turn)
                    piece.traj.append(chess.square_name(move.to_square))
                    break
            #print(board)
            #input()

        for square in range(64):
            if square >= 16 and square < (64-16):
                color_sum_per_square[square] = -1
                total_color_sum_per_square[square] = -1
            else:
                for piece in pieces_stats:
                    if square == piece.orig_square:
                        color_sum_per_square[square] = piece.squares_moved
                        total_color_sum_per_square[square] += piece.squares_moved
                        break


        if PLOT_FIRST_GAME_ONLY:
            plot_color_sum_per_square(color_sum_per_square, title='Piece movement', zname='Squares moved', cmap='viridis', plot_type=PlotType.Absolute, scale_type=ScaleType.Log)
            exit()
    
    plot_color_sum_per_square(total_color_sum_per_square, title='Piece movement', zname='Squares moved', cmap='viridis', plot_type=PlotType.Absolute, scale_type=ScaleType.Log)
    