import sys
import random
import signal
import time
import copy

class MyPlayer():
    def __init__(self):
        pass

    def move(self, board, old_move, flag):
        cells = board.find_valid_move_cells(old_move)
        return cells[random.randrange(len(cells))]
