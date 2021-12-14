import chess  # python-chess.readthedocs.io
import chess.pgn
from collections import defaultdict
from visualize_board import plot_color_sum_per_square

DEBUG = False
PLOT_FIRST_GAME_ONLY = True  # Or plot all together.

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

        color_sum_per_square = defaultdict(int)
        for move in game.mainline_moves():
            board.push(move)

            piece_map = board.piece_map()
            for square, piece in piece_map.items():
                color_sum_per_square[square] += (1 if piece.color == chess.WHITE else -1)
                total_color_sum_per_square[square] += (1 if piece.color == chess.WHITE else -1)

        if PLOT_FIRST_GAME_ONLY:
            plot_color_sum_per_square(color_sum_per_square, title='Relative difference in player control')
            exit()
    
    plot_color_sum_per_square(total_color_sum_per_square, title='Relative difference in player control')
    