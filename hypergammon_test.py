# from hypergammon_prep import next_states
#
# state = ((3,3), (6,), -1)
# print(next_states(state, (3,3)))
s = '[[2,3,(1,2)], [5,2,1]]'
s2 = eval(s)

print(s2[0][2][0])