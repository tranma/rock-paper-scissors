from enum import Enum
from rps.state.game import Move

class Player:
    def __init__(self, name) -> None:
        self.name = name

    def play(self) -> Move:
        return Move.ROCK

    def update(self, my_move: Move, opponent_move: Move) -> None:
        pass