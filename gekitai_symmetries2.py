import gekitai_combs_mapping as gcm
from itertools import combinations
import gekitai3 as g
import sqlite3

conn = sqlite3.connect('D://gekitai//main_base2.db')

# conn.execute('CREATE TABLE symmetries (k INTEGER NOT NULL, num INTEGER NOT NULL, r INTEGER NOT NULL, r2 INTEGER NOT NULL, r3 INTEGER NOT NULL, '
#              'x INTEGER NOT NULL, y INTEGER NOT NULL, left_diag INTEGER NOT NULL, right_diag INTEGER NOT NULL, primary key (k, num))')
# conn.commit()

#conn.execute('INSERT INTO symmetries values (0,0,0,0,0,0,0,0,0)')

for r in range(1, 8):
    for comb in combinations([i for i in range(36)], r):
        s = set()
        for el in comb:
            s.add((el // 6, el % 6))
        n = gcm.comb_to_num(comb)

        row = (r, n[1])
        _s = g.rot_90(s)
        _comb = set()
        for el in _s:
            _comb.add(el[0]*6 + el[1])
        n_out = gcm.comb_to_num(_comb)
        row += (n_out[1],)

        _s = g.rot_90(_s)
        _comb = set()
        for el in _s:
            _comb.add(el[0]*6 + el[1])
        n_out = gcm.comb_to_num(_comb)
        row += (n_out[1],)

        _s = g.rot_90(_s)
        _comb = set()
        for el in _s:
            _comb.add(el[0]*6 + el[1])
        n_out = gcm.comb_to_num(_comb)
        row += (n_out[1],)

        _s = g.sym_horizontal(s)
        _comb = set()
        for el in _s:
            _comb.add(el[0]*6 + el[1])
        n_out = gcm.comb_to_num(_comb)
        row += (n_out[1],)

        _s = g.sym_vertical(s)
        _comb = set()
        for el in _s:
            _comb.add(el[0] * 6 + el[1])
        n_out = gcm.comb_to_num(_comb)
        row += (n_out[1],)

        _s = g.sym_left_diag(s)
        _comb = set()
        for el in _s:
            _comb.add(el[0] * 6 + el[1])
        n_out = gcm.comb_to_num(_comb)
        row += (n_out[1],)

        _s = g.sym_right_diag(s)
        _comb = set()
        for el in _s:
            _comb.add(el[0] * 6 + el[1])
        n_out = gcm.comb_to_num(_comb)
        row += (n_out[1],)

        st = '?,'*9
        conn.execute('insert into symmetries values (' + st[:-1] + ')', row)
        print(comb)
    conn.commit()
