import class_2048
import os
from ai_2048 import predict_move, argmax_dict, highest_tile
import time

clear = lambda: os.system('cls')

playboard = class_2048.board()
playboard.random_appear()
playboard.random_appear()
move = ''
alpha = 2
beta = 1.9
gamma = 10
delta = 4.2
num_move = 1

while (not playboard.game_over()):
    move = argmax_dict(predict_move(playboard, 3, True,alpha,beta,gamma,delta))
    clear()
    print('move : ', num_move)
    print()
    playboard.show_board()
    playboard.move(move)
    print()
    playboard.show_board()
    time.sleep(3)
    num_move += 1
    

print('Permainan selesai')