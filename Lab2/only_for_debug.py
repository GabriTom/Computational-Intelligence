import logging
from pprint import pprint, pformat
from collections import namedtuple
import random
from copy import deepcopy

Nimply = namedtuple("Nimply", "row, num_objects")
N_MATCHES = 30
N_TRAINS = 50

class Nim:
    def __init__(self, num_rows: int, k: int = None) -> None:
        self._rows = [i * 2 + 1 for i in range(num_rows)]
        self._k = k

    def __bool__(self):
        return sum(self._rows) > 0

    def __str__(self):
        return "<" + " ".join(str(_) for _ in self._rows) + ">"

    @property
    def rows(self) -> tuple:
        return tuple(self._rows)

    def nimming(self, ply: Nimply) -> None:
        row, num_objects = ply
        if not self._rows[row] >= num_objects:
            print("ERROR 1 -> self._rows[row] >= num_objects")
            exit
        if not ( self._k is None or num_objects <= self._k):
            print("ERROR 2 -> self._k is None or num_objects <= self._k")
            exit
        self._rows[row] -= num_objects


def pure_random(state: Nim) -> Nimply:
    """A completely random move"""
    row = random.choice([r for r, c in enumerate(state.rows) if c > 0])
    num_objects = random.randint(1, state.rows[row])
    
    #----- random approach enhancements -----
    #Forcing k
    if num_objects >= state._k:
        num_objects = state._k
    
    #Forcing to generate another k
    #while num_objects >= state._k:
    #    num_objects = random.randint(1, state.rows[row])
    return Nimply(row, num_objects)

#def odd_even(state: Nim) -> Nimply:
    #row = random.choice([r for r, c in enumerate(state.rows) if c > 0])

    #num_objects = random.randint(1, state.rows[row])

    #Forcing k
    #if num_objects >= state._k:
    #    num_objects = state._k

    #I want to stay EVEN SINCE the LAST to pick LOSE
    #if (sum(state.rows) % 2 == 0):
        #Change row if num_object == 1
    #    while num_objects % 2 == 0:
    #        num_objects = random.randint(1, state.rows[row])
    #else:
    #    while num_objects % 2 == 1 and num_objects != 1:
    #        num_objects = random.randint(1, state.rows[row])

    #return Nimply(row, num_objects)

def gabriele(state: Nim) -> Nimply:
    """Pick always the maximum possible number of the lowest row"""
    possible_moves = [(r, o) for r, c in enumerate(state.rows) for o in range(1, c + 1)]
    return Nimply(*max(possible_moves, key=lambda m: (-m[0], m[1])))

def adaptive(state: Nim) -> Nimply:
    """A strategy that can adapt its parameters"""
    genome = {"love_small": 0.5}

import numpy as np


def nim_sum(state: Nim) -> int:
    tmp = np.array([tuple(int(x) for x in f"{c:032b}") for c in state.rows])
    xor = tmp.sum(axis=0) % 2
    ret = int("".join(str(_) for _ in xor), base=2)
    return ret


def analize(raw: Nim) -> dict:
    cooked = dict()
    cooked["possible_moves"] = dict()
    for ply in (Nimply(r, o) for r, c in enumerate(raw.rows) for o in range(1, min(c+1, raw._k+1))):
        tmp = deepcopy(raw)
        tmp.nimming(ply)
        cooked["possible_moves"][ply] = nim_sum(tmp)
    return cooked


def optimal(state: Nim) -> Nimply:
    analysis = analize(state)
    logging.debug(f"analysis:\n{pformat(analysis)}")
    spicy_moves = [ply for ply, ns in analysis["possible_moves"].items() if ns != 0]
    if not spicy_moves:
        spicy_moves = list(analysis["possible_moves"].keys())
    ply = random.choice(spicy_moves)
    return ply



MAX_PROB = 100

    

def weighted_random(state: Nim, alfa, beta) -> Nimply:
    """A weighted random move"""
    idx = abs(int(alfa/MAX_PROB))
    row = [r for r, c in enumerate(state.rows) if c > 0]
    
    # Avoiding out of bound in rows
    if idx >= len(row):
        row = row[-1]
    else:
        row = row[idx]

    num_objects = int(np.round((beta/MAX_PROB)*random.randint(1, state.rows[row]+1)))
    #Forcing a suitable num_object regarding all constraints
    if num_objects <= 0:
        num_objects = 1
    else:
        if num_objects > state._k:
            num_objects = state._k
        if num_objects > state.rows[row]:
            num_objects = state.rows[row]
 
    return Nimply(row, num_objects)




if __name__ == "__main__":
    logging.getLogger().setLevel(logging.INFO)
    strategy = (optimal, weighted_random)

    alfa = random.randint(0, MAX_PROB)
    beta = random.randint(0, MAX_PROB)
    # sigma chosen randomly
    sigma = random.randint(0, MAX_PROB)

    alfa_best = alfa
    beta_best = beta
    wins_best = 0

    for _ in range(0, N_TRAINS):
        p_wins = [0, 0]
        print(f"alfa_b: {alfa_best}, beta_best: {beta_best}")
        #Executing N_MATCHES fro alfa and beta parameters
        for _ in range(0, N_MATCHES):
            nim = Nim(5, 4)
            #logging.info(f"init : {nim}")
            player = 0
            while nim:
                if player == 0:
                    ply = strategy[player](nim)
                else:
                    ply = strategy[player](nim, alfa_best, beta_best)
                #logging.info(f"ply: player {player} plays {ply}")
                nim.nimming(ply)
                #logging.info(f"status: {nim}")
                player = 1 - player
            #logging.info(f"----------------------------     status: Player {player} won!      ----------------------------")
            p_wins[player] += 1

        print(f"BEST WINS: {wins_best} \tACTUAL WINS: {p_wins[1]}")
            
        #  --- PLUS STRATEGY ---
        #If this model scored better than the previous, model evolves from actual parameters
        if wins_best < p_wins[1]:
            wins_best = p_wins[1]
            alfa_best = round(np.random.normal(alfa, sigma))
            beta_best = round(np.random.normal(beta, sigma))
        else:
            alfa_best = round(np.random.normal(alfa_best, sigma))
            beta_best = round(np.random.normal(beta_best, sigma))

        #  --- COMMA STRATEGY ---
        #Model evolves from actual parameters
        #alfa_best = round(np.random.normal(alfa, sigma))
        #beta_best = round(np.random.normal(beta, sigma))

    p_wins = [0, 0]
    # Doing last N_MATCHES with trained values
    for _ in range(0, N_MATCHES):
        nim = Nim(5, 4)
        logging.info(f"init : {nim}")
        player = 0
        while nim:
            if player == 0:
                ply = strategy[player](nim)
            else:
                ply = strategy[player](nim, alfa_best, beta_best)
            logging.info(f"ply: player {player} plays {ply}")
            nim.nimming(ply)
            logging.info(f"status: {nim}")
            player = 1 - player
        logging.info(f"----------------------------     status: Player {player} won!      ----------------------------")
        p_wins[player] += 1
    print(p_wins)