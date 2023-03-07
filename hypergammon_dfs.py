from itertools import combinations_with_replacement
from random import shuffle
import csv
from decimal import Decimal, getcontext
from sys import setrecursionlimit

setrecursionlimit(pow(10,6))

getcontext().prec = 8

def state_after_move(white, black, ftm, move, final_move):
    if ftm == 1:
        player_pawns = white
        opp_pawns = black
    else:
        player_pawns = black
        opp_pawns = white
    if opp_pawns.count(move[1]) <= 1:
        _player_pawns = list(player_pawns)
        _opp_pawns = list(opp_pawns)
        _player_pawns.remove(move[0])
        if move[1] >= 1 and move[1] <= 24:
            _player_pawns.append(move[1])
        if opp_pawns.count(move[1]) == 1:
            _opp_pawns.remove(move[1])
            if ftm == 1:
                _opp_pawns.append(25)
            else:
                _opp_pawns.append(0)
        _player_pawns.sort()
        _opp_pawns.sort()
        if ftm == 1:
            return (tuple(_player_pawns), tuple(_opp_pawns), ftm*pow(-1,int(final_move)))
        else: return (tuple(_opp_pawns), tuple(_player_pawns), ftm*pow(-1,int(final_move)))
    else:
        if final_move:
            if ftm == 1: return (player_pawns, opp_pawns, ftm*pow(-1,int(final_move)))
            else: return (opp_pawns, player_pawns, ftm*pow(-1,int(final_move)))

def next_temp_states(states, dice, final_move):
    _next_temp_states = set()
    for state in states:
        white, black, ftm = state
        if ftm == 1:
            if len(white) > 0:
                for w in set(white):
                    _next_temp_states.add(state_after_move(white, black, ftm, (w, w+dice), final_move))
            else:
                return states
        else:
            if len(black) > 0:
                for b in set(black):
                    _next_temp_states.add(state_after_move(white, black, ftm, (b, b-dice), final_move))
            else:
                return states
    try: _next_temp_states.remove(None)
    except: pass
    return _next_temp_states

def next_states(state, roll):
    _next_states = set()
    curr_temp_states = {state}
    if roll[0] != roll[1]:
        for i in range(2):
            curr_temp_states = next_temp_states(curr_temp_states, roll[i], i == 1)
        for cts in curr_temp_states:
            _next_states.add(cts)
        curr_temp_states = {state}
        for i in range(2):
            curr_temp_states = next_temp_states(curr_temp_states, roll[1-i], i == 1)
        for cts in curr_temp_states:
            _next_states.add(cts)
    else:
        curr_temp_states = {state}
        for i in range(4):
            curr_temp_states = next_temp_states(curr_temp_states, roll[0], i == 3)
        for cts in curr_temp_states:
            _next_states.add(cts)
    if len(_next_states) == 0:
        return {state[:2] + (state[2]*(-1),)}
    return _next_states

rolls = [(i,j) for i in range(1, 7) for j in range(i, 7)]
print(rolls)

states_to_check = set()

ind = 0
posses_white = set([i for i in range(25)])
posses_black = set([i for i in range(1, 26)])
for r_white in range(3, 4):
    for comb_white in combinations_with_replacement(posses_white, r_white):
        print(ind, comb_white)
        _comb_white = set(comb_white)
        for r_black in range(3, 4):
            for comb_black in combinations_with_replacement(posses_black.difference(_comb_white), r_black):
                if (0 not in comb_white and 25 not in comb_black and min(comb_white) > max(comb_black)):
                    states_to_check.add((comb_white, comb_black, 1))
                    states_to_check.add((comb_white, comb_black, -1))
                    ind += 2

states = {}

with open('D://hypergammon//hyper_32_23.csv', 'r', newline='') as csvfile:
    _reader = csv.reader(csvfile, delimiter=';')
    for row in _reader:
        states[eval(row[0])] = float(row[1])


def dfs(state):
    if state not in states:
        em = 0
        for i in range(len(rolls)):
            roll = rolls[i]
            if roll[0] == roll[1]:
                prob = 1/36
            else:
                prob = 2/36
            _next_states = next_states(state, rolls[i])
            if state[2] == 1:
                em += max(map(lambda x: dfs(x), next_states(state, roll)))*prob
            else:
                em += min(map(lambda x: dfs(x), next_states(state, roll)))*prob
        states[state] = em
    return states[state]

ind = 0
for sc in states_to_check:
    print(ind, sc, len(states_to_check), len(states))
    dfs(sc)
    ind += 1

with open('D://hypergammon//hyper_33a.csv', 'w', newline='') as csvfile:
    _writer = csv.writer(csvfile, delimiter=';')
    for state in states:
        _writer.writerow([state, states[state]])