import numpy as np
import pygame
import sys
import math
import random

ROW = 6
COLUMN = 7
SQUARE_PX = 100
RAD = int(SQUARE_PX / 4) + 20

h = 200
w = 150

height = 200 + SQUARE_PX * (ROW + 1)
width = 150 + SQUARE_PX * COLUMN

SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 1000
surface = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

pygame.display.set_caption("Connect Four!")

# color palette
BLACK   = (0, 0, 0)
WHITE   = (255, 255, 255)
C_BOARD = (25, 42, 81)
C_BG    = (239, 235, 241)
C_BALLA = (245, 65, 183)
C_BALLB = (157, 134, 222)

def createboard():
    board = np.full((ROW, COLUMN), -1)
    return board

def drawboard(board):
    for c in range(COLUMN):
        for r in range(ROW):
            # Rect(left, top, width, height)
            pygame.draw.rect(surface, C_BOARD, pygame.Rect(w + c * SQUARE_PX, h + r * SQUARE_PX + SQUARE_PX, SQUARE_PX, SQUARE_PX))
            pygame.draw.circle(surface, WHITE, (int(w + c * SQUARE_PX + SQUARE_PX/2), int(h + r * SQUARE_PX + SQUARE_PX + SQUARE_PX/2)), RAD)

    for c in range(COLUMN):
        for r in range(ROW):
            if board[r][c] == 0:
                pygame.draw.circle(surface, C_BALLA, (int(w + c * SQUARE_PX + SQUARE_PX/2), height - int(r * SQUARE_PX + SQUARE_PX/2)), RAD)
            elif board[r][c] == 1:
                pygame.draw.circle(surface, C_BALLB, (int(w + c * SQUARE_PX + SQUARE_PX/2), height - int(r * SQUARE_PX + SQUARE_PX/2)), RAD)
            
    pygame.display.update()

def printboard(board):
    print(np.flip(board, 0))

def check_location(board, col):
    if(board[ROW - 1][col] == -1):
        return True
    else:
        return False

def next_valid_row(board, col):
    for r in range(ROW):
        if board[r][col] == -1:
            return r

def drop_ball(board, row, col, playerid):
    board[row][col] = playerid

def is_winning(board, playerid):
    for c in range(COLUMN - 3):
        for r in range(ROW):
            if board[r][c] == playerid and board[r][c+1] == playerid and board[r][c+2] == playerid and board[r][c+3] == playerid:
                return True
    
    for c in range(COLUMN):
        for r in range(ROW - 3):
            if board[r][c] == playerid and board[r+1][c] == playerid and board[r+2][c] == playerid and board[r+3][c] == playerid:
                return True

    for c in range(COLUMN - 3):
        for r in range(ROW - 3):
            if board[r][c] == playerid and board[r+1][c+1] == playerid and board[r+2][c+2] == playerid and board[r+3][c+3] == playerid:
                return True

    for c in range(COLUMN - 3):
        for r in range(3, ROW):
            if board[r][c] == playerid and board[r-1][c+1] == playerid and board[r-2][c+2] == playerid and board[r-3][c+3] == playerid:
                return True
    
    return False

def get_valid_cols(board):
    valid_cols = []
    for c in range(COLUMN):
        if next_valid_row(board, c):
            valid_cols.append(c)
    return valid_cols

def check_is_ending(board):
    a = is_winning(board, 0)
    b = is_winning(board, 1)
    valid_columns = len(get_valid_cols(board))
    return a or b or valid_columns == 0

def evaluate_sequence(sequence, playerid):
    score = 0
    if(playerid == 1):
        opponentid = 0
    else:
        opponentid = 1

    if sequence.count(playerid) == 4:
        score += 100
    elif sequence.count(playerid) == 3 and sequence.count(-1) == 1:
        score += 5
    elif sequence.count(playerid) == 2 and sequence.count(-1) == 2:
        score += 2

    if sequence.count(opponentid) == 3 and sequence.count(-1) == 1:
        score -= 4

    return score


def score_position(board, playerid):
    score = 0

    center_array = [int(i) for i in list(board[:, COLUMN//2])]
    center_count = center_array.count(playerid)
    score += center_count * 3

    for r in range(ROW):
        row_array = [int(i) for i in list(board[r, :])]
        for c in range(COLUMN - 3):
            sequence = row_array[c:c+4]
            score += evaluate_sequence(sequence, playerid)
    
    for c in range(COLUMN):
        column_array = [int(i) for i in list(board[:, c])]
        for r in range(ROW - 3):
            sequence = column_array[r:r+4]
            score += evaluate_sequence(sequence, playerid)

    for r in range(ROW - 3):
        for c in range(COLUMN - 3):
            sequence = [board[r+i][c+i] for i in range(4)]
            score += evaluate_sequence(sequence, playerid)

    for r in range(ROW - 3):
        for c in range(COLUMN - 3):
            sequence = [board[r+3-i][c+i] for i in range(4)]
            score += evaluate_sequence(sequence, playerid)

    return score

def alphabeta(board, depth, alpha, beta, maximizingPlayer):
    valid_columns = get_valid_cols(board)
    is_ending = check_is_ending(board)
    if depth == 0 or is_ending:
        if is_ending:
            if is_winning(board, 1):
                return(None, 100000000000000)
            elif is_winning(board, 0):
                return(None, -100000000000000)
            else:
                return(None, 0)
        else:
            return(None, score_position(board, 1))
    if maximizingPlayer:
        val = -math.inf
        column = random.choice(valid_columns)
        for c in valid_columns:
            r = next_valid_row(board, c)
            temp_board = board.copy()
            drop_ball(temp_board, r, c, 1)
            new_score = alphabeta(temp_board, depth-1, alpha, beta, False)[1]
            if new_score > val:
                val = new_score
                column = c
            alpha = max(alpha, val)
            if alpha >= beta:
                break
        return column, val
    else:
        val = math.inf
        column = random.choice(valid_columns)
        for c in valid_columns:
            r = next_valid_row(board, c)
            temp_board = board.copy()
            drop_ball(temp_board, r, c, 0)
            new_score = alphabeta(temp_board, depth-1, alpha, beta, True)[1]
            if new_score < val:
                val = new_score
                column = c
            beta = min(beta, val)
            if alpha >= beta:
                break
        return column, val


board = createboard()
printboard(board)
drawboard(board)

gameover = False
turn = 0

pygame.init()
pygame.display.update()
font = pygame.font.SysFont("Courier New", 50)

while not gameover:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

        # mouse movement listener
        if event.type == pygame.MOUSEMOTION and event.pos[0] < (1000-w-RAD) and event.pos[0] > w+RAD:
            pygame.draw.rect(surface, WHITE, pygame.Rect(w, h, width - w, SQUARE_PX))
            posix = event.pos[0]
            print(posix)

            if turn == 0:
                pygame.draw.circle(surface, C_BALLA, (posix, h + int(SQUARE_PX/2)), RAD)
            else:
                pygame.draw.circle(surface, C_BALLB, (posix, h + int(SQUARE_PX/2)), RAD)
        
        pygame.display.update()

        if event.type == pygame.MOUSEBUTTONDOWN:
            pygame.draw.rect(surface, BLACK, (w, h, width, SQUARE_PX))

            # player 1
            if turn == 0:
                posix = event.pos[0]
                column = int(math.floor((posix - w)/ (SQUARE_PX)))

                if check_location(board, column):
                    row = next_valid_row(board, column)
                    drop_ball(board, row, column, 0)

                    if is_winning(board, 0):
                        label = font.render("Player 1 Wins", True, WHITE)
                        label_rect = label.get_rect(center=(SCREEN_WIDTH/2, h))
                        surface.blit(label, label_rect)
                        gameover = True
            # player 2
            else:
                column, score = alphabeta(board, 3, -math.inf, math.inf, True)
                # column -= (int)(w / SQUARE_PX)
                
                if check_location(board, column):
                    row = next_valid_row(board, column)
                    drop_ball(board, row, column, 1)

                    if is_winning(board, 1):
                        label = font.render("Player 2 Wins", True, WHITE)
                        label_rect = label.get_rect(center=(SCREEN_WIDTH/2, h))
                        surface.blit(label, label_rect)
                        gameover = True

            printboard(board)
            drawboard(board)
            turn += 1
            turn = turn % 2

            if gameover:
                pygame.time.wait(5000)