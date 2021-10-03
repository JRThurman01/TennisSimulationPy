from unittest import TestCase
import math

from tennistools import Tmatch
from tennistools.simulation import stochastic_simulation_match, stochastic_simulation_set, \
    stochastic_simulation_game, stochastical_simulation_next_point

from tennistools.single_elimination_competition import calculate_bye_rounds, simulate_competition_round, simulate_competition

class TestCompetitionFunctions(TestCase):

    def test_add_byes_to_playerlist(self):
        #Ensure that the correct number of byes are added
        playerlist = [{'name':'player1'},{'name':'player2'},{'name':'player3'}]
        adjustedplayerlist = calculate_bye_rounds(playerlist)
        assert len(adjustedplayerlist) == 4
        assert len([player['name'] for player in adjustedplayerlist if player['name'] is None]) == 1

    def test_add_byes_to_playerlist2(self):
        # Ensure that the correct number of byes are added
        playerlist = [{'name':'player1'},{'name':'player2'},{'name':'player3'}, {'name':'player4'} ]
        adjustedplayerlist = calculate_bye_rounds(playerlist)
        print(adjustedplayerlist)
        assert len(adjustedplayerlist) == 4
        assert len([player['name'] for player in adjustedplayerlist if player['name'] is None]) == 0

    def test_play_single_round(self):
        # Test that single round of tennis competition can be played correctly
        playerlist = [{'name': 'player1'}, {'name': None}, {'name': 'player3'}, {'name': 'player4'}]
        nextround_playerlist, _ = simulate_competition_round(playerlist, lambda match, p1, p2: 0.5)
        print(nextround_playerlist)
        assert len(nextround_playerlist) == len(playerlist)/2


    def test_play_competition(self):
        #Test a full game of tennis is played
        playerlist = [{'name': 'player1'}, {'name': 'player2'}, {'name': 'player3'}, {'name': 'player4'}]
        winner, match_history = simulate_competition(playerlist, lambda match, p1, p2: 1.0)
        assert winner == {'name': 'player1'}
        assert len(match_history) == 2 #e.g. Two rounds of tennis played
        assert len(match_history[0])==2 #e.g. 2 match played in round 0 (semi finals)
        assert len(match_history[1])==1 #e.g. 1 match played in round 1(finals)
