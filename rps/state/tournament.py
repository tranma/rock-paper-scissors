from tqdm import tqdm
import numpy as np
import matplotlib.pyplot as plt
from rps.state.game import Result
from rps.players.player import Player

def play_round(
    tournament_result: Result, game_result: Result,
    p1: Player, p2: Player):

    m1 = p1.play()
    m2 = p2.play()

    p1.update(my_move=m1, opponent_move=m2)
    p2.update(my_move=m2, opponent_move=m1)

    w = Result.decide_winner(m1, m2)
    tournament_result.tally_round(w)
    game_result.tally_round(w)

    return w, m1, m2

def play_game(print_round, tournament_result, p1, p2, num_rounds, pbar, w):
    game_result = Result()

    for i in range(num_rounds):
        round_result = play_round(tournament_result, game_result, p1, p2)
        if pbar is not None: pbar.update(1)
        print_round_end(print_round, round_result, p1, p2, w)

    return game_result

def play_tournament(
    p1, p2, num_games, num_rounds,
    print_tour=True, print_game=False, print_round=False, print_plot=False,
    show_bar=True,
    w=40):

    print_tournament_start(print_tour, p1, p2, w)
    tour_result = Result()
    game_results = []
    n = num_games*num_rounds
    pbar = tqdm(total=n, ncols=w, bar_format='{bar}') \
        if show_bar else None

    for i in range(num_games):
        game_result = play_game(
            print_round, tour_result,
            p1, p2, num_rounds, pbar, w)
        print_game_end(print_game, game_result, f"Game {i}", p1, p2, w)
        game_results.append(game_result)

    if pbar: pbar.close()
    print_tournament_end(print_tour, tour_result, p1, p2, w)
    plot_progess(print_plot, game_results, p1, p2)

star  = '[*]'
cross = '[ ]'

def print_round_start(print_round, game, round):
    if not print_round: return
    print(f"Game {game} Round {round}")

def print_round_end(print_round, round, p1, p2, w):
    if not print_round: return
    winner, move1, move2 = round

    left  = (star if winner == 1 else cross) + ' ' + str(move1)
    right = str(move2) + ' ' + (star if winner == 2 else cross)
    print(left + ' ' * (w - len(left) - len(right)) + right)

    left, right = p1.name, p2.name
    print(left + ' ' * (w - len(left) - len(right)) + right)

    left, right = "----", "----"
    print(left + ' ' * (w - len(left) - len(right)) + right)

def print_game_end(print_game, game_result, game_str, player1, player2, w):
    if not print_game: return
    print()
    print(f"{game_str} Stats:")

    tally = game_result.tally
    n = sum(tally)
    d  = 100 * tally[0] / n
    s1 = 100 * tally[1] / n
    s2 = 100 * tally[2] / n

    left, right = player1.name, player2.name
    center = "Draw".center(w - len(left) - len(right))
    print(left + center + right)

    left, right = f"{s1:.2f}", f"{s2:.2f}"
    center = f"{d:.2f}".center(w - len(left) - len(right))
    print(left + center + right)
    
    print("-" * w)
    print()

def print_tournament_start(print_tour, player1, player2, w):
    if not print_tour: return
    print()
    left, right = player1.name, player2.name
    center = "vs".center(w - len(left) - len(right))
    print(left + center + right)
    print()

def print_tournament_end(print_tour, tournament_result, player1, player2, w):
    if not print_tour: return
    print_game_end(print_tour, tournament_result, "Tournament", player1, player2, w)

def plot_progess(do_plot, game_results, p1, p2):
    if not do_plot: return
    matrix = np.array([r.tally for r in game_results])

    plt.plot(matrix[:, 1], label=p1.name)
    plt.plot(matrix[:, 2], label=p2.name)

    plt.legend()
    plt.show()
