import sqlite3
from itertools import combinations
import gekitai_combs_mapping as gcm
import gekitai4 as gh

base = sqlite3.connect('D://gekitai//main_base2.db')

base.execute('drop table states_terminals')

base.execute('create table states_terminals (white_k INTEGER, white_num INTEGER, black_k INTEGER, black_num INTEGER,'
             'value, PRIMARY KEY (white_k, white_num, black_k, black_num))')

base.commit()

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

not_none_ct = 0
memo = {}
def update_memo(tp, value):
    memo[tp] = value
    if len(memo) > pow(10,6):
        tbl = []
        for it in memo.items():
            if it[1] is not None:
                tbl.append(it[0] + (it[1],))
        print('update', len(tbl))
        base.executemany('insert into states_terminals values (?,?,?,?,?)', tbl)
        memo.clear()
        base.commit()

def check_tp(tp):
    if tp in memo:
        return memo[tp]
    else:
        res = base.execute('select value from states_terminals where (white_k, white_num, black_k, black_num) = ' + str(tp)).fetchone()
        if res is None: return None
        return res[0]

def format_tp(tp):
    if tp[0] <= 7 and tp[2] <= 7:
        syms = get_min_sym(tp)
        _tp = (tp[0], syms[0], tp[2], syms[1])
        return _tp
    return tp

def check_board(white, black, board):
    has_none = False
    for m in board:
        temp_board, temp_white, temp_black = board.copy(), white.copy(), black.copy()
        temp_result = gh.make_move(temp_white, temp_black, temp_board, 1, m)
        if temp_result is not None:
            if temp_result == 1:
                return 1
        else:
            temp_state = gcm.comb_to_num(gcm.vec_to_comb(temp_black)) + gcm.comb_to_num(gcm.vec_to_comb(temp_white))
            _temp_state = format_tp(temp_state)
            further_temp_result = check_tp(_temp_state)
            if further_temp_result is not None:
                if further_temp_result == -1:
                    return 1
            else:
                has_none = True
    if has_none is True:
        return None
    else:
        return -1

for r in range(8):
    for comb in combinations([i for i in range(36)], r):
        _comb = set(comb)
        for j in range(r//2+1):
            for comb_left in combinations(comb, j):
                _comb_left = set(comb_left)
                _comb_right = _comb.difference(_comb_left)
                num_left, num_right = gcm.comb_to_num(_comb_left), gcm.comb_to_num(_comb_right)
                _tp1 = format_tp(num_left + num_right)
                vec_left, vec_right = gcm.comb_to_vec(_comb_left), gcm.comb_to_vec(_comb_right)
                _board = {(a, b) for a in range(6) for b in range(6)}.difference(vec_left.union(vec_right))
                if check_tp(_tp1) is None:
                    value = check_board(vec_left, vec_right, _board)
                    update_memo(_tp1, value)
                    if value is not None:
                        not_none_ct += 1
                _tp2 = format_tp(num_right + num_left)
                if check_tp(_tp2) is None:
                    value = check_board(vec_right, vec_left, _board)
                    update_memo(_tp2, value)
                    if value is not None:
                        not_none_ct += 1
        print(r, comb,len(memo), not_none_ct)

#(7, 12, 20, 22, 24)