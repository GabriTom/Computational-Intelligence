import random
from copy import deepcopy
import numpy as np
import utils
from game import Game, Move, Player

TRAINING_MATCHES = 2000
TESTING_MATCHES = 100
N_MATCH = 5

#Strategies:
#    - Random : already implemented
#    - RL

#Random player
class RandomPlayer(Player):
    def __init__(self) -> None:
        super().__init__()

    #This function chooses a random position and slide and return them.
    def make_move(self, game: 'Game') -> tuple[tuple[int, int], Move]:
        from_pos = (random.randint(0, 4), random.randint(0, 4))
        move = random.choice([Move.TOP, Move.BOTTOM, Move.LEFT, Move.RIGHT])
        return from_pos, move

#Player implemented with a q-learning strategy.
class QLearningPlayer(Player):
    def __init__(self):
        super().__init__()
        self.exp_rate = 0.3
        self.decay_gamma = 0.5
        self.lr = 0.5
        self.states = []
        self.states_values = {}

    #Function that updates the value in the dictionary for the used moves. It receives reward as an input.
    def feedReward(self, reward):
        for st in reversed(self.states):
            if self.states_values.get(st) is None:
                self.states_values[st] = 0
            self.states_values[st] += self.lr * (self.decay_gamma * reward - self.states_values[st])
            reward = self.states_values[st]

    #Function that set the exploring rate to 0 leading to using only what the player learned during training.
    def go_testing(self):
        self.exp_rate = 0

    #Function that gives a board computes all its simmetries.
    def compute_symmetries(self, board):
        rev_b = board[::-1]
        tra_b = np.matrix(board).T
        rev_tra_b = tra_b[::-1]
        return (board, rev_b, tra_b, rev_tra_b)

    #Function that resets the states reached during the last game.
    def reset(self):
        self.states = []

    #Returns a hash of a state (= state in a string)
    def get_hash(self, state):
        ret = []
        for row in state:
            for cell in row:
                ret.append(cell)
        return str(ret)
    
    #Creating two lists: the first with the free position, the second with those positions the pkayer already took.
    def available_positions(self, state):
        free_positions = []
        my_positions = []
        for i in range(len(state.get_board())):
            if i == 0 or i == 4:
                cols = range(len(state.get_board()[i]))
            else:
                cols = [0, 4]
            for j in cols:
                if state.get_board()[i][j] == -1:
                    free_positions.append((i,j))
                if state.get_board()[i][j] == state.current_player_idx:
                    my_positions.append((i,j))
        return free_positions, my_positions

    #Perform a move accordignly to the Q-Learning strategy
    #Furthermore, if there are free blocks it chooses them, otherwise it chooses already taken ones
    def make_move(self, game: 'Game') -> tuple[tuple[int, int], Move]:
        state = deepcopy(game)
        free_p, mine_p = self.available_positions(state)
        fp = deepcopy(free_p)

        #Exploration
        if len(fp) > 0:
            #If there are positions still not occupied it will choose them
            from_pos = random.choice(fp)
            fp.remove(from_pos)
            move = random.choice(utils.acceptable_slides(from_pos))
            while not state._Game__move((from_pos[1], from_pos[0]), move, game.current_player_idx):
                fp.remove(from_pos)
                if len(fp) <= 0:
                    break
                from_pos = random.choice(fp)
                move = random.choice(utils.acceptable_slides(from_pos))
        else:
            #Otherwise it chooses already taken positions (if there are any)
            if len(mine_p) > 0:
                from_pos = random.choice(mine_p)
            else:
                from_pos = random.choice(fp)
            move = random.choice(utils.acceptable_slides(from_pos))
            while not state._Game__move((from_pos[1], from_pos[0]), move, game.current_player_idx):
                from_pos = random.choice(mine_p)
                move = random.choice(utils.acceptable_slides(from_pos))

        #Saving that choice for later
        best_hash = self.get_hash(state.get_board())

        #Exploitation
        if np.random.uniform(0, 1) > self.exp_rate:
            value_max = -9999
            next_state = deepcopy(game)
            #Try every possible move and slide
            for p in free_p + mine_p:
                for s in utils.acceptable_slides(p):
                    #Check if it acceptable
                    if not next_state._Game__move((p[1], p[0]), s, game.current_player_idx):
                        break

                    #Without simmetries
                    # next_board_hash = self.get_hash(next_state.get_board())
                    # value = 0 if self.states_values.get(next_board_hash) is None else self.states_values.get(next_board_hash)
                    # if value > value_max:
                    #     value_max = value
                    #     best_hash = next_board_hash
                    #     from_pos = p
                    #     move = s

                    #With simmetries
                    for h in self.compute_symmetries(next_state.get_board()):
                        next_board_hash = self.get_hash(h)
                        value = 0 if self.states_values.get(next_board_hash) is None else self.states_values.get(next_board_hash)
                        if value > value_max:
                            value_max = value
                            best_hash = next_board_hash
                            from_pos = p
                            move = s

        #Append new state and return position and slide
        self.states.append(best_hash)
        return (from_pos[1], from_pos[0]), move

if __name__ == '__main__':
    #Initializing variables
    victories_train = [0, 0]
    match_wins = [0, 0]
    player1 = RandomPlayer()
    player2 = QLearningPlayer()

    #Training mode
    print("Progress: ")
    for pol in range(TRAINING_MATCHES):
        g = Game()
        winner = g.play(player1, player2)
        if winner == 1:
            player2.feedReward(10)
        else:
            player2.feedReward(0)

        player2.reset()
        #Printing training process percentage
        res = (pol+1)/TRAINING_MATCHES*100
        print("\t", round(res), "%", end = "\r")
        #victories_train[winner] += 1
    print()
    #print(victories_train)

    #Testing mode
    player2.go_testing()
    for _ in range(N_MATCH):
        victories = [0, 0]
        for _ in range(TESTING_MATCHES):
            g = Game()
            winner = g.play(player1, player2)
            victories[winner] += 1
        # if victories[0] > victories[1]:
        #     match_wins[0] += 1
        # else:
        #     match_wins[1] += 1
        print(victories)
    #print(match_wins)