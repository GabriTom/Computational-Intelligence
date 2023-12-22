import numpy as np
import random
from copy import deepcopy

SOL_REF = [[4, 9, 2], [3, 5, 7], [8, 1, 6]]
CMP_VALUE = 15
N_ROUNDS_TRAIN = 2000
N_ROUNDS_TEST = 10
N_MATCHES = 10
BASIC_VAL = 0
CIRCLE = -1
CROSS = 1

#Class game, it has the actual state and the remaining moves
class game:
    def __init__(self):
        self.state = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
        self.possible_moves = 9

class player:
    def __init__(self, sign):
        self.sign = sign
        self.exp_rate = 0.3
        self.decay_gamma = 0.9
        self.lr = 0.2
        self.optimals = np.zeros((3, 3))
        self.states = []
        self.states_values = {}
        self.training_phase = True

    def feedReward(self, reward):
        for st in reversed(self.states):
            if self.states_values.get(st) is None:
                self.states_values[st] = 0
            self.states_values[st] += self.lr * (self.decay_gamma * reward - self.states_values[st])
            reward = self.states_values[st]

    def reset(self):
        self.optimals = np.zeros((3, 3))

#Returns a hash of a state (= state in a string)
def get_hash(state):
    ret = []
    for row in state:
        for cell in row:
            ret.append(cell)
    return str(ret)

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
        actual_optimals[i, i] += abs(sum_diag)

    for i in range(player.optimals.shape[0]):
        actual_optimals[player.optimals.shape[0]-1-i, i] += abs(sum_anti_diag)

    player.optimals = np.multiply(actual_optimals, available_positions)
    # print("Actual optimals LATER")
    # print(player.optimals)


# #Function that receives a state and a player and do the best move based on optimals values
def opt_s(state, current_player):
    available_positions = np.zeros((len(state), len(state[0])))

    #Finding empty positions
    for i in range(len(state)):
        for j in range(len(state[i])):
            if state[i][j] == 0:
                available_positions[i][j] = 1
    # print("Available position")
    # print(available_positions)
    compute_distance(state, current_player, available_positions)

    #Selecting cell
    sr, sc = np.unravel_index(np.argmax(abs(current_player.optimals), axis=None), current_player.optimals.shape)
    # print((sr, sc))
    state[sr][sc] = current_player.sign

    return state

#Function that perform a move accordingly to the player exploration_rate and is the player is in traning phase or not
def perform_move(state, player):
    #Only player with cross is a Q-learned agent
    if player.sign == CIRCLE:
        move = random_s(state, player)
    else:
        available_positions_list = []
        if np.random.uniform(0, 1) < player.exp_rate:
            move = random_s(state, player)
        else:
            if player.training_phase:
                move = opt_s(state, player)
            else:
                #Creating a list of available positions
                for i in range(len(state)):
                    for j in range(len(state[i])):
                        if state[i][j] == 0:
                            available_positions_list.append(i*len(state)+j)

                value_max = -999
                for p in available_positions_list:
                    next_state = deepcopy(state)
                    row = p // len(state)
                    col = p % len(state)
                    next_state[row][col] = player.sign
                    next_board_hash = get_hash(next_state)
                    value = 0 if player.states_values.get(next_board_hash) is None else player.states_values.get(next_board_hash)
                    # print("value", value)
                    if value >= value_max:
                        value_max = value
                        move = next_state

        player.states.append(get_hash(move))

    return move


if __name__ == "__main__":
    player_1 = player(CIRCLE)
    player_2 = player(CROSS)
    players = [player_1, player_2]

    for i in range(N_ROUNDS_TRAIN):
        current_player = 0
        match = game()
        ending = check_finished(match.state)
        
        while ending == BASIC_VAL and match.possible_moves != 0:
            match.state = perform_move(match.state, players[current_player])
            match.possible_moves -= 1
            current_player = abs(current_player - 1)
            ending = check_finished(match.state)
        
        if ending == CROSS:
            player_2.feedReward(1)
            player_1.feedReward(0)
        elif ending != BASIC_VAL:
            player_2.feedReward(0)
            player_1.feedReward(1)
        else:
            player_1.feedReward(0.5)
            player_2.feedReward(0.1)

        player_2.reset()
    
    player_1.training_phase = False
    player_2.training_phase = False

    p_wins = [0, 0]
    p_matches = [0, 0]

    for i in range(N_ROUNDS_TEST):
        current_player = 0
        match = game()
        ending = check_finished(match.state)
        
        while ending == BASIC_VAL and match.possible_moves > 0:
            match.state = perform_move(match.state, players[current_player])
            match.possible_moves -= 1
            current_player = abs(current_player - 1)
            ending = check_finished(match.state)

        if ending == BASIC_VAL:
            print("DRAW!")
        elif ending == CROSS:
            p_wins[1] += 1
        else:
            p_wins[0] += 1

    print(p_wins)
    # if p_wins[0] > p_wins[1]:
    #     p_matches[0] += 1
    # elif p_wins[0] < p_wins[1]:
    #     p_matches[1] += 1
    
    # if p_matches[0] > p_matches[1]:
    #     print("Player 1 wins most of the matches.")
    # elif p_matches[0] == p_matches[1]:
    #     print("Match draw")
    # else:
    #     print("Player 2 wins most of the matches.")
    # print(p_matches)