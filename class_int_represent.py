import random

# board merupakan suatu integer 64-bit yang merepresentasikan suatu board 2048

def one_or_two():
    num = random.randint(1,10)
    if num == 1:
        return 2
    else:
        return 1

def num_tile(num_bit):
    if num_bit == 0:
        return 0
    return 2**num_bit

def show_board(board):
    test_bit = 15
    for i in range(4):
        for j in range(4):
            pos = ((4-i)*4 -(j+1))*4
            current_bit = (board >> pos) & test_bit
            print(num_tile(current_bit), end=' ')
        print()

def random_appear(board):
    count_zero = 0
    test_bit = 15
    save_zero_bit = 0
    for i in range(16):
        pos = (15-i)*4
        current_bit = (board >> pos) & test_bit
        if current_bit==0:
            count_zero += 1
            save_zero_bit = (1 << i) | save_zero_bit
    num = random.randint(1, count_zero)
    found_zero = 0
    for i in range(16):
        pos = 15-i
        current_bit = (save_zero_bit >> pos) & 1
        if current_bit == 1:
            found_zero += 1
            if found_zero == num:
                break
    board = board | (one_or_two() << i*4)
    return board

def move_right_16_bit(bit_16):
    analyze_index = -1
    test_bit = 15
    ans = bit_16
    for j in range(4,0,-1):
        current_bit = (ans >> ((4-j)*4)) & test_bit
        if j==4:
            if current_bit != 0:
                analyze_index = 4
        else:
            if current_bit != 0:
                if analyze_index == -1:
                    ans = ans | current_bit
                    ## 0 lin j awal
                    temp_bit = '1111111111111111'
                    for i in range(4):
                        index = j*4 - i - 1
                        temp_bit = temp_bit[:index] + '0' + temp_bit[index+1:]
                    ans = ans & int(temp_bit, 2)
                    analyze_index = 4
                else:
                    current_analyze_bit = (ans >> ((4-analyze_index)*4)) & test_bit
                    if current_bit == current_analyze_bit:
                        temp_bit = '1111111111111111'
                        for i in range(4):
                            index = analyze_index*4 - i - 1
                            temp_bit = temp_bit[:index] + '0' + temp_bit[index+1:]
                        ans = ans & int(temp_bit, 2)
                        ans = ans | ((current_bit+1) << (4-analyze_index)*4)
                        ## 0 lin j awal
                        temp_bit = '1111111111111111'
                        for i in range(4):
                            index = j*4 - i - 1
                            temp_bit = temp_bit[:index] + '0' + temp_bit[index+1:]
                        ans = ans & int(temp_bit, 2)
                        analyze_index -= 1
                    else:
                        if current_analyze_bit == 0:
                            ans = ans | (current_bit << (4-analyze_index)*4)
                            temp_bit = '1111111111111111'
                            for i in range(4):
                                index = j*4 - i - 1
                                temp_bit = temp_bit[:index] + '0' + temp_bit[index+1:]
                            ans = ans & int(temp_bit, 2)
                        else:
                            ans = ans | (current_bit << (4-analyze_index+1)*4)
                            ## 0 lin j awal
                            if j != analyze_index-1:
                                temp_bit = '1111111111111111'
                                for i in range(4):
                                    index = j*4 - i - 1
                                    temp_bit = temp_bit[:index] + '0' + temp_bit[index+1:]
                                ans = ans & int(temp_bit, 2)
                            analyze_index -= 1
    return ans

def rotate_clockwise(board):
    ans_board = 0
    test_bit = 15
    for index in range(16):
        current_bit = (board >> (15-index)*4) & test_bit
        i = index // 4
        j = index % 4
        rotated_i, rotated_j = j, 3-i
        rotated_index = rotated_i*4 + rotated_j
        ans_board = ans_board | (current_bit << (15-rotated_index)*4)
    return ans_board

def rotate_counter(board):
    ans_board = 0
    test_bit = 15
    for index in range(16):
        current_bit = (board >> (15-index)*4) & test_bit
        i = index // 4
        j = index % 4
        rotated_i, rotated_j = 3-j, i
        rotated_index = rotated_i*4 + rotated_j
        ans_board = ans_board | (current_bit << (15-rotated_index)*4)
    return ans_board

def rotate_180(board):
    ans_board = 0
    test_bit = 15
    for index in range(16):
        current_bit = (board >> (15-index)*4) & test_bit
        rotated_index = 15-index
        ans_board = ans_board | (current_bit << (15-rotated_index)*4)
    return ans_board

move_lookup = [ [ [ [0 for i in range(16)] for i in range(16)] for i in range(16)] for i in range(16)]
for i in range(16):
    for j in range(16):
        for k in range(16):
            for l in range(16):
                bit_16 = (i << 12) | (j << 8) | (k << 4) | l
                move_lookup[i][j][k][l] = move_right_16_bit(bit_16)

def move_right(board):
    initial_board = board
    test_bit = int('1111111111111111', 2)
    moved_board = 0
    for i in range(4):
        bit_16 = (initial_board >> (3-i)*16) & test_bit
        i_1 = (bit_16 >> 12) & 15
        j = (bit_16 >> 8) & 15
        k = (bit_16 >> 4) & 15
        l = (bit_16 >> 0) & 15
        bit_moved_16 = move_lookup[i_1][j][k][l]
        moved_board = moved_board | (bit_moved_16 << (3-i)*16)
    ans_board = moved_board
    return ans_board

def move_left(board):
    initial_board = rotate_180(board)
    moved_board = move_right(initial_board)
    ans_board = rotate_180(moved_board)
    return ans_board

def move_up(board):
    initial_board = rotate_clockwise(board)
    moved_board = move_right(initial_board)
    ans_board = rotate_counter(moved_board)
    return ans_board

def move_down(board):
    initial_board = rotate_counter(board)
    moved_board = move_right(initial_board)
    ans_board = rotate_clockwise(moved_board)
    return ans_board

def can_move_right(board):
    order_arr = [i for i in range(16)]
    test_bit = int('1111', 2)
    for i in range(4):
        for j in range(2,-1,-1):
            current_bit = (board >> (order_arr[i*4 + j] *4)) & test_bit
            next_bit = (board >> (order_arr[i*4 + j + 1] *4)) & test_bit
            if current_bit != 0:
                if next_bit == 0 or current_bit == next_bit:
                    return True
    return False

def can_move_left(board):
    order_arr = [15-i for i in range(16)]
    test_bit = int('1111', 2)
    for i in range(4):
        for j in range(2,-1,-1):
            current_bit = (board >> (order_arr[i*4 + j] *4)) & test_bit
            next_bit = (board >> (order_arr[i*4 + j + 1] *4)) & test_bit
            if current_bit != 0:
                if next_bit == 0 or current_bit == next_bit:
                    return True
    return False

def can_move_up(board):
    order_arr = [3,7,11,15,2,6,10,14,1,5,9,13,0,4,8,12]
    test_bit = int('1111', 2)
    for i in range(4):
        for j in range(2,-1,-1):
            current_bit = (board >> (order_arr[i*4 + j] *4)) & test_bit
            next_bit = (board >> (order_arr[i*4 + j + 1] *4)) & test_bit
            if current_bit != 0:
                if next_bit == 0 or current_bit == next_bit:
                    return True
    return False

def can_move_down(board):
    order_arr = [12,8,4,0,13,9,5,1,14,10,6,2,15,11,7,3]
    test_bit = int('1111', 2)
    for i in range(4):
        for j in range(2,-1,-1):
            current_bit = (board >> (order_arr[i*4 + j] *4 )) & test_bit
            next_bit = (board >> (order_arr[i*4 + j + 1] *4)) & test_bit
            if current_bit != 0:
                if next_bit == 0 or current_bit == next_bit:
                    return True
    return False

### DICT move = {0 : 'up', 1 : 'right', 2 : 'down', 3 : 'left'}

def move_no_appear(board, move):
    if move==0:
        board = move_up(board)
    elif move==2:
        board = move_down(board)
    elif move==1:
        board = move_right(board)
    elif move==3:
        board = move_left(board)
    return board

def move(board, move):
    if move==0:
        board = move_up(board)
    elif move==2:
        board = move_down(board)
    elif move==1:
        board = move_right(board)
    elif move==3:
        board = move_left(board)
    board = random_appear(board)
    return board

def possible_move(board):
    answer = 0
    if can_move_up(board):
        answer += (1 << 0)
    if can_move_down(board):
        answer += (1 << 2)
    if can_move_left(board):
        answer += (1 << 3)
    if can_move_right(board):
        answer += (1 << 1)
    return answer

def possible_state_2(board):
    possible_state = []
    test_bit = 15
    for index in range(16):
        current_bit = (board >> (15-index)*4) & test_bit
        if current_bit == 0:
            temp_board = board | (2 << (15-index)*4)
            possible_state.append(temp_board)
    return possible_state
    
def game_over(board):
    if board == 0:
        return False
    if possible_move(board) == 0:
        return True
    return False


