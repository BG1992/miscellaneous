from itertools import combinations_with_replacement
from random import shuffle
import csv
from decimal import Decimal, getcontext

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

states = {}

ind = 0
with open('D://hypergammon//hyper_32_21.csv', 'r', newline='') as csvfile:
    _reader = csv.reader(csvfile, delimiter=';')
    for row in _reader:
        states[eval(row[0])] = Decimal(row[1])
        if ind % 10000 == 0: print(ind, row)
        ind += 1

# ind = 0
# posses_white = set([i for i in range(25)])
# posses_black = set([i for i in range(1, 26)])
# for r_white in range(4):
#     for comb_white in combinations_with_replacement(posses_white, r_white):
#         print(ind, comb_white)
#         _comb_white = set(comb_white)
#         for r_black in range(3):
#             for comb_black in combinations_with_replacement(posses_black.difference(_comb_white), r_black):
#                 if len(comb_white) == 0 and len(comb_black) == 0: score = None
#                 elif len(comb_white) == 0 and len(comb_black) != 0: score = 1
#                 elif len(comb_white) != 0 and len(comb_black) == 0: score = -1
#                 else: score = 0
#                 if score is not None and not (len(comb_white) <= 2 and len(comb_black) <= 2):
#                     states[(comb_white, comb_black, 1)] = Decimal(score)
#                     ind += 1
#                     states[(comb_white, comb_black, -1)] = Decimal(score)
#                     ind += 1
#
# print(ind)
rolls = [(i,j) for i in range(1, 7) for j in range(1, 7)]
print(rolls)

def f():
    i = 0
    diffs = 0
    updates = 0
    states_list = list(states.keys())
    shuffle(states_list)
    for state in states_list:
        score = states[state]
        if score not in [-1, 1] and not (len(state[0]) <= 2 and len(state[1]) <= 2):
            em = 0
            for roll in rolls:
                if state[2] == 1:
                    em += max(map(lambda x: states[x], next_states(state, roll)))
                else:
                    em += min(map(lambda x: states[x], next_states(state, roll)))
            em /= len(rolls)
            diffs += abs(em - score)
            states[state] = em
            if abs(em - score) > 0: updates += 1
        if i % 1000 == 0: print(i, len(states), diffs, updates)
        i += 1
    return diffs, updates

tolerance = pow(10,-6)
ind = 22
while 1:
    diffs, updates = f()
    if diffs < tolerance: break
    ind += 1
    with open('D://hypergammon//hyper_32_'+str(ind)+'.csv', 'w', newline='') as csvfile:
        _writer = csv.writer(csvfile, delimiter= ';')
        ind2 = 0
        for el in states:
            item = [el, states[el]]
            _writer.writerow(item)
            if ind2 % 100000 == 0: print(ind2, len(states))
            ind2 += 1
