from itertools import combinations_with_replacement, combinations, product
from collections import defaultdict
import sqlite3
from math import factorial

main_base = sqlite3.connect('D://crag2.db')

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

prods_upper = []
prods_lower = []
prods_full = [[] for _ in range(14)]


ind = 0
for prod_upper in product(['NULL', 0, 1], repeat=7):
    print(ind)
    for prod_lower in product(['NULL', 0, 1, 2, 3], repeat=6):
        nulls = 0
        prod = prod_upper + prod_lower
        score = 0
        score_to_achieve = 0
        for i in range(len(prod)):
            if prod[i] != 'NULL':
                score += prod[i]*scores_cats[i]
            else:
                score_to_achieve = scores_maxes[i]
                nulls += 1
        prods_full[nulls].append((prod, score, score_to_achieve))
    ind += 1

for pf in prods_full:
    pf.sort(key= lambda x: x[1]+x[2])

for pf in prods_full:
    pf_first_sort = pf[:]
    pf_first_sort.sort(key= lambda x: -x[1])
    j = len(pf)-1
    for i in range(len(pf_first_sort)):
        el = pf_first_sort[i]
        conv_el = (tp_to_num2(el[0][:7]), tp_to_num3(el[0][7:13]))
        while sum(pf[j][1:]) >= el[1]:
            j -= 1
        for _j in range(j, -1, -1):
            conv_el2 = (tp_to_num2(pf[_j][0][:7]), tp_to_num3(pf[_j][0][7:13]))
            add_node(conv_el + conv_el2 + (0,0,0,0), 1, ('NULL', 'NULL', 'NULL'))
            add_node(conv_el2 + conv_el + (0,0,0,0), -1, ('NULL', 'NULL', 'NULL'))
