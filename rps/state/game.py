from enum import Enum

class Move(Enum):
    ROCK = 0
    PAPER = 1
    SCISSORS = 2

    def __str__(self) -> str:
        if self is Move.ROCK:
            return "ROCK"
        elif self is Move.PAPER:
            return "PAPER"
        elif self is Move.SCISSORS:
            return "SCISSORS"
        else:
            raise ValueError

    def next(self):
        members = list(self.__class__)
        index = (members.index(self) + 1) % len(members)
        return members[index]

    def beaten_by(self):
        return self.next()

class Result:
    def __init__(self) -> None:
        self.tally = [0, 0, 0]

    @staticmethod
    def decide_winner(p1: Move, p2: Move) -> int:
        if   p2 == p1.next():
            return 2
        elif p1 == p2.next():
            return 1
        else:
            assert p1 == p2
            return 0

    def tally_round(self, w: int) -> None:
        self.tally[w] += 1
