import pygame
import class_2048
from math import log

def sigmoid(x):
    return 1/(1+exp(-x))

def highest_tile(str_playboard):
    arr_playboard = str_playboard.split(',')
    max_tile = 0
    for num in arr_playboard:
        if max_tile < int(num):
            max_tile = int(num)
    return max_tile

def game_score(str_playboard):   
    arr_playboard = str_playboard.split(',')
    sum = 0
    for num in arr_playboard:
        sum += int(num)
    return sum

def count_score(str_playboard, alpha, beta, gamma, delta):
    arr_playboard = str_playboard.split(',')
    matrix_playboard = [ [0 for i in range(6)] for i in range(6)]
    for pos in range(16):
        i = (pos//4) + 1
        j = (pos%4) + 1
        matrix_playboard[i][j] = int(arr_playboard[pos])
    
    score = 0
    monotonicity = 0
    # ngitung monoton pada sumbu horizontal
    horizontal_monoton_ascend = 0
    horizontal_monoton_descend = 0
    for i in range(1,5):
        is_ascend = True
        is_descend = True
        for j in range(1,4):
            if matrix_playboard[i][j] > matrix_playboard[i][j+1]:
                is_descend = False
            if matrix_playboard[i][j] < matrix_playboard[i][j+1]:
                is_ascend = False
        horizontal_monoton_ascend += is_ascend
        horizontal_monoton_descend += is_descend

    # ngitung monton pada sumbu vertikal
    vertical_monoton_ascend = 0
    vertical_monoton_descend = 0
    for j in range(1,5):
        is_ascend = True
        is_descend = True
        for i in range(1,4):
            if matrix_playboard[i][j] > matrix_playboard[i+1][j]:
                is_descend = False
            if matrix_playboard[i][j] < matrix_playboard[i+1][j]:
                is_ascend = False
        vertical_monoton_ascend += is_ascend
        vertical_monoton_descend += is_descend

    if max(horizontal_monoton_ascend, horizontal_monoton_descend) < 2:
        monotonicity -= 1
    else:
        monotonicity += 1
    if max(vertical_monoton_ascend, vertical_monoton_descend) < 2:
        monotonicity -= 1
    else:
        monotonicity += 1

    count_same_bonus = 0
    for i in range(1,5):
        for j in range(1,5):
            if matrix_playboard[i][j] != 0:
                if matrix_playboard[i][j] == matrix_playboard[i][j+1]:
                    count_same_bonus += 1
                if matrix_playboard[i][j] == matrix_playboard[i+1][j]:
                    count_same_bonus += 1


    count_empty = 0
    for i in range(1,5):
        for j in range(1,5):
            if matrix_playboard[i][j] == 0:
                count_empty +=  1
    
    score_high_tile_corner = 0
    max_tile = 0
    for i in range(1,5):
        for j in range(1,5):
            if max_tile < matrix_playboard[i][j]:
                max_tile = matrix_playboard[i][j]
    
    if (matrix_playboard[1][1] == max_tile):
        score_high_tile_corner = 1


    # alpha 2, beta 2, gamma 10, delta 4

    score =  monotonicity*alpha + count_same_bonus*beta + score_high_tile_corner*gamma + count_empty*delta

    return score

def available_move(playboard):
    answer = ''
    if playboard.can_move_up():
        answer += ',up'
    if playboard.can_move_down():
        answer += ',down'
    if playboard.can_move_left():
        answer += ',left'
    if playboard.can_move_right():
        answer += ',right'
    return answer[1:]


def predict_move(playboard, next_move, is_root, alpha, beta, gamma, delta):
    if not is_root:
        if next_move == 0:
            return count_score(playboard.represent_string(), alpha, beta, gamma, delta)
        else:
            arr_move = available_move(playboard).split(',')
            number_move = len(arr_move)
            if number_move==0:
                return -100
            else:
                score = -100
                repetition = 1
                for move in arr_move:
                    temp_score = 0
                    for rep in range(repetition):
                        playboard_temp = playboard.copy_board()
                        playboard_temp.move(move)
                        temp_score += predict_move(playboard_temp,next_move-1, False, alpha, beta, gamma, delta)
                    temp_score /= repetition
                    score = max(score, temp_score)
                # score = score/number_move
                return score
    else:
        arr_move = available_move(playboard).split(',')
        number_move = len(arr_move)
        percentage_move = {'up' : 0, 'down' : 0, 'left' : 0, 'right' : 0}
        for move in arr_move:
            playboard_temp = playboard.copy_board()
            playboard_temp.move(move)
            percentage_move[move] = predict_move(playboard_temp, next_move-1, False,alpha, beta, gamma, delta)
        return percentage_move

def argmax_dict(dict):
    ans_key = ''
    ans_val = -100
    for key in dict:
        if ans_val < dict[key]:
            ans_key = key
            ans_val = dict[ans_key]
    return ans_key


pygame.init()
screen = pygame.display.set_mode( (1200, 1200) )
pygame.display.set_caption('2048')

arr_num = [0,2,4,8,16,32,64,128,256,512,1024,2048,4096,8192,16384,32768]
gambar_angka = {}
for i in arr_num:
    filename = 'gambar_angka/angka_' + str(i) + '.png'
    gambar_angka[i] = pygame.image.load(filename)
    gambar_angka[i] = pygame.transform.scale(gambar_angka[i], 31, 31)

arr_pos_absolute = [ [(i*150, j*150) for j in range(6)] for i in range(6)]

def display_tile(, val):
    screen.blit(gambar_angka[int(val)], (i*70, j*70))


def display_board(str_playboard):
    arr_playboard = str_playboard.split(',')
    for pos in range(16):
        i = (pos//4) + 1
        j = (pos%4) + 1
        display_tile(j,i, int(arr_playboard[pos]))

