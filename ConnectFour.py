import numpy as np
import random
import pygame
import json
import os
import matplotlib.pyplot as plt

ROWS = 6
COLS = 7
PLAYER = 1
AI1 = 2
AI2 = 3
AI_TD = 4
EMPTY = 0
SQUARESIZE = 100
WIDTH = COLS * SQUARESIZE
HEIGHT = (ROWS + 1) * SQUARESIZE
RADIUS = int(SQUARESIZE / 2 - 5)

pygame.init()
FONT = pygame.font.SysFont("monospace", 35)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
RED1 = (163, 29, 29)
BEIGE = (254, 249, 225)
screen = pygame.display.set_mode((WIDTH, HEIGHT))

def board_to_tuple(board):
    return tuple(map(tuple, board))

def create_board():
    return np.zeros((ROWS, COLS), dtype=int)

def draw_board(board):
    screen.fill(BEIGE)
    for r in range(ROWS):
        for c in range(COLS):
            pygame.draw.rect(screen, BLUE, (c * SQUARESIZE, (r + 1) * SQUARESIZE, SQUARESIZE, SQUARESIZE))
            pygame.draw.circle(screen, BEIGE, (c * SQUARESIZE + SQUARESIZE // 2, (r + 1) * SQUARESIZE + SQUARESIZE // 2), RADIUS)
    for r in range(ROWS):
        for c in range(COLS):
            color = BEIGE
            if board[r][c] == PLAYER:
                color = RED
            elif board[r][c] == AI1:
                color = YELLOW
            elif board[r][c] == AI2:
                color = GREEN
            elif board[r][c] == AI_TD:
                color = BLACK
            pygame.draw.circle(screen, color, (c * SQUARESIZE + SQUARESIZE // 2, (ROWS - r) * SQUARESIZE + SQUARESIZE // 2), RADIUS)
    pygame.display.update()

def drop_piece(board, row, col, piece):
    board[row][col] = piece

def is_valid_location(board, col):
    return board[0][col] == EMPTY

def get_valid_locations(board):
    return [c for c in range(COLS) if is_valid_location(board, c)]

def get_next_open_row(board, col):
    for r in range(ROWS - 1, -1, -1):
        if board[r][col] == EMPTY:
            return r
    return None

def winning_move(board, piece):
    for r in range(ROWS):
        for c in range(COLS - 3):
            if all(board[r, c + i] == piece for i in range(4)):
                return True
    for r in range(ROWS - 3):
        for c in range(COLS):
            if all(board[r + i, c] == piece for i in range(4)):
                return True
    for r in range(ROWS - 3):
        for c in range(COLS - 3):
            if all(board[r + i, c + i] == piece for i in range(4)):
                return True
    for r in range(3, ROWS):
        for c in range(COLS - 3):
            if all(board[r - i, c + i] == piece for i in range(4)):
                return True
    return False

def animate_drop(board, row, col, piece):
    for r in range(row + 1):
        temp_board = board.copy()
        temp_board[r][col] = piece
        draw_board(temp_board)
        pygame.time.delay(30)

def minimax(board, depth, alpha, beta, maximizingPlayer):
    valid_locations = get_valid_locations(board)
    is_terminal = winning_move(board, AI1) or winning_move(board, AI2) or len(valid_locations) == 0
    if depth == 0 or is_terminal:
        if winning_move(board, AI2):
            return (None, 1000000)
        elif winning_move(board, AI1):
            return (None, -1000000)
        else:
            return (None, 0)
    if maximizingPlayer:
        value = -float('inf')
        best_col = random.choice(valid_locations)
        for col in valid_locations:
            row = get_next_open_row(board, col)
            temp_board = board.copy()
            drop_piece(temp_board, row, col, AI2)
            new_score = minimax(temp_board, depth - 1, alpha, beta, False)[1]
            if new_score > value:
                value = new_score
                best_col = col
            alpha = max(alpha, value)
            if alpha >= beta:
                break
        return best_col, value
    else:
        value = float('inf')
        best_col = random.choice(valid_locations)
        for col in valid_locations:
            row = get_next_open_row(board, col)
            temp_board = board.copy()
            drop_piece(temp_board, row, col, AI1)
            new_score = minimax(temp_board, depth - 1, alpha, beta, True)[1]
            if new_score < value:
                value = new_score
                best_col = col
            beta = min(beta, value)
            if alpha >= beta:
                break
        return best_col, value

class TDAgent:
    def __init__(self, alpha=0.1, gamma=0.95, epsilon=0.1, qfile="q_table.json"):
        self.q_table = {}
        self.alpha = alpha
        self.gamma = gamma
        self.epsilon = epsilon
        self.qfile = qfile
        if os.path.exists(qfile):
            with open(qfile, "r") as f:
                self.q_table = json.load(f)

    def choose_action(self, board):
        state = str(board_to_tuple(board))
        valid = get_valid_locations(board)
        if not valid:
            return None
        if random.random() < self.epsilon:
            return random.choice(valid)
        q_values = self.q_table.get(state, {})
        if not q_values:
            return random.choice(valid)
        sorted_actions = sorted(q_values.items(), key=lambda x: x[1], reverse=True)
        for action, _ in sorted_actions:
            if int(action) in valid:
                return int(action)
        return random.choice(valid)

    def update_q(self, state, action, reward, next_state, done):
        state, next_state = str(state), str(next_state)
        self.q_table.setdefault(state, {})
        self.q_table[state].setdefault(str(action), 0.0)
        next_qs = self.q_table.get(next_state, {})
        max_next_q = max(next_qs.values()) if next_qs else 0
        target = reward + (0 if done else self.gamma * max_next_q)
        self.q_table[state][str(action)] += self.alpha * (target - self.q_table[state][str(action)])

    def save(self):
        with open(self.qfile, "w") as f:
            json.dump(self.q_table, f)

    def learn_from_game(self, history, final_reward):
        for i in reversed(range(len(history))):
            state, action, next_state = history[i]
            done = (i == len(history) - 1)
            reward = final_reward if done else 0
            self.update_q(state, action, reward, next_state, done)
        self.save()

def play_vs_td():
    agent = TDAgent()
    board = create_board()
    draw_board(board)
    turn = PLAYER
    game_over = False
    history = []
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
                        agent.learn_from_game(history, -1)
                        game_over = True
                    turn = AI_TD
                    draw_board(board)
        if turn == AI_TD and not game_over:
            pygame.time.wait(300)
            col = agent.choose_action(board)
            if col is not None:
                state = board_to_tuple(board)
                row = get_next_open_row(board, col)
                drop_piece(board, row, col, AI_TD)
                next_state = board_to_tuple(board)
                history.append((state, col, next_state))
                animate_drop(board, row, col, AI_TD)
                if winning_move(board, AI_TD):
                    print("IA TD gana")
                    agent.learn_from_game(history, 1)
                    game_over = True
                elif len(get_valid_locations(board)) == 0:
                    print("¡Empate!")
                    agent.learn_from_game(history, 0)
                    game_over = True
                else:
                    turn = PLAYER
                draw_board(board)

def play_multiple_minimax_vs_td(use_alpha_beta, games=1):
    results = []
    for _ in range(games):
        agent = TDAgent()
        board = create_board()
        turn = AI1
        game_over = False
        history = []
        while not game_over:
            if games == 1:
                draw_board(board)
                pygame.time.wait(300)
            if turn == AI1:
                col = minimax(board, 4, -float('inf'), float('inf'), True)[0] if use_alpha_beta else random.choice(get_valid_locations(board))
            else:
                col = agent.choose_action(board)
            if col is not None:
                row = get_next_open_row(board, col)
                if turn == AI_TD:
                    state = board_to_tuple(board)
                drop_piece(board, row, col, turn)
                if turn == AI_TD:
                    next_state = board_to_tuple(board)
                    history.append((state, col, next_state))
                if games == 1:
                    animate_drop(board, row, col, turn)
                if winning_move(board, turn):
                    if turn == AI_TD:
                        results.append(1)
                        agent.learn_from_game(history, 1)
                    else:
                        results.append(-1)
                        agent.learn_from_game(history, -1)
                    game_over = True
                elif len(get_valid_locations(board)) == 0:
                    results.append(0)
                    agent.learn_from_game(history, 0)
                    game_over = True
                turn = AI_TD if turn == AI1 else AI1
        if games == 1:
            draw_board(board)
    if games > 1:
        td_wins = results.count(1)
        minimax_wins = results.count(-1)
        draws = results.count(0)
        labels = ['TD Wins', 'Minimax Wins', 'Draws']
        values = [td_wins, minimax_wins, draws]
        plt.bar(labels, values)
        plt.title(f'Resultados en {games} partidas')
        plt.ylabel('Cantidad')
        plt.show()


def play_td_vs_td(animated=True, games=1):
    results = []
    for _ in range(games):
        td1 = TDAgent()
        td2 = TDAgent()
        board = create_board()
        turn = AI1
        game_over = False
        history1 = []
        history2 = []
        if animated:
            draw_board(board)
        while not game_over:
            if animated:
                pygame.time.wait(300)
            agent = td1 if turn == AI1 else td2
            piece = AI_TD
            col = agent.choose_action(board)
            if col is not None:
                row = get_next_open_row(board, col)
                state = board_to_tuple(board)
                drop_piece(board, row, col, piece)
                next_state = board_to_tuple(board)
                if turn == AI1:
                    history1.append((state, col, next_state))
                else:
                    history2.append((state, col, next_state))
                if animated:
                    animate_drop(board, row, col, piece)
                if winning_move(board, piece):
                    if turn == AI1:
                        td1.learn_from_game(history1, 1)
                        td2.learn_from_game(history2, -1)
                        results.append(1)
                    else:
                        td1.learn_from_game(history1, -1)
                        td2.learn_from_game(history2, 1)
                        results.append(2)
                    game_over = True
                elif len(get_valid_locations(board)) == 0:
                    td1.learn_from_game(history1, 0)
                    td2.learn_from_game(history2, 0)
                    results.append(0)
                    game_over = True
                turn = AI2 if turn == AI1 else AI1
        if animated:
            draw_board(board)
    if games > 1:
        td1_wins = results.count(1)
        td2_wins = results.count(2)
        draws = results.count(0)
        labels = ['TD1 Wins', 'TD2 Wins', 'Draws']
        values = [td1_wins, td2_wins, draws]
        plt.bar(labels, values)
        plt.title(f'TD vs TD - {games} partidas')
        plt.ylabel('Cantidad')
        plt.show()

def main_menu():
    running = True
    options = [
        "Jugador vs TD (1 partida)",
        "Minimax vs TD (1 partida)",
        "Minimax vs TD (50 partidas)",
        "Minimax+AB vs TD (1 partida)",
        "Minimax+AB vs TD (50 partidas)",
        "TD vs TD (1 partida)",
        "TD vs TD (50 partidas)",
        "Salir"
    ]
    while running:
        screen.fill(RED1)
        for i, option in enumerate(options):
            text = FONT.render(option, True, WHITE)
            rect = text.get_rect(center=(WIDTH // 2, 60 + i * 70))
            screen.blit(text, rect)
            if pygame.mouse.get_pressed()[0] and rect.collidepoint(pygame.mouse.get_pos()):
                if option == "Jugador vs TD (1 partida)":
                    play_vs_td()
                elif option == "Minimax vs TD (1 partida)":
                    play_multiple_minimax_vs_td(False, games=1)
                elif option == "Minimax vs TD (50 partidas)":
                    play_multiple_minimax_vs_td(False, games=50)
                elif option == "Minimax+AB vs TD (1 partida)":
                    play_multiple_minimax_vs_td(True, games=1)
                elif option == "Minimax+AB vs TD (50 partidas)":
                    play_multiple_minimax_vs_td(True, games=50)
                elif option == "TD vs TD (1 partida)":
                    play_td_vs_td(animated=True, games=1)
                elif option == "TD vs TD (50 partidas)":
                    play_td_vs_td(animated=False, games=50)
                elif option == "Salir":
                    running = False
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
    pygame.quit()

if __name__ == '__main__':
    main_menu()