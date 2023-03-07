from itertools import combinations_with_replacement, combinations, product
from collections import defaultdict
import sqlite3
from math import factorial

main_base = sqlite3.connect('D://crag.db')
# main_base.execute('create table crag_two_players (p0 INTEGER, p1 INTEGER, p2 INTEGER, p3 INTEGER, p4 INTEGER,'
#                   'p5 INTEGER, p6 INTEGER, p7 INTEGER, p8 INTEGER, p9 INTEGER, p10 INTEGER, p11 INTEGER, p12 INTEGER, '
#                   'q0 INTEGER, q1 INTEGER, q2 INTEGER, q3 INTEGER, q4 INTEGER,'
#                   'q5 INTEGER, q6 INTEGER, q7 INTEGER, q8 INTEGER, q9 INTEGER, q10 INTEGER, q11 INTEGER, q12 INTEGER, '
#                   'd1 INTEGER NOT NULL, d2 INTEGER NOT NULL, d3 INTEGER NOT NULL, '
#                   'remained INTEGER NOT NULL, value REAL NOT NULL, action1 INTEGER, action2 INTEGER, action3 INTEGER, '
#                   'PRIMARY KEY (p0, p1, p2, p3, p4, p5, p6, p7, p8, p9, p10, p11, p12, '
#                   'q0, q1, q2, q3, q4, q5, q6, q7, q8, q9, q10, q11, q12, d1, d2, d3, remained))')
#
# main_base.commit()

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
main_base.execute('delete from crag_two_players')
main_base.commit()

def add_node(state, value, action):
    memo[state] = (value,) + action
    if len(memo) > 5*pow(10,6):
        for _state in memo:
            main_base.execute('insert into crag_two_players values ' + str(_state + (value,) + action))
        memo.clear()
        main_base.commit()

def get_node(state):
    if state in memo:
        return memo[state]
    else:
        result = main_base.execute('select value, action1, action2, action3 from crag_two_players where ' 
                                   '(p0, p1, p2, p3, p4, p5, p6, p7, p8, p9, p10, p11, p12, '
                                   'q0, q1, q2, q3, q4, q5, q6, q7, q8, q9, q10, q11, q12) = ' + str(state[:26])).fetchone()
        return result

def dfs(curr_state, ftm, depth):
    if depth <= 64: print(depth, len(memo))
    state = curr_state[0]
    res = get_node(state)
    if res is not None:
        return res[0]
    maxes = curr_state[1]
    if maxes[0] > maxes[1] + maxes[3]:
        add_node(state, 1, ('NULL', 'NULL', 'NULL'))
        return 1
    if maxes[1] > maxes[0] + maxes[2]:
        add_node(state, -1, ('NULL', 'NULL', 'NULL'))
        return -1
    if maxes[2] == 0 and maxes[3] == 0:
        if maxes[0] > maxes[1]:
            add_node(state, 1, ('NULL', 'NULL', 'NULL'))
            return 1
        elif maxes[0] == maxes[1]:
            add_node(state, 0, ('NULL', 'NULL', 'NULL'))
            return 0
        else:
            add_node(state, -1, ('NULL', 'NULL', 'NULL'))
            return -1

    if ftm: minimax = -1.1
    else: minimax = 1.1

    if state[-1] == 0 and state[26] != 0:
        curr_scores = scores(state[26:29])
        action = None
        for cat in categories:
            if state[categories[cat] + 13 * (int(ftm) ^ 1)] == 'NULL':
                _new_state = list(state)
                _new_state[categories[cat] + 13 * (int(ftm) ^ 1)] = curr_scores[cat]
                _new_state[26] = 0
                _new_state[27] = 0
                _new_state[28] = 0
                _new_state[29] = 0
                _maxes = maxes.copy()
                if ftm:
                    _maxes[0] += curr_scores[cat]
                    _maxes[2] -= scores_maxes[categories[cat]]
                else:
                    _maxes[1] += curr_scores[cat]
                    _maxes[3] -= scores_maxes[categories[cat]]
                _next_state = (tuple(_new_state), _maxes)
                temp_value = dfs(_next_state, not ftm, depth+1)
                if ftm:
                    if temp_value > minimax:
                        minimax = temp_value
                        action = (categories[cat] + 13 * (int(ftm) ^ 1),) + ('NULL',)*2
                else:
                    if temp_value < minimax:
                        minimax = temp_value
                        action = (categories[cat] + 13 * (int(ftm) ^ 1),) + ('NULL',)*2
    elif state[-1] == 0 and state[26] == 0:
        ev = 0
        ct = 0
        for comb in combinations_with_replacement([i for i in range(1, 7)], 3):
            multiplier = 6
            cts = defaultdict(int)
            for el in comb: cts[el] += 1
            for el in cts: multiplier //= factorial(cts[el])
            _next_state = state[:26] + comb + (state[-1] ^ 1,)
            _next_state = (tuple(_next_state), maxes.copy())
            new_state_ev = dfs(_next_state, ftm, depth+1)
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
                _next_state = (tuple(new_state), maxes.copy())
                new_state_ev = dfs(_next_state, ftm, depth+1)
                ev += new_state_ev * multiplier
                ct += multiplier
            temp_value = ev/ct
            if ftm:
                if temp_value > minimax:
                    minimax = temp_value
                    action = sd + ('NULL',)*(3-len(sd))
            else:
                if temp_value < minimax:
                    minimax = temp_value
                    action = sd + ('NULL',)*(3-len(sd))

    add_node(state, minimax, action)
    return minimax

curr_state = (('NULL',)*26 + (0,0,0,0), [0,0,244,244])
print(dfs(curr_state, True, 0))

for _state in memo:
    value, action = memo[_state]
    main_base.execute('insert into crag_two_players values (' + '?,' * 26 + ') = ' + str(_state + (value,) + action))
memo.clear()
main_base.commit()