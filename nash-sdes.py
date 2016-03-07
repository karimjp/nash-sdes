'''
Created on Feb 9, 2016

@author: karim
'''

"""player 1: 
[
 [(0,2), (3,1), (2,3)],
 [(1,4), (2,1), (4,1)],
 [(2,1), (4,4), (3,2)]
]"""

from operator import sub
import pdb

def transpose(game):
    #transposes the players_strategy_profile
    """https://docs.python.org/3/library/functions.html#zip"""
    return map(list, zip(*game))

def find_coordinate(value, game):
    for y,sublist in enumerate(game):
        try:
            x = sublist.index(value)
        except ValueError:
            continue
        return y,x

def find_strategies_index(value, game):
    """
       The function is used to get a dominated index for deletion, 
       but in the case of two or more similar strategies for a player 
       it does not affect the result of the nash equilibrium
       to delete the first found instance.
      """
    return game.index(value)
    
    
    
def append_original_coordinate(game):
    new_game = []
    #appends the original search index to the strategies for reference
    for sublist in game:
        new_sublist = []
        for strategy in sublist:
            coordinate = find_coordinate(strategy, game)
            strategy =  strategy + coordinate
            new_sublist.append(strategy)
        new_game.append(new_sublist)
    return new_game


def isDominated(compared_result, weak):
    """
    Checks that subtraction result of pivot minus comparison strategies values
    breaks with strictly dominant or weakly dominant rules.
    
    """
    #print compared_result
    if not weak: 
        #print "strongly dominated testing"
        for value in compared_result:
            if value <= 0:
                return False
    else:
        #checks for weak dominated value
        #print "weakly dominated testing"
        for value in compared_result:
            if value < 0:
                return False
    return True

def get_player_strategies_payoff(player, coordinate_game):
    """
    Returns the player payoffs matrix.
    Example:
    Input --
    [(0, 2, 0, 0), (3, 1, 0, 1), (2, 3, 0, 2)]
    [(1, 4, 1, 0), (2, 1, 1, 1), (4, 1, 1, 2)]
    [(2, 1, 1, 1), (4, 4, 2, 1), (3, 2, 2, 2)]
    Output --
    [[0, 3, 2], [1, 2, 4], [2, 4, 3]]
    """
    player_strategies_payoff = []
    for strategies in coordinate_game:
        payoff = []
        for payoff_structure in strategies:
            payoff.append(payoff_structure[player])
        player_strategies_payoff.append(payoff)
    return player_strategies_payoff
 
def get_dominated_strategy(player, coordinate_game, weak):
    player_game = get_player_strategies_payoff(player, coordinate_game)
    #select each strategy set to compare against other strategy sets and return the first dominated found
    for pivot_strategies in player_game:
        for comparison_strategies in player_game:
            print player_game
            #checks that pivot list is not being compared with itself
            if pivot_strategies is not comparison_strategies:
                print pivot_strategies, comparison_strategies
                compared_result = map(sub, pivot_strategies, comparison_strategies)
                print compared_result
                dominated = isDominated(compared_result, weak)
                if dominated:
                    return find_strategies_index(comparison_strategies, player_game)
    return None
 
def delete_dominated_strategy(coordinate_game, strategy_index):
    del coordinate_game[strategy_index]             
                
def get_strategy_indices(coordinate_game):
    y = coordinate_game[0][0][2]
    x = coordinate_game[0][0][3]
    return (y,x)

def switch_players(players):
    players= [1,0]
    
def solve_game( game, weak=False):
    iteration = 0
    players=[0,1]
    coordinate_game = append_original_coordinate(game)
    while True:
        for player in players:
            iteration = iteration + 1
            print coordinate_game
            dominated_strategy_index = get_dominated_strategy(player, coordinate_game, weak)
            print dominated_strategy_index
            if dominated_strategy_index is None:
                #checks if there is only one strategy left on the game
                if len(coordinate_game[0]) == 1:
                    return get_strategy_indices(coordinate_game)
                else:
                    #switch players
                    if iteration == 1:
                        coordinate_game = transpose(coordinate_game)
                        continue
                    else:
                        return None
            delete_dominated_strategy(coordinate_game, dominated_strategy_index)
            print coordinate_game
            coordinate_game = transpose(coordinate_game)
            print "#######"
    return value 
        
    

if __name__ == '__main__':
    weakly_dominant_game = [
                            [(1,1),(0,0)],
                            [(1,1),(2,1)],
                            [(0,0),(2,1)]
                            ]
    
    prisoners_dilemma = [[(5, 5), (10,0)],
                         [(0, 10), (7, 7)]]
    
    weakly_dominant_game1 = [
             [(0,2), (3,1), (2,3)],
             [(1,4), (2,1), (4,1)],
             [(2,1), (4,4), (3,2)]
             ]
    strongly_dominant_game2 = [
                              [(10,5),(10,10)],
                              [(20,10),(30,5)],
                              [(30,10),(5,5)]
                              ]
    weakly_dominant_game3 = [
                              [(5,2),(4,2)],
                              [(3,1),(3,2)],
                              [(2,1),(4,1)],
                              [(4,3),(5,4)]
                              ]
    strongly_dominant_game4 = [
                               [(100,80),(0,90)],
                               [(80,100),(80,90)]
                               ]
    print solve_game(strongly_dominant_game1, True)

