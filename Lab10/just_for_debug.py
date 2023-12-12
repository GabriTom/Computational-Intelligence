import numpy as np
import random

SOL_REF = [[4, 9, 2], [3, 5, 7], [8, 1, 6]]
CMP_VALUE = 15
N_ROUNDS = 10
BASIC_VAL = 0
CIRCLE = -1
CROSS = 1

def init_game():
    basic_t = [BASIC_VAL, BASIC_VAL, BASIC_VAL]
    game = [basic_t, basic_t, basic_t]
    return game

def check_finished(state):
    #Checking if cicle won thrpugh summing values and comparing it to the default value to check
    circle_based_state = -(state * SOL_REF)
    win_circle_row = np.sum(circle_based_state, axis=0)
    win_circle_col = np.sum(circle_based_state, axis=1)
    win_circle_diag = circle_based_state[0, 0] + circle_based_state[1, 1] + circle_based_state[2, 2]
    if CMP_VALUE in win_circle_row:
        return CIRCLE
    if CMP_VALUE in win_circle_col:
        return CIRCLE
    if CMP_VALUE == win_circle_diag:
        return CIRCLE
    
    #Same thing with cross
    cross_based_state = (state * SOL_REF)
    win_cross_row = np.sum(cross_based_state, axis=0)
    win_cross_col = np.sum(cross_based_state, axis=1)
    win_cross_diag = cross_based_state[0, 0] + cross_based_state[1, 1] + cross_based_state[2, 2]
    if CMP_VALUE in win_cross_row:
        return CROSS
    if CMP_VALUE in win_cross_col:
        return CROSS
    if CMP_VALUE == win_cross_diag:
        return CROSS
    
    return BASIC_VAL

def new_move(game, current_player):
    print("vdishber")

def random_s(state):
    row = random.random(3)
    col = random.random(3)
    if state[row, col] == BASIC_VAL:
        #Metti il simbolo del giocatore corrispondente...come lo sai????

def opt_s(state):
    print("3frerc")

PLAYERS = [random_s, opt_s]

if __name__ == "__main__":
    
    for _ in range(N_ROUNDS):
        current_player = 0
        game = init_game()
        ending = check_finished(game)
        while  ending == BASIC_VAL:
            game = new_move(game, players[current_player])
            current_player = abs(current_player - 1)
        if ending == CROSS:
            print("Cross player won!")
        else:
            print("Circle player won!")