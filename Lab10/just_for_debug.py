import numpy as np
import random

class game:
    def __init__(self):
        self.state = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
        self.possible_moves = 9


SOL_REF = [[4, 9, 2], [3, 5, 7], [8, 1, 6]]
CMP_VALUE = 15
N_ROUNDS = 10
BASIC_VAL = 0
CIRCLE = -1
CROSS = 1

def init_game():
    game = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
    return game

def check_finished(state):
    #Checking if cicle won thrpugh summing values and comparing it to the default value to check
    circle_based_state = -np.multiply(state, SOL_REF)
    win_circle_row = np.sum(circle_based_state, axis=0)
    win_circle_col = np.sum(circle_based_state, axis=1)
    win_circle_diag = circle_based_state[0, 0] + circle_based_state[1, 1] + circle_based_state[2, 2]
    win_circle_anti_diag = cross_based_state[0, 2] + cross_based_state[1, 1] + cross_based_state[2, 0]
    if CMP_VALUE in win_circle_row:
        return CIRCLE
    if CMP_VALUE in win_circle_col:
        return CIRCLE
    if CMP_VALUE == win_circle_diag:
        return CIRCLE
    if CMP_VALUE == win_circle_anti_diag:
        return CIRCLE
    
    #Same thing with cross
    cross_based_state = np.multiply(state, SOL_REF)
    win_cross_row = np.sum(cross_based_state, axis=0)
    win_cross_col = np.sum(cross_based_state, axis=1)
    win_cross_diag = cross_based_state[0, 0] + cross_based_state[1, 1] + cross_based_state[2, 2]
    win_cross_anti_diag = cross_based_state[0, 2] + cross_based_state[1, 1] + cross_based_state[2, 0]
    if CMP_VALUE in win_cross_row:
        return CROSS
    if CMP_VALUE in win_cross_col:
        return CROSS
    if CMP_VALUE == win_cross_diag:
        return CROSS
    if CMP_VALUE == win_cross_anti_diag:
        return CIRCLE
    
    return BASIC_VAL

def random_s(state, current_player):
    row = random.randint(0, 2)
    col = random.randint(0, 2)
    while state[row][col] != BASIC_VAL:
        row = random.randint(0, 2)
        col = random.randint(0, 2)

    if current_player == 0:
        state[row][col] = CIRCLE
    else:
        state[row][col] = CROSS

    return state

def opt_s(state):
    print("3frerc")

PLAYERS = [random_s, random_s]

if __name__ == "__main__":
    p_wins = [0, 0]
    for i in range(N_ROUNDS):
        current_player = 0
        match = game()
        ending = check_finished(match)
        
        while ending == BASIC_VAL and match.possible_moves != 0:
            match = PLAYERS[current_player](match.state, current_player)
            match.possible_moves -= 1
            current_player = abs(current_player - 1)
            ending = check_finished(match.state)

        if match.possible_moves == -1:
            print("PAREGGIO!")
        if ending == CROSS:
            p_wins[1] += 1
        else:
            p_wins[0] += 1

    print(p_wins)