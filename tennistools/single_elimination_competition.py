from tennistools.simulation import stochastic_simulation_match
import math
from itertools import chain, zip_longest


def calculate_bye_rounds(playerlist):
    """This returns a list of players with additional Null players.

    Single elimination rounds need to have 2,4,8,16...etc players to work correctly. This allocates Null players that
    act as byes to some matches. The way these are allocated are based on the top n players in the playlist
    """
    # Need to find out how many rounds to complete:
    count_players_allocated = len(playerlist)
    rounds_needed = math.ceil(math.log2(count_players_allocated))
    byes_required = int(math.pow(2,rounds_needed) - count_players_allocated)
    return [x for x in chain.from_iterable(zip_longest(playerlist, byes_required*[{'name':None}])) if x is not None]


def simulate_competition_round(playerlist, player0_win_probability_function, previous_match_history = None, **kwargs):
    """
    Simulates a single round of a competition. Returns a list of winners and adds additional match instances to
     dictionary file that maintains history of the games.

    :param playerlist: list of player objects
    :param player0_win_probability_function: A function that takes Tmatch, Player, Player as arguments and returns a probabilty
    :param previous_match_history: A dictionary of dictionary of matches
    :param kwargs: Any other features that are used in the player0_win_probabiltiy_function
    """
    if previous_match_history is None:
        previous_match_history = {}

    round_matches = {}
    round_winners = []
    for game_number, (player0, player1) in enumerate(zip(playerlist[::2],playerlist[1::2])):
        if player1['name'] is None: #Dealing with any byes by awarding the win
            round_winners.append(player0)
        else:
            tmatch = stochastic_simulation_match(player0_win_probability_function, player0=player0, player1=player1, **kwargs)
            round_winners.append([player0, player1][tmatch.match_winner])
            round_matches[game_number] = {'player0':player0, 'player1':player1, 'match':tmatch}

    previous_match_history[len(previous_match_history)] = round_matches
    return round_winners, previous_match_history

def simulate_competition(playerlist, player0_win_probability_function, **kwargs):
    """
    Simulates a full single elimination round of tennis. Iteratively calls play_round until there is only
    1 player (the winner) remaining.

    :param playerlist: A list of dictionary objects that represent a player.
    :param player0_win_probability_function: A function that takes TMatch, player0, player1 as inputs and returns
    a probability
    :param kwargs:
    :return:
    """
    previous_match_history = {}
    playerlist = calculate_bye_rounds(playerlist)
    while len(playerlist) > 1:
        playerlist, previous_match_history = simulate_competition_round(playerlist, player0_win_probability_function,
                                                                        previous_match_history, **kwargs)

    return playerlist[0], previous_match_history