import numpy as np
import pygame
import sys
import math

ROW = 6
COLUMN = 7
SQUARE_PX = 100
RAD = (SQUARE_PX / 4) + 5

height = SQUARE_PX * ROW
width = SQUARE_PX * COLUMN

# surface assets
surface = pygame.display.set_mode(width, height)
font = pygame.font.SysFont("Courier New", 50)

# color palette
BLACK   = (0, 0, 0)
WHITE   = (255, 255, 255)
C_BOARD = (25, 42, 81)
C_BG    = (239, 235, 241)
C_BALLA = (252, 188, 253)
C_BALLB = (249, 174, 222)

def createboard():
    board = np.zeros((ROW, COLUMN))
    return board

def drawboard(board):
    for r in range(ROW):
        for c in range(COLUMN):
            # Rect(left, top, width, height)
            pygame.draw.rect(surface, C_BOARD, pygame.Rect(c * SQUARE_PX, r * SQUARE_PX + SQUARE_PX, SQUARE_PX, SQUARE_PX))

def printboard(board):
    print(np.flip(board, 0))

def check_location(board, col):
    if(board[ROW - 1][col] == 0):
        return True
    else:
        return False

def next_valid_row(board, col):
    for r in range(ROW):
        if board[r][col] == 0:
            return r

def drop_ball(board, row, col, playerid):
    board[row][col] = playerid

def is_winning(board, playerid):
    for c in range(COLUMN - 3):
        for r in range(ROW):
            if board[r][c] == playerid and board[r][c+1] == playerid and board[r][c+2] == playerid and board[r][c+3] == playerid:
                return True
    
    for c in range(COLUMN):
        for r in range(ROW):
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

while not gameover:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

        # mouse movement listener
        if event.type == pygame.MOUSEMOTION:
            pygame.draw.rect(surface, BLACK, pygame.Rect(0, 0, width, SQUARE_PX))
            posix = event.pos[0]

            if turn == 0:
                pygame.draw.circle(surface, C_BALLA, (posix, int(SQUARE_PX/2)), RAD)
            else:
                pygame.draw.circle(surface, C_BALLB, (posix, int(SQUARE_PX/2)), RAD)
        
        pygame.display.update()

        if event.type == pygame.MOUSEBUTTONDOWN:
            pygame.draw.rect(surface, BLACK, (0, 0, width, SQUARE_PX))

            if turn == 0:
                posix = event.pos[0]
                column = int(math.floor(posix / SQUARE_PX))

                if check_location(board, column):
                    row = next_valid_row(board, column)
                    drop_ball(board, row, column, 0)

                    if is_winning(board, 0):
                        label = font.render("Player 1 Wins", 1, WHITE)
                        surface.blit(label, (40, 10))
                        gameover = True

                    printboard(board)
                    drawboard(board)

                    turn += 1
                    turn = turn % 2

    # AI's turn
