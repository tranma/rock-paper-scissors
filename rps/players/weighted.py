import random
from rps.state.game import Move
from rps.players.player import Player

class Weighted(Player):
    """
    A player whose probability of using a certain move X is given by the
    weights, for example [0.2, 0.6, 0.2] means the player is much more likely
    to use paper.
    
    If no weights is given then the player makes their choice randomly.
    """
    def __init__(self, name, weights=None) -> None:
        self.name = name
        self.weights = weights

    def play(self) -> Move:
        choices = list(Move)
        if self.weights is None:
            m = random.choice(choices)
        else:
            m = random.choices(choices, self.weights, k=1)[0]
        return m
