import class_2048
from ai_2048 import predict_move, argmax_dict, highest_tile, game_score
import pygame
import time

def play_game(playboard, tuple ):
    alpha = tuple[0]
    beta = tuple[1]
    gamma = tuple[2]
    delta = tuple[3]

    playboard.random_appear()
    playboard.random_appear()

    running = True

    while (running):
        screen.fill((0,0,0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
        move = argmax_dict(predict_move(playboard, 3, True, alpha, beta, gamma, delta))
        playboard.move(move)
        move_block(playboard)

        display_board(playboard.represent_string())
        pygame.display.update()
        if playboard.game_over():
            pygame.display.update()
            running = False
    time.sleep(0)
    return (highest_tile(playboard.represent_string()), game_score(playboard.represent_string()))

pygame.init()
screen = pygame.display.set_mode( (600, 600) )
pygame.display.set_caption('2048')

arr_num = [0,2,4,8,16,32,64,128,256,512,1024,2048,4096,8192,16384,32768]
gambar_angka = {}
for i in arr_num:
    filename = 'gambar_angka/angka_' + str(i) + '.png'
    gambar_angka[i] = pygame.image.load(filename)

gambar_game_over = pygame.image.load('game_over.jpg')

arr_pos_tuple = [ [(i*70, j*70) for j in range(6)] for i in range(6)]

def display_tile(i,j, val):
    screen.blit(gambar_angka[int(val)], (i*70, j*70))

def display_game_over():
    screen.blit(gambar_game_over, (0, 60))

def display_board(str_playboard):
    arr_playboard = str_playboard.split(',')
    for pos in range(16):
        i = (pos//4) + 1
        j = (pos%4) + 1
        display_tile(j,i, int(arr_playboard[pos]))

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
gamma = 10
delta = 4.2
increment = 0.1

def count_variable(index, alpha, beta, gamma, delta, increment):
    if index==0:
        return (alpha,beta,gamma,delta)
    if index==1:
        return (alpha-increment,beta,gamma,delta)
    if index==2:
        return (alpha+increment,beta,gamma,delta)
    if index==3:
        return (alpha,beta-increment,gamma,delta)
    if index==4:
        return (alpha,beta+increment,gamma,delta)
    if index==5:
        return (alpha,beta,gamma-increment,delta)
    if index==6:
        return (alpha,beta,gamma+increment,delta)
    if index==7:
        return (alpha,beta,gamma,delta-increment)
    if index==8:
        return (alpha,beta,gamma,delta+increment)

generation = 1
while True:
    print('generation : ', generation)
    arr_value = [(0,0) for i in range(9)]
    for index in range(9):
        for rep in range(3):
            playboard = class_2048.board()
            print('     ',generation, index, rep, end='   ')
            tuple_value = (play_game(playboard, count_variable(index, alpha,beta,gamma,delta,increment)))
            arr_value[index] += (arr_value[index][0] + tuple_value[0], arr_value[index][1] + tuple_value[1])
            print(tuple_value)
    index_pilihan = arr_value.index((max(arr_value)))
    if index_pilihan ==0:
        break
    (alpha,beta,gamma,delta) = count_variable(index_pilihan, alpha, beta, gamma, delta, increment)
    generation +=1
    print()

print(alpha, beta, gamma, delta)