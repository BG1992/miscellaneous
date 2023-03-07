import sqlite3

base = sqlite3.connect('D://gekitai//main_base2.db')

base.execute('create table states_bta (white_k INTEGER, white_num INTEGER, black_k INTEGER, black_num INTEGER, wtm INTEGER,'
             'proof INTEGER, disproof INTEGER, expanded INTEGER, PRIMARY KEY (white_k, white_num, black_k, black_num, wtm))')

base.commit()

