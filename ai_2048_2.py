import class_2048
from math import log, exp

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

def count_score(str_playboard, alpha, beta, gamma):
    arr_playboard = str_playboard.split(',')
    matrix_playboard = [ [0 for i in range(6)] for i in range(6)]
    for pos in range(16):
        i = (pos//4) + 1
        j = (pos%4) + 1
        matrix_playboard[i][j] = int(arr_playboard[pos])
    
    score = 0
    monotonicity = 0
    # ngitung monoton pada sumbu horizontal

    count_empty = 0
    for i in range(1,5):
        for j in range(1,5):
            if matrix_playboard[i][j] == 0:
                count_empty +=  1
    count_empty = sigmoid(count_empty)

    corner_score = 0
    max_tile = 0
    for i in range(1,5):
        for j in range(1,5):
            if max_tile < matrix_playboard[i][j]:
                max_tile = matrix_playboard[i][j]
    
    if (max_tile not in matrix_playboard[1]):
        corner_score = -100
    else:
        start = matrix_playboard[1].index(max_tile)
        done = False
        prev_val = max_tile
        for i in range(1,5):
            start_j = start if (i==1) else 1
            for j in range(start_j, 5):
                if i % 2 == 0:
                    j = 5-j
                if matrix_playboard[i][j] <= prev_val and matrix_playboard[i][j] != 0:
                    corner_score += 1
                else:
                    done = True
                    break
            if done:
                break
    corner_score = sigmoid(corner_score)

    difference_score = 0
    for i in range(1,5):
        for j in range(1,5):
            if matrix_playboard[i][j] != 0:
                if i==4 and j==1:
                    difference_score += 0
                elif (j==4 and i%2==1) and (j==1 and i%2==0):
                    if matrix_playboard[i+1][j] != 0:
                        difference_score += log(matrix_playboard[i][j], 2) - log(matrix_playboard[i+1][j], 2)
                else:
                    if i%2==1:
                        if matrix_playboard[i][j+1]:
                            difference_score += log(matrix_playboard[i][j], 2) - log(matrix_playboard[i][j+1], 2)
                    else:
                        if matrix_playboard[i][j-1]:
                            difference_score += log(matrix_playboard[i][j], 2) - log(matrix_playboard[i][j-1], 2)
    difference_score = sigmoid(difference_score)
                    
    # alpha 2, beta 2, gamma 10, delta 4

    score =  corner_score*alpha + count_empty*beta + difference_score*gamma

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


def predict_move(playboard, next_move, is_root, alpha, beta, gamma):
    if not is_root:
        if next_move == 0:
            return count_score(playboard.represent_string(), alpha, beta, gamma)
        else:
            arr_move = available_move(playboard).split(',')
            number_move = len(arr_move)
            if number_move==0:
                return -100
            else:
                score = -100
                for move in arr_move:
                    temp_score = 0
                    for rep in range(4):
                        playboard_temp = playboard.copy_board()
                        playboard_temp.move(move)
                        temp_score += predict_move(playboard_temp,next_move-1, False, alpha, beta, gamma)
                    temp_score /= 4
                    score = max(score, temp_score)
                # score = score/number_move
                return score
    else:
        arr_move = available_move(playboard).split(',')
        number_move = len(arr_move)
        percentage_move = {'up' : -100, 'down' : -100, 'left' : -100, 'right' : -100}
        for move in arr_move:
            playboard_temp = playboard.copy_board()
            playboard_temp.move(move)
            percentage_move[move] = predict_move(playboard_temp, next_move-1, False,alpha, beta, gamma)
        ##### COBA COBA NIH YA
        percentage_move['down'] = -90
        return percentage_move

def argmax_dict(dict):
    ans_key = ''
    ans_val = -100
    for key in dict:
        if ans_val < dict[key]:
            ans_key = key
            ans_val = dict[ans_key]
    return ans_key
