import class_2048
from math import log, exp

def sigmoid(x):
    return 1/(1+exp(-x))

def index_to_pos(num):
    if 0<=num<4:
        return num
    elif 8<=num<12:
        return num
    elif 4<=num<8:
        return 11-num
    elif 12<=num<16:
        return 27-num

def count_score(str_playboard, alpha, beta):
    arr_playboard = str_playboard.split(',')
    arr_playboard_sort = str_playboard.split(',')
    arr_playboard.sort(reverse = True)


    score = 0
    tidy_score = 0
    sort_score = 0
    r_const = 0.85

    for i in range(16):
        pos = index_to_pos(i)
        if arr_playboard[i] != '0':
            tidy_score += log(int(arr_playboard[i]) ,2) * r_const**(pos)
        if arr_playboard_sort[i] != '0':
            sort_score += log(int(arr_playboard_sort[i]), 2) * r_const**(pos)
    
    tidiness_score = tidy_score / sort_score

    count_empty = 0
    for i in range(16):
        if int(arr_playboard[i] == 0):
            count_empty += 1
    
    score = sigmoid(tidiness_score*alpha + count_empty*beta)

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

def argmax_dict(dict):
    ans_key = ''
    ans_val = -100
    for key in dict:
        if ans_val < dict[key]:
            ans_key = key
            ans_val = dict[ans_key]
    return ans_key

def predict_move(playboard, max_iter, num_iter, alpha, beta):
    if num_iter == max_iter-1:
        arr_move = available_move(playboard).split(',')
        number_move = len(arr_move)
        if number_move == 0:
            return -100
        else:
            dict_score = {}
            for move in arr_move:
                playboard_temp = playboard.copy_board()
                playboard_temp.move_no_appear(move)
                possible_state = playboard_temp.possible_state_2()
                heuristic_score = 0
                if len(possible_state) != 0:
                    for state in possible_state:
                        heuristic_score += count_score(state.represent_string(), alpha, beta)
                    heuristic_score /= int(len(possible_state))
                dict_score[move] = heuristic_score
            optimal_move = argmax_dict(dict_score)
            return (optimal_move, dict_score[optimal_move])
    else:
        arr_move = available_move(playboard).split(',')
        number_move = len(arr_move)
        if number_move == 0:
            return -100
        else:
            dict_score = {}
            for move in arr_move:
                playboard_temp = playboard.copy_board()
                playboard_temp.move_no_appear(move)
                possible_state = playboard_temp.possible_state_2()
                heuristic_score = 0
                if len(possible_state) != 0:
                    for state in possible_state:
                        heuristic_score += predict_move(state, max_iter, num_iter+1, alpha, beta)[1]
                    heuristic_score /= int(len(possible_state))
                dict_score[move] = heuristic_score
            optimal_move = argmax_dict(dict_score)
            return (optimal_move, dict_score[optimal_move])
