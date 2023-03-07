from itertools import combinations_with_replacement
import csv
from decimal import Decimal, getcontext

getcontext().prec = 8

rolls = [(i,j) for i in range(1, 7) for j in range(i, 7)]
print(rolls)

states_checked = {}
states_unchecked = {}
ind = 0
# with open('D://hypergammon//hyper_33a.csv', 'r', newline='') as csvfile:
#     _reader = csv.reader(csvfile, delimiter= ';')
#     for row in _reader:
#         states_checked[eval(row[0])] = Decimal(row[1])
#         ind += 1
#         if ind % 10000 == 0: print(ind, len(states_checked))

ind = 0
posses_white = set([i for i in range(25)])
posses_black = set([i for i in range(1, 26)])
for r_white in range(3, 4):
    for comb_white in combinations_with_replacement(posses_white, r_white):
        print(ind, comb_white)
        _comb_white = set(comb_white)
        for r_black in range(3, 4):
            for comb_black in combinations_with_replacement(posses_black.difference(_comb_white), r_black):
                if not (0 not in comb_white and 25 not in comb_black and min(comb_white) > max(comb_black)):
                    if (comb_white, comb_black, 1) not in states_checked:
                        states_unchecked[(comb_white, comb_black, 1)] = Decimal(0)
                    if (comb_white, comb_black, -1) not in states_checked:
                        states_unchecked[(comb_white, comb_black, -1)] = Decimal(0)

def get_value(x):
    if x not in states_unchecked: return 0
    return states_unchecked[x]

def f():
    i = 0
    diffs = 0
    updates = 0
    for comb_white in combinations_with_replacement(posses_white, 3):
        s = 'D://hypergammon//states33_' + str(comb_white[0]) + '_' + str(comb_white[1]) + '_' + str(
            comb_white[2]) + '.csv'
        with open(s, 'r', newline='') as csvfile:
            _reader = csv.reader(csvfile, delimiter = ';')
            for row in _reader:
                state = eval(row[0])
                next_states = eval(row[1])
                score = states_unchecked[state]
                if state in states_unchecked:
                    em = 0
                    for j in range(len(rolls)):
                        roll = rolls[j]
                        if roll[0] == roll[1]: prob = 1/36
                        else: prob = 2/36
                        for st in next_states:
                            for el in st: em += Decimal(0)
                        # if state[2] == 1:
                        #     em += max(map(lambda x: get_value(x), next_states[j]))*Decimal(prob)
                        # else:
                        #     em += min(map(lambda x: get_value(x), next_states[j]))*Decimal(prob)
                em /= len(rolls)
                diffs += abs(em - score)
                states_unchecked[state] = em
                if abs(em - score) > 0: updates += 1
                if i % 1000 == 0: print(i, len(states_unchecked), diffs, updates)
                i += 1
    return diffs, updates

tolerance = pow(10,-6)
ind = 0
while 1:
    diffs, updates = f()
    if diffs < tolerance: break
    ind += 1
    with open('D://hypergammon//hyper_33b_'+str(ind)+'.csv', 'w', newline='') as csvfile:
        _writer = csv.writer(csvfile, delimiter= ';')
        ind2 = 0
        for el in states_unchecked:
            item = [el, states_unchecked[el]]
            _writer.writerow(item)
            if ind2 % 100000 == 0: print(ind2, len(states_unchecked))
            ind2 += 1