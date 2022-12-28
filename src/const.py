#All constant variables

WIDTH = 700
HEIGHT = 700

COLS = 8
ROWS = 8

SQSIZE = WIDTH // COLS

CHECKMATE = 1000000
DEPTH = 2

knight_position_score = [[1, 1, 1, 1, 1, 1, 1, 1],
                         [1, 2, 2, 2, 2, 2, 2, 1],
                         [1, 2, 3, 3, 3, 3, 2, 1],
                         [1, 2, 3, 4, 4, 3, 2, 1],
                         [1, 2, 3, 4, 4, 3, 2, 1],
                         [1, 2, 3, 3, 3, 3, 2, 1],
                         [1, 2, 2, 2, 2, 2, 2, 1],
                         [1, 1, 1, 1, 1, 1, 1, 1]]

piece_position_score = {"N": knight_position_score}