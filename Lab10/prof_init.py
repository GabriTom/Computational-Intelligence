import numpy as np
from itertools import combinations
from random import choice
from collections import namedtuple, defaultdict
from copy import deepcopy
from tqdm.auto import tqdm

State = namedtuple('Position', ['x', 'o'])

MAGIC = [4, 9, 2, 
         3, 5, 7, 
         8, 1, 6]

def win(elements):
    '''Check if element is winning'''
    return any(sum(c) == 15 for c in combinations(elements, 3))

def state_value(pos: State):
    '''Evaluate position'''
    if(win(pos.x)):
        return 1
    elif (win(pos.o)):
        return -1
    else:
        return 0
    
def print_board(state: State):
    for row in range(3):
        for col in range(3):
            index = row*3+col
            if MAGIC[index] in state.x:
                print('X', end='')
            elif MAGIC[index] in state.o:
                print('O', end='')
            else:
                print('- ', end='')
        print()


def random_game():
    trajectory = list()
    state = State()
    available = set(range(1, 9+1))

    while available:
        x = choice(list(available))
        state.x.add(x)
        trajectory.append(deepcopy(state))
        available.remove(x)
        if win(state.x) or not available(x):
            return trajectory
        

        y = choice(list(available))
        state.y.add(y)
        trajectory.append(deepcopy(state))
        available.remove(y)
        if win(state.y) or not available(y):
            return trajectory

    return trajectory

if __name__ == "__main__":
    value_dictionary = defaultdict(float)
    epsilon = .001
    
    for step in range(100):
        trajectory = random_game()
        final_reward = state_value(trajectory[-1])
        for state in trajectory:
            hashable_state = State(frozenset(state.x), frozenset(state.o))
            state_value[hashable_state] = state_value[hashable_state] + epsilon * (final_reward + value_dictionary[hashable_state])

    print(hit_state.items, key)