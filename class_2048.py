import random

# fungsi untuk mengeluarkan 2 dengan kemungkina 90% dan 4 dengan kemungkina 10%
def two_or_four():
    num = random.randint(1,10)
    if num == 1:
        return 4
    else:
        return 2


# Buat class tile
class tile:
    def __init__(self, val): # val buat nunjukin nilai tile berapa
        self.val = val
        
    def is_zero(self): # fungsi boolean apakah isi tile 0 atau bukan
        return self.val==0


# buat kelas board yang isinya array of tile
class board:
    def __init__(self):
        self.arr_val = [ [tile(0) for i in range(6)]  for i in range(6)] # buat matriks 6x6, tapi yang bakal dipakai dari indeks 1-4
        self.prev_val = [ [tile(0) for i in range(6)]  for i in range(6)]
        self.prev_move = [ [(0,0) for i in range(6)] for i in range(6) ]

    # nge show board
    def show_board(self):
        for i in range(1,5):
            for j in range(1,5):
                tile_ij_value = self.arr_val[i][j].val
                print(tile_ij_value, end = ' ')
            print()

    def show_board_prev(self):
        for i in range(1,5):
            for j in range(1,5):
                tile_ij_value = self.prev_val[i][j].val
                print(tile_ij_value, end = ' ')
            print()
    
    def update_prev_val(self):
        for i in range(6):
            for j in range(6):
                self.prev_val[i][j] = tile(self.arr_val[i][j].val)

    def show_move(self):
        for i in range(1,5):
            for j in range(1,5):
                move_ij_value = self.prev_move[i][j]
                print(move_ij_value, end = ' ')
            print()

    # kalo mau ngubah manual
    def manual_change(self,i,j, val):
        self.arr_val[i][j] = tile(val)
    
    # masukin angka dengan posisi random ke dalam matriks
    def random_appear(self):
        count_zero = 0
        for i in range(1,5):
            for j in range(1,5):
                if self.arr_val[i][j].is_zero():
                    count_zero += 1
        num = random.randint(1, count_zero)
        pos = 0
        done = False
        for i in range(1,5):
            if done:
                break
            for j in range(1,5):
                if self.arr_val[i][j].is_zero():
                    pos += 1
                if pos == num:
                    self.arr_val[i][j] = tile(two_or_four())
                    done = True
                    break
        
    # buat ngegerakin ke atas
    def move_up(self):
        self.prev_move = [ [(0,0) for i in range(6)] for i in range(6) ]
        for j in range(1,5):
            analyze_index = -1
            for i in range(1,5):
                if i==1:
                    if not self.arr_val[i][j].is_zero():
                        analyze_index = 1
                        self.prev_move[i][j] = (i,j)
                else:
                    if not self.arr_val[i][j].is_zero():
                        if analyze_index == -1:
                            self.arr_val[1][j] = tile(self.arr_val[i][j].val)
                            self.arr_val[i][j] = tile(0)
                            analyze_index = 1
                            self.prev_move[i][j] = (1, j)
                        else:
                            if self.arr_val[i][j].val == self.arr_val[analyze_index][j].val:
                                self.arr_val[analyze_index][j] = tile(2 * self.arr_val[i][j].val)
                                self.arr_val[i][j] = tile(0)
                                self.prev_move[i][j] = (analyze_index,j)
                                analyze_index += 1
                            else:
                                if self.arr_val[analyze_index][j].is_zero():
                                    self.arr_val[analyze_index][j] = tile(self.arr_val[i][j].val)
                                    self.arr_val[i][j] = tile(0)
                                    self.prev_move[i][j] = (analyze_index,j)
                                else:
                                    self.arr_val[analyze_index+1][j] = tile(self.arr_val[i][j].val)
                                    if i != analyze_index+1:
                                        self.arr_val[i][j] = tile(0)
                                    analyze_index += 1
                                    self.prev_move[i][j] = (analyze_index,j)
    
    # buat ngegerakin ke kiri
    def move_left(self):
        self.prev_move = [ [(0,0) for i in range(6)] for i in range(6) ]
        for i in range(1,5):
            analyze_index = -1
            for j in range(1,5):
                if j==1:
                    if not self.arr_val[i][j].is_zero():
                        analyze_index = 1
                        self.prev_move[i][j] = (i,j)
                else:
                    if not self.arr_val[i][j].is_zero():
                        if analyze_index == -1:
                            self.manual_change(i,1, self.arr_val[i][j].val)
                            self.manual_change(i,j, 0)
                            analyze_index = 1
                            self.prev_move[i][j] = (i, 1)
                        else:
                            if self.arr_val[i][j].val == self.arr_val[i][analyze_index].val:
                                self.manual_change(i, analyze_index, 2*self.arr_val[i][j].val)
                                self.manual_change(i,j, 0)
                                self.prev_move[i][j] = (i, analyze_index)
                                analyze_index += 1
                            else:
                                if self.arr_val[i][analyze_index].is_zero():
                                    self.manual_change(i, analyze_index, self.arr_val[i][j].val)
                                    self.manual_change(i,j, 0)
                                    self.prev_move[i][j] = (i, analyze_index)
                                else:
                                    self.manual_change(i, analyze_index+1, self.arr_val[i][j].val)
                                    if j != analyze_index+1:
                                        self.manual_change(i,j, 0)
                                    analyze_index += 1
                                    self.prev_move[i][j] = (i, analyze_index)

    # buat ngegerakin ke bawah
    def move_down(self):
        self.prev_move = [ [(0,0) for i in range(6)] for i in range(6) ]
        for j in range(1,5):
            analyze_index = -1
            for i in range(4,0,-1):
                if i==4:
                    if not self.arr_val[i][j].is_zero():
                        analyze_index = 4
                        self.prev_move[i][j] = (i, j)
                else:
                    if not self.arr_val[i][j].is_zero():
                        if analyze_index == -1:
                            self.arr_val[4][j] = tile(self.arr_val[i][j].val)
                            self.arr_val[i][j] = tile(0)
                            analyze_index = 4
                            self.prev_move[i][j] = (4, j)
                        else:
                            if self.arr_val[i][j].val == self.arr_val[analyze_index][j].val:
                                self.arr_val[analyze_index][j] = tile(2 * self.arr_val[i][j].val)
                                self.arr_val[i][j] = tile(0)
                                self.prev_move[i][j] = (analyze_index, j)
                                analyze_index -= 1
                            else:
                                if self.arr_val[analyze_index][j].is_zero():
                                    self.arr_val[analyze_index][j] = tile(self.arr_val[i][j].val)
                                    self.arr_val[i][j] = tile(0)
                                    self.prev_move[i][j] = (analyze_index, j)
                                else:
                                    self.arr_val[analyze_index-1][j] = tile(self.arr_val[i][j].val)
                                    if i != analyze_index-1:
                                        self.arr_val[i][j] = tile(0)
                                    analyze_index -= 1
                                    self.prev_move[i][j] = (analyze_index, j)

    # buat ngegerakin ke kanan
    def move_right(self):
        self.prev_move = [ [(0,0) for i in range(6)] for i in range(6) ]
        for i in range(1,5):
            analyze_index = -1
            for j in range(4,0,-1):
                if j==4:
                    if not self.arr_val[i][j].is_zero():
                        analyze_index = 4
                        self.prev_move[i][j] = (i, j)
                else:
                    if not self.arr_val[i][j].is_zero():
                        if analyze_index == -1:
                            self.manual_change(i,4, self.arr_val[i][j].val)
                            self.manual_change(i,j, 0)
                            analyze_index = 4
                            self.prev_move[i][j] = (i, 4)
                        else:
                            if self.arr_val[i][j].val == self.arr_val[i][analyze_index].val:
                                self.manual_change(i, analyze_index, 2*self.arr_val[i][j].val)
                                self.manual_change(i,j, 0)
                                self.prev_move[i][j] = (i, analyze_index)
                                analyze_index -= 1
                            else:
                                if self.arr_val[i][analyze_index].is_zero():
                                    self.manual_change(i, analyze_index, self.arr_val[i][j].val)
                                    self.manual_change(i,j, 0)
                                    self.prev_move[i][j] = (i, analyze_index)
                                else:
                                    self.manual_change(i, analyze_index-1, self.arr_val[i][j].val)
                                    if j != analyze_index-1:
                                        self.manual_change(i,j, 0)
                                    analyze_index -= 1
                                    self.prev_move[i][j] = (i, analyze_index)
    
    # boolean apakah bisa digerakin ke atas
    def can_move_up(self):
        for j in range(1,5):
            for i in range(2,5):
                if not self.arr_val[i][j].is_zero():
                    if self.arr_val[i-1][j].is_zero() or self.arr_val[i-1][j].val == self.arr_val[i][j].val:
                        return True
        return False
    
    # boolean apakah bisa digerakin ke bawah
    def can_move_down(self):
        for j in range(1,5):
            for i in range(3,0,-1):
                if not self.arr_val[i][j].is_zero():
                    if self.arr_val[i+1][j].is_zero() or self.arr_val[i+1][j].val == self.arr_val[i][j].val:
                        return True
        return False
    
    # boolean apakah bisa digerakin ke kiri
    def can_move_left(self):
        for i in range(1,5):
            for j in range(2,5):
                if not self.arr_val[i][j].is_zero():
                    if self.arr_val[i][j-1].is_zero() or self.arr_val[i][j-1].val == self.arr_val[i][j].val:
                        return True
        return False

    # boolean apakah bisa digerakin ke kanan
    def can_move_right(self):
        for i in range(1,5):
            for j in range(3,0,-1):
                if not self.arr_val[i][j].is_zero():
                    if self.arr_val[i][j+1].is_zero() or self.arr_val[i][j+1].val == self.arr_val[i][j].val:
                        return True
        return False
    
    # representasi string dari board
    def represent_string(self):
        ans = ""
        for i in range(1,5):
            for j in range(1,5):
                tile_ij_value = self.arr_val[i][j].val
                ans += ',' + str(tile_ij_value)
        return ans[1:]
    
    # untuk ngegerakin board
    def move(self, move):
        if move == 'up':
            if self.can_move_up():
                self.update_prev_val()
                self.move_up()
                self.random_appear()
                #print('\nMove executed\n')
            #else:
                #print('\nMove is prohibited\n')
        elif move == 'down':
            if self.can_move_down():
                self.update_prev_val()
                self.move_down()
                self.random_appear()
                #print('\nMove executed\n')
            #else:
                #print('\nMove is prohibited\n')
        elif move == 'left':
            if self.can_move_left():
                self.update_prev_val()
                self.move_left()
                self.random_appear()
                #print('\nMove executed\n')
            #else:
                #print('\nMove is prohibited\n')
        elif move == 'right':
            if self.can_move_right():
                self.update_prev_val()
                self.move_right()
                self.random_appear()
                #print('\nMove executed\n')
            #else:
                #print('\nMove is prohibited\n')
        #else:
            #print('\n\n')
    
    def move_no_appear(self, move):
        if move == 'up':
            if self.can_move_up():
                self.update_prev_val()
                self.move_up()
                #print('\nMove executed\n')
            #else:
                #print('\nMove is prohibited\n')
        elif move == 'down':
            if self.can_move_down():
                self.update_prev_val()
                self.move_down()
                #print('\nMove executed\n')
            #else:
                #print('\nMove is prohibited\n')
        elif move == 'left':
            if self.can_move_left():
                self.update_prev_val()
                self.move_left()
                #print('\nMove executed\n')
            #else:
                #print('\nMove is prohibited\n')
        elif move == 'right':
            if self.can_move_right():
                self.update_prev_val()
                self.move_right()
                #print('\nMove executed\n')
            #else:
                #print('\nMove is prohibited\n')
        #else:
            #print('\n\n')
    def possible_state_2(self):
        possible_state = []
        for i in range(1,5):
            for j in range(1,5):
                if self.arr_val[i][j].is_zero():
                    playboard_temp = self.copy_board()
                    playboard_temp.manual_change(i,j, 2)
                    possible_state.append(playboard_temp)
        return possible_state

    def random_appear(self):
        count_zero = 0
        for i in range(1,5):
            for j in range(1,5):
                if self.arr_val[i][j].is_zero():
                    count_zero += 1
        num = random.randint(1, count_zero)
        pos = 0
        done = False
        for i in range(1,5):
            if done:
                break
            for j in range(1,5):
                if self.arr_val[i][j].is_zero():
                    pos += 1
                if pos == num:
                    self.arr_val[i][j] = tile(two_or_four())
                    done = True
                    break


    # jika tidak ada lagi langkah yang bisa dijalankan, game berakhir
    def game_over(self):
        if not (self.can_move_down() or self.can_move_left() or self.can_move_right() or self.can_move_up()):
            return True
        return False
    
    def copy_board(self):
        playboard_temp = board()
        for i in range(6):
            for j in range(6):
                playboard_temp.arr_val[i][j] = self.arr_val[i][j]
                playboard_temp.prev_move[i][j] = self.prev_move[i][j]
                playboard_temp.prev_move[i][j] = self.prev_move[i][j]
        return playboard_temp