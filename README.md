# Rock Paper Scissors

This project simulates a game of rock-paper-scissors, where a human player can play against several computer players for multiple rounds.

## Game

From the project root, run to launch the CLI:
```
python -m rps.cli
```

You will be prompted for how many rounds you wish to play, and then to choose
the two players.
```
Player Choices:
- [h]: Human
- [r]: Randy
- [s]: Scissorhands
- [m]: Mark
- [q]: Queenie
- [b]: Bary
- [e]: Ensemble of Computer Players
```

If you pick `Human` the game will prompt you to choose a move every round for that player.

The following are computer players:
- `Randy` makes random choices every round.
- `Scissorhands` tends to play scissors.
- `Mark` will remember how you played (up to a certain point).
- `Queenie` will also remember how you played up to a point, but also how your sequence of plays are correlated.
- `Bary` makes some assumptions about the way you play and update its beliefs as the game progresses.

If you pick `Ensemble` you will be prompted to choose the computer players to add to your ensemble.

Here is an example of a full game:
```
python -m rps.cli
Let's play Rock-Paper-Scissors!

We will play N games, with M rounds per game.

How many games: 100
How many rounds per game: 1000

Player Choices:
- [h]: Human
- [r]: Randy
- [s]: Scissorhands
- [m]: Mark
- [q]: Queenie
- [b]: Bary
- [e]: Rabble

Choose player 1: m
Choose player 2: e
How many in the ensemble: 4
Choose ensemble player 1: m
Choose ensemble player 2: b
Choose ensemble player 3: q
Choose ensemble player 4: r
Rabble: ['Mark', 'Bary', 'Queenie', 'Randy']

Mark              vs              Rabble

████████████████████████████████████████

Tournament Stats:
Mark             Draw             Rabble
42.29            17.84             39.87
----------------------------------------
```

## Players

The purpose of the game is to choose the optimal next move from `{Rock, Paper, Scissors}`.

As the simplest baseline, the random player (Randy) assigns equal probability to each option: `[1/3, 1/3, 1/3]`

We have weighted players, who are more inclined towards some options than others. The Scissorhands player assigns probability `[0.1, 0.1, 0.8]` to the options.

In a real game of rock-paper-scissors, we might attempt to learn something about our opponent's pattern of play and try to counter it. The Markov Chain player (Mark) keeps a table of frequencies for sequences of the opponent's last N moves:
```
Pr(t=X|ts=[X_i..X_n]) for X in {Rock, Paper, Scissors}
```

Making the optimal choice each round sometimes does not lead to winning the game, especially if our opponent is playing adversarially. Addtionally in a long-running game, our opponent might also learn our pattern of play and use it against us.

The reinforcement learning player (Queenie) uses a longer term strategy that takes into account future wins. It also tries random moves to explore new patterns of play.

The Bayes player (Bary) keeps an explicit distribution for the possible moves,
and update it as it observes new frequencies.

The ensemble player randomly chooses a member of the ensemble to play each round.

## Results

The `notebooks` directory contains some experimental results, summarised here.
`<` means beaten (more means more heavily beaten) ,`>` means winning, `=` means parity.

```
-------------------------------------------------------
|          | Randy | Scissors | Mark | Queenie | Bary |
-------------------------------------------------------
| Randy    |       | >        | ==   | ==      | ==   |
| Scissors | <<    |          | <<<< | <<<     | <<<< |
| Mark     | ==    | >>>>     |      | <       | ==   |
| Queenie  | ==    | >>>      | >    |         |      |
| Bary     | ==    | >>>>     | <<<< |         |      |
-------------------------------------------------------
```

Overall the Mark, Markov chain player, performs best against the other players. Given the limited dimensions of data (only using the game's outcome and no other information on the players), this makes sense.

## Thoughts

No one has made a dataset of rock-paper-scissors games, with player features corresponding to their wins/losses!

I only explored the simplest methods I know. It would be interesting to try this project on a similar problem with more data.
