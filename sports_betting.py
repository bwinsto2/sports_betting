#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Dec  3 17:49:38 2022

@author: bwinston
"""
import random

def payout(odds, wager, free=False):
    if odds>0:
       yo = odds/100      
    else:
        yo = 100/-odds
    payout = yo*wager
    if free==False:
        return payout+wager
    else:
        return payout  

def hedge_calc(odds1, wager1, odds2, wager2):
    wagers = wager1 + wager2
    profit1 = payout(odds1, wager1) - wagers
    #print(f'If team 1 wins, you profit ${profit1}')
    hole = payout(odds2, wager2) - wagers
    #print(f'If team 2 wins, you lose ${-hole} and get a {wager1} free bet')
    return profit1, hole
    

def free_bet_hedge(odds1, free_bet_size, odds2, wager2):
    win1 = payout(odds1, free_bet_size, True) - wager2
    #print(f'If team 1 wins, you make ${win1}')
    win2 = payout(odds2, wager2) - wager2
    #print(f'If team 2 wins, you make ${win2}')
    return win1, win2

#wager2a and wager 1a should be the same
def two_step_hedge(odds1a, wager1a, odds1b, wager1b, odds2a, wager2a, odds2b, wager2b,print_output=False):
    profit1, hole = hedge_calc(odds1a, wager1a, odds1b, wager1b)
    #print(f'In step 1, if team 1 wins, you profit {profit1}')
    #print(f'In step 1, if team 2 wins, you lose {hole} and get {wager1a} in free bets')
    win1, win2 = free_bet_hedge(odds2a, wager2a, odds2b, wager2b)
    #print(f'In step 2, if team 1 wins, you profit overall {win1+hole}')
    #print(f'In step 2, if team 2 wins, you profit overall {win2+hole}')
    if print_output:
        print(f'Team 1 wins: ${profit1}; Team 2 then 1: ${win1+hole}; Team 2 then 2: ${win2+hole}')
    else:
        return profit1, win1+hole, win2+hole
    
def optimize_tsh(odds1a, wager1a, odds1b, wager1b, odds2a, wager2a, odds2b, wager2b):
    #free parameters: wager1b, wager2b
    solution_found = False
    iterations = 0
    spread = 5*wager1a
    while solution_found == False:
        wager1b_temp = wager1b + random.randint(-spread,spread)
        wager2b_temp = wager1b + random.randint(-spread,spread)
        scen1, scen2, scen3 = two_step_hedge(odds1a, wager1a, odds1b, wager1b_temp, odds2a, wager2a, odds2b, wager2b_temp)
        x = abs(scen1 - scen2)
        y = abs(scen1 - scen3)
        if (x+y) < 5:
            solution_found=True
            two_step_hedge(odds1a, wager1a, odds1b, wager1b_temp, odds2a, wager2a, odds2b, wager2b_temp, print_output=True)
            print(f'took {iterations} iterations')
            return wager1b_temp,wager2b_temp
        else:
            wager1b_temp = wager1b
            wager2b_temp = wager2b
            iterations = iterations + 1

def opt_tsh_userinput():
    wager1a = int(input('How much are you wagering? To maximize profits, pick the amount of the RF bet: '))
    print('Pick two games. The result of the first should be known before the second starts')
    odds1a = int(input('Game 1: odds that Team 1A wins: '))
    odds1b = int(input('Game 1: odds that Team 1B wins: '))
    odds2a = int(input('Game 2: odds that Team 2A wins: '))
    odds2b = int(input('Game 2: odds that Team 2B wins: '))
    w1b, w2b = optimize_tsh(odds1a, wager1a, odds1b, 2*wager1a, odds2a, wager1a, odds2b, 2*wager1a)
    print(f'In Game 1, Bet {wager1a} on Team 1A and hedge {w1b} on Team 1B. If Team 1B wins, move to Game 2. Use your {wager1a} free bet on Team 2A and hedge {w2b} on Team 2B')
    
    
