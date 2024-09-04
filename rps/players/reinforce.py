import random
import numpy as np
from rps.state.game import Move, Result
from rps.players.player import Player

class Q(Player):
    """
    A player who keeps track of the reward they get for making a move X
    following a sequence of opponent moves.
    
    For each round we choose between exploiting the current known long-term
    rewards, and explore new actions.
    """
    def __init__(self, name,
        num_moves=2,\
        learning_rate=0.1,
        discount_rate=0.9,
        exploration_rate=0.1) -> None:
        self.name = "Queenie"
        self.num_moves = num_moves
        self.moves = list(Move)

        self.name = name
        self.q = dict()
        self.state = [] # number of past opponent moves
        self.current_move = None

        self.alpha = learning_rate
        self.gamma = discount_rate
        self.epsilon = exploration_rate

    def get_reward(self, my_move: Move, opponent_move: Move) -> int:
        w = Result.decide_winner(my_move, opponent_move)
        if w == 1:
            return 1
        elif w == 2:
            return -1
        else:
            return 0

    def play(self) -> Move:
        """
        If we have seen the opponent use the sequence of moves stored in
        'state' before, we can use the counter-move that historically had
        given the best reward.

        Or choose to play a random move with epsilon chance.
        """
        state_key = tuple(self.state)

        if random.uniform(0, 1) < self.epsilon:
            best_move = random.choice(self.moves)

        else:
            if state_key not in self.q:
                best_move = random.choice(self.moves)

            else:
                best_move = Move(np.argmax(self.q[state_key]))

        return best_move

    def update(self, my_move, opponent_move):
        """
        Use the result of this round to update the reward table.
        """
        # Next state last N opponent moves including this round.
        next_state = [x for x in self.state]
        if len(next_state) == self.num_moves:
            next_state.pop(0)
        next_state.append(opponent_move)

        state_key = tuple(self.state)
        next_state_key = tuple(next_state)

        if state_key not in self.q:
            self.q[state_key] = np.zeros((3))
        if next_state_key not in self.q:
            self.q[next_state_key] = np.zeros((3))

        best_next_move = np.argmax(self.q[next_state_key])
        reward = self.get_reward(my_move, opponent_move)

        # q(s,a) <- q(s,a) + alpha * (r + gamma * max_a'(Q(s',a')) - Q(s,a))
        self.q[state_key][my_move.value] += self.alpha * (reward + \
            self.gamma * self.q[next_state_key][best_next_move] - \
            self.q[state_key][my_move.value])

        self.state = next_state
