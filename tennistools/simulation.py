#########################################################################################################
### Random play functions
### These functions can be used to stochastically simulate a tennis match where a
### function provides the probabilities of winning based on some kw args.
#########################################################################################################

import numpy as np
from tennistools import Tmatch


def stochastical_simulation_next_point(tmatch, player0_win_probability_function, player0=None, player1=None, **kwargs):
     """Stochastically play point where a function of point win probabilities is known"""
     player0_win_probability = player0_win_probability_function(tmatch, player0, player1, **kwargs)
     tmatch.play_point(np.random.uniform() < player0_win_probability)

def stochastic_simulation_game(player0_win_probability_function, player0=None, player1=None, **kwargs):
    """Create and randomly play a tennis match"""
    #random assign first server
    tmatch = Tmatch(np.random.uniform() < 0.5)
    while len(tmatch.current_set.game_history) == 0:
        stochastical_simulation_next_point(tmatch, player0_win_probability_function, player0, player1, **kwargs)
    return tmatch

def stochastic_simulation_set(player0_win_probability_function, player0=None, player1=None, **kwargs):
    """Create and randomly play a tennis match"""
    #random assign first server
    tmatch = Tmatch(is_player0_server=(np.random.uniform() < 0.5))
    while len(tmatch.set_history) == 0:
        stochastical_simulation_next_point(tmatch, player0_win_probability_function, player0, player1, **kwargs)
    return tmatch

def stochastic_simulation_match(player0_win_probability_function, player0=None, player1=None, **kwargs):
    """Create and randomly play a tennis match"""
    #random assign first server
    tmatch = Tmatch(is_player0_server=np.random.binomial(1,0.5)==0)

    while not tmatch.is_match_over():
        stochastical_simulation_next_point(tmatch, player0_win_probability_function, player0, player1, **kwargs)
    return tmatch

