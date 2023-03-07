from random import randint
from itertools import combinations_with_replacement, combinations, product
from collections import defaultdict

scores_cats = [50, 26, 25, 20, 20, 20, 20, 6, 5, 4, 3, 2, 1]

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
        _scores['thirteen'] = 1
        if set(cts.values()) == {1,2}:
            if 2 in cts.values():
                _scores['crag'] = 1
    if len(cts) == 1: _scores['three-of-a-kind'] = 1
    if dices == (1,2,3): _scores['low straight'] = 1
    if dices == (4,5,6): _scores['high straight'] = 1
    if dices == (1,3,5): _scores['odd straight'] = 1
    if dices == (2,4,6): _scores['even straight'] = 1
    for i in range(1, 7):
        if i in cts:
            _scores[str(i)] = cts[i]
    return _scores

def state_parents(state):
    ct1, ct2 = 0, 0
    for i in range(13):
        if state[i] is not None: ct1 += 1
    for i in range(13, 26):
        if state[i] is not None: ct2 += 1
    if ct1 - ct2 > 1:
        first_move = False
    else:
        first_move = True
    non_nones = []
    if first_move:
        for i in range(13):
            if state[i] is not None: non_nones.append(i)
    else:
        for i in range(13, 26):
            if state[i] is not None: non_nones.append(i)
    _state_parents = set()
    if state[-1] == 1:
        _new_state = list(state)
        _new_state[26] = 0
        _new_state[27] = 0
        _new_state[28] = 0
        _new_state[29] = 0
        _state_parents.add(tuple(_new_state))
    else:
        if state[13] == 0:
            for nn in non_nones:
                for comb in combinations_with_replacement([j for j in range(1, 7)], 3):
                    _new_state = list(state)
                    _new_state[nn] = 0
                    _new_state[26] = comb[0]
                    _new_state[27] = comb[1]
                    _new_state[28] = comb[2]
                    _new_state[29] = 0
                    _state_parents.add(tuple(_new_state))
        else:
            for comb in combinations_with_replacement([j for j in range(1, 7)], 3):
                _new_state = list(state)
                _new_state[26] = comb[0]
                _new_state[27] = comb[1]
                _new_state[28] = comb[2]
                _new_state[29] = 1
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
        multiplier = 1
        cts = defaultdict(int)
        for el in comb: cts[el] += 1
        for el in cts: multiplier *= cts[el]
        _comb = tuple(list(sorted(saved_dices + comb)))
        next_state = state[:26] + _comb + (state[-1] ^ 1,)
        next_state_ev = memo[next_state][0]
        ev += next_state_ev*multiplier
        ct += multiplier
    return ev/ct

def first_to_move(state):
    ct1, ct2 = 0, 0
    for i in range(13):
        if state[i] is not None: ct1 += 1
    for i in range(13, 26):
        if state[i] is not None: ct2 += 1
    if ct1 - ct2 > 0:
        return False
    else:
        return True

def choose_action(state):
    if state[-1] == 0 and state[26] != 0:
        curr_scores = scores(state[26:29])
        action = None
        ftm = first_to_move(state)
        if ftm:
            minimax_value = -1
        else:
            minimax_value = 1
        for cat in categories:
            if state[categories[cat] + 13*(int(ftm)^1)] is None:
                _new_state = list(state)
                _new_state[categories[cat] + 13*(int(ftm)^1)] = curr_scores[cat]
                _new_state[26] = 0
                _new_state[27] = 0
                _new_state[28] = 0
                _new_state[29] = 0
                temp_value = memo[tuple(_new_state)][0]
                if ftm:
                    if temp_value > minimax_value:
                        minimax_value = temp_value
                        action = categories[cat] + 13*(int(ftm)^1)
                else:
                    if temp_value < minimax_value:
                        minimax_value = temp_value
                        action = categories[cat] + 13*(int(ftm)^1)
    elif state[-1] == 0 and state[26] == 0:
        action = None
        ev = 0
        ct = 0
        for comb in combinations_with_replacement([i for i in range(1, 7)], 3):
            multiplier = 1
            cts = defaultdict(int)
            for el in comb: cts[el] += 1
            for el in cts: multiplier *= cts[el]
            next_state = state[:26] + comb + (state[-1] ^ 1,)
            next_state_ev = memo[next_state][0]
            ev += next_state_ev * multiplier
            ct += multiplier
        minimax_value = ev/ct
    else:
        dices = state[26:29]
        saved_dices_set = set()
        action = None
        ftm = first_to_move(state)
        if ftm:
            minimax_value = -1
        else:
            minimax_value = 1
        for r in range(0, 4):
            for comb in combinations(dices, r):
                saved_dices_set.add(comb)
        for sd in saved_dices_set:
            temp_value = expected_value(state, sd)
            if ftm:
                if temp_value > minimax_value:
                    minimax_value = temp_value
                    action = sd
            else:
                if temp_value < minimax_value:
                    minimax_value = temp_value
                    action = sd
    return (minimax_value, action)

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


curr_states = set()

prods_upper = []
prods_lower = []

for prod in product([0,1], repeat=7):
    prods_upper.append(prod)
for prod in product([0,1,2], repeat=6):
    prods_lower.append(prod)

full_prods = []
for pu in prods_upper:
    for pl in prods_lower:
        p = pu + pl
        score = 0
        for i in range(len(p)):
            score += p[i]*scores_cats[i]
        full_prods.append([p, score])

ind = 0
for p1 in full_prods:
    if ind % 1000 == 0: print(ind)
    for p2 in full_prods:
        curr_states.add(p1[0] + p2[0] + (0, 0, 0, 0))
        if p1[1] > p2[1]:
            memo[p1[0] + p2[0] + (0,0,0,0)] = (1, None)
        elif p1[1] == p2[1]:
            memo[p1[0] + p2[0] + (0,0,0,0)] = (0, None)
        else:
            memo[p1[0] + p2[0] + (0,0,0,0)] = (-1, None)
    ind += 1

print('hehe', len(memo))
depth = 0
while len(curr_states) > 0:
    curr_states = backward(curr_states, depth)
    print(len(curr_states), len(memo))
    depth += 1

print(memo[(0,)*17])

import sqlite3

main_base = sqlite3.connect('D://crag.db')
main_base.execute('create table crag_two_results (t_upper1 INTEGER NOT NULL, t_lower1 INTEGER NOT NULL, '
                  't_upper2 INTEGER NOT NULL, t_lower2 INTEGER NOT NULL, '
                  'd1 INTEGER NOT NULL, d2 INTEGER NOT NULL, d3 INTEGER NOT NULL, '
                  'remained INTEGER NOT NULL, ev REAL NOT NULL, action1 INTEGER, action2 INTEGER, action3 INTEGER, '
                  'PRIMARY KEY (t_upper1, t_lower1, t_upper2, t_lower2, d1, d2, d3, remained))')

main_base.commit()
ind = 0
for el in memo:
    tp = ()
    _t = 0
    for i in range(7):
        _t += pow(3,i)*el[i]
    tp += (_t,)
    _t = 0
    for i in range(7, 13):
        _t += pow(2,i)*el[i]
    tp += (_t,)
    _t = 0
    for i in range(13, 20):
        _t += pow(3,i) * el[i]
    tp += (_t,)
    _t = 0
    for i in range(20, 27):
        _t += pow(2,i) * el[i]
    tp += (_t,)

    tp += (_t, el[-4:])
    action = memo[el][1]
    if action is not None:
        if type(action,) is int:
            tp += (action,)
        else:
            for a in action:
                tp += (a,)
    tp += ('NULL',)*(12-len(tp))
    main_base.execute('insert into crag_two_results values ' + str(tp))
    if ind % 1000 == 0: print(ind, len(memo))
    ind += 1
main_base.commit()