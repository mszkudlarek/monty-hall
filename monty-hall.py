from random import randint

import matplotlib.pyplot as plt
import matplotlib.ticker as ticker


def generating_outcome(n: int) -> list:
    """
    Generates a n of simulations where two doors are hiding goats and one 
    door reveals the main prize.
    """
    outcome = []

    for _ in range(n):
        the_doors = [False] * 3
        winning_door = randint(0,2)
        the_doors[winning_door] = True
        outcome.append(the_doors)

    return outcome


def revealing_goat(doors) -> int:
    """
    For great code simplicity, we are assuming that players always take
    door number 1.
    This way, we are searching for goats behind gates 2 and 3.
    """
    for idx in range(1,3):
        if doors[idx] == False:
            return idx
        

def simulating_random_choice(game: list) -> list:
    """
    The player changes the selected door after the host shows one door with
    a goat behind it.
    """
    n_wins: int = 0
    n_attempts: int = 0
    history = []

    for attempt in game:
        n_attempts += 1

        goat = revealing_goat(attempt)

        choice = randint(0, 1) # in case of truth, change chosen door
        final_choice = 0 if choice == 0 else 2 if goat == 1 else 1

        if attempt[final_choice] == True:
            n_wins += 1

        history.append(n_wins/n_attempts)

    return history


def simulating_keeping_choice(game: list) -> list:
    """
    The player always stays with his choice.
    """
    n_wins: int = 0
    n_attempts: int = 0
    history = []

    for attempt in game:
        n_attempts += 1

        if attempt[0] == True:
            n_wins += 1

        history.append(n_wins/n_attempts)

    return history


def simulating_switching_choice(game: list) -> list:
    """
    The player always changes his choice after revealing one door hiding a goat.
    """
    n_wins: int = 0
    n_attempts: int = 0
    history = []

    for attempt in game:
        n_attempts += 1

        goat = revealing_goat(attempt)
        final_choice = 1 if goat == 2 else 2

        if attempt[final_choice] == True:
            n_wins += 1

        history.append(n_wins/n_attempts)

    return history


def plotting_results(random: list, keep: list, switch: list, n_games: int):
    plt.figure(figsize=(12,8))

    plt.plot(random, 'g', label="Switching randomly")
    plt.plot(keep, 'b', label="Never changing")
    plt.plot(switch, 'r', label="Always switching")

    plt.legend(loc='upper right')
    plt.ylim(0, 1.0)
    plt.xlim(0, n_games)

    plt.ylabel("Ratio of won games", fontsize=16)
    plt.xlabel("Number of games", fontsize=16)

    plt.gca().yaxis.set_major_formatter(ticker.PercentFormatter(xmax=1.0)) 
    plt.grid(True)
    plt.show()


def simulating_games(n_games: int):
    """
    You could think that using multi-threading may improve performance, 
    but not with GIL. 
    So I tried to overcome this by using multi-processing,
    but it was the worst case for my architecture.
    """
    games = generating_outcome(n_games)

    random_history = simulating_random_choice(games)
    keeping_history = simulating_keeping_choice(games)
    switching_history = simulating_switching_choice(games)

    plotting_results(random=random_history,
                     keep=keeping_history,
                     switch=switching_history,
                     n_games=n_games)


if __name__ == "__main__":

    simulating_games(1000)
