from core import *

KNIGHT_PVT = ((0, 1, 2, 2, 2, 2, 1, 0),
              (1, 3, 5, 5, 5, 5, 3, 1),
              (2, 5, 6, 7, 7, 6, 5, 2),
              (2, 6, 7, 8, 8, 7, 6, 2),
              (2, 5, 7, 8, 8, 7, 5, 2),
              (2, 6, 5, 7, 7, 5, 6, 2),
              (1, 3, 5, 5, 5, 5, 3, 1),
              (0, 3, 2, 2, 2, 2, 3, 0))

KING_PVT = ((0, 0, 0, 0, 0, 0, 0, 0),
            (0, 0, 0, 0, 0, 0, 0, 0),
            (0, 0, 0, 0, 0, 0, 0, 0),
            (0, 0, 0, 0, 0, 0, 0, 0),
            (2, 0, 0, 0, 0, 0, 0, 2),
            (4, 3, 3, 3, 3, 3, 3, 4),
            (7, 8, 4, 4, 4, 4, 8, 7),
            (8, 9, 5, 5, 5, 5, 9, 8),)

ROOK_PVT = ((5, 5, 5, 5, 5, 5, 5, 5),
            (6, 7, 7, 7, 7, 7, 7, 6),
            (4, 5, 5, 5, 5, 5, 5, 4),
            (4, 5, 5, 5, 5, 5, 5, 4),
            (4, 5, 5, 5, 5, 5, 5, 4),
            (4, 5, 5, 5, 5, 5, 5, 4),
            (4, 5, 5, 5, 5, 5, 5, 4),
            (5, 4, 5, 7, 7, 6, 4, 5),)

PAWN_PVT = ((5, 5, 5, 5, 5, 5, 5, 5),
            (10, 10, 10, 10, 10, 10, 10, 10),
            (6, 6, 7, 8, 8, 7, 6, 5),
            (5, 5, 6, 7, 7, 6, 5, 5),
            (5, 5, 5, 7, 7, 5, 5, 5),
            (6, 4, 4, 5, 5, 4, 4, 6),
            (5, 6, 6, 3, 3, 6, 6, 5),
            (5, 5, 5, 5, 5, 5, 5, 5),)


BISHOP_PVT = ((3, 4, 4, 4, 4, 4, 4, 3),
              (4, 5, 5, 5, 5, 5, 5, 4),
              (4, 5, 6, 7, 7, 6, 5, 4),
              (4, 6, 6, 7, 7, 6, 6, 4),
              (4, 5, 7, 7, 7, 7, 5, 4),
              (4, 6, 7, 7, 7, 7, 6, 4),
              (4, 6, 5, 5, 5, 5, 6, 4),
              (3, 4, 4, 4, 4, 4, 4, 3))

QUEEN_PVT = ((3, 4, 4, 5, 5, 4, 4, 3),
             (4, 5, 5, 5, 5, 5, 5, 4),
             (4, 5, 6, 6, 6, 6, 5, 4),
             (5, 5, 6, 6, 6, 6, 5, 5),
             (5, 5, 6, 6, 6, 6, 5, 5),
             (4, 5, 6, 6, 6, 6, 5, 4),
             (4, 5, 5, 5, 5, 5, 5, 4),
             (3, 4, 4, 5, 5, 4, 4, 3),)


def minimax(board, team, M, depth, alpha, beta, current_eval):
    if depth == 0:
        return (M, current_eval)
    
    if len(M) == 5:
        board = move(board, M)
        n = len(board)
        if depth > 2 and n >= 110:
            if ((board[n - 40:n - 35] == board[n - 20:n - 15]) and
                (board[n - 35:n - 30] == board[n - 15:n - 10]) and
                (board[n - 30:n - 25] == board[n - 10:n - 5]) and
                (board[n - 25:n - 20] == board[n - 5:n])):
                return (M, 0)

    if team:
        best_eval = -math.inf
        best_move = None
        if depth == 1:
            moves = get_moves(board, team)
        else:
            moves = get_sorted_moves(board, team)
        for m in moves:
            mval = minimax(board, not team, m, depth - 1, alpha, beta, current_eval + eval_move(board, m))
            if mval[1] > best_eval:
                best_eval = mval[1]
                best_move = m
            
            alpha = max(best_eval, alpha)
            if beta <= alpha:
                break
        
        if best_move == None:
            x, y = get_king(board, team)
            if in_check(board, team, x, y):
                return (M, -99999999)
            else:
                return (M, 0)
        
        else:
            return (best_move, best_eval)
    
    else:
        best_eval = math.inf
        best_move = None
        if depth == 1:
            moves = get_moves(board, team)
        else:
            moves = get_sorted_moves(board, team)
        for m in moves:
            mval = minimax(board, not team, m, depth - 1, alpha, beta, current_eval + eval_move(board, m))
            if mval[1] < best_eval:
                best_eval = mval[1]
                best_move = m
            
            beta = min(best_eval, beta)
            if beta <= alpha:
                break
        
        if best_move == None:
            x, y = get_king(board, team)
            if in_check(board, team, x, y):
                return (M, 99999999)
            else:
                return (M, 0)
        
        else:
            return (best_move, best_eval)


def evaluate(board):
    total = 0
    for y in range(8):
        for x in range(8):
            total += get_val(board[8 * y + x], x, y)

    return total 


def eval_move(board, m):
    '''new - old - taken'''
    x1, y1, x2, y2, attr = m
    p1 = board[8 * y1 + x1]
    p2 = board[8 * y2 + x2]
    if attr == '-':
        return get_pos_dif(p1, x1, y1, x2, y2) - get_val(p2, x2, y2)
    elif attr == 'p':
        return get_pos_dif(p1, x1, y1, x2, y2) - get_val(board[8 * y1 + x2], x2, y1)
    elif attr == 'c':
        return get_pos_dif(p1, x1, y1, x2, y2) * 2



def get_pos_dif(p, x1, y1, x2, y2):
    if p == 'P':
        return  PAWN_PVT[7 - y2][x2] - PAWN_PVT[7 - y1][x1]
    elif p == 'p':
        return PAWN_PVT[y1][x1] - PAWN_PVT[y2][x2]
    elif p == 'N':
        return KNIGHT_PVT[7 - y2][x2] - KNIGHT_PVT[7 - y1][x1]
    elif p == 'n':
        return KNIGHT_PVT[y1][x1] - KNIGHT_PVT[y2][x2]
    elif p == 'B':
        return BISHOP_PVT[7 - y2][x2] - BISHOP_PVT[7 - y1][x1]
    elif p == 'b':
        return BISHOP_PVT[y1][x1] - BISHOP_PVT[y2][x2]
    elif p == 'R':
        return ROOK_PVT[7 - y2][x2] - ROOK_PVT[7 - y1][x1]
    elif p == 'r':
        return ROOK_PVT[y1][x1] - ROOK_PVT[y2][x2]
    elif p == 'Q':
        return QUEEN_PVT[7 - y2][x2] - QUEEN_PVT[7 - y1][x1]
    elif p == 'q':
        return QUEEN_PVT[y1][x1] - QUEEN_PVT[y2][x2]
    elif p == 'K':
        return KING_PVT[7 - y2][x2] - KING_PVT[7 - y1][x1]
    elif p == 'k':
        return KING_PVT[y1][x1] - KING_PVT[y2][x2]


def get_val(p, x, y):
    if p == 'P':
        return 100 + PAWN_PVT[7 - y][x]
    elif p == 'p':
        return -100 - PAWN_PVT[y][x]
    elif p == 'N':
        return 300 + KNIGHT_PVT[7 - y][x]
    elif p == 'n':
        return -300 - KNIGHT_PVT[y][x]
    elif p == 'B':
        return 305 + BISHOP_PVT[7 - y][x]
    elif p == 'b':
        return -305 - BISHOP_PVT[y][x]
    elif p == 'R':
        return 500 + ROOK_PVT[7 - y][x]
    elif p == 'r':
        return -500 - ROOK_PVT[y][x]
    elif p == 'Q':
        return 900 + QUEEN_PVT[7 - y][x]
    elif p == 'q':
        return -900 - QUEEN_PVT[y][x]
    elif p == 'K':
        return KING_PVT[7 - y][x]
    elif p == 'k':
        return -KING_PVT[y][x]
    else:
        return 0

def get_sorted_moves(board, team):
    candidates = []
    for m in get_moves(board, team):
        candidates.append((eval_move(board, m), m))
    candidates.sort()
    sorted_moves = []
    if team:
        for c in reversed(candidates):
            sorted_moves.append(c[1])
    else:
        for c in candidates:
            sorted_moves.append(c[1])
            
    return sorted_moves
