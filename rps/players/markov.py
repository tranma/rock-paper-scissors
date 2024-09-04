import random
import numpy as np
from rps.state.game import Move
from rps.players.player import Player

class Markov(Player):
    """
    A player who uses the conditional probability that the opponent
    will make a certain move following a sequence of past N moves:
    Pr(t=X|t-1,t-2,...)

    When opponent play move X, and we have state H, we update the
    frequencies associated with H,

    To decide a counter-move, we find the opponent move with highest
    probability.
    """
    def __init__(self, name, num_moves=2) -> None:
        self.name = name
        self.state = []
        self.num_moves = num_moves
        self.counts = dict()

    def update(self, opponent_move: Move, my_move=None) -> None:
        """
        Update the probability that current state leads to this move, then
        add the move to state.
        """
        k = tuple(self.state)

        if len(self.state) == self.num_moves:
            # Update the count for the new move.
            if k not in self.counts:
                self.counts[k] = np.zeros((3))
            self.counts[k][opponent_move.value] += 1

            # Update running state
            self.state.pop(0)

        self.state.append(opponent_move)

    def play(self) -> Move:
        """
        Given the current state of opponent moves, decide our next move.
        """
        k = tuple(self.state)

        if k in self.counts:
            # How many times have we seen this sequence of moves.
            total = sum(self.counts[k])

            freqs = self.counts[k] / total
            max_likelihood_move = np.argmax(freqs)
            m = Move(max_likelihood_move).beaten_by()

        else:
            m = random.choice(list(Move))

        return m
