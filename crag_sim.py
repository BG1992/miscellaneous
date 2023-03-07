import sqlite3
from random import randint, random, choice
from collections import defaultdict
import statistics

main_base = sqlite3.connect('D://crag.db')
memo = {}

for row in main_base.execute('select * from crag_single_results'):
    _el = ()
    t = row[0]
    _t = tuple(bin(t)[2:])
    for i in range(len(_t)):
        _el += (int(_t[i]),)
    rev_el = list(_el)[::-1]
    rev_el += (0,)*(13 - len(rev_el))
    _el = tuple(rev_el) + row[1:5]
    action = ()
    for i in range(6, 9):
        if row[i] != 'NULL':
            action += (row[i],)
    memo[_el] = (row[5], action)

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

categories_list = ['crag', 'thirteen', 'three-of-a-kind', 'low straight', 'high straight', 'odd straight',
                   'even straight', '6', '5', '4', '3', '2', '1']

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

sims_ct = 1000000
tbl = []
for _ in range(sims_ct):
    score = 0
    state = (0,)*13 + (0,0,0,0)
    while state[:13] != (1,)*13:
        roll = sorted([randint(1,6), randint(1,6), randint(1,6)])
        next_state = state[:13] + tuple(roll) + (1,)
        act = memo[next_state][1]
        if len(act) == 0:
            roll = sorted([randint(1,6), randint(1,6), randint(1,6)])
        elif len(act) == 1:
            roll = sorted([randint(1,6), randint(1,6)])
        elif len(act) == 2:
            roll = [randint(1,6)]
        else:
            roll = []
        dices = roll + list(act)
        dices = tuple(sorted(dices))
        next_state = state[:13] + dices + (0,)
        act = memo[next_state][1][0]
        cat = categories_list[act]
        _scores = scores(dices)
        score += _scores[cat]
        state = list(state[:13]) + [0,0,0,0]
        state[act] = 1
        state = tuple(state)
    #print(score)
    tbl.append(score)
    if _ % 10000 == 0: print(_/sims_ct)

print(statistics.mean(tbl), statistics.stdev(tbl), min(tbl), max(tbl))

sims_ct = 1000000
tbl = []
for _ in range(sims_ct):
    score = 0
    state = (0,)*13 + (0,0,0,0)
    while state[:13] != (1,)*13:
        roll = sorted([randint(1,6), randint(1,6), randint(1,6)])
        act = ()
        for j in range(3):
            if random() <= 0.5:
                act += (roll[j],)
        if len(act) == 0:
            roll = sorted([randint(1,6), randint(1,6), randint(1,6)])
        elif len(act) == 1:
            roll = sorted([randint(1,6), randint(1,6)])
        elif len(act) == 2:
            roll = [randint(1,6)]
        else:
            roll = []
        dices = roll + list(act)
        dices = tuple(sorted(dices))
        next_state = state[:13] + dices + (0,)
        act = memo[next_state][1][0]
        cat = categories_list[act]
        _scores = scores(dices)
        score += _scores[cat]
        state = list(state[:13]) + [0, 0, 0, 0]
        state[act] = 1
        state = tuple(state)
    #print(score)
    tbl.append(score)
    if _ % 10000 == 0: print(_/sims_ct)

print(statistics.mean(tbl), statistics.stdev(tbl), min(tbl), max(tbl))

sims_ct = 1000000
tbl = []
for _ in range(sims_ct):
    score = 0
    state = (0,)*13 + (0,0,0,0)
    while state[:13] != (1,)*13:
        roll = sorted([randint(1,6), randint(1,6), randint(1,6)])
        act = ()
        for j in range(3):
            if random() <= 0.5:
                act += (roll[j],)
        if len(act) == 0:
            roll = sorted([randint(1,6), randint(1,6), randint(1,6)])
        elif len(act) == 1:
            roll = sorted([randint(1,6), randint(1,6)])
        elif len(act) == 2:
            roll = [randint(1,6)]
        else:
            roll = []

        cats = []
        dices = roll + list(act)
        dices = tuple(sorted(dices))
        _scores = scores(dices)
        for j in range(len(categories_list)):
            if state[j] == 0:
                cats.append([_scores[categories_list[j]], j])
        cats.sort(key= lambda x: -x[0])
        score += cats[0][0]
        state = list(state[:13]) + [0, 0, 0, 0]
        state[cats[0][1]] = 1
        state = tuple(state)
    #print(score)
    tbl.append(score)
    if _ % 10000 == 0: print(_/sims_ct)

print(statistics.mean(tbl), statistics.stdev(tbl), min(tbl), max(tbl))