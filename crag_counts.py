scores_cats = [50, 26, 25, 20, 20, 20, 20, 1, 2, 3, 4, 5, 6]
scores_maxes = [50, 26, 25, 20, 20, 20, 20, 3, 6, 9, 12, 15, 18]

maxes = [[] for _ in range(14)]

def bfs(curr_states):
    next_states = {}
    for cs in curr_states:
        achieved, remaining = curr_states[cs]
        if len(cs) < 7:
            for i in ['NULL', 0, 1, 2]:
                ns = cs + (i,)
                if ns[-1] != 'NULL':
                    new_achieved = achieved + ns[-1] * scores_cats[len(ns) - 1]
                    new_remaining = remaining - scores_maxes[len(ns) - 1]
                else:
                    new_achieved = achieved
                    new_remaining = remaining
                next_states[ns] = (new_achieved, new_remaining)
        else:
            for i in ['NULL', 0, 1]:
                ns = cs + (i,)
                if ns[-1] != 'NULL':
                    new_achieved = achieved + ns[-1] * scores_cats[len(ns) - 1]
                    new_remaining = remaining - scores_maxes[len(ns) - 1]
                else:
                    new_achieved = achieved
                    new_remaining = remaining
                next_states[ns] = (new_achieved, new_remaining)

    return next_states

curr_states = {(): (0, 244)}
for i in range(13):
    curr_states = bfs(curr_states)
    print(i, len(curr_states))

for tp in curr_states:
    ct = tp.count('NULL')
    maxes[13-ct].append(curr_states[tp])

del curr_states

main_ct = 0
for i in range(1, 14):
    maxes_first = maxes[i].copy()
    maxes_first.sort(key= lambda x: -x[0])
    maxes[i].sort(key= lambda x: -sum(x))
    k = 0
    for j in range(len(maxes_first)):
        while maxes_first[j][0] < sum(maxes[i][k]):
            k += 1
            if k >= len(maxes):
                print(k, len(maxes))
                break
        main_ct += len(maxes) - k
        if k >= len(maxes): break
    print(i, 'first', main_ct)

    if i < 13:
        maxes_first = maxes[i+1].copy()
        maxes_first.sort(key=lambda x: -x[0])
        maxes[i].sort(key=lambda x: -sum(x))
        k = 0
        for j in range(len(maxes)):
            while maxes_first[j][0] < sum(maxes[i][k]):
                k += 1
                if k >= len(maxes): break
            main_ct += len(maxes) - k
            if k >= len(maxes): break
        print(i, 'second', main_ct)

print(main_ct)