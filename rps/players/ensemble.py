import random
import numpy as np
from typing import List
from rps.state.game import Move
from rps.players.player import Player

class Ensemble(Player):
    """
    A ensemble of rock-paper-scissors players. Every round we randomly choose
    a player.
    """
    def __init__(self, name, players: List[Player]) -> None:
        self.name = name
        self.players = players
        self.last_played = 0

    def update(self, my_move: Move, opponent_move: Move) -> None:
        self.players[self.last_played].update(my_move, opponent_move)

    def play(self) -> Move:
        i = random.randint(0, len(self.players) - 1)
        self.last_played = i
        return self.players[i].play()
