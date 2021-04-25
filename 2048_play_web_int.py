from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from ai_2048_integer import predict_move
from class_int_represent import game_over, show_board
from math import log
from time import sleep

browser = webdriver.Chrome('chromedriver')
browser.get('https://play2048.co/')

def get_board():
    board = 0

    tile_number = browser.find_element_by_xpath('/html/body/div[3]/div[4]/div[3]')
    tile_number.text
    num_of_tiles = len(tile_number.text.split('\n'))
    x_path_root = '/html/body/div[3]/div[4]/div[3]'

    for index in range(1, num_of_tiles+1):
        x_path = x_path_root + '/div[' + str(index) + ']'
        current_tile = browser.find_element_by_xpath(x_path)
        str_class = current_tile.get_attribute('class')
        value = int(str_class.split(' ')[1][5:])
        position_i = int(str_class.split(' ')[2][-1])
        position_j = int(str_class.split(' ')[2][-3])
        position = (position_i-1)*4 + position_j-1
        current_board_bit = (board >> ((15-position)*4)) & 15
        current_bit = int(log(value, 2))
        final_bit = max(current_bit, current_board_bit)
        temp_bit = '1'*64
        for i in range(4):
            index_pos = (15-position)*4 - i - 1
            temp_bit = temp_bit[:index_pos] + '0' + temp_bit[index_pos+1:]
        board = board & int(temp_bit, 2)
        board = board | (final_bit << ((15-position)*4))
    return board
        

body = browser.find_element_by_css_selector('body')
sleep(2)
board = get_board()

show_board(board)
print()
alpha = 2
beta = 1.9


while (not game_over(board)):
    move = predict_move(board, 2, 0, alpha, beta)[0]
    print(move)
    if move==0:
        body.send_keys(Keys.ARROW_UP)
    elif move==2:
        body.send_keys(Keys.ARROW_DOWN)
    elif move==1:
        body.send_keys(Keys.ARROW_RIGHT)
    elif move==3:
        body.send_keys(Keys.ARROW_LEFT)

    board = get_board()
    
    show_board(board)
    print()
    sleep(0.1)
    

print('Permainan selesai')
print()