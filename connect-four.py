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

def createboard(ROW, COLUMN):
    board = np.full((ROW, COLUMN), -1)
    return board

def drawboard(board, ROW, COLUMN, height, width):
    if ROW == 5 and COLUMN == 6:
        w = 190
        h = 240

    if ROW == 6 and COLUMN == 7:
        w = 150
        h = 200

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

def check_location(board, ROW, col):
    if board[ROW - 1][col] == -1:
        return True
    else:
        return False

def next_valid_row(board, ROW, col):
    for r in range(ROW):
        if board[r][col] == -1:
            return r

def drop_ball(board, row, col, playerid):
    board[row][col] = playerid

def is_winning(board, playerid, ROW, COLUMN):
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

def get_valid_cols(board, ROW, COLUMN):
    valid_cols = []
    for c in range(COLUMN):
        if check_location(board, ROW, c):
            valid_cols.append(c)
    return valid_cols

def check_is_ending(board, ROW, COLUMN):
    a = is_winning(board, 0, ROW, COLUMN)
    b = is_winning(board, 1, ROW, COLUMN)
    valid_columns = len(get_valid_cols(board, ROW, COLUMN))
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


def score_position(board, playerid, ROW, COLUMN):
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

def alphabeta(board, depth, alpha, beta, maximizingPlayer, ROW, COLUMN):
    valid_columns = get_valid_cols(board, ROW, COLUMN)
    is_ending = check_is_ending(board, ROW, COLUMN)
    if depth == 0 or is_ending:
        if is_ending:
            if is_winning(board, 1, ROW, COLUMN):           # AI wins
                return(None, 1000000000000)
            elif is_winning(board, 0, ROW, COLUMN):
                return(None, -1000000000000)
            else:
                return(None, 0)
        else:
            return(None, score_position(board, 1, ROW, COLUMN))
    if maximizingPlayer:
        val = -math.inf
        column = random.choice(valid_columns)
        for c in valid_columns:
            r = next_valid_row(board, ROW, c)
            temp_board = board.copy()
            drop_ball(temp_board, r, c, 1)
            new_score = alphabeta(temp_board, depth-1, alpha, beta, False, ROW, COLUMN)[1]
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
            r = next_valid_row(board, ROW, c)
            temp_board = board.copy()
            drop_ball(temp_board, r, c, 0)
            new_score = alphabeta(temp_board, depth-1, alpha, beta, True, ROW, COLUMN)[1]
            if new_score < val:
                val = new_score
                column = c
            beta = min(beta, val)
            if alpha >= beta:
                break
        return column, val

def showinstruction():
    pygame.display.update()
    quitImg = pygame.image.load('./assets/pixel/asset12.png')
    quitImg = pygame.transform.scale(quitImg, (205, 81))
    menuImg = pygame.image.load('./assets/pixel/asset15.png')
    menuImg = pygame.transform.scale(menuImg, (360, 81))

    menuImgRect = menuImg.get_rect(center=(SCREEN_WIDTH/2, h*4))
    quitImgRect = quitImg.get_rect(center=(SCREEN_WIDTH/2, h*4.5))

    instruction = True

    while instruction:
        surface = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        surface.fill(WHITE)
        surface.blit(quitImg, quitImgRect)
        surface.blit(menuImg, menuImgRect)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                if menuImgRect.collidepoint(x, y):
                    callmenu()
                    return
                elif quitImgRect.collidepoint(x, y):
                    sys.exit()
                    return
        pygame.display.update()

def callmenu():
    pygame.init()
    pygame.display.update()
    logoImg = pygame.image.load('./assets/pixel/asset14.png')
    logoImg = pygame.transform.scale(logoImg, (385, 224))
    optionAImg = pygame.image.load('./assets/pixel/asset9.png')
    optionAImg = pygame.transform.scale(optionAImg, (205, 81))
    optionBImg = pygame.image.load('./assets/pixel/asset10.png')
    optionBImg = pygame.transform.scale(optionBImg, (205, 81))
    instructionImg = pygame.image.load('./assets/pixel/asset16.png')
    instructionImg = pygame.transform.scale(instructionImg, (360, 81))
    quitImg = pygame.image.load('./assets/pixel/asset12.png')
    quitImg = pygame.transform.scale(quitImg, (205, 81))

    logoImgRect = logoImg.get_rect(center=(SCREEN_WIDTH/2, h+50))
    optionAImgRect = optionAImg.get_rect(center=(SCREEN_WIDTH/2, h*2.5))
    optionBImgRect = optionBImg.get_rect(center=(SCREEN_WIDTH/2, h*3))
    instructionImgRect = instructionImg.get_rect(center=(SCREEN_WIDTH/2, h*3.5))
    # quitImgRect = quitImg.get_rect(SCREEN_WIDTH+50, h*4)

    mainmenu = True

    while mainmenu:
        surface = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        surface.fill(WHITE)
        surface.blit(logoImg, logoImgRect)
        surface.blit(optionAImg, optionAImgRect)
        surface.blit(optionBImg, optionBImgRect)
        surface.blit(instructionImg, instructionImgRect)

        ROW = 0
        COLUMN = 0

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                if optionAImgRect.collidepoint(x, y):
                    ROW = 6
                    COLUMN = 7
                    mainmenu = False
                    surface = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
                    return ROW, COLUMN
                elif optionBImgRect.collidepoint(x, y):
                    ROW = 5
                    COLUMN = 6
                    mainmenu = False
                    surface = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
                    return ROW, COLUMN
                elif instructionImgRect.collidepoint(x, y):
                    showinstruction()
        pygame.display.update()


pygame.init()
pygame.display.update()
font = pygame.font.SysFont("Courier New", 50)

quitImg = pygame.image.load('./assets/pixel/asset12.png')
quitImg = pygame.transform.scale(quitImg, (205, 81))
menuImg = pygame.image.load('./assets/pixel/asset15.png')
menuImg = pygame.transform.scale(menuImg, (360, 81))

ROW, COLUMN = callmenu()

if ROW == 6 and COLUMN == 7:
    height = 200 + SQUARE_PX * (ROW + 1)
    width = 150 + SQUARE_PX * COLUMN
    w = 150
    h = 200
    surface = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
elif ROW == 5 and COLUMN == 6:
    height = 240 + SQUARE_PX * (ROW + 1)
    width = 190 + SQUARE_PX * COLUMN
    w = 190
    h = 240
    surface = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

board = createboard(ROW, COLUMN)
printboard(board)
drawboard(board, ROW, COLUMN, height, width)

gameover = False
turn = 0
# pygame.display.update()

while not gameover:
    # back to menu and quit buttons
    # menuImgRect = menuImg.get_rect(100, h*4.5)
    # quitImgRect = quitImg.get_rect(SCREEN_WIDTH-100, h*4.5)

    # surface.blit(quitImg, quitImgRect)
    # surface.blit(menuImg, menuImgRect)

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

            # player 1
            if turn == 0:
                posix = event.pos[0]
                column = int(math.floor((posix - w)/ (SQUARE_PX)))

                if check_location(board, ROW, column):
                    row = next_valid_row(board, ROW, column)
                    drop_ball(board, row, column, 0)

                    if is_winning(board, 0, ROW, COLUMN):
                        label = font.render("Player 1 Wins", True, WHITE)
                        label_rect = label.get_rect(center=(SCREEN_WIDTH/2, h))
                        pygame.draw.rect(surface, BLACK, pygame.Rect(w, h, width - w, SQUARE_PX))
                        surface.blit(label, label_rect)
                        gameover = True
                    
                    printboard(board)
                    drawboard(board, ROW, COLUMN, height, width)
                    turn += 1
                    turn = turn % 2

    # player AI
    if turn == 1 and not gameover:
        column, score = alphabeta(board, 3, -math.inf, math.inf, True, ROW, COLUMN)
            
        if check_location(board, ROW, column):
            row = next_valid_row(board, ROW, column)
            pygame.time.wait(500)
            drop_ball(board, row, column, 1)

            if is_winning(board, 1, ROW, COLUMN):
                label = font.render("Player 2 Wins", True, WHITE)
                label_rect = label.get_rect(center=(SCREEN_WIDTH/2, h))
                pygame.draw.rect(surface, BLACK, pygame.Rect(w, h, width - w, SQUARE_PX))
                surface.blit(label, label_rect)
                gameover = True

        printboard(board)
        drawboard(board, ROW, COLUMN, height, width)
        turn += 1
        turn = turn % 2

    if gameover:
        menuImgRect = menuImg.get_rect(center=(SCREEN_WIDTH/2, h*2.5))
        quitImgRect = quitImg.get_rect(center=(SCREEN_WIDTH/2, h*3))

        idle = True

        while idle:
            pygame.display.update()

            surface.fill(WHITE)
            surface.blit(quitImg, quitImgRect)
            surface.blit(menuImg, menuImgRect)

            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    x, y = event.pos
                    if menuImgRect.collidepoint(x, y):
                        ROW, COLUMN = callmenu()
                        if ROW == 6 and COLUMN == 7:
                            height = 200 + SQUARE_PX * (ROW + 1)
                            width = 150 + SQUARE_PX * COLUMN
                            w = 150
                            h = 200
                            idle = False
                        elif ROW == 5 and COLUMN == 6:
                            height = 240 + SQUARE_PX * (ROW + 1)
                            width = 190 + SQUARE_PX * COLUMN
                            w = 190
                            h = 240
                            idle = False
                        board = createboard(ROW, COLUMN)
                        printboard(board)
                        drawboard(board, ROW, COLUMN, height, width)
                        gameover = False
                        turn = 0
                    elif quitImgRect.collidepoint(x, y):
                        sys.exit()
            pygame.display.update()

