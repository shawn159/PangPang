from bangtal import *
import random
import time
import os

setGameOption(GameOption.INVENTORY_BUTTON, False)
setGameOption(GameOption.MESSAGE_BOX_BUTTON, False)


start_scene = Scene('Pang Pang', 'images/start_scene.png')
game_scene = Scene('Pang Pang', 'images/game_scene.png')

start_button = Object('images/start_button.png')
restart_button = Object('images/restart.png')

GAME_BASE_X = 350
GAME_BASE_Y = 70
UNIT_LEN = 64

SCORE_BASE_X = 1150
SCORE_BASE_Y = 450
SCORE_LEN = 35

MOVE_BASE_X = 160
MOVE_BASE_Y = 450
MOVE_LEN = 35

APPLE = 0 #0.13
GRAPE = 1
ORANGE = 2
LEMON = 3
PEAR = 4
BOMB = 5 #0.14
DYNAMITE = 6
TNT = 7

U = 0
D = 1
R = 2
L = 3

start_button.locate(start_scene, 50, 80)
start_button.show()

game_data = None

cwd = os.getcwd()
records_file = os.path.join(cwd, 'records.txt')
if not os.path.exists(records_file):
    with open(records_file, 'w') as f:
        f.write('0')

def  transparent_screen_on_click(x, y, action):
    idx_x = x // 65
    idx_y = y // 65
    if idx_y < 8 and action == MouseAction.DRAG_UP:
        game_data.move_control(idx_x, idx_y, U)
    elif idx_y > 0 and action == MouseAction.DRAG_DOWN:
        game_data.move_control(idx_x, idx_y, D)
    elif idx_x < 8 and action == MouseAction.DRAG_RIGHT:
        game_data.move_control(idx_x, idx_y, R)
    elif idx_x > 0 and action == MouseAction.DRAG_LEFT:
        game_data.move_control(idx_x, idx_y, L)
    else:
        pass

class GameData:
    def __init__(self):
        self.move_count = 20
        self.score = 0
        self.transparent_screen = Object('images/game_scene.png')
        self.num_data = []
        self.img_data = []
        self.score_img = []
        self.move_img = []
        for j in range(9):
            num_data_line = []
            img_data_line = []
            for i in range(9):
                fruit = random.randrange(0, 5)
                num_data_line.append(fruit)
                if fruit == APPLE:
                    apple = Object('images/apple.png')
                    apple.setScale(0.13)
                    apple.locate(game_scene, GAME_BASE_X + i * UNIT_LEN, GAME_BASE_Y + j * UNIT_LEN)
                    apple.show()
                    img_data_line.append(apple)
                elif fruit == GRAPE:
                    grape = Object('images/grape.png')
                    grape.setScale(0.13)
                    grape.locate(game_scene, GAME_BASE_X + i * UNIT_LEN, GAME_BASE_Y + j * UNIT_LEN)
                    grape.show()
                    img_data_line.append(grape)
                elif fruit == ORANGE:
                    orange = Object('images/orange.png')
                    orange.setScale(0.13)
                    orange.locate(game_scene, GAME_BASE_X + i * UNIT_LEN, GAME_BASE_Y + j * UNIT_LEN)
                    orange.show()
                    img_data_line.append(orange)
                elif fruit == LEMON:
                    lemon = Object('images/lemon.png')
                    lemon.setScale(0.13)
                    lemon.locate(game_scene, GAME_BASE_X + i * UNIT_LEN, GAME_BASE_Y + j * UNIT_LEN)
                    lemon.show()
                    img_data_line.append(lemon)
                elif fruit == PEAR:
                    pear = Object('images/pear.png')
                    pear.setScale(0.13)
                    pear.locate(game_scene, GAME_BASE_X + i * UNIT_LEN, GAME_BASE_Y + j * UNIT_LEN)
                    pear.show()
                    img_data_line.append(pear)
                else:
                    pass

            self.num_data.append(num_data_line)
            self.img_data.append(img_data_line)

        self.score_logo = Object('images/score.png')
        self.score_logo.locate(game_scene, 930, 535)
        self.score_logo.show()

        self.move_logo = Object('images/move.png')
        self.move_logo.locate(game_scene, 30, 535)
        self.move_logo.show()

        restart_button.locate(game_scene, 960, 80)
        restart_button.show()

        self.complete_map_movement()
        self.score = 0
        self.show_score()
        self.show_move()

    def reset_transparent_screen(self):
        self.transparent_screen.hide()
        del self.transparent_screen
        self.transparent_screen = Object('images/game_scene.png')
        self.transparent_screen.locate(game_scene, 341, 61)
        self.transparent_screen.show()
        self.transparent_screen.onMouseAction = transparent_screen_on_click

    def show_score(self):
        for img in self.score_img:
            img.hide()
        self.score_img = []
        for idx, num in enumerate(str(self.score)[::-1]):
            file_name = 'images/' + num + '.png'
            number = Object(file_name)
            number.locate(game_scene, SCORE_BASE_X - idx * SCORE_LEN, SCORE_BASE_Y)
            number.show()
            self.score_img.insert(0, number)

    def show_move(self):
        for img in self.move_img:
            img.hide()
        self.move_img = []
        for idx, num in enumerate(str(self.move_count)[::-1]):
            file_name = 'images/m' + num + '.png'
            number = Object(file_name)
            number.locate(game_scene, MOVE_BASE_X - idx * MOVE_LEN, MOVE_BASE_Y)
            number.show()
            self.move_img.insert(0, number)

    def create_explosive(self, x, y, explosive):
       if explosive == BOMB:
            bomb = Object('images/bomb.png')
            bomb.setScale(0.15)
            bomb.locate(game_scene, GAME_BASE_X + x * UNIT_LEN, GAME_BASE_Y + y * UNIT_LEN)
            bomb.show()
            self.num_data[y][x] = BOMB
            self.img_data[y][x] = bomb
       elif explosive == DYNAMITE:
            dynamite = Object('images/dynamite.png')
            dynamite.setScale(0.13)
            dynamite.locate(game_scene, GAME_BASE_X + x * UNIT_LEN, GAME_BASE_Y + y * UNIT_LEN)
            dynamite.show()
            self.num_data[y][x] = DYNAMITE
            self.img_data[y][x] = dynamite
       elif explosive == TNT:
            tnt = Object('images/tnt.png')
            tnt.setScale(0.13)
            tnt.locate(game_scene, GAME_BASE_X + x * UNIT_LEN, GAME_BASE_Y + y * UNIT_LEN)
            tnt.show()
            self.num_data[y][x] = TNT
            self.img_data[y][x] = tnt
       else:
            pass

    def continuous_check(self, check_list):
        max_count = 1
        distroy_target = []
        check_list.sort()

        for idx in check_list:
            x = idx % 9 + 1
            hor_check = [idx]
            hor_count = 1
            cmp_val = idx + 1
            while x < 9:
                if cmp_val in check_list:
                    hor_count += 1
                    hor_check.append(cmp_val)
                    cmp_val += 1
                    x += 1
                else:
                    break
            if hor_count > 2:
                distroy_target += hor_check
                if hor_count > max_count:
                    max_count = hor_count

            y = idx // 9 + 1
            ver_check = [idx]
            ver_count = 1
            cmp_val = idx + 9
            while y < 9:
                if cmp_val in check_list:
                    ver_count += 1
                    ver_check.append(cmp_val)
                    cmp_val += 9
                    y += 1
                else:
                    break
            if ver_count > 2:
                distroy_target += ver_check
                if ver_count > max_count:
                    max_count = ver_count

        return max_count, list(set(distroy_target))

    def matched_control(self, matched_list, option, locate_x, locate_y):
        local_scan = 0
        global_scan = 1

        max_continue, target_list = self.continuous_check(matched_list)
        num = len(target_list)
        if num > 2:
            for idx in target_list:
                x = idx % 9
                y = idx // 9
                self.num_data[y][x] = -1
                self.img_data[y][x].hide()
                del self.img_data[y][x]
                self.img_data[y].insert(x, None)
                self.score += 1
            x = 0
            y = 0
            if option == local_scan:
                x = locate_x
                y = locate_y
            elif option == global_scan:
                index = min(target_list)
                x = index % 9
                y = index // 9
            else:
                pass

            if num == 3:
                pass
            elif num == 4:
                self.create_explosive(x, y, BOMB)
            elif num == 5:
                if max_continue >= 5:
                    self.create_explosive(x, y, TNT)
                else:
                    self.create_explosive(x, y, DYNAMITE)
            elif num == 6:
                if max_continue >= 5:
                    self.create_explosive(x, y, TNT)
                else:
                    self.create_explosive(x, y, DYNAMITE)
            else:
                if max_continue >= 5:
                    self.create_explosive(x, y, TNT)
                else:
                    self.create_explosive(x, y, DYNAMITE)
            return True
        else:
            return False


    def matched_full_scan(self):
        moved = False
        global_checked = []

        for j in range(9):
            for i in range(9):
                checked = []
                to_check = []
                seq_num = i + j * 9
                if seq_num not in global_checked:
                    fruit = self.num_data[j][i]
                    to_check.append(seq_num)
                    while to_check:
                        element = to_check.pop()
                        x = element % 9
                        y = element // 9
                        if y < 8 and element + 9 not in checked and self.num_data[y + 1][x] == fruit:
                            if element + 9 not in to_check:
                                to_check.append(element + 9)
                        if y > 0 and element - 9 not in checked and self.num_data[y - 1][x] == fruit:
                            if element - 9 not in to_check:
                                to_check.append(element - 9)
                        if x < 8 and element + 1 not in checked and self.num_data[y][x + 1] == fruit:
                            if element + 1 not in to_check:
                                to_check.append(element + 1)
                        if x > 0 and element - 1 not in checked and self.num_data[y][x - 1] == fruit:
                            if element - 1 not in to_check:
                                to_check.append(element - 1)
                        checked.append(element)
                if len(checked) > 2 and self.matched_control(checked, 1, 0, 0):
                    moved = True
                global_checked += checked

        return moved

    def matched_local_scan(self, i, j):
        moved = False
        checked = []
        to_check = []
        seq_num = i + j * 9
        fruit = self.num_data[j][i]
        to_check.append(seq_num)
        while to_check:
            element = to_check.pop()
            x = element % 9
            y = element // 9
            if y < 8 and element + 9 not in checked and self.num_data[y + 1][x] == fruit:
                if element + 9 not in to_check:
                    to_check.append(element + 9)
            if y > 0 and element - 9 not in checked and self.num_data[y - 1][x] == fruit:
                if element - 9 not in to_check:
                    to_check.append(element - 9)
            if x < 8 and element + 1 not in checked and self.num_data[y][x + 1] == fruit:
                if element + 1 not in to_check:
                    to_check.append(element + 1)
            if x > 0 and element - 1 not in checked and self.num_data[y][x - 1] == fruit:
                if element - 1 not in to_check:
                    to_check.append(element - 1)
            checked.append(element)
        if len(checked) > 2 and self.matched_control(checked, 0, i, j):
            moved = True

        return moved

    def push_down_element(self):
        for i in range(9):
            for j in range(9):
                if self.num_data[j][i] != -1:
                    bottom_idx = j - 1
                    while bottom_idx >= 0:
                        if self.num_data[bottom_idx][i] != -1:
                            break
                        bottom_idx -= 1
                    if j - bottom_idx > 1:
                        new_j = bottom_idx + 1
                        self.num_data[new_j][i] = self.num_data[j][i]
                        self.num_data[j][i] = -1
                        self.img_data[j][i].locate(game_scene, GAME_BASE_X + i * UNIT_LEN, GAME_BASE_Y + new_j * UNIT_LEN)
                        self.img_data[new_j][i] = self.img_data[j][i]
                        self.img_data[j][i] = None
        self.refill_element()

    def refill_element(self):
        for i in range(9):
            for j in range(9):
                if self.num_data[j][i] == -1:
                    fruit = random.randrange(0, 5)
                    self.num_data[j][i] = fruit
                    if fruit == APPLE:
                        apple = Object('images/apple.png')
                        apple.setScale(0.13)
                        apple.locate(game_scene, GAME_BASE_X + i * UNIT_LEN, GAME_BASE_Y + j * UNIT_LEN)
                        apple.show()
                        self.img_data[j][i] = apple
                    elif fruit == GRAPE:
                        grape = Object('images/grape.png')
                        grape.setScale(0.13)
                        grape.locate(game_scene, GAME_BASE_X + i * UNIT_LEN, GAME_BASE_Y + j * UNIT_LEN)
                        grape.show()
                        self.img_data[j][i] = grape
                    elif fruit == ORANGE:
                        orange = Object('images/orange.png')
                        orange.setScale(0.13)
                        orange.locate(game_scene, GAME_BASE_X + i * UNIT_LEN, GAME_BASE_Y + j * UNIT_LEN)
                        orange.show()
                        self.img_data[j][i] = orange
                    elif fruit == LEMON:
                        lemon = Object('images/lemon.png')
                        lemon.setScale(0.13)
                        lemon.locate(game_scene, GAME_BASE_X + i * UNIT_LEN, GAME_BASE_Y + j * UNIT_LEN)
                        lemon.show()
                        self.img_data[j][i] = lemon
                    elif fruit == PEAR:
                        pear = Object('images/pear.png')
                        pear.setScale(0.13)
                        pear.locate(game_scene, GAME_BASE_X + i * UNIT_LEN, GAME_BASE_Y + j * UNIT_LEN)
                        pear.show()
                        self.img_data[j][i] = pear
                else:
                    pass


    def complete_map_movement(self):
        while self.matched_full_scan():
            self.push_down_element()
        self.reset_transparent_screen()

    def move_control(self, x, y, dir):
        moved = False
        fruit = self.num_data[y][x]
        x_switch = x
        y_switch = y

        if dir == U:
            y_switch += 1
        elif dir == D:
            y_switch -= 1
        elif dir == R:
            x_switch += 1
        elif dir == L:
            x_switch -= 1
        else:
            pass

        if fruit == BOMB:
            seq_num = x_switch + y_switch * 9
            target = [seq_num - 1, seq_num, seq_num + 1, seq_num - 9, seq_num + 9]
            for idx in target:
                if idx >= 0 and idx <= 80:
                    i = idx % 9
                    j = idx // 9
                    self.num_data[j][i] = -1
                    self.img_data[j][i].hide()
                    del self.img_data[j][i]
                    self.img_data[j].insert(i, None)
                    self.score += 1
            self.score += 3
            moved = True
        elif fruit == DYNAMITE:
            seq_num = x_switch + y_switch * 9
            target = []
            for k in range(3):
               for l in range(3):
                   target.append(seq_num - 10 + l + 9 * k)
            for idx in target:
                if idx >= 0 and idx <= 80:
                    i = idx % 9
                    j = idx // 9
                    self.num_data[j][i] = -1
                    self.img_data[j][i].hide()
                    del self.img_data[j][i]
                    self.img_data[j].insert(i, None)
                    self.score += 1
            self.score += 7
            moved = True
        elif fruit == TNT:
            seq_num = x_switch + y_switch * 9
            target = []
            for k in range(5):
               for l in range(5):
                   target.append(seq_num - 20 + l + 9 * k)
            for idx in target:
                if idx >= 0 and idx <= 80:
                    i = idx % 9
                    j = idx // 9
                    self.num_data[j][i] = -1
                    self.img_data[j][i].hide()
                    del self.img_data[j][i]
                    self.img_data[j].insert(i, None)
                    self.score += 1
            self.score += 15
            moved = True
        else:
            temp = self.num_data[y][x]
            self.num_data[y][x] = self.num_data[y_switch][x_switch]
            self.num_data[y_switch][x_switch] = temp

            temp_img = self.img_data[y][x]
            self.img_data[y][x] = self.img_data[y_switch][x_switch]
            self.img_data[y_switch][x_switch] = temp_img 

            moved1 = self.matched_local_scan(x, y)
            moved2 = self.matched_local_scan(x_switch, y_switch)
            if moved1 and moved2:
                moved = True
            elif moved1 and not moved2:
                self.img_data[y_switch][x_switch].locate(game_scene, GAME_BASE_X + x_switch * UNIT_LEN, GAME_BASE_Y + y_switch * UNIT_LEN)
                moved = True
            elif not moved1 and moved2:
                self.img_data[y][x].locate(game_scene, GAME_BASE_X + x * UNIT_LEN, GAME_BASE_Y + y * UNIT_LEN)
                moved = True
            else:
                pass

        if moved:
            self.move_count -= 1
            self.push_down_element()
            self.complete_map_movement()
            self.show_score()
            self.show_move()
            if self.move_count < 1:
                self.transparent_screen.hide()
                self.finish_game()
        else:
            showMessage('터르릴 수 있는게 없어요!!')

    def finish_game(self):
        f = open(records_file, 'r')
        top_record = int(f.read())
        f.close()

        if self.score > top_record:
            with open(records_file, 'w') as f:
                f.write(str(self.score))
            showMessage('새로운 기록 갱신!! ' + str(self.score) + ' 점')
        else:
            showMessage('기록 갱신 실패.. ' + str(self.score) + ' 점')

def start_button_on_click(x, y, action):
    global game_data
    game_data = GameData()
    game_scene.enter()

start_button.onMouseAction = start_button_on_click

def restart_button_on_click(x, y, action):
    global game_scene
    global game_data
    game_scene = Scene('Pang Pang', 'images/game_scene.png')
    game_data = GameData()
    game_scene.enter()

restart_button.onMouseAction = restart_button_on_click


startGame(start_scene)