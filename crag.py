from random import randint
from itertools import combinations_with_replacement, combinations
from collections import defaultdict
from math import factorial

def roll(n):
    _roll = []
    for _ in range(n):
        _roll.append(randint(1, 6))

categories = {}
categories['crag'] = 0
categories['thirteen'] = 1
categories['three-of-a-kind'] = 2
categories['low straight'] = 3
categories['high straight'] = 4
categories['odd straight'] = 5
categories['even straight'] = 6
categories['6'] = 7
categories['5'] = 8
categories['4'] = 9
categories['3'] = 10
categories['2'] = 11
categories['1'] = 12

def scores(dices):
    _scores = defaultdict(int)
    cts = defaultdict(int)
    for d in dices:
        cts[d] += 1
    if sum(dices) == 13:
        _scores['thirteen'] = 26
        if set(cts.values()) == {1,2}:
            if 2 in cts.values():
                _scores['crag'] = 50
    if len(cts) == 1: _scores['three-of-a-kind'] = 25
    if dices == (1,2,3): _scores['low straight'] = 20
    if dices == (4,5,6): _scores['high straight'] = 20
    if dices == (1,3,5): _scores['odd straight'] = 20
    if dices == (2,4,6): _scores['even straight'] = 20
    for i in range(1, 7):
        if i in cts:
            _scores[str(i)] = i*cts[i]
    return _scores

def state_parents(state):
    ones = []
    for i in range(13):
        if state[i] == 1: ones.append(i)
    _state_parents = set()
    if state[-1] == 1:
        _new_state = list(state)
        _new_state[13] = 0
        _new_state[14] = 0
        _new_state[15] = 0
        _new_state[16] = 0
        _state_parents.add(tuple(_new_state))
    else:
        if state[13] == 0:
            for i in ones:
                for comb in combinations_with_replacement([j for j in range(1, 7)], 3):
                    _new_state = list(state)
                    _new_state[i] = 0
                    _new_state[13] = comb[0]
                    _new_state[14] = comb[1]
                    _new_state[15] = comb[2]
                    _new_state[16] = 0
                    _state_parents.add(tuple(_new_state))
        else:
            for comb in combinations_with_replacement([j for j in range(1, 7)], 3):
                _new_state = list(state)
                _new_state[13] = comb[0]
                _new_state[14] = comb[1]
                _new_state[15] = comb[2]
                _new_state[16] = 1
                _state_parents.add(tuple(_new_state))
    return _state_parents


#state: (0,1)*13 + (3 dices, sorted) + rolls remained, if no dices: (0,0,0) 3 dices + (0,) - rolls remained
memo = {}

#state after action (if applicable)
def expected_value(state, saved_dices):
    n = 3 - len(saved_dices)
    ev = 0
    ct = 0
    for comb in combinations_with_replacement([i for i in range(1, 7)], n):
        multiplier = 6
        cts = defaultdict(int)
        for el in comb: cts[el] += 1
        for el in cts: multiplier //= factorial(cts[el])
        _comb = tuple(list(sorted(saved_dices + comb)))
        next_state = state[:13] + _comb + (state[-1] ^ 1,)
        next_state_ev = memo[next_state][0]
        ev += next_state_ev*multiplier
        ct += multiplier
    return ev/ct

def choose_action(state):
    if state[-1] == 0 and state[13] != 0:
        curr_scores = scores(state[13:16])
        action = None
        max_value = -1
        for cat in categories:
            if state[categories[cat]] == 0:
                _new_state = list(state)
                _new_state[categories[cat]] = 1
                _new_state[13] = 0
                _new_state[14] = 0
                _new_state[15] = 0
                _new_state[16] = 0
                temp_value = curr_scores[cat] + memo[tuple(_new_state)][0]
                if temp_value > max_value:
                    max_value = temp_value
                    action = categories[cat]
    elif state[-1] == 0 and state[13] == 0:
        action = None
        ev = 0
        ct = 0
        for comb in combinations_with_replacement([i for i in range(1, 7)], 3):
            multiplier = 1
            cts = defaultdict(int)
            for el in comb: cts[el] += 1
            for el in cts: multiplier *= cts[el]
            next_state = state[:13] + comb + (state[-1] ^ 1,)
            next_state_ev = memo[next_state][0]
            ev += next_state_ev * multiplier
            ct += multiplier
        max_value = ev/ct
    else:
        dices = state[13:16]
        saved_dices_set = set()
        action = None
        max_value = 0
        for r in range(0, 4):
            for comb in combinations(dices, r):
                saved_dices_set.add(comb)
        for sd in saved_dices_set:
            temp_value = expected_value(state, sd)
            if temp_value > max_value:
                max_value = temp_value
                action = sd
    return (max_value, action)

def backward(curr_states, depth):
    backed_states = set()
    ind = 0
    for cs in curr_states:
        if ind % 1000 == 0: print(ind, depth)
        backed_states = backed_states.union(state_parents(cs))
        ind += 1
    for bs in backed_states:
        memo[bs] = choose_action(bs)
        if depth >= 36: print(bs, memo[bs])
    return backed_states

curr_states = {(1,)*13 + (0,0,0,0)}
memo[(1,)*13 + (0,0,0,0)] = (0, None)

depth = 0
while len(curr_states) > 0:
    curr_states = backward(curr_states, depth)
    print(len(curr_states), len(memo))
    depth += 1

print(memo[(0,)*17])

import sqlite3

main_base = sqlite3.connect('D://crag.db')
main_base.execute('create table crag_single_results (t INTEGER NOT NULL, '
                  'd1 INTEGER NOT NULL, d2 INTEGER NOT NULL, d3 INTEGER NOT NULL, remained INTEGER NOT NULL, ev REAL NOT NULL, '
                  'action1 INTEGER, action2 INTEGER, action3 INTEGER, PRIMARY KEY (t, d1, d2, d3, remained))')

main_base.commit()
ind = 0
for el in memo:
    _t = 0
    for i in range(13):
        _t += pow(2,i)*el[i]
    tp = (_t, el[13], el[14], el[15], el[16], memo[el][0])
    action = memo[el][1]
    if action is not None:
        if type(action,) is int:
            tp += (action,)
        else:
            for a in action:
                tp += (a,)
    tp += ('NULL',)*(9-len(tp))
    main_base.execute('insert into crag_single_results values ' + str(tp))
    if ind % 1000 == 0: print(ind, len(memo))
    ind += 1
main_base.commit()