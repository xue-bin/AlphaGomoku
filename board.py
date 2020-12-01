from enum import Enum
import numpy as np

class Color(Enum):
    EMPTY = 0
    BLACK = 1
    WHITE = 2

def check_list_len_5_and_equal(lst):
    if len(lst) > 5:
        lst.pop(0)
    return len(lst) == 5 and all(x == lst[0] and x != Color.EMPTY.value for x in lst)
"""
represent the game as a numpy, handing the abstract logic of the game
"""

class Board:

    def __init__(self, size):
        self.size = size
        self.current_player = Color.BLACK
        self.board = np.zeros((self.size, self.size ), dtype=np.uint8)
        self.winner = None
        self.end = False

    def reset(self):
        self.current_player = Color.BLACK
        self.board = np.zeros((self.size , self.size ), dtype=np.uint8)
        self.winner = None
        self.end = False

    def play_stone(self, coord, color=None):
        if color is None:
            color = self.current_player
        if self.board[coord[1]][coord[0]] != color.EMPTY.value:
            return None
        self.board[coord[1]][coord[0]] = color.value
        self._check_for_win()
        self._switch_player()
        return color

    def _switch_player(self):
        if self.current_player == Color.BLACK:
            self.current_player = Color.WHITE
        else:
            self.current_player = Color.BLACK

    def _check_for_win(self):

        if np.count_nonzero(self.board) == self.size*self.size:
            self.end = True
            self.winner = None
        transpose_board = np.transpose(self.board)
        # print('======================')
        ascending_diag = [self.board[::-1,:].diagonal(i) for i in range(-self.size+1, self.size)]
        # print(len(ascending_diag))
        # print(ascending_diag)
        descending_diag =[self.board.diagonal(i) for i in range(self.size-1, -self.size,-1)]
        # print(len(descending_diag))
        # print(descending_diag)


        for row in range(2*self.size-1):
            horizontal_seq = []
            vertical_seq = []
            ascending_seq = []
            descending_seq = []


            for col in range(self.size):
                if row< self.size:
                    horizontal_seq.append(self.board[row][col])
                    vertical_seq.append(transpose_board[row][col])
                if col < len(ascending_diag[row]):
                    ascending_seq.append(ascending_diag[row][col])
                if col < len(descending_diag[row]):
                    descending_seq.append(descending_diag[row][col])


                if check_list_len_5_and_equal(horizontal_seq) or check_list_len_5_and_equal(vertical_seq) \
                        or check_list_len_5_and_equal(ascending_seq) \
                        or check_list_len_5_and_equal(descending_seq):
                    self.end = True
                    # print(self.current_player)
                    self.winner = self.current_player
