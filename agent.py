import numpy as np
from board import Color

class AlphaGomoku:

    def __init__(self, board):
        self.board = board

    def get_move(self):
        # return self.get_random_move()
        # return self.get_search_move()
        return self.get_pattern_move()

    def get_empty_moves(self):
        return np.transpose(np.where(self.board.board==Color.EMPTY.value))

    def get_neighbour_moves(self):
        size = self.board.size
        empty_moves = self.get_empty_moves()
        moves = np.empty([0, 2], dtype=int)
        for move in empty_moves:
            neighbour = []
            # for i in range(-1, 2):
                # for j in range(-1, 2):
                    # try:
                        # neighbour.append(self.board.board[move[0] + i][move[1] + j])
                    # except:
                        # pass
            if move[0] == 0 and move[1] == 0:
                for i in range(0, 2):
                    for j in range(0, 2):
                        neighbour.append(self.board.board[move[0] + i][move[1] + j])
            elif move[0] == 0 and move[1] == size - 1:
                for i in range(0, 2):
                    for j in range(-1, 1):
                        neighbour.append(self.board.board[move[0] + i][move[1] + j])
            elif move[0] == size - 1 and move[1] == 0:
                for i in range(-1, 1):
                    for j in range(0, 2):
                        neighbour.append(self.board.board[move[0] + i][move[1] + j])
            elif move[0] == size - 1 and move[1] == size - 1:
                for i in range(-1, 1):
                    for j in range(-1, 1):
                        neighbour.append(self.board.board[move[0] + i][move[1] + j])
            elif move[0] == 0:
                for i in range(0, 2):
                    for j in range(-1, 2):
                        neighbour.append(self.board.board[move[0] + i][move[1] + j])
            elif move[0] == size - 1:
                for i in range(-1, 1):
                    for j in range(-1, 2):
                        neighbour.append(self.board.board[move[0] + i][move[1] + j])
            elif move[1] == 0:
                for i in range(-1, 2):
                    for j in range(0, 2):
                        neighbour.append(self.board.board[move[0] + i][move[1] + j])
            elif move[1] == size - 1:
                for i in range(-1, 2):
                    for j in range(-1, 1):
                        neighbour.append(self.board.board[move[0] + i][move[1] + j])
            else:
                for i in range(-1, 2):
                    for j in range(-1, 2):
                        neighbour.append(self.board.board[move[0] + i][move[1] + j])
            if (1 in neighbour) or (2 in neighbour):
                moves = np.append(moves, [move], axis=0)
        if np.size(moves, 0) == 0:
            return empty_moves
        return moves

    def get_random_move(self):
        moves = self.get_neighbour_moves()
        np.random.shuffle(moves)
        for move in moves:
            return (move[1], move[0])
        return None

    def get_pattern_move(self):
        moves = self.get_neighbour_moves()
        move_score = []
        pattern_move = []
        for move in moves:
            score = self.calculate_score(move)
            move_score.append([move, score])
        move_score.sort(key=lambda x: x[1], reverse=True)
        max_score = move_score[0][1]
        for move in move_score:
            if move[1] == max_score:
                pattern_move.append(move)
        np.random.shuffle(pattern_move)
        for move, _ in pattern_move:
            return (move[1], move[0])
        return None

    def calculate_score(self, move):
        board = self.board.board
        size = self.board.size

        row = board[move[0]]
        column = board[:, move[1]]

        diagnol_left = np.empty([0], dtype=int)
        if move[0] >= move[1]:
            for i in range(size - move[0] + move[1]):
                value = board[i + move[0] - move[1]][i]
                diagnol_left = np.append(diagnol_left, value)
                left_index = move[1]
        else:
            for i in range(size + move[0] - move[1]):
                value = board[i][i - move[0] + move[1]]
                diagnol_left = np.append(diagnol_left, value)
                left_index = move[0]

        diagnol_right = np.empty([0], dtype=int)
        if move[0] + move[1] >= size:
            for i in range(2 * size - move[0] - move[1] - 1):
                value = board[size - i - 1][move[0] + move[1] - size + i + 1]
                diagnol_right = np.append(diagnol_right, value)
                right_index = size - move[0] - 1
        else:
            for i in range(move[0] + move[1] + 1):
                value = board[move[0] + move[1] - i][i]
                diagnol_right = np.append(diagnol_right, value)
                right_index = move[1]

        attack_weight = 1
        defense_weight = 2
        color = self.board.current_player.value
        opponent = 3 - color
        score_sum = 0
        score_sum += attack_weight * self.sequence_score(row, move[1], color)
        score_sum += attack_weight * self.sequence_score(column, move[0], color)
        score_sum += attack_weight * self.sequence_score(diagnol_left, left_index, color)
        score_sum += attack_weight * self.sequence_score(diagnol_right, right_index, color)
        if score_sum >= 3 ** 5:
            return 4000
        score_sum += defense_weight * self.sequence_score(row, move[1], opponent)
        score_sum += defense_weight * self.sequence_score(column, move[0], opponent)
        score_sum += defense_weight * self.sequence_score(diagnol_left, left_index, opponent)
        score_sum += defense_weight * self.sequence_score(diagnol_right, right_index, opponent)
        return score_sum

    def sequence_score(self, ori_array, index, color):
        array = ori_array.copy()
        array[index] = color
        opponent = 3 - color
        start_index = 0
        end_index = np.size(array)
        opp_index = np.where(array == opponent)[0]
        for i in opp_index:
            if i < index and i > start_index:
                start_index = i
            elif i > index and i < end_index:
                end_index = i
        if start_index != 0:
            start_index += 1
        final_array = array[start_index:end_index]

        if np.size(final_array) < 5:
            return 0
        score = np.size(np.where(final_array == color)[0])

        data_list = [str(x) for x in list(final_array)]
        data_str = "".join(data_list)
        data_continue = str(color) * score
        if data_continue not in data_str:
            score -= 1

        if score < 4:
            if final_array[0] == color or final_array[-1] == color:
                score -= 1

        if score > 5:
            score = 5

        return (3 ** score)

    '''
    def get_search_move(self):
        isWin, move = self.negamax()
        if isWin == self.board.current_player:
            return move
        else:
            return get_random_move()

    def negamax(self):
        self.board._check_for_win()
        if self.board.winner != None:
            return False, None

        moves = self.get_neighbour_moves()
        if len(moves) == 0:
            return False, None

        for move in moves:
            self.board.play_stone(move, self.board.current_player)
            isWin, _ = self.negamax()
            if isWin == True:
                isWin == False
            elif isWin == False:
                isWin == True
            self.board.board[move[1]][move[0]] = Color.EMPTY
            self.board._switch_player
            if isWin == True:
                return True, move
        return False, move
    '''