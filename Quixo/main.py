import random
from copy import deepcopy
import numpy as np
from game import Game, Move, Player

#Strategies:
#    - Random : already implemented
#    - Optimal
#    - Mathematical
#    - RL

class RandomPlayer(Player):
    def __init__(self) -> None:
        super().__init__()

    def make_move(self, game: 'Game') -> tuple[tuple[int, int], Move]:
        from_pos = (random.randint(0, 4), random.randint(0, 4))
        move = random.choice([Move.TOP, Move.BOTTOM, Move.LEFT, Move.RIGHT])
        return from_pos, move

class OptimalPlayer(Player):
    def __init__(self) -> None:
        super().__init__()

    def make_move(self, game: 'Game') -> tuple[tuple[int, int], Move]:
        #Check su righe e colonne, sommi, fai mossa in quella che esce puteggio più altoù
        row_max_idx = np.argmax(np.sum(game.get_board(), axis = 1))
        col_max_idx = np.argmax(np.sum(game.get_board(), axis = 0))
        print(col_max_idx, " ", row_max_idx)
        from_pos = (random.randint(0, 4), random.randint(0, 4))
        move = random.choice([Move.TOP, Move.BOTTOM, Move.LEFT, Move.RIGHT])
        return from_pos, move
    
    def find_neighbours():
        print("de")

class QLearningPlayer(Player):
    def __init__(self, sign):
        super().__init__()
        self.exp_rate = 0.3
        self.decay_gamma = 0.5
        self.lr = 0.5
        self.states = []
        self.states_values = {}
        self.training_phase = True
        self.sign = sign

    def feedReward(self, reward):
        for st in reversed(self.states):
            if self.states_values.get(st) is None:
                self.states_values[st] = 0
            self.states_values[st] += self.lr * (self.decay_gamma * reward - self.states_values[st])
            reward = self.states_values[st]

    #Returns a hash of a state (= state in a string)
    def get_hash(state):
        ret = []
        for row in state:
            for cell in row:
                ret.append(cell)
        return str(ret)

    #Memorizza nel dictionary facendo rotazioni della board così occupi meno spazio
    def make_move(self, game: 'Game') -> tuple[tuple[int, int], Move]:
        state = game.get_board()
        available_positions_list = []
        if np.random.uniform(0, 1) < self.exp_rate:
            from_pos, move = RandomPlayer().make_move(state)
        else:
            #Creating a list of available positions
            for i in range(len(state)):
                for j in range(len(state[i])):
                    if state[i][j] == 0:
                        available_positions_list.append([i, j])

            value_max = -9999
            for p in available_positions_list:
                for s in __acceptable_slides(p):
                    next_state = deepcopy(game)

                    next_state = next_state.__move(p, s, self)

                    next_board_hash = self.get_hash(next_state)
                    value = 0 if self.states_values.get(next_board_hash) is None else self.states_values.get(next_board_hash)
                    # print("value", value)
                    if value >= value_max:
                        value_max = value
                        from_pos = p
                        move = s

            self.states.append(self.get_hash(next_state))

        return from_pos, move
        

# class MathematicalPlayer(Player):
#     def __init__(self) -> None:
#         super().__init__()

#     def make_move(self, game: 'Game') -> tuple[tuple[int, int], Move]:
#         from_pos = (random.randint(0, 4), random.randint(0, 4))
#         move = random.choice([Move.TOP, Move.BOTTOM, Move.LEFT, Move.RIGHT])
#         return from_pos, move

if __name__ == '__main__':
    g = Game()
    g.print()
    # Fai un tot di partite per tuning parameters
    # TO DO playerone must be vector of strategies
    # TO DO 2 then chnage player2 have see if something happens
    player1 = RandomPlayer()
    player2 = QLearningPlayer(1)
    winner = g.play(player1, player2)
    g.print()
    print(f"Winner: Player {winner}")
