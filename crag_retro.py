from itertools import combinations_with_replacement, combinations, product
from collections import defaultdict
import sqlite3
from math import factorial

main_base = sqlite3.connect('D://crag3.db')
# main_base.execute('create table crag_retro (p0 INTEGER, p1 INTEGER, q0 INTEGER, q1 INTEGER, '
#                   'ftm INTEGER, value REAL, PRIMARY KEY (p0, p1, q0, q1, ftm))')
#
# main_base.commit()

main_base.execute('delete from crag_retro')
main_base.commit()
scores_cats = [50, 26, 25, 20, 20, 20, 20, 1, 2, 3, 4, 5, 6]
scores_maxes = [50, 26, 25, 20, 20, 20, 20, 3, 6, 9, 12, 15, 18]

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
        _scores[1] = 1
        if set(cts.values()) == {1,2}:
            if 2 in cts.values():
                _scores[0] = 1
    if len(cts) == 1: _scores[2] = 1
    if dices == (1,2,3): _scores[3] = 1
    if dices == (4,5,6): _scores[4] = 1
    if dices == (1,3,5): _scores[5] = 1
    if dices == (2,4,6): _scores[6] = 1
    for i in range(1, 7):
        if i in cts:
            _scores[6+i] = cts[i]
    return _scores

memo = {}

def tp_to_num2(tp):
    _num = 0
    for i in range(len(tp)):
        if tp[i] != 'NULL':
            _num += pow(3, i)*(tp[i]+1)
    return _num

def tp_to_num3(tp):
    _num = 0
    for i in range(len(tp)):
        if tp[i] != 'NULL':
            _num += pow(4, i)*(tp[i]+1)
    return _num

def expectiminimax(state, ftm):
    memo_local = {}
    ev = 0
    for dices in combinations_with_replacement([i for i in range(1, 7)], 3):
        multiplier = 6
        cts = defaultdict(int)
        for el in dices: cts[el] += 1
        for el in cts: multiplier //= factorial(cts[el])
        saved_dices_set = set()
        for r in range(0, 4):
            for comb in combinations(dices, r):
                saved_dices_set.add(comb)
        if ftm: _ev = float('-inf')
        else: _ev = float('inf')
        for sd in saved_dices_set:
            n = 3 - len(sd)
            __em = 0
            __ct = 0
            for comb in combinations_with_replacement([i for i in range(1, 7)], n):
                _multiplier = factorial(len(comb))
                _cts = defaultdict(int)
                for el in comb: _cts[el] += 1
                for el in _cts: _multiplier //= factorial(_cts[el])
                new_state_dices = tuple(list(sorted(sd + comb)))
                if new_state_dices in memo_local:
                    __em += memo_local[new_state_dices]
                else:
                    if ftm: _temp_minimax_score = float('-inf')
                    else: _temp_minimax_score = float('inf')
                    curr_scores = scores(new_state_dices)
                    possible_actions = []
                    for i in range(13*(int(ftm)^1), 13 + 13*(int(ftm)^1)):
                        if state[i] == 'NULL': possible_actions.append(i)
                    for i in possible_actions:
                        _temp_next_state = list(state)
                        _temp_next_state[i] = curr_scores[i%13]
                        _temp_score = get_score(_temp_next_state, ftm)
                        if ftm:_temp_minimax_score = max(_temp_minimax_score, _temp_score)
                        else: _temp_minimax_score = min(_temp_minimax_score, _temp_score)
                    __em += _temp_minimax_score
                    memo_local[new_state_dices] = _temp_minimax_score
                __ct += _multiplier
            if ftm: _ev = max(_ev, __em/__ct)
            else: _ev = min(_ev, __em/__ct)
        ev += _ev*multiplier
    return ev/pow(6,3)

def get_score(state, ftm):
    sc = tp_to_num2(state[:7]) + tp_to_num3(state[7:13]) + \
                                        tp_to_num2(state[13:20]) + tp_to_num3(state[20:26])
    if state.count('NULL') == 0:
        _pool = get_pool(state)
        if _pool[0] > _pool[1]: return 1
        elif _pool[0] == _pool[1]: return 0
        else: return -1
    if (sc, ftm) in memo:
        return memo[(sc, ftm)]
    else:
        result = main_base.execute('select value from crag_retro where '
                                   'p0 = ' + str(state[0]) + ' and p1 = ' + str(state[1]) + ' and q0 = ' + str(state[2])
                                   + ' and q1 = ' + str(state[3]) + ' and ftm = ' + str(state[4])).fetchone()
        memo[(sc, ftm)] = result[0]
        if len(memo) > pow(10,7): memo.clear()
        return result

def compute(state, pool, ftm):
    state_conversed = (tp_to_num2(state[:7]),) + (tp_to_num3(state[7:13]),) + \
                      (tp_to_num2(state[13:20]),) + (tp_to_num3(state[20:26]),)
    #print(state_conversed)
    if pool[0] > pool[1] + pool[3]:
        score = 1
    elif pool[1] > pool[0] + pool[2]:
        score = -1
    else:
        score = expectiminimax(state, ftm)
    add_score(state_conversed, ftm, score)

def add_score(state_conversed, ftm, score):
    sc = state_conversed
    #print(sc)
    s = 'insert into crag_retro values (' + str(sc[0]) + ', ' + str(sc[1]) + ', ' + str(sc[2]) + ', ' + str(sc[3]) + ', ' + str(int(ftm)) + ', ' + str(score) + ')'
    #print(s)
    main_base.execute(s)
    main_base.commit()

def get_pool(state):
    _pool = [0, 0, 244, 244]
    for i in range(13):
        if state[i] != 'NULL':
            _pool[0] += state[i]*scores_cats[i]
            _pool[2] -= state[i]*scores_maxes[i]
    for i in range(13, 26):
        if state[i] != 'NULL':
            _pool[1] += state[i]*scores_cats[i-13]
            _pool[3] -= state[i]*scores_maxes[i-13]
    return _pool

#s = (0,)*13 + ('NULL',) + (0,)*12
#print(expectiminimax(s, False))

prev = ()
ftm = False
for r in range(13, -1, -1):
    curr = ()
    for comb in combinations([i for i in range(r)], r):
        _comb = set(comb)
        twos = []
        threes = []
        for el in comb:
            if el < 7: twos.append(el)
            else: threes.append(el)
        for num_upp in range(8):
            num_low = r - num_upp
            if num_upp <= 7 and num_low <= 6:
                for prod_upp in product([0,1], repeat=num_upp):
                    print(r, num_upp, prod_upp, comb, len(prev), len(curr))
                    for prod_low in product([0,1,2], repeat=num_low):
                        merged_prod = prod_upp + prod_low
                        state = ['NULL']*13
                        ind_merged_prod = 0
                        for i in range(13):
                            if i in _comb:
                                state[i] = merged_prod[ind_merged_prod]
                                ind_merged_prod += 1
                        state = tuple(state)
                        if r == 13: prev += (state,)
                        else: curr += (state,)
    if len(curr) > 0 and len(prev) > 0:
        ind = 0
        print('hehe')
        ftm = False
        for p in prev:
            for c in curr:
                pool = get_pool(p + c)
                #print(p, c)
                compute(p+c, pool, ftm)
                if ind % 10 == 0: print(ind)
                ind += 1
        ind = 0
        ftm = True
        for c1 in curr:
            for c2 in curr:
                pool = get_pool(c1 + c2)
                compute(c1+c2, pool, ftm)
                if ind % 10 == 0: print(ind)
                ind += 1
    if len(curr) != 0: prev = curr