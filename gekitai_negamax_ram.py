import sqlite3
import gekitai_combs_mapping as gcm
import gekitai4 as gh
from random import shuffle
from math import log
from sys import setrecursionlimit

setrecursionlimit(pow(10,5))

base = sqlite3.connect('D://gekitai//main_base2.db')

#base.execute('drop table states')
# base.execute('create table states2 (white_k INTEGER, white_num INTEGER, black_k INTEGER, black_num INTEGER, wtm INTEGER,'
#              'negamax INTEGER, PRIMARY KEY (white_k, white_num, black_k, black_num, wtm))')
# base.commit()
#
base.execute('delete from states2')
base.commit()

base.commit()
memo = {}

def get_min_sym(tp):
    #get pairs (white, black) smallest in the order (a, b) -> a least, than b least
    white_tp, black_tp = tp[:2], tp[2:]
    white_row = base.execute('select * from symmetries where (k, num) = ' + str(white_tp)).fetchone()[2:]
    black_row = base.execute('select * from symmetries where (k, num) = ' + str(black_tp)).fetchone()[2:]
    a, b = float('inf'), float('inf')
    for i in range(1, len(white_row)):
        if white_row[i] < a:
            a = white_row[i]
            b = float('inf')
            if black_row[i] < b:
                b = black_row[i]
        elif white_row[i] == a:
            if black_row[i] < b:
                b = black_row[i]
    return a, b

def get_heurestic(white, black):
    res = 0
    for w in white:
        res += 1/(abs(2.5-w[0])+abs(2.5-w[1]))
    for b in black:
        res -= 1/(abs(2.5-b[0])+abs(2.5-b[1]))
    return res

def state_to_sets(state):
    white_set, black_set = gcm.num_to_comb(state[0], state[1]), gcm.num_to_comb(state[2], state[3])
    return white_set, black_set, {[i for i in range(36)]}.difference(white_set.union(black_set))

checked_tp = [0]
def check_tp(tp):
    if tp in memo:
        return memo[tp]
    else:
        return None
        # res = base.execute('select negamax from states where (white_k, white_num, black_k, black_num, wtm) = ' + str(tp)).fetchone()
        # if res is None: return None
        # checked_tp[0] += 1
        # return res[0]

def format_tp(tp):
    if tp[0] <= 7 and tp[2] <= 7:
        syms = get_min_sym(tp)
        _tp = (tp[0], syms[0], tp[2], syms[1])
        return _tp
    return tp

def add_tp(tp, value):
    memo[tp] = value
    # temp = base.execute('select negamax from states where (white_k, white_num, black_k, black_num, wtm) = ' + str(tp)).fetchone()
    # if temp is None: memo[tp] = value
    if len(memo) > pow(10,6):
        tbl = []
        for it in memo.items():
            tbl.append(it[0] + (it[1],))
        base.executemany('insert into states2 values (?,?,?,?,?,?)', tbl)
        memo.clear()
        base.commit()

ct = [0]
def dfs(states, curr_tp, curr_board, curr_white, curr_black, sign, depth):
    if depth > 5: return None
    _tp = format_tp(curr_tp)
    _check = check_tp(_tp + (sign,))
    has_none_child = False
    if _check is not None: return _check
    if _tp in states:
        if states[_tp] == sign:
            return 0
    next_states = []
    next_states_set = set()
    minimax = -sign
    if depth <= 2: print(curr_tp, depth, checked_tp[0], len(memo))
    #curr_board = {(i,j) for i in range(6) for j in range(6)}.difference(curr_white.union(curr_black))
    for m in curr_board:
        temp_board, temp_white, temp_black = curr_board.copy(), curr_white.copy(), curr_black.copy()
        temp_result = gh.make_move(temp_white, temp_black, temp_board, sign, m)
        temp_state = gcm.comb_to_num(gcm.vec_to_comb(temp_white)) + gcm.comb_to_num(gcm.vec_to_comb(temp_black))
        if temp_result is not None:
            if temp_result == sign:
                add_tp(_tp + (sign,), sign)
                return sign
        temp_hval = get_heurestic(temp_white, temp_black)
        if depth == 0:
            temp_tp = format_tp(temp_state)
        else:
            temp_tp = temp_state
        next_states.append((temp_tp, temp_board, temp_white, temp_black, temp_hval))
        next_states_set.add(temp_tp)
    states[_tp] = sign
    next_states.sort(key= lambda x: -sign*x[4])
    #if depth <= 3: print(curr_tp, depth, len(memo), len(_next_states))
    for ns in next_states:
        if ns[0] in next_states_set:
            temp_res = dfs(states.copy(), ns[0], ns[1], ns[2], ns[3], sign * (-1), depth + 1)
            if sign == 1:
                if temp_res is not None:
                    minimax = max(minimax, temp_res)
                else:
                    has_none_child = True
            else:
                if temp_res is not None:
                    minimax = min(minimax, temp_res)
                else:
                    has_none_child = True
            if minimax == sign:
                #_tp = format_tp(curr_tp)
                add_tp(format_tp(curr_tp) + (sign,), minimax)
                #print(curr_tp, depth, minimax, 'terminal')
                return minimax
    if has_none_child is True: return None
    add_tp(_tp + (sign,), minimax)
    return minimax

print(dfs({}, (0,0,0,0), {(i,j) for i in range(6) for j in range(6)}, set(), set(), 1, 0))

tbl = []
for it in memo.items():
    tbl.append(it[0] + (it[1],))
base.executemany('insert into states2 values (?,?,?,?,?,?)', tbl)
memo.clear()
base.commit()