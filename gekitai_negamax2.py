import sqlite3
import gekitai_combs_mapping as gcm
import gekitai4 as gh
from random import shuffle
from math import log
from sys import setrecursionlimit

setrecursionlimit(pow(10,5))

base = sqlite3.connect('D://gekitai//main_base2.db')

# base.execute('drop table states')
# base.execute('create table states (white_k INTEGER, white_num INTEGER, black_k INTEGER, black_num INTEGER, wtm INTEGER,'
#              'negamax INTEGER, PRIMARY KEY (white_k, white_num, black_k, black_num, wtm))')
# base.commit()
#
# base.execute('delete from states')
# base.commit()

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
        res = base.execute('select negamax from states where (white_k, white_num, black_k, black_num, wtm) = ' + str(tp)).fetchone()
        if res is None: return None
        checked_tp[0] += 1
        return res[0]

def format_tp(tp):
    if tp[0] <= 7 and tp[2] <= 7:
        syms = get_min_sym(tp)
        _tp = (tp[0], syms[0], tp[2], syms[1])
        return _tp
    return tp

def add_tp(tp, value):
    temp = base.execute('select negamax from states where (white_k, white_num, black_k, black_num, wtm) = ' + str(tp)).fetchone()
    if temp is None: memo[tp] = value
    if len(memo) > pow(10,5):
        tbl = []
        for it in memo.items():
            tbl.append(it[0] + (it[1],))
        base.executemany('insert into states values (?,?,?,?,?,?)', tbl)
        memo.clear()
        base.commit()

#states_memo = set()
none_nodes = set()

ct = [0]
def dfs(states, curr_tp, sign, depth):
    if depth > 5: return None
    _check = check_tp(format_tp(curr_tp) + (sign,))
    has_none_child = False
    if len(memo) % pow(10,3) == 0:
        tbl = []
        for it in memo.items():
            tbl.append(it[0] + (it[1],))
        base.executemany('insert into states values (?,?,?,?,?,?)', tbl)
        memo.clear()
        base.commit()
    if _check is not None: return _check
    # if frozenset(states.keys()) in states_memo:
    #     return None
    if curr_tp in states:
        if states[curr_tp] == sign:
            return 0
    next_states = {}
    minimax = -sign
    if depth <= 3:
        print(curr_tp, depth, checked_tp[0], len(memo), len(none_nodes))
    curr_white, curr_black = gcm.comb_to_vec(gcm.num_to_comb(curr_tp[0], curr_tp[1])), gcm.comb_to_vec(gcm.num_to_comb(curr_tp[2], curr_tp[3]))
    curr_board = {(i,j) for i in range(6) for j in range(6)}.difference(curr_white.union(curr_black))
    for m in curr_board:
        temp_board, temp_white, temp_black = curr_board.copy(), curr_white.copy(), curr_black.copy()
        temp_result = gh.make_move(temp_white, temp_black, temp_board, sign, m)
        temp_state = gcm.comb_to_num(gcm.vec_to_comb(temp_white)) + gcm.comb_to_num(gcm.vec_to_comb(temp_black))
        if temp_result is not None:
            if temp_result == sign:
                #_tp = format_tp(curr_tp)
                add_tp(curr_tp + (sign,), sign)
                #print(curr_tp, depth, minimax, 'terminal')
                return sign
        temp_hval = get_heurestic(temp_white, temp_black)
        next_states[format_tp(temp_state)] = temp_hval
    #states_memo.add(frozenset(states.keys()))
    states[format_tp(curr_tp)] = sign
    _next_states = list(next_states.items())
    _next_states.sort(key= lambda x: -sign*x[1])
    #if depth <= 3: print(curr_tp, depth, len(memo), len(_next_states))
    explained = 0
    for ns in _next_states:
        if ns not in none_nodes:
            temp_res = dfs(states.copy(), ns[0], sign * (-1), depth + 1)
            if sign == 1:
                if temp_res is not None:
                    minimax = max(minimax, temp_res)
                    explained += 1
                else:
                    has_none_child = True
            else:
                if temp_res is not None:
                    minimax = min(minimax, temp_res)
                    explained += 1
                else:
                    has_none_child = True
            if minimax == sign:
                #_tp = format_tp(curr_tp)
                add_tp(curr_tp + (sign,), minimax)
                #print(curr_tp, depth, minimax, 'terminal')
                return minimax
        else:
            has_none_child = True
    if has_none_child is True:
        # try:
        #     base.execute('insert into states_indicates values ' + str(curr_tp + (sign, explained, len(_next_states))))
        # except:
        #     base.execute('update states_indicates set explained = ' + str(explained) + ', all_nodes = ' + str(len(_next_states))
        #                  + ' where (white_k, white_num, black_k, black_num, wtm) = ' + str(curr_tp + (sign,)))
        # base.commit()
        none_nodes.add(curr_tp)
        return None
    _tp = format_tp(curr_tp)
    add_tp(_tp + (sign,), minimax)
    #print(curr_tp, depth, minimax, 'terminal')
    return minimax

print(dfs({}, (0,0,0,0), 1, 0))

tbl = []
for it in memo.items():
    tbl.append(it[0] + (it[1],))
base.executemany('insert into states values (?,?,?,?,?,?)', tbl)
memo.clear()
base.commit()