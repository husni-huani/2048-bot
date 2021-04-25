import class_2048
from ai_2048_2 import predict_move, argmax_dict, highest_tile
import pygame
import time

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
    duration = 0.01
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
        time.sleep(duration/frame)






running = True

alpha = 1.2
beta = 1.7
gamma = -2
delta = 3.7
increment = 0.1


playboard = class_2048.board()
playboard.random_appear()
playboard.random_appear()
prev_time = time.time()
prev_state = playboard.represent_string()
running = True
while (running):
    screen.fill((0,0,0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
    move = argmax_dict(predict_move(playboard, 3, True,alpha,beta, gamma))
    
    playboard.move(move)
    move_block(playboard)
    time.sleep(0.05)

    display_board(playboard.represent_string())
    pygame.display.update()
    time.sleep(0.05)

    if int(time.time() - prev_time) > 3:
        if prev_state == playboard.represent_string():
            print('Error')
            break
        prev_time = time.time()
        prev_state = playboard.represent_string()

    if playboard.game_over():
        pygame.display.update()
        running = False

print('Permainan selesai')
print(highest_tile(playboard.represent_string()))