from itertools import combinations_with_replacement, combinations, product
from collections import defaultdict
import sqlite3
from math import factorial

main_base = sqlite3.connect('D://crag4.db')
main_base.execute('create table crag_dfs (p0 INTEGER, p1 INTEGER, q0 INTEGER, q1 INTEGER, ftm INTEGER, value REAL NOT NULL,'
                  'PRIMARY KEY (p0, p1, q0, q1, ftm))')

main_base.commit()

scores_cats = [50, 26, 25, 20, 20, 20, 20, 6, 5, 4, 3, 2, 1]
scores_maxes = [50, 26, 25, 20, 20, 20, 20, 18, 15, 12, 9, 6, 3]

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

memo = {}

def tp_to_num2(tp):
    _num = 0
    for i in range(len(tp)):
        if tp[i] != 'NULL':
            _num += pow(3, tp[i]+1)
    return _num

def tp_to_num3(tp):
    _num = 0
    for i in range(len(tp)):
        if tp[i] != 'NULL':
            _num += pow(4, tp[i]+1)
    return _num

def add_node(state, value, action):
    memo[state] = (value,) + action
    if len(memo) > pow(10,7):
        for _state in memo:
            main_base.execute('insert into crag_two_players values ' + str(_state + (value,) + action))
        memo.clear()
        main_base.commit()

def get_node(state):
    if state in memo:
        return memo[state]
    else:
        result = main_base.execute('select value from crag_two_players where '
                                   'p0 = ' + str(state[0]) + ' and p1 = ' + str(state[1]) + ' and q0 = ' + str(state[2])
                                   + ' and q1 = ' + str(state[3]) + ' and d1 = ' + str(state[4]) + ' and d2 = ' + str(state[5])
                                   + ' and d3 = ' + str(state[6]) + ' and remained = ' + str(state[7])).fetchone()
        return result

def dfs(curr_state, ftm, depth):
    visited[0] += 1
    if visited[0] % 100000 == 0:
        print(visited, depth, len(memo))
        print(curr_state)
    state = curr_state[0]
    nA1 = tp_to_num2(state[:7])
    nA2 = tp_to_num3(state[7:13])
    nB1 = tp_to_num2(state[13:20])
    nB2 = tp_to_num3(state[20:26])
    conversed_state = (nA1, nA2, nB1, nB2) + state[26:]
    res = get_node(conversed_state)
    if res is not None:
        return res[0]
    maxes = curr_state[1]
    if maxes[0] > maxes[1] + maxes[3]:
        add_node(conversed_state, 1, ('NULL', 'NULL', 'NULL'))
        visited[1] += 1
        return 1
    if maxes[1] > maxes[0] + maxes[2]:
        add_node(conversed_state, -1, ('NULL', 'NULL', 'NULL'))
        visited[1] += 1
        return -1
    if maxes[2] == 0 and maxes[3] == 0:
        if maxes[0] > maxes[1]:
            #add_node(state, 1, ('NULL', 'NULL', 'NULL'))
            return 1
        elif maxes[0] == maxes[1]:
            #add_node(state, 0, ('NULL', 'NULL', 'NULL'))
            return 0
        else:
            #add_node(state, -1, ('NULL', 'NULL', 'NULL'))
            return -1

    if ftm:
        minimax = -1.1
    else:
        minimax = 1.1

    if state[-1] == 0 and state[26] != 0:
        curr_scores = scores(state[26:29])
        action = None
        temp_next_states = []
        for cat in categories:
            if state[categories[cat] + 13 * (int(ftm) ^ 1)] == 'NULL':
                _new_state = list(state)
                _new_state[categories[cat] + 13 * (int(ftm) ^ 1)] = curr_scores[cat]
                _new_state[26] = 0
                _new_state[27] = 0
                _new_state[28] = 0
                _new_state[29] = 0
                _maxes = list(maxes)
                if ftm:
                    _maxes[0] += curr_scores[cat]*scores_cats[categories[cat]]
                    _maxes[2] -= scores_maxes[categories[cat]]
                else:
                    _maxes[1] += curr_scores[cat]*scores_cats[categories[cat]]
                    _maxes[3] -= scores_maxes[categories[cat]]
                _next_state = (tuple(_new_state), tuple(_maxes))
                res = get_node(_next_state[0])
                if res is None:
                    temp_next_states.append((_next_state, cat))
                else:
                    if ftm and res == 1:
                        minimax = 1
                        action = (categories[cat] + 13 * (int(ftm) ^ 1),) + ('NULL',) * 2
                    elif not ftm and res == -1:
                        minimax = -1
                        action = (categories[cat] + 13 * (int(ftm) ^ 1),) + ('NULL',) * 2
                    else:
                        temp_next_states.append((_next_state, cat))

        if action is None:
            for _next_state, cat in temp_next_states:
                temp_value = dfs(_next_state, not ftm, depth + 1)
                if ftm:
                    if temp_value > minimax:
                        minimax = temp_value
                        action = (categories[cat] + 13 * (int(ftm) ^ 1),) + ('NULL',) * 2
                else:
                    if temp_value < minimax:
                        minimax = temp_value
                        action = (categories[cat] + 13 * (int(ftm) ^ 1),) + ('NULL',) * 2
        else:
            visited[2] += 1

    elif state[-1] == 0 and state[26] == 0:
        ev = 0
        ct = 0
        for comb in combinations_with_replacement([i for i in range(1, 7)], 3):
            multiplier = 6
            cts = defaultdict(int)
            for el in comb: cts[el] += 1
            for el in cts: multiplier //= factorial(cts[el])
            _next_state = state[:26] + comb + (state[-1] ^ 1,)
            _next_state = (tuple(_next_state), maxes)
            new_state_ev = dfs(_next_state, ftm, depth + 1)
            ev += new_state_ev * multiplier
            ct += multiplier
        minimax = ev / ct
        action = ('NULL', 'NULL', 'NULL')

    else:
        dices = state[26:29]
        saved_dices_set = set()
        action = None
        for r in range(0, 4):
            for comb in combinations(dices, r):
                saved_dices_set.add(comb)
        for sd in saved_dices_set:
            n = 3 - len(sd)
            ev = 0
            ct = 0
            for comb in combinations_with_replacement([i for i in range(1, 7)], n):
                multiplier = 1
                cts = defaultdict(int)
                for el in comb: cts[el] += 1
                for el in cts: multiplier *= cts[el]
                _comb = tuple(list(sorted(sd + comb)))
                new_state = state[:26] + _comb + (state[-1] ^ 1,)
                _next_state = (tuple(new_state), maxes)
                new_state_ev = dfs(_next_state, ftm, depth + 1)
                ev += new_state_ev * multiplier
                ct += multiplier
            temp_value = ev / ct
            if ftm:
                if temp_value > minimax:
                    minimax = temp_value
                    action = sd + ('NULL',) * (3 - len(sd))
            else:
                if temp_value < minimax:
                    minimax = temp_value
                    action = sd + ('NULL',) * (3 - len(sd))

    add_node(conversed_state, minimax, action)
    return minimax

visited = [0, 0, 0]
curr_state = (('NULL',)*26 + (0,0,0,0), (0,0,244,244))
print(dfs(curr_state, True, 0))

for _state in memo:
    value, action = memo[_state]
    main_base.execute('insert into crag_two_players values ' + str(_state + (value,) + action))
memo.clear()
main_base.commit()