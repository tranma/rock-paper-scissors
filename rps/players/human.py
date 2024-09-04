from enum import Enum
from rps.state.game import Move
from rps.players.player import Player

class Human(Player):
    def __init__(self, name) -> None:
        self.name = name

    def play(self) -> Move:
        x = input("Your move [r/p/s]: ")
        if   x == 'r':
            return Move.ROCK 
        elif x == 'p':
            return Move.PAPER
        elif x == 's':
            return Move.SCISSORS
        else:
            raise ValueError(f"Invalid move {x}")
