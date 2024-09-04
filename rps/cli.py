from tqdm import tqdm
from rps.state.tournament import play_tournament
from rps.players.player import Player
from rps.players.human import Human
from rps.players.weighted import Weighted
from rps.players.markov import Markov
from rps.players.reinforce import Q
from rps.players.bayes import Bayes
from rps.players.ensemble import Ensemble

def get_valid_input(prompt, f):
    while True:
        try:
            s = input(prompt)
            x = f(s)
            return x
        except ValueError:
            print("Invalid input. Please try again.")

def player_choice_computer(s: str) -> Player:
    if s == 'e':
        n = get_valid_input(
            "How many in the ensemble: ", lambda s: int(s))
        ps = []
        for i in range(n):
            p = get_valid_input(
                f"Choose ensemble player {i+1}: ",
                lambda s: player_choice_computer_single(s))
            ps.append(p)
        m = Ensemble("Rabble", ps)
        print(f"{m.name}: {[p.name for p in ps]}")
    else:
        m = player_choice_computer_single(s)
    return m

def player_choice_computer_single(s: str) -> Player:
    if s == 'r':
        m = Weighted(name='Randy', weights=None)
    elif s == 's':
        m = Weighted(name='Scissorhands', weights=[1,1,8])
    elif s == 'm':
        m = Markov(name='Mark', num_moves=2)
    elif s == 'q':
        m = Q(name="Queenie", num_moves=2)
    elif s == 'b':
        m = Bayes(name="Bary")
    else:
        raise ValueError(f"Invalid player {s}")
    return m

def player_choice(s: str, have_human):
    h = have_human
    if   s == 'h':
        m = Human(name="Human")
        h = True
    else:
        m = player_choice_computer(s)
    return m, h

if __name__ == "__main__":
    print("Let's play Rock-Paper-Scissors!")

    instructions = """
We will play N games, with M rounds per game.
    """
    print(instructions)
    num_games = get_valid_input("How many games: ", lambda s: int(s))
    num_rounds = get_valid_input("How many rounds per game: ", lambda s: int(s))

    player_viz = """
Player Choices:
- [h]: Human
- [r]: Randy
- [s]: Scissorhands
- [m]: Mark
- [q]: Queenie
- [b]: Bary
- [e]: Rabble
    """
    print(player_viz)
    have_human = False
    p1, have_human = get_valid_input("Choose player 1: ",
        lambda s: player_choice(s, have_human))
    p2, have_human = get_valid_input("Choose player 2: ",
        lambda s: player_choice(s, have_human))

    play_tournament(
        p1, p2,
        num_games, num_rounds,
        print_tour=True,
        print_game=have_human,
        print_round=have_human,
        print_plot=False,
        show_bar=not have_human)