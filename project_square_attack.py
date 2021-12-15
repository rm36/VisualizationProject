import chess  # python-chess.readthedocs.io
import chess.pgn
from collections import defaultdict
from visualize_board import plot_color_sum_per_square
from argparse import ArgumentParser

parser = ArgumentParser()
parser.add_argument('-g', '--games', help="Either 'first' to analyze only the first game or 'all' for an aggregate", default='first')
parser.add_argument('-d', '--debug', help="Whether to debug", action='store_true', default=False)
args = parser.parse_args()

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

            for square in range(64):
                is_attacked_by_white = board.is_attacked_by(chess.WHITE, square)
                is_attacked_by_black = board.is_attacked_by(chess.BLACK, square)
                attack_sum = 0
                attack_sum += (1 if is_attacked_by_white else 0)
                attack_sum -= (1 if is_attacked_by_black else 0)
                color_sum_per_square[square] += attack_sum
                total_color_sum_per_square[square] += attack_sum

        if args.games == 'first':
            plot_color_sum_per_square(color_sum_per_square, title='Relative difference in player control')
            exit()
    
    plot_color_sum_per_square(total_color_sum_per_square, title='Relative difference in player control')
    