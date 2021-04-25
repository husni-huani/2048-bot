from class_int_represent import possible_move, possible_state_2, move_no_appear
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

def count_set_bits(n): 
    count = 0
    while (n): 
        count += n & 1
        n >>= 1
    return count 

def argmax_dict(dict):
    ans_key = ''
    ans_val = -100
    for key in dict:
        if ans_val < dict[key]:
            ans_key = key
            ans_val = dict[ans_key]
    return ans_key

def count_score(board, alpha, beta):

    score = 0
    tidy_score = 0
    r_const = 0.85
    test_bit = 15
    count_empty = 0
    for i in range(16):
        pos = index_to_pos(i)
        current_bit = (board >> (pos*4)) & test_bit
        tidy_score += current_bit * r_const**(pos)
        if current_bit == 0:
            count_empty += 1
    
    score = sigmoid(tidy_score*alpha + count_empty*beta)

    return score

def predict_move(board, max_iter, num_iter, alpha, beta):
    if num_iter == max_iter-1:
        int_move = possible_move(board)
        number_move = count_set_bits(int_move)
        if number_move == 0:
            return 0
        else:
            dict_score = {}
            for i in range(4):
                if ((int_move >> i) & 1) != 0:
                    playboard_temp = board
                    playboard_temp = move_no_appear(playboard_temp, i)
                    possible_state = possible_state_2(playboard_temp)
                    heuristic_score = 0
                    if len(possible_state) != 0:
                        for state in possible_state:
                            heuristic_score += count_score(state, alpha, beta)
                        heuristic_score /= int(len(possible_state))
                    dict_score[i] = heuristic_score
            optimal_move = argmax_dict(dict_score)
            return (optimal_move, dict_score[optimal_move])
    else:
        int_move = possible_move(board)
        number_move = count_set_bits(int_move)
        if number_move == 0:
            return 0
        else:
            dict_score = {}
            for i in range(4):
                if ((int_move >> i) & 1) != 0:
                    playboard_temp = board
                    playboard_temp = move_no_appear(playboard_temp, i)
                    possible_state = possible_state_2(playboard_temp)
                    heuristic_score = 0
                    if len(possible_state) != 0:
                        for state in possible_state:
                            heuristic_score += predict_move(state, max_iter, num_iter+1, alpha, beta)[1]
                        heuristic_score /= int(len(possible_state))
                    dict_score[i] = heuristic_score
            optimal_move = argmax_dict(dict_score)
            return (optimal_move, dict_score[optimal_move])
