import numpy as np
from rps.state.game import Move
from rps.players.player import Player

class Bayes(Player):
    def __init__(self, name, priors=None, frequencies=None, record=None) -> None:
        self.name = name

        # Prior distribution. This is our initial belief about the opponent's
        # preference for each choice. Defaults to equal chances, ie. the opponent
        # has no preference for any of rock/papaer/scissors.
        default_priors = np.full((3), 1/3)

        # Initial frequency matrix. This encodes our belief about the opponent's
        # pattern of play.
        default_counts = np.full((3), 0.0)

        # Smoothing constant to avoid distribution collapse.
        self.epsilon = 0.1

        self.priors = np.array(priors) if priors is not None else default_priors
        self.counts = np.array(frequencies) if frequencies is not None else default_counts
        self.record = record

    def update(self, my_move: Move, opponent_move: Move) -> None:
        # Update observed counts
        self.counts[opponent_move.value] += 1

        # Calculate likelihood
        smoothed = self.counts + self.epsilon
        likelihood = smoothed / np.sum(smoothed)

        # Update priors using the likelihood
        posterior = self.priors * likelihood
        posterior /= np.sum(posterior)

        # Do not update if probabilities become too small
        if all(posterior > self.epsilon):
            self.priors = posterior
            if self.record is not None:
                self.record.append(self.priors.copy())

    def play(self) -> Move:
        predict = np.argmax(self.priors)
        return Move(predict).beaten_by()
