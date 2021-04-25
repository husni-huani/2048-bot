import class_2048
from ai_2048 import predict_move, argmax_dict, highest_tile, game_score
from time import time

def play_game(playboard, tuple ):
    alpha = tuple[0]
    beta = tuple[1]
    gamma = tuple[2]
    delta = tuple[3]

    playboard.random_appear()
    playboard.random_appear()


    prev_time = time()
    prev_state = playboard.represent_string()

    running = True

    while (running):
        move = argmax_dict(predict_move(playboard, 3, True, alpha, beta, gamma, delta))
        playboard.move(move)

        if int(time() - prev_time) > 3:
            if prev_state == playboard.represent_string():
                break
            prev_time = time()
            prev_state = playboard.represent_string()

        if playboard.game_over():
            running = False
    return (highest_tile(playboard.represent_string()), game_score(playboard.represent_string()))

alpha = 2
beta = 2
gamma = 9.8
delta = 4
increment = 0.5

# 2.2, 2.2, 10.2 4.6


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

print('current value : ', (alpha,beta,gamma,delta))

generation = 1
start_time = time()

while True:
    print('generation : ', generation)
    arr_value = [(0,0) for i in range(9)]
    for index in range(9):
        print('    index : ', index)
        for rep in range(3):
            playboard = class_2048.board()
            print('        rep : ', rep, end='   ')
            tuple_value = (play_game(playboard, count_variable(index, alpha,beta,gamma,delta,increment)))
            arr_value[index] = (arr_value[index][0] + tuple_value[0], arr_value[index][1] + tuple_value[1])
            print(tuple_value)
        arr_value[index] = (arr_value[index][0]/3, arr_value[index][1]/3)
        print('        total : ', arr_value[index])
    index_pilihan = arr_value.index((max(arr_value)))
    if index_pilihan ==0:
        break
    (alpha,beta,gamma,delta) = count_variable(index_pilihan, alpha, beta, gamma, delta, increment)
    generation +=1
    print()
    print('index chosen : ', index_pilihan)
    print('current value : ', (alpha,beta,gamma,delta))
    print()

print('final value : ',alpha, beta, gamma, delta)
print('elapsed time : ', time()-start_time)