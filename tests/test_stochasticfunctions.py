from unittest import TestCase
import math

from tennistools import Tmatch
from tennistools.simulation import stochastic_simulation_match, stochastic_simulation_set, \
    stochastic_simulation_game, stochastical_simulation_next_point

#from tennistools.single_elimination_competition import calculate_bye_rounds, play_round, play_competition


class TestStochastic_Tennis_simulations_Points(TestCase):

    def test_play_point(self):
        """Single point with 100% likelihood gives answer as expected"""

        tmatch = Tmatch(True) # player 0 serves first
        stochastical_simulation_next_point(tmatch, lambda match, p1, p2: 1.0) #player 0 wins 100%
        tmatch.current_set.current_game.score_history[0]

        assert tmatch.current_set.current_game.get_current_score() == (1,0)
        assert tmatch.current_set.current_game.is_game_over() == False
        assert tmatch.current_set.current_game.score_history == [0]

    def test_play_point_stochastically(self):
        """Ensuring the match can play with a simple fixed probability of winning each point"""
        tmatch = Tmatch(True) # player 0 serves first
        stochastical_simulation_next_point(tmatch, lambda match, p1, p2: 0.5) #player 0 wins 50%
        tmatch.current_set.current_game.score_history[0]

        assert tmatch.current_set.current_game.get_current_score() in [(1,0), (0,1)]
        assert tmatch.current_set.current_game.is_game_over() == False
        assert tmatch.current_set.current_game.score_history in [[0],[1]]

    def test_play_point_stochastically_with_policy(self):
        """Ensuring the match can play with a simple policy function"""
        # e.g. this will not be deterministic, but we can check if it fails

        #Define a function that determines a probability of winning for player0
        def winscore(match, player0, player1):
            def sigmoid(x):
                return 1 / (1 + math.exp(-x))

            if match.current_set.current_game.is_player0_server:
                return sigmoid(player0['attack'] - player1['defence'])
            else:
                return 1 - sigmoid(player1['attack'] - player0['defence'])

        player0 = {'name':'player 0', 'attack':2.0, 'defence':1.6} #<--stronger player
        player1 = {'name':'player 1', 'attack':1.6, 'defence':1.6}

        tmatch = Tmatch(True) # player 0 serves first
        stochastical_simulation_next_point(tmatch, winscore, player0, player1)
        tmatch.current_set.current_game.score_history[0]

        assert tmatch.current_set.current_game.get_current_score() in [(1,0), (0,1)]
        assert tmatch.current_set.current_game.is_game_over() == False
        assert tmatch.current_set.current_game.score_history in [[0],[1]]

class TestStochastic_Tennis_simulations_Game(TestCase):

    def test_play_game(self):
        """Single game with 100% likelihood gives answer as expected"""

        tmatch = stochastic_simulation_game(lambda match, p1, p2: 1.0)  # player 0 wins 100%
        assert tmatch.current_set.game_history[-1].get_current_score() == (4,0)
        assert tmatch.current_set.game_history[-1].is_game_over() == True
        assert tmatch.current_set.game_history[-1].game_winner == 0

    def test_play_game_stochastically(self):
        """Ensuring the match can play with a simple fixed probability of winning each point"""
        tmatch = stochastic_simulation_game(lambda match, p1, p2: 0.5)  # player 0 wins 50%

        assert max(tmatch.current_set.game_history[-1].get_current_score()) >= 4
        assert tmatch.current_set.game_history[-1].is_game_over() == True
        assert tmatch.current_set.game_history[-1].game_winner in [0,1]

    def test_play_game_stochastically_with_policy(self):
        """Ensuring the match can play with a simple policy function"""

        # e.g. this will not be deterministic, but we can check if it fails

        # Define a function that determines a probability of winning for player0
        def winscore(match, player0, player1):
            def sigmoid(x):
                return 1 / (1 + math.exp(-x))

            if match.current_set.current_game.is_player0_server:
                return sigmoid(player0['attack'] - player1['defence'])
            else:
                return 1 - sigmoid(player1['attack'] - player0['defence'])

        player0 = {'name': 'player 0', 'attack': 2.0, 'defence': 1.6}  # <--stronger player
        player1 = {'name': 'player 1', 'attack': 1.6, 'defence': 1.6}

        tmatch = stochastic_simulation_game(winscore, player0, player1)

        assert max(tmatch.current_set.game_history[-1].get_current_score()) >= 4
        assert tmatch.current_set.game_history[-1].is_game_over() == True
        assert tmatch.current_set.game_history[-1].game_winner in [0, 1]

class TestStochastic_Tennis_simulations_Set(TestCase):

    def test_play_set(self):
        """Single game with 100% likelihood gives answer as expected"""

        tmatch = stochastic_simulation_set(lambda match, p1, p2: 1.0)  # player 0 wins 100%
        assert tmatch.set_history[-1].get_current_score() == (6, 0)
        assert tmatch.set_history[-1].is_set_over() == True
        assert tmatch.set_history[-1].set_winner == 0

    def test_play_set_stochastically(self):
        """Ensuring the match can play with a simple fixed probability of winning each point"""
        tmatch = stochastic_simulation_set(lambda match, p1, p2: 0.5)  # player 0 wins 50%
        assert max(tmatch.set_history[-1].get_current_score()) in [6,7]
        assert tmatch.set_history[-1].is_set_over() == True
        assert tmatch.set_history[-1].set_winner in [0,1]

    def test_play_set_stochastically_with_policy(self):
        """Ensuring the match can play with a simple policy function"""

        # Define a function that determines a probability of winning for player0
        def winscore(match, player0, player1):
            def sigmoid(x):
                return 1 / (1 + math.exp(-x))

            if match.current_set.current_game.is_player0_server:
                return sigmoid(player0['attack'] - player1['defence'])
            else:
                return 1 - sigmoid(player1['attack'] - player0['defence'])

        player0 = {'name': 'player 0', 'attack': 2.0, 'defence': 1.6}  # <--stronger player
        player1 = {'name': 'player 1', 'attack': 1.6, 'defence': 1.6}

        tmatch = stochastic_simulation_set(winscore, player0, player1)  # player 0 wins 50%
        assert max(tmatch.set_history[-1].get_current_score()) in [6,7]
        assert tmatch.set_history[-1].is_set_over() == True
        assert tmatch.set_history[-1].set_winner in [0,1]

class TestStochastic_Tennis_simulations_Match(TestCase):

    def test_play_match(self):
        """Single game with 100% likelihood gives answer as expected"""

        tmatch = stochastic_simulation_match(lambda match, p1, p2: 1.0)  # player 0 wins 100%
        assert tmatch.get_match_score() == (3, 0)
        assert tmatch.is_match_over() == True
        assert tmatch.match_winner == 0

    def test_play_match_stochastically(self):
        """Ensuring the match can play with a simple fixed probability of winning each point"""
        tmatch = stochastic_simulation_match(lambda match, p1, p2: 0.5)  # player 0 wins 100%
        assert max(tmatch.get_match_score()) == 3
        assert tmatch.is_match_over() == True
        assert tmatch.match_winner in [0,1]

    def test_play_match_stochastically_with_policy(self):
        """Ensuring the match can play with a simple policy function"""

        # Define a function that determines a probability of winning for player0
        def winscore(match, player0, player1):
            def sigmoid(x):
                return 1 / (1 + math.exp(-x))

            if match.current_set.current_game.is_player0_server:
                return sigmoid(player0['attack'] - player1['defence'])
            else:
                return 1 - sigmoid(player1['attack'] - player0['defence'])

        player0 = {'name': 'player 0', 'attack': 2.0, 'defence': 1.6}  # <--stronger player
        player1 = {'name': 'player 1', 'attack': 1.6, 'defence': 1.6}

        tmatch = stochastic_simulation_set(winscore, player0, player1)  # player 0 wins 50%
        assert max(tmatch.set_history[-1].get_current_score()) in [6,7]
        assert tmatch.set_history[-1].is_set_over() == True
        assert tmatch.set_history[-1].set_winner in [0,1]
    #
    # def test_play_set_randomly(self):
    #     """Ensuring the match can play with a simple fixed probability of winning each point"""
    #     # e.g. this will not be deterministic, but we can check if it fails
    #
    #     tmatch = stochastic_simulation_set(lambda match, p1, p2: 0.5)
    #     results.append(tmatch.set_history[0].set_winner)
    #
    #     assert tmatch.is_match_over()
    #     assert tmatch.match_winner is not None
    #     assert tmatch.match_winner in [0,1]
    #     assert len(tmatch.set_history) in range(3,6)
    #
    #
    # def test_play_set_randomly2(self):
    #     """Ensuring the match can play with a simple fixed probability of winning each point"""
    #     #define a function for determing the win probability for player 1
    #     def winscore(match, player0, player1):
    #         def sigmoid(x):
    #             return 1 / (1 + math.exp(-x))
    #
    #         if match.current_set.current_game.is_player0_server:
    #             return sigmoid(player0['attack'] - player1['defence'])
    #         else:
    #             return 1 - sigmoid(player1['attack'] - player0['defence'])
    #
    #     player0 = {'name':'player 0', 'attack':2.0, 'defence':1.6}
    #     player1 = {'name':'player 1', 'attack':2.0, 'defence':1.6}
    #
    #     # e.g. this will not be deterministic, but we can check if it fails
    #     results = []
    #     for _ in range(1000):
    #         tmatch = stochastic_simulation_set(winscore, player0, player1)
    #         results.append(tmatch.set_history[0].set_winner)
    #     print(Counter(results))
    #     assert tmatch.is_match_over()
    #     assert tmatch.match_winner is not None
    #     assert tmatch.match_winner in [0,1]
    #     assert len(tmatch.set_history) in range(3,6)
    #
    # def test_play_match_randomly(self):
    #     """Ensuring the match can play with a simple fixed probability of winning each point"""
    #     # e.g. this will not be deterministic, but we can check if it fails
    #     results = []
    #     for _ in range(1000):
    #         tmatch = stochastic_simulation_match(lambda match, p1, p2: 0.5)
    #         results.append(tmatch.match_winner)
    #     print(Counter(results))
    #     print(tmatch)
    #     assert tmatch.is_match_over()
    #     assert tmatch.match_winner is not None
    #     assert tmatch.match_winner in [0,1]
    #     assert len(tmatch.set_history) in range(3,6)
    #
    # def test_play_match_randomly_with_policy(self):
    #     """Ensuring the match can play with a more complex conditional probability"""
    #     #define a function for determing the win probability for player 1
    #     def winscore(match, player0, player1):
    #         def sigmoid(x):
    #             return 1 / (1 + math.exp(-x))
    #
    #         if match.current_set.current_game.is_player0_server:
    #             return sigmoid(player0['attack'] - player1['defence'])
    #         else:
    #             return 1 - sigmoid(player1['attack'] - player0['defence'])
    #
    #     player0 = {'name':'player 0', 'attack':2.0, 'defence':1.6}
    #     player1 = {'name':'player 1', 'attack':2.0, 'defence':1.6}
    #
    #     results=[]
    #     for _ in range(1000):
    #         tmatch = stochastic_simulation_match(winscore, player0, player1)
    #         results.append(tmatch.match_winner)
    #     print(Counter(results))
    #     #tmatch = play_match_randomly(winscore, player0=player0, player1=player1)
    #     #print(tmatch)
    #     assert tmatch.is_match_over()
    #     assert tmatch.match_winner is not None
    #     assert tmatch.match_winner in [0,1]
    #     assert len(tmatch.set_history) in range(3,6)
    #
    # def test_add_byes_to_playerlist(self):
    #     #Ensure that the correct number of byes are added
    #     playerlist = [{'name':'player1'},{'name':'player2'},{'name':'player3'}]
    #     adjustedplayerlist = calculate_bye_rounds(playerlist)
    #     assert len(adjustedplayerlist) == 4
    #     assert len([player['name'] for player in adjustedplayerlist if player['name'] is None]) == 1
    #
    # def test_add_byes_to_playerlist2(self):
    #     # Ensure that the correct number of byes are added
    #     playerlist = [{'name':'player1'},{'name':'player2'},{'name':'player3'}, {'name':'player4'} ]
    #     adjustedplayerlist = calculate_bye_rounds(playerlist)
    #     print(adjustedplayerlist)
    #     assert len(adjustedplayerlist) == 4
    #     assert len([player['name'] for player in adjustedplayerlist if player['name'] is None]) == 0
    #
    # def test_play_single_round(self):
    #     # Test that single round of tennis competition can be played correctly
    #     playerlist = [{'name': 'player1'}, {'name': None}, {'name': 'player3'}, {'name': 'player4'}]
    #     nextround_playerlist, _ = play_round(playerlist, lambda match, p1, p2: 0.5)
    #     print(nextround_playerlist)
    #     assert len(nextround_playerlist) == len(playerlist)/2
    #
    #
    # def test_play_competition(self):
    #     #Test a full game of tennis is played
    #     playerlist = [{'name': 'player1'}, {'name': 'player2'}, {'name': 'player3'}, {'name': 'player4'}]
    #     winner, match_history = play_competition(playerlist, lambda match, p1, p2: 1.0)
    #     assert winner == {'name': 'player1'}
    #     assert len(match_history) == 2 #e.g. Two rounds of tennis played
    #     assert len(match_history[0])==2 #e.g. 2 match played in round 0 (semi finals)
    #     assert len(match_history[1])==1 #e.g. 1 match played in round 1(finals)
