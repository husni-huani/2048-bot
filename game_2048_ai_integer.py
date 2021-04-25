from class_int_represent import move, random_appear, game_over
from ai_2048_integer import predict_move, argmax_dict
import pygame
import time

def play_game(board, tuple):
    alpha = tuple[0]
    beta = tuple[1]

    board = random_appear(board)
    board = random_appear(board)

    running = True

    while (running):
        screen.fill((0,0,0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        num_move = predict_move(board, 3, 0, alpha, beta)[0]

        board = move(board, num_move)
        # move_block(playboard)

        display_board(board)
        pygame.display.update()
        if game_over(board):
            pygame.display.update()
            running = False
            time.sleep(4)
    time.sleep(0.1)
    #return (highest_tile(playboard.represent_string()), game_score(playboard.represent_string()))

pygame.init()
screen = pygame.display.set_mode( (600, 600) )
pygame.display.set_caption('2048 game')

arr_num = [0,2,4,8,16,32,64,128,256,512,1024,2048,4096,8192,16384,32768]
gambar_angka = {}
for i in arr_num:
    filename = 'gambar_angka/angka_' + str(i) + '.png'
    gambar_angka[i] = pygame.image.load(filename)


arr_pos_tuple = [ [(i*70, j*70) for j in range(6)] for i in range(6)]

def display_tile(i,j, val):
    screen.blit(gambar_angka[val], (i*70, j*70))

def display_board(board):
    test_bit = 15
    for pos in range(16):
        i = (pos//4) + 1
        j = (pos%4) + 1
        current_num = 2**((board >> (15-pos)*4) & test_bit)
        if current_num == 1:
            current_num = 0
        display_tile(j,i, current_num)

# Coba-coba

def move_block(playboard):
    duration = 0
    frame = 15
    move_matrix = playboard.prev_move
    position_matrix = [ [(i,j) for j in range(6)] for i in range(6)]
    for k in range(frame):
        screen.fill((0,0,0))
        for i in range(1,5):
            for j in range(1,5):
                display_tile(j, i, 0)

        for i in range(1,5):
            for j in range(1,5):
                if not (move_matrix[i][j] == (0,0)):
                    val = playboard.prev_val[i][j].val
                    prev_tuple = position_matrix[i][j]
                    delta_matrix = (move_matrix[i][j][0] - i, move_matrix[i][j][1] -j)
                    position_matrix[i][j] = (prev_tuple[0] + delta_matrix[0]/frame, prev_tuple[1] + delta_matrix[1]/frame)
                    display_tile(position_matrix[i][j][1], position_matrix[i][j][0], val)
        pygame.display.update()
        # time.sleep(duration/frame)



#
#   Game AI
#

# alpha, beta, gamma, delta = 2,2,10,4 awalnya

alpha = 2
beta = 1.9


playboard = 0
play_game(playboard, (alpha, beta))

