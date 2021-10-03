import numpy as np
SETS_REQUIRED = 3

GAMES_REQUIRED = 6 #In addition to win by 2
POINTS_REQUIRED = 4 #In addition to win by 2
POINTS_TIEBREAK_REQUIRED = 7 #In addition to win by 2


class Tgame(object):
    """
    A class to represent a game of tennis

    Attributes
    ---------
    score_history: ordered list of points in the game so far
    game_winner: returns whether player 0 or player 1 won (once game is complete)
    is_player0_server: Is the first player listed serving. Needed to determine which player won the game

    Methods
    ---------
    is_game_over: determines if game is complete
    get_current_score: returns score as tuple of points won by server, receiver
    _str_from_score(score): (private) method to convert score representation to human readable score
    play_point(is_player0_winner): Adds additional point to score_history
    __str__: string representation of the score_history

    """

    def __init__(self, is_player0_server):#=True):
        self.score_history = []
        self.game_winner = None
        self.is_player0_server = is_player0_server

    def is_game_over(self):
        score = self.get_current_score()
        maxscore = max(score)
        minscore = min(score)
        return (maxscore >=POINTS_REQUIRED) & (maxscore > minscore + 1)

    def get_current_score(self):
        """returns tuple of server points won, receiver points won"""
        player0_score = sum([point==0 for point in self.score_history])
        player1_score = sum([point==1 for point in self.score_history])
        return (player0_score, player1_score)

    def _str_from_score(self, score):
        """Returns (semi)traditional score wording (e.g. 'Advantage player 0' from tuple of server, receiver points won
        Always returns score from player0 perspective and not neccesary traditional return from server status
        """

        score_mapper = {(0, 0): 'love - all', (1, 0): '15 - love', (2, 0): '30 - love', (3, 0): '40 - love',
                             (4, 0): 'game player 0',
                             (0, 1): 'love - 15', (1, 1): '15 - all', (2, 1): '30 - 15', (3, 1): '40 - 15',
                             (4, 1): 'game player 0',
                             (0, 2): 'love - 30', (1, 2): '15 - 30', (2, 2): '30 - all', (3, 2): '40 - 30',
                             (4, 2): 'game player 0',
                             (0, 3): 'love - 40', (1, 3): '15 - 40', (2, 3): '30 - 40', (3, 3): 'deuce',
                             (0, 4): 'game player 1', (1, 4): 'game player 1', (2, 4): 'game player 1'}

        (player0_score, player1_score) = score
        points_played = player0_score + player1_score

        if points_played <= 6:
            return score_mapper[(player0_score, player1_score)]
        elif player0_score == player1_score:
            return 'deuce'
        elif player0_score == player1_score + 1:
            return 'advantage player 0'
        elif player0_score == player1_score + 2:
            return 'game player 0'
        elif player0_score == player1_score - 1:
            return 'advantage player 1'
        elif player0_score == player1_score -2:
            return 'game player 1'
        else:
            raise ValueError(f'{score} is not a possible score')

    def play_point(self, is_player0_point_winner):
        """Gives either the server or the receiver an additional point"""
        self.score_history.append(int(not is_player0_point_winner))
        if self.is_game_over():
            self.finalise_game()

    def finalise_game(self):
        """sets the game_winner attribute so that set scores and match scores can be calculated more quickly"""
        player0_points, player1_points = self.get_current_score()
        if player0_points > player1_points:
            self.game_winner = 0
        else:
            self.game_winner = 1

    def __str__(self):
        """string reprentation"""
        running_scores = [(0,0)]
        score_history_str = []
        for point in self.score_history:
            old_score = running_scores[-1]
            new_score = (old_score[0] + int(point==0), old_score[1] + int(point==1))
            running_scores.append(new_score)
            score_history_str.append(self._str_from_score(new_score))

        return str(score_history_str)


class Ttiebreak(Tgame):
    """
    A class to represent a tiebeaker game of tennis

    Attributes
    ---------
    score_history: ordered list of points in the game so far
    game_winner: returns whether player 0 or player 1 won (once game is complete)
    is_player0_server: Is the first player listed serving. Needed to determine which player won the game

    Methods
    ---------
    is_game_over: determines if game is complete
    get_current_score: returns score as tuple of points won by server, receiver
    _str_from_score(score): returns human readable scores
    play_point(is_player0_winner): Adds additional point to score_history
    __str__: string representation of the score_history

    """
    def _str_from_score(self, score):
        """Tiebreaker scores same as the actual points scored"""
        return score

    def is_game_over(self):
        """Check to see if either player has won the tiebreaker"""
        score = self.get_current_score()
        maxscore = max(score)
        minscore = min(score)
        return (maxscore >= POINTS_TIEBREAK_REQUIRED) & (maxscore > minscore + 1)

    def play_point(self, is_player0_point_winner):
        """Gives either the server or the receiver an additional point, depending on winner"""
        self.score_history.append(int(is_player0_point_winner))
        if len(self.score_history) % 2 == 1:
            self.is_player0_server = not self.is_player0_server
        if self.is_game_over():
            self.finalise_game()


class Tset(object):
    """"
    A class to represent a set of tennis

    Attributes
    ---------
    game_history: ordered list of games of tennis completed so far in set
    set_winner: returns who won the set, once complete.
    is_player0_server: Is the first player listed serving at the start of the current game

    Methods
    ---------
    is_set_over: determines if srt is complete
    get_current_score: returns score as tuple of games won by server, receiver
    play_point(is_player0_winner): Adds additional point to score_history
    finalise_current_game: sets current game game_winner property and sets current_game to a new game/tiebreaker
    finalise_set: sets winner of the set to the person with the most points. To be called after is_set_over is True
    __str__: string representation of the score_history

    """

    def __init__(self,is_player0_server):
        self.game_history = []
        self.current_game = Tgame(is_player0_server)
        self.set_winner = None
        self.is_player0_server = is_player0_server

    def get_current_score(self):
        winners = [game.game_winner for game in self.game_history]
        player0_sets = sum([winner==0 for winner in winners])
        player1_sets = len(winners) - player0_sets
        return (player0_sets, player1_sets)

    def is_set_over(self):
        player_0_games, player_1_games = self.get_current_score()
        maxgames = max(player_0_games, player_1_games)
        mingames = min(player_0_games, player_1_games)
        return (maxgames == GAMES_REQUIRED) & (maxgames>= mingames+2) | maxgames == (GAMES_REQUIRED +1) #won during a tiebreaker

    def finalise_current_game(self):
        """On game finish, append game to game history and set up the next game"""
        self.game_history.append(self.current_game)
        if self.get_current_score() == (GAMES_REQUIRED,GAMES_REQUIRED):
            # in the event of tiebreak the person who received in the previous set serves.
            self.is_player0_server = not self.is_player0_server
            self.current_game = Ttiebreak(self.is_player0_server)
        else:
            self.is_player0_server = not self.is_player0_server
            self.current_game = Tgame(self.is_player0_server)

    def finalise_set(self):
        player_0_games, player_1_games = self.get_current_score()
        if player_0_games > player_1_games:
            self.set_winner = 0
        else:
            self.set_winner = 1

    def play_point(self, is_player0_point_winner):
        self.current_game.play_point(is_player0_point_winner)
        if self.current_game.is_game_over():
            self.finalise_current_game()
        if self.is_set_over():
            self.finalise_set()

    def __str__(self):
        return f'Result:{str(self.set_winner)}\n Setscore:{self.get_current_score()}\n\n'+'\n'.join([str(s) for s in self.game_history])

class Tmatch(object):
    """
    A class to represent a match of tennis

    Attributes
    ---------
    set_history: ordered list of sets of tennis completed so far in set
    current_set: The current set being played
    match_winner: returns who won the set, once complete.
    is_player0_server: Is the first player listed serving at the start of the current set

    Methods
    ---------
    is_match_over: determines if match is complete
    get_match_score: returns score as tuple of sets won by server, receiver
    play_point(is_player0_winner): Adds additional point to score_history of current game in current set
    finalise_current_set: sets current set set_winner property and sets current_set to a new set
    finalise_match: sets winner of the match to the person with the most sets. To be called after is_match_over is True
    __str__: string representation of the score_history
    """
    def __init__(self, is_player0_server=True):
        self.set_history=[]
        self.current_set = Tset(is_player0_server)
        self.match_winner = None
        self.is_player0_server = is_player0_server

    def is_match_over(self):
        (player0score, player1score) = self.get_match_score()
        return max(player0score, player1score)== SETS_REQUIRED

    def get_match_score(self):
        winners = [tset.set_winner for tset in self.set_history]
        player0_wins = sum([win==0 for win in winners])
        player1_wins = len(winners) - player0_wins
        return (player0_wins, player1_wins)

    def finalise_current_set(self):
        self.set_history.append(self.current_set)
        self.is_player0_server = self.current_set.is_player0_server
        self.current_set = Tset(self.is_player0_server)

    def finalise_match(self):
        player0_sets, player1_sets = self.get_match_score()
        if player0_sets > player1_sets:
            self.match_winner = 0
        else:
            self.match_winner = 1

    def play_point(self, is_player1_point_winner):
        self.current_set.play_point(is_player1_point_winner)
        if self.current_set.is_set_over():
            self.finalise_current_set()
        if self.is_match_over():
            self.finalise_match()

    def __str__(self):
        return f'Winner: {self.match_winner}\nScore:{self.get_match_score()}\n\n' + '\n'.join([str(tset) for tset in self.set_history])


