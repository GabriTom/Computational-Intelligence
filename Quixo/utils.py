from game import Game, Move, Player

def acceptable_slides(from_pos):
    # define the corners
    SIDES = [(0, 0), (0, 4), (4, 0), (4, 4)]
    possible_slides = set()
    # if the piece position is not in a corner
    if from_pos not in SIDES:
        # if it is at the TOP, it can be moved down, left or right
        if from_pos[0] == 0:
            possible_slides.add(Move.BOTTOM)
            possible_slides.add(Move.LEFT)
            possible_slides.add(Move.RIGHT)
        if from_pos[0] == 4:
            possible_slides.add(Move.TOP)
            possible_slides.add(Move.LEFT)
            possible_slides.add(Move.RIGHT)
        if from_pos[1] == 0:
            possible_slides.add(Move.BOTTOM)
            possible_slides.add(Move.TOP)
            possible_slides.add(Move.RIGHT)
        if from_pos[1] == 4:
            possible_slides.add(Move.BOTTOM)
            possible_slides.add(Move.LEFT)
            possible_slides.add(Move.TOP)
    # if the piece position is in a corner
    else:
        # if it is in the upper left corner, it can be moved to the right and down
        if from_pos == (0, 0):
            possible_slides.add(Move.BOTTOM)
            possible_slides.add(Move.RIGHT)
        # if it is in the lower left corner, it can be moved to the right and up
        if from_pos == (4, 0):
            possible_slides.add(Move.TOP)
            possible_slides.add(Move.RIGHT)
        # if it is in the upper right corner, it can be moved to the left and down
        if from_pos == (0, 4):
            possible_slides.add(Move.BOTTOM)
            possible_slides.add(Move.LEFT)
        # if it is in the lower right corner, it can be moved to the left and up
        if from_pos == (4, 4):
            possible_slides.add(Move.TOP)
            possible_slides.add(Move.LEFT)
    return list(possible_slides)

#Ritorna un game
def move(g: Game, from_pos: tuple[int, int], slide: Move, player_id: int) -> bool:
    g._Game__move(from_pos, slide, player_id)
    return g.get_board()