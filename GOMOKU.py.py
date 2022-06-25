#libraries
import numpy as np
import pygame
import math
import sys
import random


#Global variable
row = 9
column = 9
player = 1
bot =2
piece_1 =1
piece_2=2
Min = -math.inf
Max = math.inf


#Screen Sizes
block_size = 70 
screen_width = column * block_size
screen_height = row * block_size
screen_size = (screen_width,screen_height)
piece_radius =  25

#colors values
BLACK = (0,0,0)
WHITE = (255,255,255)
BROWN = (205,128,0)


#return 2D Matrix of Zeros
def board(row=9,col=9):
    return np.zeros((row,col))

#drop the piece of player in the board
def drop_piece(board,row,col,piece):
    board[row][col]=piece

#check the location is valid for move
def is_location_valid(board,row,col):
    return board[row][col]== 0

#check winning condition
def check_winner(board,piece):
    #horizontal checking
    for col in range(column-4):
        for row_ in range(row):
            if board[row_][col]==piece and board[row_][col+1]==piece and board[row_][col+2]==piece and board[row_][col+3]==piece and board[row_][col+4]==piece:
                 return True
    
    #vertical checking
    for col in range(column):
        for row_ in range(row-4): 
            if board[row_][col]==piece and board[row_+1][col]==piece and board[row_+2][col]==piece  and board[row_+3][col]==piece  and board[row_+4][col]==piece:
                return True

    #increasing diagonal checking
    for col in range(column-4):
        for row_ in range(4,row):
            if board[row_][col]==piece and board[row_-1][col+1]==piece and board[row_-2][col+2]==piece  and board[row_-3][col+3]==piece  and board[row_-4][col+4]==piece:
                return True

    #decreasing diagonal checking
    for col in range(column-4):
        for row_ in range(row-4):
            if board[row_][col]==piece and board[row_+1][col+1]==piece and board[row_+2][col+2]==piece  and board[row_+3][col+3]==piece  and board[row_+4][col+4]==piece:
                return True


#--------------------------------------------------GUI---------------------------------------------------------


#GUI draw a board in pygame window
def draw_board(screen):
    for x in range(0,screen_width,block_size):
        for y in range(0,screen_height,block_size):
            rect = pygame.Rect(x, y, block_size, block_size)
            pygame.draw.rect(screen,BROWN,rect)

    # draw inner grid lines
    # draw vertical lines
    for x in range(block_size // 2, screen_width - block_size // 2 + block_size, block_size):
        line_start = (x, block_size // 2)
        line_end = (x,screen_height-block_size // 2)
        pygame.draw.line(screen, BLACK, line_start,line_end,2)

    # draw horizontal lines
    for y in range(block_size // 2, screen_height - block_size // 2 + block_size, block_size):
        line_start = (block_size // 2,y)
        line_end = (screen_width-block_size // 2,y)
        pygame.draw.line(screen, BLACK, line_start,line_end,2)
    pygame.display.update()


# draw a piece on board
def draw_piece(screen,board):
    # draw game pieces at mouse location
    for x in range(column):
        for y in range(row):
            circle_pos = (x * block_size + block_size//2, y * block_size + block_size//2)
            if board[y][x] == 1:
                pygame.draw.circle(screen, BLACK, circle_pos, piece_radius)
            elif board[y][x] == 2:
                pygame.draw.circle(screen, WHITE, circle_pos, piece_radius)
    pygame.display.update()


#-------------------------------------------------------------------------------------------------------------

#calculate Heuristics of Row and Columns
def evalute_window(window,piece):
    score = 0
    opp_piece = player
    if piece == player:
        opp_piece = bot
    
    if window.count(piece) == 5:
        score += 100
    elif window.count(piece) == 4 and window.count(0) == 1:
        score+=20
    elif window.count(piece) ==3 and window.count(0) == 2:
        score += 10
    elif window.count(piece) == 2 and window.count(0) == 3:
        score +=5
    if window.count(opp_piece) == 3 and window.count(0) == 2:
        score -= 40
    if window.count(opp_piece) == 4 and window.count(0) == 1:
        score -= 80
    return score 



def score_position(board,piece):
    score = 0

    #center score
    center_list = [int(i) for i in list(board[:,column//2])]
    center_count = center_list.count(piece)
    score =+ center_count*9


    #horizontal score
    for r in range(row):
        row_list = [int(i) for i in list(board[r,:])]
        for c in range(column-4):
            window = row_list[c:c+5]
            score += evalute_window(window,piece)
    

    #vertical score
    for c in range(column):
        col_list = [int(i) for i in list(board[:,c])]
        for r in range (row-4):
            window = col_list[r:r+5]
            score += evalute_window(window,piece)
    
    #increasing diagonal score
    for r in range(row-4):
        for c in range(column-4):
            window = [board[r+i][c+i] for i in range(5)]
            score += evalute_window(window,piece)

    
    #decreasing diagonal score
    for r in range(row-4):
        for c in range(column-4):
            window = [board[r+4-i][c+i] for i in range(5)]
            score += evalute_window(window,piece)


    return score

#return all valid positions for next move
def get_valid_position(board):
    valid_location = []
    for r in range(row):
        for c in range(column):
            if is_location_valid(board,r,c):
                valid_location.append((r,c))
    return valid_location


#check the node is terminmal\leaf node
def is_terminal_node(board):
    return check_winner(board,piece_1) or check_winner(board,piece_1)\
         or len(get_valid_position(board)) ==0


#mini-max algorithm for AI implimentation
def alpha_beta_pruning(board,depth,maximizing_player, alpha, beta):
    valid_location = get_valid_position(board)
    is_terminal = is_terminal_node(board)
    if depth == 0 or is_terminal:
        if is_terminal:
            if check_winner(board,piece_2):
                return(None,None),1000000000
            elif check_winner(board,piece_1):
                return(None,None),-1000000000
            else:
                return(None,None),0
        else: #if depth is zero
            return (None,None),score_position(board,piece_2)
    if maximizing_player:
        value = -math.inf
        row,col = random.choice(valid_location)
        for row_,col_ in valid_location:
            temp_board = board.copy()
            drop_piece(temp_board,row_,col_,piece_2)
            new_score = alpha_beta_pruning(temp_board,depth-1,False, alpha, beta)[1]
            if new_score > value:
                value = new_score
                row,col= row_,col_
            alpha = max(alpha, value)
            if alpha >= beta:
                break
        return (row,col),value
    
    else:
        value = math.inf
        row,col = random.choice(valid_location)
        for row_,col_ in valid_location:
            temp_board = board.copy()
            drop_piece(temp_board,row_,col_,piece_2)
            new_score = alpha_beta_pruning(temp_board,depth-1,True, alpha, beta)[1]
            if new_score < value:
                value = new_score
                row,col= row_,col_
            beta = min(beta, value)
            if alpha >= beta:
                break
            # # break
        return (row,col),value


def main():
    pygame.init()
    
    game_over=False
    turn=random.randint(player,bot)
    
  

    # FPS
    FPS = 60
    frames_per_sec = pygame.time.Clock()


    # board 2D array
    board_ = board(row,column)
    print(board_)


     # game screen
    SCREEN = pygame.display.set_mode(screen_size)
    SCREEN.fill(WHITE)
    pygame.display.set_caption('Gomoku By Ahsan Ali ')

    # font
    my_font = pygame.font.Font('freesansbold.ttf', 32)

    # text message
    label_1 = my_font.render('Black wins!', True, WHITE, BLACK)
    label_2 = my_font.render('White wins!', True, WHITE, BLACK)
    label_3 = my_font.render('Draw!', True, WHITE, BLACK)

    # display the screen
    draw_board(SCREEN)
    if turn == bot:
        drop_piece(board_,4,4,piece_2)
        draw_piece(SCREEN,board_)
        turn =player

    

    while not game_over:
        
        #exit button functionality 
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            #check the user mouse movement and get position where the user want to put piece
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x_pos = event.pos[0]
                y_pos = event.pos[1]

                col_ = int(math.floor(x_pos / block_size))
                row_ = int(math.floor(y_pos / block_size))

                # turn decision, if black(1)/white(2) piece already placed, go back to the previous turn
                if board_[row_][col_] == 1 or board_[row_][col_] == 2:
                    turn = player

                #Ask for player 1 Input
                if turn==player:
                    if is_location_valid(board_,row_,col_):
                        drop_piece(board_,row_,col_,piece_1)
                        draw_piece(SCREEN,board_)
                    
                        if check_winner(board_,piece_1):
                            print("Player 1 Wins !!!!!!!")
                            SCREEN.blit(label_1, (280,50))
                            pygame.display.update()
                            game_over=True

                        turn = bot
                        
                        

        if turn==bot and not  game_over:
            #calling of aplha_beta_pruning to get best move for Bot
            r_c = alpha_beta_pruning(board_,2,True, -math.inf, math.inf)[0]
            row_,col_=r_c

            #if the move suggested by the aplha_beta_pruning is already filled then again turn set to bot
            if board_[row_][col_] == piece_1 or board_[row_][col_] == piece_2:
                    turn = bot
            
            if is_location_valid(board_,row_,col_):
                pygame.time.wait(500)
                drop_piece(board_,row_,col_,piece_2)
                draw_piece(SCREEN,board_)
            
                if check_winner(board_,2):
                    print("Player 2  Wins !!!!!!!")
                    SCREEN.blit(label_2, (280,50))
                    pygame.display.update()
                    game_over=True
                turn = player
                
            print(board_)
        
        if  np.count_nonzero(board_==0) == 0 and not game_over:
            SCREEN.blit(label_3, (280,50))
            pygame.display.update()
            print("Draw!!!! Game Over!!")
            pygame.time.wait(4000)
            break

        if game_over:
            pygame.time.wait(4000)

        frames_per_sec.tick(FPS)

if __name__ == '__main__':
    main()