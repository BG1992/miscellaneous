import sqlite3
import gekitai_combs_mapping as gcm
import gekitai_helper as gh
from random import shuffle
from math import log

base = sqlite3.connect('D://gekitai//main_base.db')

# base.execute('drop table states')
# base.execute('create table states (white_k INTEGER, white_num INTEGER, black_k INTEGER, black_num INTEGER, white_to_move INTEGER, w INTEGER, '
#              'n INTEGER, PRIMARY KEY (white_k, white_num, black_k, black_num, white_to_move))')
# base.commit()

def get_params(tp):
    s = 'select w, n from states where (white_k, white_num, black_k, black_num, white_to_move) = ' + str(tp)
    res = base.execute(s).fetchone()
    if res is None:
        return [0, 1]
    return list(res)

sims_ct = pow(10,7)
for i in range(sims_ct):

    queue = {}
    board = {(i,j) for i in range(6) for j in range(6)}
    white, black = set(), set()
    result = None
    tp = (gcm.comb_to_num(gcm.vec_to_comb(white)) + gcm.comb_to_num(gcm.vec_to_comb(black)) + (1,))
    queue[tp] = get_params(tp)
    white_to_move = 1

    while True:

        if white_to_move == 1:
            score = float('-inf')
        else:
            score = float('inf')
        N = get_params((gcm.comb_to_num(gcm.vec_to_comb(white)) + gcm.comb_to_num(gcm.vec_to_comb(black))) + (1,))[1]
        next_board = None
        next_white, next_black = None, None
        move_chosen = None

        moves = list(board)
        shuffle(moves)
        for move in moves:
            temp_res = gh.make_move(white, black, board, white_to_move, move)
            if temp_res == 1 and white_to_move == 1:
                temp_score = float('inf')
                score = temp_score
                break
            elif temp_res == 0 and white_to_move == 0:
                temp_score = float('-inf')
                score = temp_score
                break
            elif temp_res == 1 and white_to_move == 0:
                temp_score = float('inf')
            elif temp_res == 0 and white_to_move == 1:
                temp_score = float('-inf')
            else:
                temp_board = temp_res
                tp = (gcm.comb_to_num(gcm.vec_to_comb(temp_board[0])) + gcm.comb_to_num(gcm.vec_to_comb(temp_board[1]))) + (white_to_move ^ 1,)
                w, n = get_params(tp)
                if white_to_move:
                    temp_score = w/n + (2*log(N)/n)**0.5
                else:
                    temp_score = (n-w)/n + (2*log(N)/n)**0.5
            if white_to_move == 1:
                if temp_score > score:
                    score = temp_score
                    if temp_score != float('inf') and temp_score != float('-inf'):
                        next_board, next_white, next_black = temp_board[0], temp_board[1], temp_board[2]
                        move_chosen = move
            else:
                if temp_score < score:
                    score = temp_score
                    if temp_score != float('inf') and temp_score != float('-inf'):
                        next_board, next_white, next_black = temp_board[0], temp_board[1], temp_board[2]
                        move_chosen = move

        if score != float('inf') and score != float('-inf'):

            board = next_board.copy()
            white = next_white.copy()
            black = next_black.copy()

            tp = (gcm.comb_to_num(gcm.vec_to_comb(white)) + gcm.comb_to_num(gcm.vec_to_comb(black))) + (white_to_move ^ 1,)
            queue[tp] = get_params(tp)

        elif score == float('inf'):
            for tp in queue:
                queue[tp][0] += 1
                queue[tp][1] += 1
            break

        elif score == float('-inf'):
            for tp in queue:
                queue[tp][1] += 1
            break

        white_to_move ^= 1
        N = n
        # print(move_chosen)
        # gh.print_board(white, black)
        # print()

    tbl = []
    for it in queue.items():
        tbl.append(it[0] + tuple(it[1]))

    for it in tbl:
        try:
            base.execute('insert into states values (?,?,?,?,?,?,?)', it)
        except:
            base.execute('update states set w = ' + str(it[5]) + ', n = ' + str(it[6]) +
                         ' where (white_k, white_num, black_k, black_num, white_to_move) = ' + str(it[:5]))

        if i % 100 == 0:
            print(i, it)
    if i % 100 == 0:
        ct = 0
        for _ in base.execute('select white_k from states'):
            ct += 1
        print(ct)
    base.commit()