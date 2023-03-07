import sqlite3
from itertools import combinations
import gekitai_combs_mapping as gcm
import gekitai4 as gh

base = sqlite3.connect('D://gekitai//main_base3.db')
base_syms = sqlite3.connect('D://gekitai//main_base2.db')

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

ct = 0
updated_ct = 0
terminals_ct = 0
rows = base.execute('select * from states_nonterminals where white_k + black_k <= 5 order by explained/all_children desc')
for row in rows:

    white, black = gcm.comb_to_vec(gcm.num_to_comb(row[0], row[1])), gcm.comb_to_vec(gcm.num_to_comb(row[2], row[3]))
    board = {(i, j) for i in range(6) for j in range(6)}.difference(white.union(black))
    result = check_board(white, black, board)
    if type(result) is tuple:
        if result[0] != row[4]:
            memo[row[:4]] = result
            updated_ct += 1
    else:
        memo[row[:4]] = result
        terminals_ct += 1
    ct += 1
    if ct % 100 == 0: print(ct, updated_ct, terminals_ct)

print(updated_ct)
print(terminals_ct)
print(ct)

for it in memo.items():
    if type(it[1]) is tuple:
        base.execute('update states_nonterminals set explained = ' + str(it[1][0]) + ', all_children = ' + str(it[1][1]) + ' where ' +
        '(white_k, white_num, black_k, black_num) = ' + str(it[0]))
    else:
        base.execute('update states_terminals set value ' + str(it[1]) + ', where ' +
                     '(white_k, white_num, black_k, black_num) = ' + str(it[0]))
    base.commit()
