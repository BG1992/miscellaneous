from random import choice

vecs = [[0,1], [1,0], [1,1], [0,-1], [-1,0], [-1,-1], [-1,1], [1,-1]]
lines3 = [[[1,0],[2,0]], [[1,0],[-1,0]], [[-1,0],[-2,0]], [[0,1],[0,2]], [[0,1],[0,-1]], [[0,-1],[0,-2]],
            [[1,1],[-1,-1]], [[1,1],[2,2]], [[-1,-1], [-2,-2]], [[-1,1],[-2,2]], [[-1,1],[1,-1]], [[1,-1], [2,-2]]]


def sym_horizontal(s):
    _s = set()
    for w in s:
        _s.add((5 - w[0], w[1]))
    return _s

def sym_vertical(s):
    _s = set()
    for w in s:
        _s.add((w[0], 5 - w[1]))
    return _s

def sym_left_diag(s):
    _s = set()
    for w in s:
        _s.add((w[1], w[0]))
    return _s

def sym_right_diag(s):
    _s = set()
    for w in s:
        _s.add((5 - w[1], 5 - w[0]))
    return _s

def rot_90(s):
    _s = set()
    for w in s:
        _s.add((w[1], 5-w[0]))
    return _s

class Board():
    def __init__(self, state=None):
        if state is None:
            self.white = set()
            self.black = set()
            self.board = {(i,j) for i in range(6) for j in range(6)}
            self.result = None
        else:
            self.white, self.black = state[0], state[1]
            self.board = {(i,j) for i in range(6) for j in range(6)}.difference(self.white.union(self.black))
            self.result = None

    def available_moves(self):
        return self.board

    def push(self, square, vec, squares_3line):
        if square[0] >= 0 and square[0] <= 5 and square[1] >= 0 and square[1] <= 5:
            if square in self.white or square in self.black:
                new_square = (square[0] + vec[0], square[1] + vec[1])
                if new_square[0] >= 0 and new_square[0] <= 5 and new_square[1] >= 0 and new_square[1] <= 5:
                    if new_square not in self.white and new_square not in self.black:
                        if square in self.white:
                            self.white.remove(square)
                            self.white.add(new_square)
                        else:
                            self.black.remove(square)
                            self.black.add(new_square)
                        self.board.remove(new_square)
                        self.board.add(square)
                        squares_3line.add(new_square)
                else:
                    self.board.add(square)
                    if square in self.white:
                        self.white.remove(square)
                    else:
                        self.black.remove(square)

    def line3_check(self, square):
        if square in self.white:
            color = 1
        else:
            color = 0
        for line in lines3:
            is_3 = True
            for vec in line:
                if square[0] + vec[0] >= 0 and square[0] + vec[0] <= 5 and square[1] + vec[1] >= 0 and square[1] + vec[1] <= 5:
                    if color == 1:
                        if (square[0] + vec[0], square[1] + vec[1]) not in self.white:
                            is_3 = False
                            break
                    else:
                        if (square[0] + vec[0], square[1] + vec[1]) not in self.black:
                            is_3 = False
                            break
                else:
                    is_3 = False
                    break
            if is_3: return True
        return False

    def reverse_pawns(self):
        self.white, self.black = self.black, self.white

    def make_move(self, move):
        squares_3line = set()
        board8_before_push = len(self.white) == 7
        squares_3line.add(move)
        self.white.add(move)
        self.board.remove(move)
        for vec in vecs:
            self.push((move[0]+vec[0], move[1]+vec[1]), vec, squares_3line)
        if len(self.white) == 8 and board8_before_push:
            self.result = 1
            return
        for sq in squares_3line:
            line3 = self.line3_check(sq)
            if line3:
                if sq in self.white:
                    self.result = 1
                    return
                if sq in self.black:
                    self.result = 0
                    return
        self.reverse_pawns()

    def print(self):
        tb = [[' ']* 6 for _ in range(6)]
        for w in self.white:
            tb[w[0]][w[1]] = 'W'
        for b in self.black:
            tb[b[0]][b[1]] = 'B'
        for row in tb:
            print(row)

# board = Board()
# while board.result is None:
#     moves = board.available_moves()
#     move = choice(list(moves))
#     board.make_move(move)
#     print(move)
#     board.print()
#     print()
