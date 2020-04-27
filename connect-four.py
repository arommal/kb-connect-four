import numpy as np
import pygame
import sys
import math

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
                posix = event.pos[0]
                column = int(math.floor((posix - w) / SQUARE_PX))

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