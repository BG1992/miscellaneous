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
with open('D://hypergammon//hyper_32a_52.csv', 'r', newline='') as csvfile:
    _reader = csv.reader(csvfile, delimiter=';')
    for row in _reader:
        tp1 = eval(row[0])
        if tp1 not in states: states[tp1] = Decimal(row[1])
        tp2 = ()
        _tp20 = []
        for i in tp1[1]:
            _i = 25 - i
            _tp20.append(_i)
        _tp20.sort()
        tp2 += (tuple(_tp20),)
        _tp21 = []
        for i in tp1[0]:
            _i = 25 - i
            _tp21.append(_i)
        _tp21.sort()
        tp2 += (tuple(_tp21),)
        tp2 += (tp1[2]*(-1),)
        if tp2 not in states: states[tp2] = Decimal(row[1])*(-1)
        if ind % 10000 == 0: print(ind, row, len(states))
        ind += 1

with open('D://hypergammon//hyper_32b_11.csv', 'r', newline='') as csvfile:
    _reader = csv.reader(csvfile, delimiter=';')
    for row in _reader:
        tp1 = eval(row[0])
        if tp1 not in states: states[tp1] = Decimal(row[1])
        tp2 = ()
        _tp20 = []
        for i in tp1[1]:
            _i = 25 - i
            _tp20.append(_i)
        _tp20.sort()
        tp2 += (tuple(_tp20),)
        _tp21 = []
        for i in tp1[0]:
            _i = 25 - i
            _tp21.append(_i)
        _tp21.sort()
        tp2 += (tuple(_tp21),)
        tp2 += (tp1[2]*(-1),)
        if tp2 not in states: states[tp2] = Decimal(row[1])*(-1)
        if ind % 10000 == 0: print(ind, row, len(states))
        ind += 1

with open('D://hypergammon//hyper_32_23.csv', 'w', newline='') as csvfile:
    _writer = csv.writer(csvfile, delimiter=';')
    for s in states:
        _writer.writerow([s, states[s]])
