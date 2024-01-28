import random
from copy import deepcopy
import numpy as np
import utils
from game import Game, Move, Player

TRAINING_MATCHES = 1000
TESTING_MATCHES = 100

#Strategies:
#    - Random : already implemented
#    - Optimal
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
        from_pos = (random.randint(0, 4), random.randint(0, 4))
        move = random.choice([Move.TOP, Move.BOTTOM, Move.LEFT, Move.RIGHT])
        return from_pos, move
    
    def find_neighbours():
        print("de")

# TODO implementa fase di training e test
class QLearningPlayer(Player):
    def __init__(self):
        super().__init__()
        self.exp_rate = 0.1
        self.decay_gamma = 0.5
        self.lr = 0.5
        self.states = []
        self.states_values = {}

    def feedReward(self, reward):
        for st in reversed(self.states):
            if self.states_values.get(st) is None:
                self.states_values[st] = 0
            self.states_values[st] += self.lr * (self.decay_gamma * reward - self.states_values[st])
            reward = self.states_values[st]

    def go_testing(self):
        self.exp_rate = 0.01

    def reset(self):
        self.states = []

    #Returns a hash of a state (= state in a string)
    def get_hash(self, state):
        ret = []
        for row in state:
            for cell in row:
                ret.append(cell)
        return str(ret)

    #Memorizza nel dictionary facendo rotazioni della board così occupi meno spazio
    def make_move(self, game: 'Game') -> tuple[tuple[int, int], Move]:
        state = deepcopy(game)
        available_positions_list = []

        #Creating a list of available positions
        for i in range(len(state.get_board())):
            if i == 0 or i == 4:
                cols = range(len(state.get_board()[i]))
            else:
                cols = [0, 4]
            for j in cols:
                if state.get_board()[i][j] == -1 or state.get_board()[i][j] == 1:
                    available_positions_list.append((i,j))

        from_pos = random.choice(available_positions_list)
        move = random.choice(utils.acceptable_slides(from_pos))
        while not state._Game__move((from_pos[1], from_pos[0]), move, game.current_player_idx):
            from_pos = random.choice(available_positions_list)
            move = random.choice(utils.acceptable_slides(from_pos))
        
        if np.random.uniform(0, 1) >= self.exp_rate:
            value_max = -9999
            best_hash = ''
            next_state = deepcopy(game)
            #Try every possible move and slide
            for p in available_positions_list:
                for s in utils.acceptable_slides(p):
                    if next_state._Game__move((p[1], p[0]), s, game.current_player_idx):
                        next_board_hash = self.get_hash(next_state.get_board())
                        value = 0 if self.states_values.get(next_board_hash) is None else self.states_values.get(next_board_hash)

                        if value > value_max:
                            value_max = value
                            best_hash = next_board_hash
                            from_pos = p
                            move = s

            self.states.append(best_hash)
        return (from_pos[1], from_pos[0]), move

if __name__ == '__main__':
    victories = [0, 0]
    victories_train = [0, 0]

    #Training mode
    player1 = RandomPlayer()
    player2 = QLearningPlayer()

    for pol in range(TRAINING_MATCHES):
        g = Game()
        winner = g.play(player1, player2)
        #print(player2.states)
        if winner == 1:
            player2.feedReward(1)
        else:
            player2.feedReward(0)
        player2.reset()
        victories_train[winner] += 1
    print(victories_train)

    #Testing mode
    player2.go_testing()
    for _ in range(TESTING_MATCHES):
        g = Game()
        winner = g.play(player1, player2)
        victories[winner] += 1
    print(victories)