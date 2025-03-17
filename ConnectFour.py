import numpy as np
import random
import pygame

ROWS = 6
COLS = 7
PLAYER = 1
AI = 2
EMPTY = 0
SQUARESIZE = 100
WIDTH = COLS * SQUARESIZE
HEIGHT = (ROWS + 1) * SQUARESIZE
RADIUS = int(SQUARESIZE / 2 - 5)

pygame.init()
FONT = pygame.font.SysFont("monospace", 50)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
RED1 = (163, 29, 29)
BEIGE = (254, 249, 225)

screen = pygame.display.set_mode((WIDTH, HEIGHT))

def draw_board(board):
    screen.fill(BEIGE)
    for r in range(ROWS):
        for c in range(COLS):
            pygame.draw.rect(screen, BLUE, (c * SQUARESIZE, (r + 1) * SQUARESIZE, SQUARESIZE, SQUARESIZE))
            pygame.draw.circle(screen, BEIGE, (c * SQUARESIZE + SQUARESIZE // 2, (r + 1) * SQUARESIZE + SQUARESIZE // 2), RADIUS)

    for r in range(ROWS):
        for c in range(COLS):
            if board[r][c] == PLAYER:
                pygame.draw.circle(screen, RED, (c * SQUARESIZE + SQUARESIZE // 2, (r + 1) * SQUARESIZE + SQUARESIZE // 2), RADIUS)
            elif board[r][c] == AI:
                pygame.draw.circle(screen, YELLOW, (c * SQUARESIZE + SQUARESIZE // 2, (r + 1) * SQUARESIZE + SQUARESIZE // 2), RADIUS)

    pygame.display.update()

def animate_drop(board, row, col, piece):
    for r in range(row + 1):
        temp_board = board.copy()
        temp_board[r][col] = piece
        draw_board(temp_board)
        pygame.time.delay(50)

def create_board():
    return np.zeros((ROWS, COLS), dtype=int)

def drop_piece(board, row, col, piece):
    board[row][col] = piece

def is_valid_location(board, col):
    return board[0][col] == EMPTY

def get_next_open_row(board, col):
    for r in range(ROWS-1, -1, -1):
        if board[r][col] == EMPTY:
            return r
    return None

def main_menu():
    alpha_beta_pruning = True
    while True:
        screen.fill(RED1)
        title_text = FONT.render("Connect Four", True, WHITE)
        screen.blit(title_text, (WIDTH // 2 - title_text.get_width() // 2, 50))
        
        pvp_text = FONT.render("PvAI", True, WHITE)
        pvp_rect = pvp_text.get_rect(center=(WIDTH // 2, 150))
        screen.blit(pvp_text, pvp_rect)
        
        ai_vs_ai_text = FONT.render("AI v AI", True, WHITE)
        ai_vs_ai_rect = ai_vs_ai_text.get_rect(center=(WIDTH // 2, 250))
        screen.blit(ai_vs_ai_text, ai_vs_ai_rect)
        
        pruning_text = FONT.render(f"Alpha-Beta Pruning: {'ON' if alpha_beta_pruning else 'OFF'}", True, WHITE)
        pruning_rect = pruning_text.get_rect(center=(WIDTH // 2, 350))
        screen.blit(pruning_text, pruning_rect)
        
        pygame.display.update()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            if event.type == pygame.MOUSEBUTTONDOWN:
                if pvp_rect.collidepoint(event.pos):
                    play_human_vs_ai(alpha_beta_pruning)
                elif ai_vs_ai_rect.collidepoint(event.pos):
                    play_ai_vs_ai(alpha_beta_pruning)
                elif pruning_rect.collidepoint(event.pos):
                    alpha_beta_pruning = not alpha_beta_pruning

def winning_move(board, piece):
    for r in range(ROWS):
        for c in range(COLS - 3):
            if all(board[r, c+i] == piece for i in range(4)):
                return True
    for r in range(ROWS - 3):
        for c in range(COLS):
            if all(board[r+i, c] == piece for i in range(4)):
                return True
    for r in range(ROWS - 3):
        for c in range(COLS - 3):
            if all(board[r+i, c+i] == piece for i in range(4)):
                return True
    for r in range(3, ROWS):
        for c in range(COLS - 3):
            if all(board[r-i, c+i] == piece for i in range(4)):
                return True
    return False

def play_human_vs_ai(alpha_beta_pruning):
    board = create_board()
    game_over = False
    turn = PLAYER
    draw_board(board)
    
    while not game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            if event.type == pygame.MOUSEBUTTONDOWN and turn == PLAYER:
                col = event.pos[0] // SQUARESIZE
                if is_valid_location(board, col):
                    row = get_next_open_row(board, col)
                    animate_drop(board, row, col, PLAYER)
                    drop_piece(board, row, col, PLAYER)
                    if winning_move(board, PLAYER):
                        print("¡Jugador gana!")
                        game_over = True
                    turn = AI
                    draw_board(board)
        if turn == AI and not game_over:
            pygame.time.wait(500)
            col = random.choice([c for c in range(COLS) if is_valid_location(board, c)])
            if col is not None:
                row = get_next_open_row(board, col)
                animate_drop(board, row, col, AI)
                drop_piece(board, row, col, AI)
                if winning_move(board, AI):
                    print("IA gana")
                    game_over = True
                turn = PLAYER
                draw_board(board)

def play_ai_vs_ai(alpha_beta_pruning):
    board = create_board()
    game_over = False
    turn = AI
    draw_board(board)
    
    while not game_over:
        pygame.time.wait(500)
        col = random.choice([c for c in range(COLS) if is_valid_location(board, c)])
        if col is not None:
            row = get_next_open_row(board, col)
            animate_drop(board, row, col, turn)
            drop_piece(board, row, col, turn)
            if winning_move(board, turn):
                print(f"{'IA 1' if turn == AI else 'IA 2'} gana")
                game_over = True
            turn = AI if turn == PLAYER else PLAYER
            draw_board(board)

main_menu()
