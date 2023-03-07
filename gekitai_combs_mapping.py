from sympy import binomial
from itertools import combinations
# import sqlite3
#
# conn = sqlite3.connect('D://gekitai//main_base.db')
def comb_to_num(comb):
    _comb = sorted(list(comb), reverse=True)
    k = len(_comb)
    n = 0
    for i in range(len(_comb)):
        n += int(binomial(_comb[i], k-i))
    return (k, n)

def num_to_comb(k, n):
    if k == 0: return set()
    _comb = set()
    _k, _n = k, n
    while len(_comb) < k:
        i = _k-1
        res = 0
        while res <= _n:
            res = binomial(i, _k)
            i += 1
        _comb.add(i-2)
        _n -= binomial(i-2, _k)
        _k -= 1
    return _comb

def comb_to_vec(comb):
    vec = set()
    for el in comb:
        vec.add((el//6, el % 6))
    return vec

def vec_to_comb(vec):
    comb = set()
    for el in vec:
        comb.add(el[0]*6 + el[1])
    return comb

    # if k == 0: return set()
    # else: return set(conn.execute('select * from combs_dict' + str(k) + ' where ind = ' + str(n)).fetchone()[1:])
#
# conn.execute('CREATE TABLE combs_dict1 (ind INTEGER PRIMARY KEY, t1 INTEGER)')
# conn.execute('CREATE TABLE combs_dict2 (ind INTEGER PRIMARY KEY, t1 INTEGER, t2 INTEGER)')
# conn.execute('CREATE TABLE combs_dict3 (ind INTEGER PRIMARY KEY, t1 INTEGER, t2 INTEGER, t3 INTEGER)')
# conn.execute('CREATE TABLE combs_dict4 (ind INTEGER PRIMARY KEY, t1 INTEGER, t2 INTEGER, t3 INTEGER, t4 INTEGER)')
# conn.execute('CREATE TABLE combs_dict5 (ind INTEGER PRIMARY KEY, t1 INTEGER, t2 INTEGER, t3 INTEGER, t4 INTEGER, t5 INTEGER)')
# conn.execute('CREATE TABLE combs_dict6 (ind INTEGER PRIMARY KEY, t1 INTEGER, t2 INTEGER, t3 INTEGER, t4 INTEGER, t5 INTEGER, t6 INTEGER)')
# conn.execute('CREATE TABLE combs_dict7 (ind INTEGER PRIMARY KEY, t1 INTEGER, t2 INTEGER, t3 INTEGER, t4 INTEGER, t5 INTEGER, t6 INTEGER, t7 INTEGER)')
# conn.commit()

# for r in range(1, 8):
#     tbl = []
#     s = '?,'*(r+1)
#     for comb in combinations([i for i in range(36)], r):
#         tbl.append((comb_to_num(comb)[1],) + comb)
#     _s = 'INSERT INTO combs_dict' + str(r) + ' VALUES (' + str(s[:-1]) + ')'
#     #print(_s, tbl)
#     conn.executemany(_s, tbl)
#
# conn.commit()
#
# print(num_to_comb(5, 72))
# for r in range(7, 78):
#     print(r)
#     for comb in combinations([i for i in range(36)], r):
#         print(r, comb)
#         num = comb_to_num(comb)[1]
#         _comb = num_to_comb(len(comb), num)
#         if set(comb) != _comb:
#             print(comb)
#             break