from tennistools.single_elimination_competition import simulate_competition
import math
from tqdm import tqdm
from collections import Counter

# Example code to simulate a single-elimination tennis competition


# probabiltiy model based solely on the player strengths and who is serving
def probability_model1(match, player0, player1):
    def sigmoid(x):
        return 1 / (1 + math.exp(-x))

    if match.current_set.current_game.is_player0_server:
        return sigmoid(player0['attack'] - player1['defence'])
    else:
        return 1 - sigmoid(player1['attack'] - player0['defence'])

# List of players - players are indentified as a dictonary - but this is solely based on how I defined my probability model
playerlist = [
    {'name': 'player 0', 'attack': 2.0, 'defence': 1.6}, #<--stronger player
    {'name': 'player 1', 'attack': 2.0, 'defence': 1.6}, #<--stronger player
    {'name': 'player 2', 'attack': 1.6, 'defence': 1.4},
    {'name': 'player 3', 'attack': 1.6, 'defence': 1.4},
    {'name': 'player 4', 'attack': 1.6, 'defence': 1.4},
    {'name': 'player 5', 'attack': 1.6, 'defence': 1.4},
    {'name': 'player 6', 'attack': 1.6, 'defence': 1.4},
    {'name': 'player 7', 'attack': 2.0, 'defence': 1.6},#<--stronger player
    #{'name': 'player 8', 'attack': 1.6, 'defence': 1.4},
    # {'name': 'player 9', 'attack': 1.6, 'defence': 1.4},
    # {'name': 'player 10', 'attack': 1.6, 'defence': 1.4},
    # {'name': 'player 11', 'attack': 1.6, 'defence': 1.4},
    # {'name': 'player 12', 'attack': 1.6, 'defence': 1.4},
    # {'name': 'player 13', 'attack': 1.6, 'defence': 1.4},
    # {'name': 'player 14', 'attack': 1.6, 'defence': 1.4},
    # {'name': 'player 15', 'attack': 1.6, 'defence': 1.4},
    # {'name': 'player 16', 'attack': 1.6, 'defence': 1.4},
    # {'name': 'player 17', 'attack': 1.6, 'defence': 1.4},
    # {'name': 'player 18', 'attack': 1.6, 'defence': 1.4},
    # {'name': 'player 19', 'attack': 1.6, 'defence': 1.4},
    # {'name': 'player 20', 'attack': 1.6, 'defence': 1.4},
    # {'name': 'player 21', 'attack': 1.6, 'defence': 1.4},
    # {'name': 'player 22', 'attack': 1.6, 'defence': 1.4},
    # {'name': 'player 23', 'attack': 1.6, 'defence': 1.4},
    # {'name': 'player 24', 'attack': 1.6, 'defence': 1.4},
    # {'name': 'player 25', 'attack': 1.6, 'defence': 1.4},
    # {'name': 'player 26', 'attack': 2.0, 'defence': 1.6}, #<--stronger player
    # {'name': 'player 27', 'attack': 1.6, 'defence': 1.4},
    # {'name': 'player 28', 'attack': 1.6, 'defence': 1.4},
    # {'name': 'player 29', 'attack': 1.6, 'defence': 1.4},
    # {'name': 'player 30', 'attack': 1.6, 'defence': 1.4},
    # {'name': 'player 31', 'attack': 1.6, 'defence': 1.4},
    # {'name': 'player 32', 'attack': 1.6, 'defence': 1.4},
    # {'name': 'player 33', 'attack': 1.6, 'defence': 1.4},
    # {'name': 'player 34', 'attack': 1.6, 'defence': 1.4},
    # {'name': 'player 35', 'attack': 1.6, 'defence': 1.4},
    # {'name': 'player 36', 'attack': 1.6, 'defence': 1.4},
    # {'name': 'player 37', 'attack': 1.6, 'defence': 1.4},
    # {'name': 'player 38', 'attack': 1.6, 'defence': 1.4},
    # {'name': 'player 39', 'attack': 1.6, 'defence': 1.4},
    # {'name': 'player 40', 'attack': 1.6, 'defence': 1.4},
    # {'name': 'player 41', 'attack': 1.6, 'defence': 1.4},
    # {'name': 'player 42', 'attack': 1.6, 'defence': 1.4},
    # {'name': 'player 43', 'attack': 1.6, 'defence': 1.4},
    # {'name': 'player 44', 'attack': 1.6, 'defence': 1.4},
    # {'name': 'player 45', 'attack': 1.6, 'defence': 1.4},
    # {'name': 'player 46', 'attack': 1.6, 'defence': 1.4},
    # {'name': 'player 47', 'attack': 1.6, 'defence': 1.4},
    # {'name': 'player 48', 'attack': 1.6, 'defence': 1.4},
    # {'name': 'player 49', 'attack': 1.6, 'defence': 1.4},
    # {'name': 'player 50', 'attack': 1.6, 'defence': 1.4},
    # {'name': 'player 51', 'attack': 1.6, 'defence': 1.4},
    # {'name': 'player 52', 'attack': 1.6, 'defence': 1.4},
    # {'name': 'player 53', 'attack': 1.6, 'defence': 1.4},
    # {'name': 'player 54', 'attack': 1.6, 'defence': 1.4},
    # {'name': 'player 55', 'attack': 1.6, 'defence': 1.4},
    # {'name': 'player 56', 'attack': 1.6, 'defence': 1.4},
    # {'name': 'player 57', 'attack': 1.6, 'defence': 1.4},
    # {'name': 'player 58', 'attack': 1.6, 'defence': 1.4},
    # {'name': 'player 59', 'attack': 1.6, 'defence': 1.4},
    # {'name': 'player 60', 'attack': 2.0, 'defence': 1.6}, #<--stronger player
    # {'name': 'player 61', 'attack': 1.6, 'defence': 1.4},
    # {'name': 'player 62', 'attack': 1.6, 'defence': 1.4},
    # {'name': 'player 63', 'attack': 1.6, 'defence': 1.4},
]

# Simulating running competitoion once and looking at games history:
winner, match_histories = simulate_competition(playerlist, probability_model1)

print('Results of a single simulation')
for round_number, round in match_histories.items():
    print('\n',f'Round {round_number}')
    for match_number, matchobject in round.items():
        player0 = matchobject['player0']
        player1 = matchobject['player1']
        print(f'Match {match_number}***************************')
        print(f'{player0["name"]} \t\t:'+','.join([str(set.get_current_score()[0]) for set in matchobject['match'].set_history]))
        print(f'{player1["name"]}\t\t:' + ','.join([str(set.get_current_score()[1]) for set in matchobject['match'].set_history]))
print(f'Competition Winner:{winner["name"]}')


# Simulating running competition 1000 time
winners = []
for _ in tqdm(range(1000)):
    winner, match_histories = simulate_competition(playerlist, probability_model1)
    winners.append(winner['name'])
print('Frequency of winners in 1000 simulations')
print(Counter(winners))