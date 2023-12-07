import random
from game import Game, Move, Player

#Strategies:
#    - Random : already implemented
#    - Optimal
#    - Mathematical
#    - Evolutionary

class RandomPlayer(Player):
    def __init__(self) -> None:
        super().__init__()

    def make_move(self, game: 'Game') -> tuple[tuple[int, int], Move]:
        from_pos = (random.randint(0, 4), random.randint(0, 4))
        move = random.choice([Move.TOP, Move.BOTTOM, Move.LEFT, Move.RIGHT])
        return from_pos, move

# class OptimalPlayer(Player):
#     def __init__(self) -> None:
#         super().__init__()

#     def make_move(self, game: 'Game') -> tuple[tuple[int, int], Move]:
#         from_pos = (random.randint(0, 4), random.randint(0, 4))
#         move = random.choice([Move.TOP, Move.BOTTOM, Move.LEFT, Move.RIGHT])
#         return from_pos, move

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
    player2 = RandomPlayer()
    winner = g.play(player1, player2)
    g.print()
    print(f"Winner: Player {winner}")
