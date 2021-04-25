from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from ai_2048 import predict_move, argmax_dict, highest_tile
import class_2048

browser = webdriver.Chrome('chromedriver')
browser.get('https://play2048.co/')

def get_str_playboard():
    playboard = [[0 for i in range(6)] for i in range(6)]

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
        playboard[position_i][position_j] = max(playboard[position_i][position_j], value)
        
    str_playboard = ''
    for i in range(1,5):
        for j in range(1,5):
            str_playboard += ',' + str(playboard[i][j])
    
    return str_playboard[1:]

def get_board_from_str(str_playboard):
    playboard = class_2048.board()
    arr_playboard = str_playboard.split(',')
    for index in range(16):
        i = index//4 + 1
        j = index%4 + 1
        playboard.arr_val[i][j] = class_2048.tile(int(arr_playboard[index]))
    return playboard

body = browser.find_element_by_css_selector('body')
playboard = get_board_from_str(get_str_playboard())

alpha = 0.9
beta = 1.7
gamma = 9.3
delta = 3.5

while (not playboard.game_over()):
    move = argmax_dict(predict_move(playboard, 3, True,alpha,beta,gamma,delta))
    if move=='up':
        body.send_keys(Keys.ARROW_UP)
    elif move=='down':
        body.send_keys(Keys.ARROW_DOWN)
    elif move=='right':
        body.send_keys(Keys.ARROW_RIGHT)
    elif move=='left':
        body.send_keys(Keys.ARROW_LEFT)

    playboard = get_board_from_str(get_str_playboard())

    

print('Permainan selesai')
print()
playboard.show_board()