from itertools import combinations

vecs = [(0,1), (0,-1), (1,0), (-1,0), (1,1), (1,-1), (-1,1), (-1,-1)]
winning = set()
winning.add(frozenset({(0,0), (0,1), (0,2), (0,3)}))
winning.add(frozenset({(0,1), (0,2), (0,3), (0,4)}))
winning.add(frozenset({(1,0), (1,1), (1,2), (1,3)}))
winning.add(frozenset({(1,1), (1,2), (1,3), (1,4)}))
winning.add(frozenset({(2,0), (2,1), (2,2), (2,3)}))
winning.add(frozenset({(2,1), (2,2), (2,3), (2,4)}))
winning.add(frozenset({(3,0), (3,1), (3,2), (3,3)}))
winning.add(frozenset({(3,1), (3,2), (3,3), (3,4)}))
winning.add(frozenset({(4,0), (4,1), (4,2), (4,3)}))
winning.add(frozenset({(4,1), (4,2), (4,3), (4,4)}))

winning.add(frozenset({(0,0), (1,0), (2,0), (3,0)}))
winning.add(frozenset({(1,0), (2,0), (3,0), (4,0)}))
winning.add(frozenset({(0,1), (1,1), (2,1), (3,1)}))
winning.add(frozenset({(1,1), (2,1), (3,1), (4,1)}))
winning.add(frozenset({(0,2), (1,2), (2,2), (3,2)}))
winning.add(frozenset({(1,2), (2,2), (3,2), (4,2)}))
winning.add(frozenset({(0,3), (1,3), (2,3), (3,3)}))
winning.add(frozenset({(1,3), (2,3), (3,3), (4,3)}))
winning.add(frozenset({(0,4), (1,4), (2,4), (3,4)}))
winning.add(frozenset({(1,4), (2,4), (3,4), (4,4)}))

winning.add(frozenset({(0,3), (1,2), (2,1), (3,0)}))
winning.add(frozenset({(0,4), (1,3), (2,2), (3,1)}))
winning.add(frozenset({(1,3), (2,2), (3,1), (4,0)}))
winning.add(frozenset({(1,4), (2,3), (3,2), (4,1)}))

winning.add(frozenset({(1,0), (2,1), (3,2), (4,3)}))
winning.add(frozenset({(0,0), (1,1), (2,2), (3,3)}))
winning.add(frozenset({(1,1), (2,2), (3,3), (4,4)}))
winning.add(frozenset({(0,1), (1,2), (2,3), (3,4)}))

def states_after_move(state, pawn):
    states = []
    for vec in vecs:
        i = 1
        while pawn[0] + i*vec[0] <= 4 and pawn[0] + i*vec[0] >= 0 and \
            pawn[1] + i*vec[1] <= 4 and pawn[1] + i*vec[1] >= 0 and \
            (pawn[0] + i*vec[0], pawn[1] + i*vec[1]) not in state[0] and \
            (pawn[0] + i*vec[0], pawn[1] + i*vec[1]) not in state[1]:
            if state[2] == 1:
                _temp = set(state[0]).difference({pawn})
                _temp.add((pawn[0] + i*vec[0], pawn[1] + i*vec[1]))
                states.append((frozenset(_temp), state[1], state[2]*(-1)))
            else:
                _temp = set(state[1]).difference({pawn})
                _temp.add((pawn[0] + i*vec[0], pawn[1] + i*vec[1]))
                states.append((state[0], frozenset(_temp), state[2] *(-1)))
            i += 1
    return states

def next_states(state):
    _next_states = []
    if state[2] == 1:
        for w in state[0]:
            _next_states += states_after_move(state, w)
    else:
        for b in state[1]:
            _next_states += states_after_move(state, b)
    return _next_states

def final_result(state):
    if state[2] == 1:
        for comb in combinations(state[1], 4):
            _comb = frozenset(comb)
            if _comb in winning:
                return -1
        return 0
    else:
        for comb in combinations(state[0], 4):
            _comb = frozenset(comb)
            if _comb in winning:
                return 1
        return 0

memo = {}
finals = [0, 0]
def dfs(state, depth, limit):
    if depth <= 4: print(state, depth, limit, finals)
    _final_result = final_result(state)
    if _final_result in [-1, 1]:
        finals[0] += 1
        return _final_result
    if depth == limit: return 0
    if state[2] == 1:
        res = 0
        for ns in next_states(state):
            next_res = dfs(ns, depth+1, limit)
            if next_res == 1:
                res = 1
                finals[1] += 1
                break
            res = max(res, next_res)
    else:
        res = 0
        for ns in next_states(state):
            next_res = dfs(ns, depth+1, limit)
            if next_res == -1:
                res = -1
                finals[1] += 1
                break
            res = min(res, next_res)
    return res

start = (frozenset({(0,0), (0,2), (0,4), (4,1), (4,3), (2,0)}),
         frozenset({(0,1), (0,3), (4,0), (4,2), (4,4), (2,2)}), 1)

for limit in range(8, 15):
    print(limit, dfs(start, 0, limit))