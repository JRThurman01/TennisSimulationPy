# TennisSimulationPy
#### John Thurman

### Overview
A package to stochastically simulate tennis single-elimination competitions. Provides a basis to complete simulations to determine the likelihood of certain events occuring in a competition. e.g. Person A winning, Number of games played over competition, number of points played, Person A and Person C making it to the final.

### Assumptions and limitiations:
* 3 SETS required for a match win
* If a set is 6 games all, A tiebreaker, with slightly different rules is played to decide the set.
* Lets, service faults, replays and some other features of tennis are not captured within the model
* A single elimination competition is being played

### How to use
The tennis_simulation_example.py provides two examples of how the package can be used:
1. A single simulation is created and the scores of each set are shown
2. The same competition is simulated 1000 times, and the count of the number of wins for each player is calculated. Provides an estimate of the probability of the player winning the competition

The structure of the module is:
* competitions - high level functions to simulate a single elimination competition.
* stochastic functions - Simulates the playing of points, games, sets and matches where a black box model can b
* class library of game, (tiebreaker game), set and match.

### Win Probabilities function
An important and subjective part of the model is the likelihood of a player winning a single point given the context of the game. This function is required to be provided by the user. In the examples, a function to calculate these is given based on the:
* Who's serve it is
* The strengths of the players as a server, receiver

The modelling allows flexibility in the choice of probability functions that can be used for predictions of the likelihood of the point winner. It can be extended to include additional features, e.g.:
* Player representation - which could include labelled features (e.g. fitness, first serve %, second serve percentage), or a representation developed though statistical means
* Current game features - e.g. Current set score, Current game score, is_it_break_point, is_it_match_point, who is serving, momentum, match length
* Weather - e.g. Very hot, raining, clay/ grass
* Court type - Clay, Hard, Grass
