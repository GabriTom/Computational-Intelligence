import numpy as np
import random

#Tic-tac-toe game solved in a Markovian way

EMPTY_STATE = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]

#Class game, it has the actual state and the remaining moves
class game:
    def __init__(self):
        self.state = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
        self.possible_moves = 9

#Se la strategia è ottima vedi di fare una specie di distance e scegliere la soluzione migliore
class player:
    def __init__(self, sign, strategy):
        self.sign = sign
        self.strategy = strategy
        self.alpha = 1.0
        if strategy == opt_s:
            self.optimals = np.zeros((3, 3))
            self.optimals[1, 1] = 2
            #self.optimals = np.ones((3, 3))

    def reset(self, winnings):
        self.optimals = np.ones((3, 3))
        self.optimals[1, 1] = 3
        # if winnings[1] < winnings[0]:
        #     self.alpha *= 1.1
        # else:
        #     self.alpha *= 0.9

#Defining constraints
SOL_REF = [[4, 9, 2], [3, 5, 7], [8, 1, 6]]
CMP_VALUE = 15
N_ROUNDS = 5
N_MATCHES = 1
BASIC_VAL = 0
CIRCLE = -1
CROSS = 1

#Function that receives a state a computes if it is won or not
def check_finished(state):
    #Checking if cicle won thrpugh summing values and comparing it to the default value to check
    circle_based_state = -np.multiply(state, SOL_REF)
    win_circle_row = np.sum(circle_based_state, axis=0)
    win_circle_col = np.sum(circle_based_state, axis=1)
    win_circle_diag = circle_based_state[0, 0] + circle_based_state[1, 1] + circle_based_state[2, 2]
    win_circle_anti_diag = circle_based_state[0, 2] + circle_based_state[1, 1] + circle_based_state[2, 0]
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
        return CROSS
    
    return BASIC_VAL

#Function that receive a state and a player and plays a random move. Player is only for the symbol choice.
def random_s(state, current_player):
    row = random.randint(0, 2)
    col = random.randint(0, 2)
    while state[row][col] != BASIC_VAL:
        row = random.randint(0, 2)
        col = random.randint(0, 2)

    state[row][col] = current_player.sign
    return state

#Distance is computed and saved in players optimals
def compute_distance(state, player, available_positions):
    actual_optimals = player.optimals * available_positions
    # print("Actual optimals FIRST")
    # print(actual_optimals)

    sum_row = np.sum(state, axis=1).reshape(len(state[0]), 1)
    for e in sum_row:
        if e[0] == -2:
            e[0] *= 2
        elif e == 2:
            e[0] = e[0] * 2 + 1
    actual_optimals += abs(sum_row)
    
        
    sum_col = np.sum(state, axis=0).reshape(1, len(state[1]))
    for e in sum_col[0]:
        if e == -2:
            e *= 2
        elif e == 2:
            e = e * 2 + 1
    actual_optimals += abs(sum_col)

    sum_diag = state[0][0] + state[1][1] + state[2][2]
    if sum_diag == -2:
        sum_diag *= 2
    elif sum_diag == 2:
        sum_diag = sum_diag * 2 + 1

    sum_anti_diag = state[0][2] + state[1][1] + state[2][0]
    if sum_anti_diag == -2:
        sum_anti_diag *= 2
    elif sum_anti_diag == 2:
        sum_anti_diag = sum_anti_diag * 2 + 1
    
    for i in range(player.optimals.shape[0]):
        #actual_optimals[i, i] = round(actual_optimals[i, i] + abs(sum_diag) * player.alpha)
        actual_optimals[i, i] += abs(sum_diag)

    for i in range(player.optimals.shape[0]):
        #actual_optimals[player.optimals.shape[0]-1-i, i] = round(actual_optimals[player.optimals.shape[0]-1-i, i] + abs(sum_anti_diag) * player.alpha)
        actual_optimals[player.optimals.shape[0]-1-i, i] += abs(sum_anti_diag)

    #Scegli cella con abs maggiore
    player.optimals = np.multiply(actual_optimals, available_positions)
    # print("Actual optimals LATER")
    # print(player.optimals)
    print()

    

#Function that receives a state and a player and do the best move based on optimals values
def opt_s(state, current_player):
    available_positions = np.zeros((len(state), len(state[0])))
    #Analize state (find empty position) and updating optimals
    for i in range(len(state)):
        for j in range(len(state[i])):
            if state[i][j] == 0:
                available_positions[i][j] = 1

    # print("Available position")
    # print(available_positions)
    compute_distance(state, current_player, available_positions)

    #Selecting cell
    sr, sc = np.unravel_index(np.argmax(abs(current_player.optimals), axis=None), current_player.optimals.shape)
    print((sr, sc))
    state[sr][sc] = current_player.sign

    return state


if __name__ == "__main__":
    p_wins = [0, 0]
    p_matches = [0, 0]
    player_1 = player(CIRCLE, random_s)
    player_2 = player(CROSS, opt_s)
    players = [player_1, player_2]

    #Dopo un tot dai feed back e vari parametri
    #Potresti definire un epslion che è il peso da sommarte nell'optimal e saeconda del feedback lo vari
    for j in range(N_MATCHES):
        for i in range(N_ROUNDS):
            current_player = 0
            match = game()
            ending = check_finished(match.state)
            
            while ending == BASIC_VAL and match.possible_moves != 0:
                match.state = players[current_player].strategy(match.state, players[current_player])
                print("GAME STATE: ")
                print(match.state)
            
                match.possible_moves -= 1
                current_player = abs(current_player - 1)
                ending = check_finished(match.state)

            if ending == BASIC_VAL:
                print("PAREGGIO!")
            else:
                if ending == CROSS:
                    p_wins[1] += 1
                else:
                    print("AAAAAAAAAAAAAAAAAAAAAAA")
                    p_wins[0] += 1

            player_2.reset(p_wins)

        print(p_wins)

        if p_wins[0] > p_wins[1]:
            p_matches[0] += 1
        else:
            p_matches[1] += 1
    