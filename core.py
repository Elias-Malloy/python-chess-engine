import math
import random
import time
import cProfile, pstats


def print_board(board, team):
    if team:
        s = ''
        for y in range(7, -1, -1):
            s += '\n'
            s += str(y + 1) + ' '
            for x in range(8):
                if board[8 * y + x] == ' ':
                    s += '· '
                else:
                    s += board[8 * y + x] + ' '

        s += '\n  a b c d e f g h'
        print(s)
    else:
        s = ''
        for y in range(8):
            s += '\n'
            s += str(y+1) + ' '
            for x in range(8):
                if board[8 * y + x] == ' ':
                    s += '· '
                else:
                    s += board[8 * y + x] + ' '

        s += '\n  a b c d e f g h'
        print(s)


def move(board, m):
    '''attr (- none, p en_passant, c castle) m[0] = x1, m[1] = y1, m[2] = x2, m[3] = y2, m[4] = attr'''
    if board[65:67] != '--':
        if board[8 * m[1] + m[0]] == 'K':
            board = board[:65] + '--' + board[67:]
        
        elif board[8 * m[1] + m[0]] == 'R':
            if board[65] != '-' and m[0] == 7:
                board = board[:65] + '-' + board[66:]
            
            elif board[66] != '-' and m[0] == 0:
                board = board[:66] + '-' + board[67:]

    if board[67:69] != '--':
        if board[8 * m[1] + m[0]] == 'k':
            board = board[:67] + '--' + board[69:]
        
        elif board[8 * m[1] + m[0]] == 'r':
            if board[67] != '-' and m[0] == 7:
                board = board[:67] + '-' + board[68:]
            
            elif board[68] != '-' and m[0] == 0:
                board = board[:68] + '-' + board[69:]

    if m[4] == '-':
        board = make_move(board, m[:4])
        
        if m[3] == 7 and board[8 * m[3] + m[2]] == 'P': #PAWN PROMO
            board = board[:8 * m[3] + m[2]] + 'Q' + board[8 * m[3] + m[2] + 1:]
        elif m[3] == 0 and board[8 * m[3] + m[2]] == 'p':
            board = board[:8 * m[3] + m[2]] + 'q' + board[8 * m[3] + m[2] + 1:]

    elif m[4] == 'p':
        board = make_move(board, m[:4])
        if m[1] < m[3]:
            board = board[:8 * (m[3] - 1) + m[2]] + ' ' + board[8 * (m[3] - 1) + m[2] + 1:]
        else:
            board = board[:8 * (m[3] + 1) + m[2]] + ' ' + board[8 * (m[3] + 1) + m[2] + 1:]

    elif m[4] == 'c':
        board = make_move(board, m[:4])
        if m[0] < m[2]:
            board = make_move(board, (m[2] + (m[2] - m[0]) // 2, m[1], m[0] + (m[2] - m[0]) // 2, m[3]))
        else:
            board = make_move(board, (m[2] + (m[2] - m[0]), m[1], m[0] + (m[2] - m[0]) // 2, m[3]))            

    board += f'{m[0]}{m[1]}{m[2]}{m[3]}{m[4]}' # prev moves
    return board


def make_move(board, m):
    board = board[:8 * m[3] + m[2]] + board[8 * m[1] + m[0]] + board[8 * m[3] + m[2] + 1:]
    board = board[:8 * m[1] + m[0]] + ' ' + board[8 * m[1] + m[0] + 1:]
    return board


def get_attackers(board, team, x, y):
    if team:
        if x > 0:
            yield check_square(board, x - 1, y, 'k')
            yield check_path(board, team, x, y, -1, 0, x + 1)
            if y > 0:
                yield check_square(board, x - 1, y - 1, 'k')
                yield check_path(board, team, x, y, -1, -1, min(x + 1, y + 1))
                if x > 1:
                    yield check_square(board, x - 2, y - 1, 'n')
                if y > 1:
                    yield check_square(board, x - 1, y - 2, 'n')
            if y < 7:
                yield check_square(board, x - 1, y + 1, 'pk')
                yield check_path(board, team, x, y, -1, 1, min(x + 1, 8 - y))
                if x > 1:
                    yield check_square(board, x - 2, y + 1, 'n')
                if y < 6:
                    yield check_square(board, x - 1, y + 2, 'n')
            
        if x < 7:
            yield check_square(board, x + 1, y, 'k')
            yield check_path(board, team, x, y, 1, 0, 8 - x)
            if y > 0:
                yield check_square(board, x + 1, y - 1, 'k')
                yield check_path(board, team, x, y, 1, -1, min(8 - x, y + 1))
                if x < 6:
                    yield check_square(board, x + 2, y - 1, 'n')
                if y > 1:
                    yield check_square(board, x + 1, y - 2, 'n')
            if y < 7:
                yield check_square(board, x + 1, y + 1, 'pk')
                yield check_path(board, team, x, y, 1, 1, min(8 - x, 8 - y))
                if x < 6:
                    yield check_square(board, x + 2, y + 1, 'n')
                if y < 6:
                    yield check_square(board, x + 1, y + 2, 'n')
                    
        if y < 7:
            yield check_path(board, team, x, y, 0, 1, 8 - y)
            yield check_square(board, x, y + 1, 'k')
        if y > 0:
            yield check_path(board, team, x, y, 0, -1, y + 1)
            yield check_square(board, x, y - 1, 'k')
    
    else:
        if x > 0:
            yield check_square(board, x - 1, y, 'K')
            yield check_path(board, team, x, y, -1, 0, x + 1)
            if y > 0:
                yield check_square(board, x - 1, y - 1, 'PK')
                yield check_path(board, team, x, y, -1, -1, min(x + 1, y + 1))
                if x > 1:
                    yield check_square(board, x - 2, y - 1, 'N')
                if y > 1:
                    yield check_square(board, x - 1, y - 2, 'N')
            if y < 7:
                yield check_square(board, x - 1, y + 1, 'K')
                yield check_path(board, team, x, y, -1, 1, min(x + 1, 8 - y))
                
                if x > 1:
                    yield check_square(board, x - 2, y + 1, 'N')
                if y < 6:
                    yield check_square(board, x - 1, y + 2, 'N')
            
        if x < 7:
            yield check_square(board, x + 1, y, 'K')
            yield check_path(board, team, x, y, 1, 0, 8 - x)
            if y > 0:
                yield check_square(board, x + 1, y - 1, 'PK')
                yield check_path(board, team, x, y, 1, -1, min(8 - x, y + 1))
                if x < 6:
                    yield check_square(board, x + 2, y - 1, 'N')
                if y > 1:
                    yield check_square(board, x + 1, y - 2, 'N')
            if y < 7:
                yield check_square(board, x + 1, y + 1, 'K')
                yield check_path(board, team, x, y, 1, 1, min(8 - x, 8 - y))
                if x < 6:
                    yield check_square(board, x + 2, y + 1, 'N')
                if y < 6:
                    yield check_square(board, x + 1, y + 2, 'N')
        
        if y < 7:
            yield check_path(board, team, x, y, 0, 1, 8 - y)
            yield check_square(board, x, y + 1, 'K')
        if y > 0:
            yield check_path(board, team, x, y, 0, -1, y + 1)
            yield check_square(board, x, y - 1, 'K')


def check_path(board, team, x, y, horz, vert, dist):
    piece_blocking = 0
    if team:
        q = 'q'
        if vert == 0 or horz == 0:
            threat = 'r'
        else:
            threat = 'b'
    else:
        q = 'Q'
        if vert == 0 or horz == 0:
            threat = 'R'
        else:
            threat = 'B'
    
    for n in range(1, dist):
        p = board[8 * (y + n * vert) + x + n * horz]
        if p == ' ':
            continue
        if p == q or p == threat:
            return (x + n * horz, y + n * vert, piece_blocking)
        elif piece_blocking != 0: #Here if its another piece blocking
            break
        else:
            piece_blocking = (x + n * horz, y + n * vert)
    
    return None


def check_square(board, x, y, t):
    if board[8 * y + x] in t:
        return (x, y, 2)
    return None
    

def in_check(board, team, x, y):
    for a in get_attackers(board, team, x, y):
        if a == None:
            continue
        elif a[2] == 2 or a[2] == 0:
            return True
    
    return False


def attackers_threats(board, team, x, y):
    static = ()
    dynamic = []
    potential = []
    for a in get_attackers(board, team, x, y):
        if a == None:
            continue
        elif a[2] == 2:
            static = a
        elif a[2] == 0:
            dynamic.append(a)
        else:
            potential.append(a)

    return (static, dynamic, potential)


def get_moves(board, team):
    kx, ky = get_king(board, team)
    static, dynamic, potential = attackers_threats(board, team, kx, ky)
    if team:
        p = 'P'
        n = 'N'
        b = 'B'
        r = 'R'
        q = 'Q'
        k = 'K'
        nt = ' pnbrqk'
    else:
        p = 'p'
        n = 'n'
        b = 'b'
        r = 'r'
        q = 'q'
        k = 'k'
        nt = ' PNBRQK'
 
    for y in range(8):
        for x in range(8):
            piece = board[8 * y + x]
            if piece in nt:
                continue

            if piece == p:
                move_gen = pawn_moves(board, team, x, y)

            if piece == n:
                move_gen = knight_moves(board, team, x, y)

            if piece == b:
                move_gen = bishop_moves(board, team, x, y)

            if piece == r:
                move_gen = rook_moves(board, team, x, y)
       
            if piece == q:
                move_gen = queen_moves(board, team, x, y)

            if piece == k:
                move_gen = king_moves(board, team, x, y)
    
            for m in move_gen:
                x1, y1, x2, y2, a = m
                if x1 == kx and y1 == ky:
                    if in_check(move(board, m), team, x2, y2) == False:
                        yield m
                        continue
                    else:
                        continue
                if static:
                    if (x2, y2) != (static[0], static[1]):
                        continue
                if dynamic and check_dynamic(dynamic, kx, ky, x2, y2):
                    continue
                if potential and check_potential(potential, kx, ky, x1, y1, x2, y2):
                    continue
                
                yield m
    
    for m in castle_moves(board, team):
        yield m

        
def check_dynamic(dynamic, kx, ky, x2, y2):
    for ax, ay, b in dynamic:
        if ay == ky:
            if y2 == ay:
                if (ax >= x2 > kx or kx > x2 >= ax) == False:
                    return True
            else:
                return True
        
        if ax == kx:
            if x2 == ax:
                if (ay >= y2 > ky or ky > y2 >= ay) == False:
                    return True
            else:
                return True
            
        if ky - kx == ay - ax:
            if ay - ax == y2 - x2:
                if (ay >= y2 > ky or ky > y2 >= ay) == False:
                    return True
            else:
                return True

        elif ky + kx == ay + ax:
            if ay + ax == y2 + x2:
                if (ax >= x2 > kx or kx > x2 >= ax) == False:
                    return True
            else:
                return True
    
    return False


def check_potential(potential, kx, ky, x1, y1, x2, y2):
    for ax, ay, b in potential:
        if (x1, y1) != b:
            continue
        if ay == ky:
            if y2 == ay:
                if (ax >= x2 > kx or kx > x2 >= ax) == False:
                    return True
            else:
                return True
        
        elif ax == kx:
            if x2 == ax:
                if (ay >= y2 > ky or ky > y2 >= ay) == False:
                    return True
            else:
                return True
            
        elif ky - kx == ay - ax:
            if ay - ax == y2 - x2:
                if (ay >= y2 > ky or ky > y2 >= ay) == False:
                    return True
            else:
                return True

        elif ky + kx == ay + ax:
            if ay + ax == y2 + x2:
                if (ay >= y2 > ky or ky > y2 >= ay) == False:
                    return True
            else:
                return True
    
    return False

       
def pawn_moves(board, team, x, y):
    if team:
        if board[8 * (y + 1) + x] == ' ':
            yield (x, y, x, y + 1, '-')
            if y == 1 and board[8 * (y + 2) + x] == ' ':
                yield(x, y, x, y + 2, '-')
        
        if x < 7:
            p = board[8 * (y + 1) + x + 1]
            if p != ' ' and p.lower() == p:
                yield (x, y, x + 1, y + 1, '-')
        
        if x > 0:
            p = board[8 * (y + 1) + x - 1]
            if p != ' ' and p.lower() == p:
                yield (x, y, x - 1, y + 1, '-')
        
        if y == 4:
            if (x > 0 and board[8 * y + x - 1] == 'p' and
            int(board[-5]) == x - 1 and int(board[-4]) == 6 and
            int(board[-3]) == x - 1 and int(board[-2]) == 4):
                yield (x, y, x - 1, y + 1, 'p')
            
            if (x < 7 and board[8 * y + x + 1] == 'p' and
            int(board[-5]) == x + 1 and int(board[-4]) == 6 and
            int(board[-3]) == x + 1 and int(board[-2]) == 4):
                yield (x, y, x + 1, y + 1, 'p')
    else:
        if board[8 * (y - 1) + x] == ' ':
            yield (x, y, x, y - 1, '-')
            if y == 6 and board[8 * (y - 2) + x] == ' ':
                yield(x, y, x, y - 2, '-')
        
        if x < 7:
            p = board[8 * (y - 1) + x + 1]
            if p != ' ' and p.upper() == p:
                yield (x, y, x + 1, y - 1, '-')
        
        if x > 0:
            p = board[8 * (y - 1) + x - 1]
            if p != ' ' and p.upper() == p:
                yield (x, y, x - 1, y - 1, '-')
        
        if y == 3:
            if (x > 0 and board[8 * y + x - 1] == 'P' and
            int(board[-5]) == x - 1 and int(board[-4]) == 1 and
            int(board[-3]) == x - 1 and int(board[-2]) == 3):
                yield (x, y, x - 1, y - 1, 'p')
            
            if (x < 7 and board[8 * y + x + 1] == 'P' and
            int(board[-5]) == x + 1 and int(board[-4]) == 1 and
            int(board[-3]) == x + 1 and int(board[-2]) == 3):
                yield (x, y, x + 1, y - 1, 'p')


def knight_moves(board, team, x, y):
    if y > 1:
        down2 = True
        down1 = True
    elif y > 0:
        down2 = False
        down1 = True
    else:
        down2 = False
        down1 = False
    
    if y < 6:
        up2 = True
        up1 = True
    elif y < 7:
        up2 = False
        up1 = True
    else:
        up2 = False
        up1 = False
        
    if x > 1:
        if up1 and add_square(board[8 * (y + 1) + x - 2], team):
            yield (x, y, x - 2, y + 1, '-')
        if down1 and add_square(board[8 * (y - 1) + x - 2], team):
            yield (x, y, x - 2, y - 1, '-')
        if up2 and add_square(board[8 * (y + 2) + x - 1], team):
            yield (x, y, x - 1, y + 2, '-')
        if down2 and add_square(board[8 * (y - 2) + x - 1], team):
            yield (x, y, x - 1, y - 2, '-')
        
    elif x > 0:
        if up2 and add_square(board[8 * (y + 2) + x - 1], team):
            yield (x, y, x - 1, y + 2, '-')
        if down2 and add_square(board[8 * (y - 2) + x - 1], team):
            yield (x, y, x - 1, y - 2, '-')
    
    if x < 6:
        if up1 and add_square(board[8 * (y + 1) + x + 2], team):
            yield (x, y, x + 2, y + 1, '-')
        if down1 and add_square(board[8 * (y - 1) + x + 2], team):
            yield (x, y, x + 2, y - 1, '-')
        if up2 and add_square(board[8 * (y + 2) + x + 1], team):
            yield (x, y, x + 1, y + 2, '-')
        if down2 and add_square(board[8 * (y - 2) + x + 1], team):
            yield (x, y, x + 1, y - 2, '-')
    
    elif x < 7:
        if up2 and add_square(board[8 * (y + 2) + x + 1], team):
            yield (x, y, x + 1, y + 2, '-')
        if down2 and add_square(board[8 * (y - 2) + x + 1], team):
            yield (x, y, x + 1, y - 2, '-')


def add_square(p, team):
    if team:
        if p == ' ' or p.lower() == p:
            return True
    else:
        if p == ' ' or p.upper() == p:
            return True
        

def rook_moves(board, team, x, y):
    for m in add_line(board, team, x, y, 1, 0, 8 - x):
        yield m
    
    for m in add_line(board, team, x, y, -1, 0, 1 + x):
        yield m
    
    for m in add_line(board, team, x, y, 0, 1, 8 - y):
        yield m
    
    for m in add_line(board, team, x, y, 0, -1, 1 + y):
        yield m

def queen_moves(board, team, x, y):
    for m in add_line(board, team, x, y, 1, 1, min(8 - x, 8 - y)):
        yield m
    
    for m in add_line(board, team, x, y, -1, 1, min(x + 1, 8 - y)):
        yield m
    
    for m in add_line(board, team, x, y, 1, -1, min(8 - x, y + 1)):
        yield m
    
    for m in add_line(board, team, x, y, -1, -1, min(x + 1, y + 1)):
        yield m
    
    for m in add_line(board, team, x, y, 1, 0, 8 - x):
        yield m
    
    for m in add_line(board, team, x, y, -1, 0, 1 + x):
        yield m
    
    for m in add_line(board, team, x, y, 0, 1, 8 - y):
        yield m
    
    for m in add_line(board, team, x, y, 0, -1, 1 + y):
        yield m


def add_line(board, team, x, y, horz, vert, dist):
    if team:
        for n in range(1, dist):
            p = board[8 * (y + n * vert) + x + n * horz]
            if p == ' ':
                yield (x, y, x + n * horz, y + n * vert, '-')
            elif p.lower() == p:
                yield (x, y, x + n * horz, y + n * vert, '-')
                break
            else:
                break
    
    else:
        for n in range(1, dist):
            p = board[8 * (y + n * vert) + x + n * horz]
            if p == ' ':
                yield (x, y, x + n * horz, y + n * vert, '-')
            elif p.upper() == p:
                yield (x, y, x + n * horz, y + n * vert, '-')
                break
            else:
                break

def bishop_moves(board, team, x, y):
    for m in add_line(board, team, x, y, 1, 1, min(8 - x, 8 - y)):
        yield m
    
    for m in add_line(board, team, x, y, -1, 1, min(x + 1, 8 - y)):
        yield m
    
    for m in add_line(board, team, x, y, 1, -1, min(8 - x, y + 1)):
        yield m
    
    for m in add_line(board, team, x, y, -1, -1, min(x + 1, y + 1)):
        yield m


def king_moves(board, team, x, y):
    if x < 7:
        if add_square(board[8 * y + x + 1], team):
            yield (x, y, x + 1, y, '-')
        if y < 7:
            if add_square(board[8 * (y + 1) + x + 1], team):
                yield (x, y, x + 1, y + 1, '-')
            
            if add_square(board[8 * (y + 1) + x], team):
                yield (x, y, x, y + 1, '-')
        
        if y > 0:
            if add_square(board[8 * (y - 1) + x + 1], team):
                yield (x, y, x + 1, y - 1, '-')
            if add_square(board[8 * (y - 1) + x], team):
                yield (x, y, x, y - 1, '-')
    if x > 0:
        if add_square(board[8 * y + x - 1], team):
            yield (x, y, x - 1, y, '-')
        
        if y < 7:
            if add_square(board[8 * (y + 1) + x - 1], team):
                yield (x, y, x - 1, y + 1, '-')
        if y > 0:
            if add_square(board[8 * (y - 1) + x - 1], team):
                yield (x, y, x - 1, y - 1, '-')


def castle_moves(board, team):
    if team:
        k_side = board[65] == 'T'
        q_side = board[66] == 'T'
        r = 'R'
    else:
        k_side = board[67] == 'T'
        q_side = board[68] == 'T'
        r = 'r'
        
    x, y = get_king(board, team)
    
    if (k_side and board[8 * y + x + 3] == r and board[8 * y + x + 2] == ' ' and
        board[8 * y + x + 1] == ' ' and in_check(board, team, x, y) == False and
        in_check(move(board, (x, y, x + 1, y, '-')), team, x + 1, y) == False and
        in_check(move(board, (x, y, x + 2, y, '-')), team, x + 2, y) == False):
        yield (x, y, x + 2, y, 'c')
    
    if (q_side and board[8 * y + x - 4] == r and board[8 * y + x - 3] == ' ' and
        board[8 * y + x - 2] == ' ' and board[8 * y + x - 1] == ' ' and
        in_check(board, team, x, y) == False and
        in_check(move(board, (x, y, x - 1, y, '-')), team, x - 1, y) == False and
        in_check(move(board, (x, y, x - 2, y, '-')), team, x - 2, y) == False):
        yield (x, y, x - 2, y, 'c')


def get_king(board, team):
    if team:
        for y in range(8):
            for x in range(8):
                if board[8 * y + x] == 'K':
                    return (x, y)
    else:
        for y in range(7, -1, -1):
            for x in range(8):
                if board[8 * y + x] == 'k':
                    return (x, y)
    
    print(board, team)
    exit('get_king, king taken!')


def check_loss(board, moves, team):
    if len(board) >= 75:
        prev = board[70:]
        sim = standard_set()
        draw_counter = 0
        positions = []
        for i in range(len(prev)): #forgive me
            if (i + 1) % 5 == 0:
                draw_counter += 1
                m = (int(prev[i-4]), int(prev[i-3]), int(prev[i-2]), int(prev[i-1]), prev[i])
                if sim[8 * m[1] + m[0]] == 'p' or sim[8 * m[3] + m[2]] != ' ':
                    draw_counter = 0
                elif draw_counter == 100:
                    return 'Draw by 50 move rule'
                
                sim = move(sim, m)
                positions.append(sim[:64])
        
        if positions.count(board[:64]) == 3:
            return 'Draw by threefold repetition'
        
    if len(moves) == 0:
        x, y = get_king(board, team)
        if in_check(board, team, x, y):
            return 'Checkmate'
        else:
            return 'Stalemate'
    
    else:
        return 'continue'


def same_team(p, team):
    if p == ' ':
        return False
    if team and p.upper() == p:
        return True
    elif team == False and p.lower() == p:
        return True
    return False


def standard_set():
    return 'RNBQKBNRPPPPPPPP                                pppppppprnbqkbnrwTTTT '

def nopawns_set():
    return 'RNBQKBNR                                                rnbqkbnrwTTTT '

def castle_set():
    return 'R   K  R                                                r   k  rwTTTT '
