import sqlite3

main_base = sqlite3.connect('D://crag2.db')

# main_base.execute('create table test (id1 INTEGER, id2 INTEGER, id3 INTEGER NOT NULL, PRIMARY KEY (id1, id2))')
# main_base.commit()

#main_base.execute('drop table test')
main_base.execute('drop table crag_two_players')
main_base.commit()
