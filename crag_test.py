import sqlite3

main_base = sqlite3.connect('D://crag.db')

tp = [0]*13 + sorted([0,0,0]) + [0]

# tp[0] = 1
# tp[1] = 1
# #tp[2] = 1
# tp[3] = 1
# tp[4] = 1
# tp[5] = 1
# tp[6] = 1
# tp[7] = 1
# tp[8] = 1
# tp[9] = 1
# tp[10] = 1
# tp[11] = 1
# tp[12] = 1

n = 0
for i in range(13):
    n += pow(2,i)*tp[i]

_tp = tuple([n] + tp[13:])

categories_list = ['crag', 'thirteen', 'three-of-a-kind', 'low straight', 'high straight', 'odd straight',
                   'even straight', '6', '5', '4', '3', '2', '1']

for row in main_base.execute('select * from crag_single_results where (t, d1, d2, d3, remained) = ' + str(_tp)):
    print(row)
    if tp[-1] == 0: print(categories_list[row[-3]])