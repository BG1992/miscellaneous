import sqlite3
from itertools import combinations
import gekitai_combs_mapping as gcm
import gekitai4 as gh

base = sqlite3.connect('D://gekitai//main_base3.db')
base_syms = sqlite3.connect('D://gekitai//main_base2.db')

# base.execute('create table states_terminals (white_k INTEGER, white_num INTEGER, black_k INTEGER, black_num INTEGER,'
#              'value, PRIMARY KEY (white_k, white_num, black_k, black_num))')
#
# base.execute('create table states_nonterminals (white_k INTEGER, white_num INTEGER, black_k INTEGER, black_num INTEGER,'
#              'explained INTEGER, all_children INTEGER, PRIMARY KEY (white_k, white_num, black_k, black_num))')
#
# base.execute('create table combs_checked (k INTEGER, num INTEGER, PRIMARY KEY (k, num))')

# base.execute('delete from states_terminals')
# base.execute('delete from states_nonterminals')
# base.execute('delete from combs_checked')
#
# base.commit()

def get_min_sym(tp):
    #get pairs (white, black) smallest in the order (a, b) -> a least, than b least
    white_tp, black_tp = tp[:2], tp[2:]
    white_row = base_syms.execute('select * from symmetries where (k, num) = ' + str(white_tp)).fetchone()[2:]
    black_row = base_syms.execute('select * from symmetries where (k, num) = ' + str(black_tp)).fetchone()[2:]
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
        tbl_terminals, tbl_nonterminals = [], []
        for it in memo.items():
            if type(it[1]) is not tuple:
                tbl_terminals.append(it[0] + (it[1],))
            else:
                tbl_nonterminals.append(it[0] + it[1])

        ct_terminals = 0
        ct_nonterminals = 0
        for it in tbl_terminals:
            try:
                base.execute('insert into states_terminals ' + str(it))
                ct_terminals += 1
            except: pass
        for it in tbl_nonterminals:
            try:
                base.execute('insert into states_nonterminals ' + str(it))
                ct_nonterminals += 1
            except: pass
        print('update terminals', ct_terminals)
        print('update nonterminals', ct_nonterminals)
        memo.clear()
        base.commit()

memo_sym = set()
def check_sym(tp):
    if tp in memo_sym: return True
    res = base.execute('select * from combs_checked where (k, num) = ' + str(tp)).fetchone()
    if res is not None: return True
    return False

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
    explained = 0
    children = set()
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
                    explained += 1
            else:
                has_none = True
                children.add(_temp_state)
    if has_none is True:
        return (explained, len(children))
    else:
        return -1

start = False
for r in range(6, 8):
    for comb in combinations([i for i in range(36)], r):
        if comb == (0, 1, 8, 12, 18, 31): start = True
        if start:
            _comb = set(comb)
            _comb_vec = gcm.comb_to_vec(comb)
            _num_main = gcm.comb_to_num(comb)[1]
            _num_h = gcm.comb_to_num(gcm.vec_to_comb(gh.sym_horizontal(_comb_vec)))[1]
            _num_v = gcm.comb_to_num(gcm.vec_to_comb(gh.sym_vertical(_comb_vec)))[1]
            _num_ld = gcm.comb_to_num(gcm.vec_to_comb(gh.sym_left_diag(_comb_vec)))[1]
            _num_rd = gcm.comb_to_num(gcm.vec_to_comb(gh.sym_right_diag(_comb_vec)))[1]
            _s = gh.rot_90(_comb_vec)
            _num_90 = gcm.comb_to_num(gcm.vec_to_comb(_s))[1]
            _s = gh.rot_90(_s)
            _num_180 = gcm.comb_to_num(gcm.vec_to_comb(_s))[1]
            _s = gh.rot_90(_s)
            _num_270 = gcm.comb_to_num(gcm.vec_to_comb(_s))[1]
            num = min(_num_main, _num_h, _num_v, _num_ld, _num_rd, _num_90, _num_180, _num_270)
            if check_sym((len(comb), num)) is False:
                for j in range(r//2+1):
                    for comb_left in combinations(comb, j):

                        _comb_left = set(comb_left)
                        _comb_right = _comb.difference(_comb_left)
                        num_left, num_right = gcm.comb_to_num(_comb_left), gcm.comb_to_num(_comb_right)
                        vec_left, vec_right = gcm.comb_to_vec(_comb_left), gcm.comb_to_vec(_comb_right)
                        _board = {(a, b) for a in range(6) for b in range(6)}.difference(vec_left.union(vec_right))

                        _tp1 = format_tp(num_left + num_right)
                        _tp2 = format_tp(num_right + num_left)
                        if j == r//2 and r % 2 == 0:
                            if gh.get_result(vec_left, vec_right) is None:
                                if check_tp(_tp1) is None:
                                    value = check_board(vec_left, vec_right, _board)
                                    update_memo(_tp1, value)
                                    if type(value) is not tuple:
                                        not_none_ct += 1
                                if check_tp(_tp2) is None:
                                    value = check_board(vec_right, vec_left, _board)
                                    update_memo(_tp2, value)
                                    if type(value) is not tuple:
                                        not_none_ct += 1
                        else:
                            if gh.get_result(vec_left, vec_right) is None:
                                value = check_board(vec_left, vec_right, _board)
                                update_memo(_tp1, value)
                                if type(value) is not tuple:
                                    not_none_ct += 1
                                value = check_board(vec_right, vec_left, _board)
                                update_memo(_tp2, value)
                                if type(value) is not tuple:
                                    not_none_ct += 1

                print(r, comb, len(memo_sym), len(memo), not_none_ct)
                memo_sym.add((len(comb), num))
                if len(memo_sym) > pow(10,6):
                    tbl = []
                    for it in memo_sym:
                        tbl.append(it)
                    print('update', len(tbl))
                    base.executemany('insert into combs_checked values (?,?)', tbl)
                    memo_sym.clear()
                    base.commit()

#(7, 12, 20, 22, 24)