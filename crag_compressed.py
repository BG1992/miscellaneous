from itertools import combinations, product

scores_cats = [1,2,3,4,5,6,20,30,40,50]
scores_cats = [1,2,3,4,5,6,20,20,20,20,25,26,50]

ct = 0
scores_set = [set() for _ in range(len(scores_cats)+1)]
scores_set[len(scores_cats)].add((frozenset(), 0))
s = {i for i in range(len(scores_cats))}
for r in range(1, len(scores_cats)+1):
    for comb in combinations([i for i in range(len(scores_cats))], r):
        left_ct = sum(el <= 5 for el in comb)
        right_ct = len(comb) - left_ct
        for left_prod in product([i for i in range(4)], repeat=left_ct):
            sm_left = 0
            for k in range(len(left_prod)):
                sm_left += left_prod[k]*scores_cats[k]
            for right_prod in product([j for j in range(2)], repeat=right_ct):
                sm_right = 0
                for k in range(len(right_prod)):
                    sm_right += right_prod[k]*scores_cats[k+6]
                _comb = set(comb)
                scores_set[len(s) - len(comb)].add((frozenset(s.difference(_comb)), sm_left+sm_right))
        print(r, comb, len(scores_set))

main_ct = 0
scores_lists = [[] for _ in range(len(scores_set))]
for i in range(len(scores_set)):
    for el in scores_set[i]:
        rem = 0
        for j in range(len(scores_cats)):
            if j in el[0]:
                if j <= 5: rem += scores_cats[j]*3
                else: rem += scores_cats[j]
        scores_lists[i].append((el[0], el[1], rem))
    print(i, len(scores_set[i])*len(scores_set[i]))
    main_ct += len(scores_set[i])*len(scores_set[i])

print(main_ct)

del scores_set
# for el in scores_lists[1]:
#     print(el)

ct = 0
for r_left in range(1, len(scores_lists)):

    data_left = scores_lists[r_left].copy()
    data_left.sort(key=lambda x:-x[1])
    data_right = scores_lists[r_left].copy()
    data_right.sort(key=lambda x:-(x[1]+x[2]))

    j = 0
    for i in range(len(data_left)):
        if j < len(data_right):
            while data_left[i][1] <= sum(data_right[j][1:]):
                ct += 1
                #calc expectimax
                j += 1
                if j == len(data_right): break
        else:
            ct += len(data_left)-i-1
            #calc expectimax
            pass

    data_left.sort(key=lambda x: -(x[1]+x[2]))
    data_right = scores_lists[r_left-1].copy()
    data_right.sort(key=lambda x: -x[1])

    j = 0
    for i in range(len(data_right)):
        if j < len(data_left):
            while data_right[i][1] <= sum(data_left[j][1:]):
                ct += 1
                # calc expectimin
                j += 1
                if j == len(data_left): break
        else:
            ct += len(data_left)-i-1
            # calc expectimin
            pass

print(ct)