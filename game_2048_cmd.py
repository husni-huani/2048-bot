import class_2048
import os

clear = lambda: os.system('cls')

playboard = class_2048.board()
playboard.random_appear()
playboard.random_appear()
move = ''
while (not playboard.game_over()):
    move = input('Masukkan langkah : ')
    clear()
    playboard.show_board()
    playboard.move(move)
    playboard.show_board()
    

print('Permainan selesai')