import pygame
from core import *
from engine import *

WIDTH, HEIGHT = 800, 800
SQUARE_SIZE = 100
DARK_SQUARE = (196, 158, 133) 
LIGHT_SQUARE = (255, 214, 175)
DARK_HIGHLIGHT = (196, 158, 133)
LIGHT_HIGHLIGHT = (245, 214, 175)


B_BISHOP = pygame.image.load('assets/black_bishop.png')
B_ROOK = pygame.image.load('assets/black_rook.png')
B_KNIGHT = pygame.image.load('assets/black_knight.png')
B_PAWN = pygame.image.load('assets/black_pawn.png')
B_KING = pygame.image.load('assets/black_king.png')
B_QUEEN = pygame.image.load('assets/black_queen.png')

W_BISHOP = pygame.image.load('assets/white_bishop.png')
W_ROOK = pygame.image.load('assets/white_rook.png')
W_KNIGHT = pygame.image.load('assets/white_knight.png')
W_PAWN = pygame.image.load('assets/white_pawn.png')
W_KING = pygame.image.load('assets/white_king.png')
W_QUEEN = pygame.image.load('assets/white_queen.png')


FPS = 60

WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Chess')
surface = pygame.Surface((WIDTH,HEIGHT), pygame.SRCALPHA) #For transparent layers


def run_game(board, turn1, turn2, depth):
    loop = True
    clock = pygame.time.Clock()
    turn = board[64] == 'w'
    moves = []
    for mov in get_moves(board, turn):
        moves.append(mov)
    active_square = ()
    active_moves = []
    game_over = False
    prev_move = ()
    prev_positions = [] #(board, prev_move)
    current = 0

    while loop:
        if current == 0:
            draw_board(WIN, surface, active_square, active_moves, prev_move)
            draw_pieces(board, WIN)
        else:
            if len(prev_positions) > -current:
                draw_board(WIN, surface, (), (), prev_positions[current - 1][1])
            else:
                draw_board(WIN, surface, (), (), ())
            draw_pieces(prev_positions[current][0], WIN)
        pygame.display.update()
        clock.tick(FPS)


        if ((turn and turn1) or (turn == False and turn2)) and game_over == False:
            st = time.time()
            engine_output = minimax(board, turn, (), depth, -math.inf, math.inf, evaluate(board))
            et = time.time()
            print(f'Process time: {et - st:.5f} seconds')
            engine_move = engine_output[0]
            prev_positions.append((board, engine_move))
            board = move(board, engine_move)
            prev_move = engine_move
            
            if turn:
                board = board[:64] + 'b' + board[65:]
            else:
                board = board[:64] + 'w' + board[65:]

            turn = board[64] == 'w'
            moves = []
            for mov in get_moves(board, turn):
                moves.append(mov)
   
            game_state = check_loss(board, moves, turn)
            if game_state != 'continue':
                print(game_state)
                print(board)
                game_over = True


        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                loop = False
                pygame.quit()
                return
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    if len(prev_positions) > -current :
                        current -= 1
                if event.key == pygame.K_RIGHT:
                    if current < 0:
                        current += 1

            if event.type == pygame.MOUSEBUTTONDOWN and game_over == False and current == 0:
                if True:
                    x, y = pygame.mouse.get_pos()
                    x, y = (int(x / 100), 7 - int(y / 100))
                    if (x, y) == active_square:
                        active_square = ()
                        active_moves = []

                    elif active_square == ():
                        p = board[8 * y + x]
                        if same_team(p, turn):
                            active_square = (x, y)
                            active_moves = []
                            for m in moves:
                                if (m[0], m[1]) == active_square:
                                    active_moves.append(m)

                    elif len(active_square) == 2:
                        moved = False
                        for m in active_moves:
                            if (x, y) == (m[2], m[3]):
                                prev_positions.append((board, m))
                                kx, ky = get_king(board, turn)
                                c = in_check(board, turn, kx, ky)
                                board = move(board, m)
                                prev_move = m
                                moved = True

                        active_moves = []
                        active_square = ()
                        if moved:
                            if turn:
                                board = board[:64] + 'b' + board[65:]
                            else:
                                board = board[:64] + 'w' + board[65:]
                            turn = board[64] == 'w'
                            moves = []
                            for mov in get_moves(board, turn):
                                moves.append(mov)
                            game_state = check_loss(board, moves, turn)
                            if game_state != 'continue':
                                print(game_state)
                                print(board)
                                game_over = True

    
def draw_board(win, layer, active_s, active_m, prev_move):
    win.fill(LIGHT_SQUARE)
    surface.fill(0)
    for y in range(8):
        for x in range(8):
            if (y % 2 == 0 and x % 2 == 1) or (y % 2 == 1 and x % 2 == 0):
                pygame.draw.rect(win, DARK_SQUARE, (SQUARE_SIZE * x, SQUARE_SIZE * y, SQUARE_SIZE, SQUARE_SIZE))
    
    if len(prev_move) != 0:
        pygame.draw.rect(layer,(250, 207, 65, 100),(100 * prev_move[0], 100 * (7 - prev_move[1]), 100, 100))
        pygame.draw.rect(layer,(250, 207, 65, 100),(100 * prev_move[2], 100 * (7 - prev_move[3]), 100, 100))
    
    if len(active_s) == 2:
        pygame.draw.rect(layer,(250, 207, 65, 100),(100 * active_s[0], 100 * (7 - active_s[1]), 100, 100))
    
    for m in active_m:
        pygame.draw.circle(layer,(0, 0, 0,100),(100 * m[2] + 50, 100 * (7 - m[3]) + 50),15)
    
    win.blit(layer, (0,0))

def draw_pieces(board, win):
    for y in range(8):
        for x in range(8):
            disp_y = (7-y) * 100
            disp_x = x * 100
            if board[8 * y + x] == 'P':
                win.blit(W_PAWN, (disp_x, disp_y))
            
            elif board[8 * y + x] == 'p':
                win.blit(B_PAWN, (disp_x, disp_y))
            
            elif board[8 * y + x] == 'R':
                win.blit(W_ROOK, (disp_x, disp_y))
                
            elif board[8 * y + x] == 'r':
                win.blit(B_ROOK, (disp_x, disp_y))
            
            elif board[8 * y + x] == 'N':
                win.blit(W_KNIGHT, (disp_x, disp_y))
            
            elif board[8 * y + x] == 'n':
                win.blit(B_KNIGHT, (disp_x, disp_y))
            
            elif board[8 * y + x] == 'B':
                win.blit(W_BISHOP, (disp_x, disp_y))
            
            elif board[8 * y + x] == 'b':
                win.blit(B_BISHOP, (disp_x, disp_y))
            
            elif board[8 * y + x] == 'K':
                win.blit(W_KING, (disp_x, disp_y))
                
            elif board[8 * y + x] == 'k':
                win.blit(B_KING, (disp_x, disp_y))
                
            elif board[8 * y + x] == 'Q':
                win.blit(W_QUEEN, (disp_x, disp_y))
                
            elif board[8 * y + x] == 'q':
                win.blit(B_QUEEN, (disp_x, disp_y))

def profile(board, depth):
    profiler = cProfile.Profile()
    profiler.enable()
    minimax(board, True, (), depth, -math.inf, math.inf, evaluate(board))
    profiler.disable()
    profiler.dump_stats("profstats")
    stats = pstats.Stats(profiler).strip_dirs().sort_stats('tottime')
    stats.print_stats()

if (__name__ == "__main__"):
    board = standard_set()
    depth = 6;
    white_is_engine = False;
    black_is_engine = True;
    run_game(board, white_is_engine, black_is_engine, depth)
    #profile(board, 6)









