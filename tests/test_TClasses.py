from unittest import TestCase
from tennistools import Tgame, Tset, Tmatch


class TestTGame(TestCase):

    def test___init__(self):
        """Does it initialise"""
        Tgame(True)
        assert True

    def test_get_current_score1(self):
        """scores as expected 1"""
        game = Tgame(True)
        assert game.get_current_score() == (0,0)

    def test_get_current_score2(self):
        """scores as expected 2"""
        game = Tgame(True)
        for player0_won_point in [True, True, False, True, False, False, True, False, False, False]:
            game.play_point(player0_won_point)
        assert game.get_current_score() == (4,6)

    def test___str__(self):
        """correct traditional representation"""
        game = Tgame(True)
        for player0_won_point in [True, True, False, True, False, False, True, False, False, False]:
            game.play_point(player0_won_point)
        print(str(game))
        print(game.get_current_score())
        assert str(game) == "['15 - love', '30 - love', '30 - 15', '40 - 15', '40 - 30', 'deuce', 'advantage player 0', 'deuce', 'advantage player 1', 'game player 1']"

    def test_is_game_over(self):
        """Expected game over"""
        game = Tgame(True)
        for player0_won_point in [True, True, False, True, False, False, True, False]:
            game.play_point(player0_won_point)
        assert game.is_game_over() is False
        for player0_won_point in [False, False]:
            game.play_point(player0_won_point)
        assert game.is_game_over() is True

    def test_finalise_game(self):
        ###assets on game over, game_winner is set
        game = Tgame(True)
        for is_server_winner in [True, True, False, True, False, False, True, False]:
            game.play_point(is_server_winner)
        assert game.game_winner is None
        for is_server_winner in [False, False]:
            game.play_point(is_server_winner)
        assert game.game_winner == 1


    def test_changing_server_logic1(self):
        """Depending on whether player 0 is servering, and whether the server won - returns player that did win"""
        game = Tgame(True)
        for player0_won_point in [True, True, True, True]:
            game.play_point(player0_won_point)
        print(game)
        print(game.get_current_score())
        assert game.game_winner == 0


    def test_changing_server_logic2(self):
        """Depending on whether player 0 is servering, and whether the server won - returns player that did win"""
        game = Tgame(False)
        for player0_won_point in [True, True, True, True]:
            game.play_point(player0_won_point)

        assert game.game_winner == 0


    def test_changing_server_logic3(self):
        """Depending on whether player 0 is servering, and whether the server won - returns player that did win"""
        game = Tgame(True)
        for player0_won_point in [False, False, False, False]:
            game.play_point(player0_won_point)

        assert game.game_winner == 1


    def test_changing_server_logic4(self):
        """Depending on whether player 0 is servering, and whether the server won - returns player that did win"""
        game = Tgame(False)
        for player0_won_point in [False, False, False, False]:
            game.play_point(player0_won_point)

        assert game.game_winner == 1

class TestTset(TestCase):

    def test___init__(self):
        """Does it initialise"""
        Tset(True)
        assert True

    def test_get_current_score1(self):
        """ Correct score"""
        tset = Tset(True)
        assert tset.get_current_score() ==(0,0)
        assert True
        #self.fail()

    def test_get_current_score2(self):
        """ Correct score"""
        tset = Tset(True)
        for _ in range(4*6):
            tset.play_point(True)
        assert tset.get_current_score() == (6,0)
        assert (tset.set_winner == 0)

    def test_get_current_score3(self):
        """ Correct score when not expected game to have finished"""
        tset = Tset(True)
        for player0win in [True, False, True, False, True, False]:
            for _ in range(4):
                tset.play_point(is_player0_point_winner = player0win)
        print(tset.get_current_score())
        assert tset.get_current_score() == (3,3)
        assert(tset.set_winner is None)

class TestMatch(TestCase):

    def test___init__(self):
        """Does initialise"""
        Tmatch()
        assert True

    def test_get_current_score1(self):
        """Check score"""
        tmatch = Tmatch()
        assert tmatch.get_match_score() == (0,0)
        assert True
        #self.fail()

    def test_get_current_score2(self):
        """Check score"""
        tmatch = Tmatch()
        for _ in range(3):
            for player0_win in [True, True, True, True, True, True]:
                for _ in range(4):
                    tmatch.play_point(player0_win)

        print(tmatch.get_match_score())
        print(tmatch.match_winner)

        assert tmatch.get_match_score()==(3,0)
        assert tmatch.match_winner == 0

