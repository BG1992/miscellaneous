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

def push(square, white, black, board, vec, squares_3line):
    if square[0] >= 0 and square[0] <= 5 and square[1] >= 0 and square[1] <= 5:
        if square in white or square in black:
            new_square = (square[0] + vec[0], square[1] + vec[1])
            if new_square[0] >= 0 and new_square[0] <= 5 and new_square[1] >= 0 and new_square[1] <= 5:
                if new_square not in white and new_square not in black:
                    if square in white:
                        white.remove(square)
                        white.add(new_square)
                    else:
                        black.remove(square)
                        black.add(new_square)
                    board.remove(new_square)
                    board.add(square)
                    squares_3line.add(new_square)
            else:
                board.add(square)
                if square in white:
                    white.remove(square)
                else:
                    black.remove(square)

def line3_check(square, white, black):
    if square in white:
        color = 1
    else:
        color = 0
    for line in lines3:
        is_3 = True
        for vec in line:
            if square[0] + vec[0] >= 0 and square[0] + vec[0] <= 5 and square[1] + vec[1] >= 0 and square[1] + vec[1] <= 5:
                if color == 1:
                    if (square[0] + vec[0], square[1] + vec[1]) not in white:
                        is_3 = False
                        break
                else:
                    if (square[0] + vec[0], square[1] + vec[1]) not in black:
                        is_3 = False
                        break
            else:
                is_3 = False
                break
        if is_3: return True
    return False

def make_move(white, black, board, white_to_move, move):
    _white, _black, _board = white.copy(), black.copy(), board.copy()
    squares_3line = set()

    if white_to_move == 1:
        _white.add(move)
    else:
        _black.add(move)

    squares_3line.add(move)
    _board.remove(move)

    for vec in vecs:
        push((move[0]+vec[0], move[1]+vec[1]), _white, _black, _board, vec, squares_3line)
    if len(_white) == 8:
        return 1
    for sq in squares_3line:
        line3 = line3_check(sq, _white, _black)
        if line3:
            if sq in _white:
                return 1
            if sq in _black:
                return 0
    return _board, _white, _black

def print_board(white, black):
    tb = [[' ']* 6 for _ in range(6)]
    for w in white:
        tb[w[0]][w[1]] = 'W'
    for b in black:
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
