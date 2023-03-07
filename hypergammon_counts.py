from collections import defaultdict
from itertools import combinations_with_replacement

memo = defaultdict(int)
posses_white = set([i for i in range(25)])
posses_black = set([i for i in range(1, 26)])

ind = 0
for r_white in range(3, 4):
    for comb_white in combinations_with_replacement(posses_white, r_white):
        print(ind, comb_white)
        _comb_white = set(comb_white)
        for r_black in range(3, 4):
            for comb_black in combinations_with_replacement(posses_black.difference(_comb_white), r_black):
                if len(comb_white) == 0 and len(comb_black) == 0: score = None
                elif len(comb_white) == 0 and len(comb_black) != 0: score = 1
                elif len(comb_white) != 0 and len(comb_black) == 0: score = -1
                else: score = 0
                if score == 0:
                    if 0 not in comb_white and 25 not in comb_black:
                        if min(comb_white) > max(comb_black):
                            memo['final'] += 2
                        else:
                            memo['not final'] += 2
                    else:
                        memo['not final'] += 2
                    ind += 1

print(ind, memo)