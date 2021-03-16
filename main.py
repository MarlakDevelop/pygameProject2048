import pygame
import json
from random import choice
from datetime import datetime

import settings


def read_json_file():
    with open(settings.DATA, 'r', encoding='utf-8') as JSONFile:
        return json.load(JSONFile)


def write_json_file(data):
    open(settings.DATA, 'w', encoding='utf-8')
    with open(settings.DATA, 'w', encoding='utf-8') as JSONFile:
        json.dump(data, JSONFile)


class MetaInfo:
    def __init__(self):
        self.top = 20
        self.left = width // 2
        self.record = record
        self.score = score

    def render(self):
        if self.score != score:
            self.score = score
            data['score'] = self.score
            write_json_file(data)
        if self.record < self.score:
            record = self.score
            self.record = self.score
        font = pygame.font.Font(None, 50)
        title = font.render('2048 game', True, pygame.Color('#AAAAAA'))
        title_x = self.left - title.get_width() // 2
        title_y = self.top + 100 - title.get_height() // 2
        screen.blit(title, (title_x, title_y))
        font = pygame.font.Font(None, 30)
        record = font.render(f'Текущий Рекорд: {self.record}', True, pygame.Color('#AAAAAA'))
        record_x = (self.left + (settings.CEIL_SIZE * settings.SIDE_LENGTH + 10 * settings.SIDE_LENGTH + 10) // 2 -
                    record.get_width())
        record_y = self.top + 140 - record.get_height() // 2
        screen.blit(record, (record_x, record_y))
        result = font.render(f'Очки: {self.score}', True, pygame.Color('#AAAAAA'))
        result_x = (self.left + (settings.CEIL_SIZE * settings.SIDE_LENGTH + 10 * settings.SIDE_LENGTH + 10) // 2 -
                    result.get_width())
        result_y = self.top + 160 - result.get_height() // 2
        screen.blit(result, (result_x, result_y))
        font = pygame.font.Font(None, 26)
        new_game = font.render('Нажмите ПРОБЕЛ для запуска новой игры', True, pygame.Color('#AAAAAA'))
        new_game_x = width // 2 - new_game.get_width() // 2
        new_game_y = 220 + settings.CEIL_SIZE * settings.SIDE_LENGTH + 10 * settings.SIDE_LENGTH
        screen.blit(new_game, (new_game_x, new_game_y))


class Board:
    def __init__(self):
        self.board_init()
        self.cell_size = settings.CEIL_SIZE
        self.left = width // 2 - (self.cell_size * self.side_length + 10 * self.side_length + 10) // 2
        self.top = 200
        self.transition_delay = False
        self.transition_step = 0
        self.transition_way = []
        self.game_over_delay = False
        self.flag = False

    def board_init(self):
        global data

        self.side_length = settings.SIDE_LENGTH
        self.board = data['grid']
        if not data['grid']:
            data['grid'] = [[0] * settings.SIDE_LENGTH for _ in range(settings.SIDE_LENGTH)]
            self.board = data['grid']
            first_title = choice([1, 1, 2])
            self.random_tile([first_title])
            self.random_tile([first_title])
            data['grid'] = self.board
            write_json_file(data)

    def new_game(self):
        global score

        if not self.flag:
            data['records'].reverse()
            data['records'].append({'score': score, 'date': datetime.now().strftime("%d-%m-%Y %H:%M")})
            data['records'].reverse()
        else:
            self.flag = False
        self.game_over_delay = False
        data['grid'] = []
        data['score'] = 0
        score = data['score']
        write_json_file(data)
        self.board_init()

    def game_over(self):
        self.board = []
        data['grid'] = []
        self.flag = True
        data['score'] = 0
        data['records'].reverse()
        data['records'].append({'score': score, 'date': datetime.now().strftime("%d-%m-%Y %H:%M")})
        data['records'].reverse()
        self.game_over_delay = True
        write_json_file(data)

    def render(self):
        global record, score

        if data['grid'] != self.board:
            data['grid'] = self.board
            write_json_file(data)
        if self.game_over_delay:
            pygame.draw.rect(screen, pygame.Color('#D8CEC4'),
                             (self.left, self.top, self.cell_size * self.side_length + 10 * self.side_length + 10,
                              self.cell_size * self.side_length + 10 * self.side_length + 10), 0)
            font = pygame.font.Font(None, 50)
            title = font.render('Игра окончена', True, pygame.Color('#888888'))
            title_x = width // 2 - title.get_width() // 2
            title_y = self.top + 100 - title.get_height() // 2
            screen.blit(title, (title_x, title_y))
            font = pygame.font.Font(None, 30)
            no_more_chance = font.render('Ходов не осталось', True, pygame.Color('#888888'))
            no_more_chance_x = width // 2 - no_more_chance.get_width() // 2
            no_more_chance_y = self.top + 160 - no_more_chance.get_height() // 2
            screen.blit(no_more_chance, (no_more_chance_x, no_more_chance_y))
            result = font.render(f'Результат: {score}', True, pygame.Color('#888888'))
            result_x = width // 2 - result.get_width() // 2
            result_y = self.top + 190 - result.get_height() // 2
            screen.blit(result, (result_x, result_y))
            return None
        pygame.draw.rect(screen, pygame.Color(settings.BOARD_BACKGROUND), (self.left, self.top,
                         self.cell_size * self.side_length + 10 * self.side_length + 10,
                         self.cell_size * self.side_length + 10 * self.side_length + 10), 0)
        if not self.transition_delay or self.transition_step == settings.TRANSITION:
            if self.transition_step == settings.TRANSITION:
                self.transition_delay = False
                self.transition_step = 0
                self.random_tile([1, 1, 1, 1, 1, 2])
            for i in range(self.side_length):
                for j in range(self.side_length):
                    pygame.draw.rect(screen, pygame.Color('#D8CEC4'),
                                     (self.left + self.cell_size * j + 10 * j + 10,
                                      self.top + self.cell_size * i + 10 * i + 10,
                                      self.cell_size, self.cell_size), 0, 10)
                    if self.board[i][j] == 0:
                        continue
                    font = pygame.font.Font(None, int(self.cell_size * 0.3 // 1))
                    if str(self.board[i][j]) in settings.TILES_COLORS:
                        pygame.draw.rect(screen, pygame.Color(settings.TILES_COLORS[str(self.board[i][j])]['background']),
                                         (self.left + self.cell_size * j + 10 * j + 10,
                                          self.top + self.cell_size * i + 10 * i + 10,
                                          self.cell_size, self.cell_size), 0, 10)
                        text = font.render(str(2 ** self.board[i][j]), True,
                                           pygame.Color(settings.TILES_COLORS[str(self.board[i][j])]['text']))
                    else:
                        pygame.draw.rect(screen, pygame.Color(settings.TILES_COLORS['other']['background']),
                                         (self.left + self.cell_size * j + 10 * j + 10,
                                          self.top + self.cell_size * i + 10 * i + 10,
                                          self.cell_size, self.cell_size), 0, 10)
                        text = font.render(str(2 ** self.board[i][j]), True,
                                           pygame.Color(settings.TILES_COLORS['other']['text']))
                    text_x = (self.left + self.cell_size * j + 10 * j + 10) + self.cell_size // 2 - text.get_width() // 2
                    text_y = (self.top + self.cell_size * i + 10 * i + 10) + self.cell_size // 2 - text.get_height() // 2
                    screen.blit(text, (text_x, text_y))
        else:
            for i in range(self.side_length):
                for j in range(self.side_length):
                    pygame.draw.rect(screen, pygame.Color('#D8CEC4'),
                                     (self.left + self.cell_size * j + 10 * j + 10,
                                      self.top + self.cell_size * i + 10 * i + 10,
                                      self.cell_size, self.cell_size), 0, 10)
            self.transition_step += 1
            part = self.transition_step / settings.TRANSITION
            for elem in self.transition_way:
                font = pygame.font.Font(None, int(self.cell_size * 0.3 // 1))
                if str(elem['value']) in settings.TILES_COLORS:
                    pygame.draw.rect(screen, pygame.Color(settings.TILES_COLORS[str(elem['value'])]['background']),
                                     ((self.left + self.cell_size * elem['j_1'] + 10 * elem['j_1'] + 10) +
                                      ((self.cell_size * elem['j_2'] + 10 * elem['j_2']) -
                                       (self.cell_size * elem['j_1'] + 10 * elem['j_1'])) * part,
                                      (self.top + self.cell_size * elem['i_1'] + 10 * elem['i_1'] + 10) +
                                      ((self.cell_size * elem['i_2'] + 10 * elem['i_2']) -
                                       (self.cell_size * elem['i_1'] + 10 * elem['i_1'])) * part,
                                      self.cell_size, self.cell_size), 0, 10)
                    text = font.render(str(2 ** elem['value']), True,
                                       pygame.Color(settings.TILES_COLORS[str(elem['value'])]['text']))
                else:
                    pygame.draw.rect(screen, pygame.Color(settings.TILES_COLORS['other']['background']),
                                     ((self.left + self.cell_size * elem['j_1'] + 10 * elem['j_1'] + 10) +
                                      ((self.cell_size * elem['j_2'] + 10 * elem['j_2']) -
                                       (self.cell_size * elem['j_1'] + 10 * elem['j_1'])) * part,
                                      (self.top + self.cell_size * elem['i_1'] + 10 * elem['i_1'] + 10) +
                                      ((self.cell_size * elem['i_2'] + 10 * elem['i_2']) -
                                       (self.cell_size * elem['i_1'] + 10 * elem['i_1'])) * part,
                                      self.cell_size, self.cell_size), 0, 10)
                    text = font.render(str(2 ** elem['value']), True,
                                       pygame.Color(settings.TILES_COLORS['other']['text']))
                text_x = ((self.left + self.cell_size * elem['j_1'] + 10 * elem['j_1'] + 10) +
                          ((self.cell_size * elem['j_2'] + 10 * elem['j_2']) -
                           (self.cell_size * elem['j_1'] + 10 * elem['j_1'])) * part + self.cell_size // 2 -
                          text.get_width() // 2)
                text_y = ((self.top + self.cell_size * elem['i_1'] + 10 * elem['i_1'] + 10) +
                          ((self.cell_size * elem['i_2'] + 10 * elem['i_2']) -
                           (self.cell_size * elem['i_1'] + 10 * elem['i_1'])) * part + self.cell_size // 2 -
                          text.get_height() // 2)
                screen.blit(text, (text_x, text_y))

    def do_move(self, action: str):
        global score

        if self.transition_delay or self.game_over_delay:
            return None
        if self.check_game_over():
            self.game_over()
            return None
        if action == 'up':
            old_board = []
            for elem in self.board:
                row = []
                for elem1 in elem:
                    row.append(elem1)
                old_board.append(row)
            new_board = self.board[:]
            new_board_clone = []
            for i in range(self.side_length):
                new_board_clone.append([])
                for j in range(self.side_length):
                    new_board_clone[i].append(new_board[j][i])
                new_board_clone[i] = [x for x in new_board_clone[i] if x != 0]
                new_board_clone[i] += [0 for x in range(self.side_length - len(new_board_clone[i]))]
            for i in range(self.side_length):
                j = 0
                while j < self.side_length:
                    if j + 1 == self.side_length:
                        new_board[i][j] = new_board_clone[i][j]
                        j += 1
                        break
                    if new_board_clone[i][j] == new_board_clone[i][j + 1] and new_board_clone[i][j] != 0:
                        new_board[i][j] = new_board_clone[i][j] + 1
                        new_board_clone[i][j + 1] = 0
                        score += 2 ** new_board[i][j]
                    else:
                        new_board[i][j] = new_board_clone[i][j]
                    j += 1
            new_board_clone = []
            for i in range(self.side_length):
                new_board_clone.append([])
                new_board_clone[i] = [x for x in new_board[i] if x != 0]
                new_board_clone[i] += [0 for x in range(self.side_length - len(new_board_clone[i]))]
            for i in range(self.side_length):
                for j in range(self.side_length):
                    new_board[i][j] = new_board_clone[j][i]
            self.board = new_board[:]
            if old_board != self.board:
                self.do_transition(old_board[:], self.board[:], action)
        elif action == 'down':
            old_board = []
            for elem in self.board:
                row = []
                for elem1 in elem:
                    row.append(elem1)
                old_board.append(row)
            new_board = self.board[:]
            new_board_clone = []
            for i in range(self.side_length):
                new_board_clone.append([])
                for j in range(self.side_length):
                    new_board_clone[i].append(new_board[j][i])
                new_board_clone[i] = [x for x in new_board_clone[i] if x != 0]
                new_board_clone[i] += [0 for x in range(self.side_length - len(new_board_clone[i]))]
                new_board_clone[i].reverse()
            for i in range(self.side_length):
                j = 0
                while j < self.side_length:
                    if j + 1 == self.side_length:
                        new_board[i][j] = new_board_clone[i][j]
                        j += 1
                        break
                    if new_board_clone[i][j] == new_board_clone[i][j + 1] and new_board_clone[i][j] != 0:
                        new_board[i][j] = new_board_clone[i][j] + 1
                        new_board_clone[i][j + 1] = 0
                        score += 2 ** new_board[i][j]
                    else:
                        new_board[i][j] = new_board_clone[i][j]
                    j += 1
            new_board_clone = []
            for i in range(self.side_length):
                new_board_clone.append([])
                new_board_clone[i] = [x for x in new_board[i] if x != 0]
                new_board_clone[i] += [0 for x in range(self.side_length - len(new_board_clone[i]))]
                new_board_clone[i].reverse()
            for i in range(self.side_length):
                for j in range(self.side_length):
                    new_board[i][j] = new_board_clone[j][i]
            self.board = new_board[:]
            if old_board != self.board:
                self.do_transition(old_board[:], self.board[:], action)
        elif action == 'left':
            old_board = []
            for elem in self.board:
                row = []
                for elem1 in elem:
                    row.append(elem1)
                old_board.append(row)
            new_board = self.board[:]
            new_board_clone = []
            for i in range(self.side_length):
                new_board_clone.append([])
                for j in range(self.side_length):
                    new_board_clone[i].append(new_board[i][j])
                new_board_clone[i] = [x for x in new_board_clone[i] if x != 0]
                new_board_clone[i] += [0 for x in range(self.side_length - len(new_board_clone[i]))]
            for i in range(self.side_length):
                j = 0
                while j < self.side_length:
                    if j + 1 == self.side_length:
                        new_board[i][j] = new_board_clone[i][j]
                        j += 1
                        break
                    if new_board_clone[i][j] == new_board_clone[i][j + 1] and new_board_clone[i][j] != 0:
                        new_board[i][j] = new_board_clone[i][j] + 1
                        new_board_clone[i][j + 1] = 0
                        score += 2 ** new_board[i][j]
                    else:
                        new_board[i][j] = new_board_clone[i][j]
                    j += 1
            new_board_clone = []
            for i in range(self.side_length):
                new_board_clone.append([])
                new_board_clone[i] = [x for x in new_board[i] if x != 0]
                new_board_clone[i] += [0 for x in range(self.side_length - len(new_board_clone[i]))]
            self.board = new_board_clone[:]
            if old_board != self.board:
                self.do_transition(old_board[:], self.board[:], action)
        elif action == 'right':
            old_board = []
            for elem in self.board:
                row = []
                for elem1 in elem:
                    row.append(elem1)
                old_board.append(row)
            new_board = self.board[:]
            new_board_clone = []
            for i in range(self.side_length):
                new_board_clone.append([])
                for j in range(self.side_length):
                    new_board_clone[i].append(new_board[i][j])
                new_board_clone[i] = [x for x in new_board_clone[i] if x != 0]
                new_board_clone[i] += [0 for x in range(self.side_length - len(new_board_clone[i]))]
                new_board_clone[i].reverse()
            for i in range(self.side_length):
                j = 0
                while j < self.side_length:
                    if j + 1 == self.side_length:
                        new_board[i][j] = new_board_clone[i][j]
                        j += 1
                        break
                    if new_board_clone[i][j] == new_board_clone[i][j + 1] and new_board_clone[i][j] != 0:
                        new_board[i][j] = new_board_clone[i][j] + 1
                        new_board_clone[i][j + 1] = 0
                        score += 2 ** new_board[i][j]
                    else:
                        new_board[i][j] = new_board_clone[i][j]
                    j += 1
            new_board_clone = []
            for i in range(self.side_length):
                new_board_clone.append([])
                new_board_clone[i] = [x for x in new_board[i] if x != 0]
                new_board_clone[i] += [0 for x in range(self.side_length - len(new_board_clone[i]))]
                new_board_clone[i].reverse()
            self.board = new_board_clone[:]
            if old_board != self.board:
                self.do_transition(old_board[:], self.board[:], action)

    def random_tile(self, possible_titles: list):
        if list(filter(lambda x: 0 in x, self.board)):
            while True:
                cords = [choice(list(range(self.side_length))),
                         choice(list(range(self.side_length)))]
                if self.board[cords[0]][cords[1]] == 0:
                    break
            self.board[cords[0]][cords[1]] = choice(possible_titles)
            data['grid'] = self.board
            write_json_file(data)

    def check_game_over(self):
        new_board = self.board[:]
        for i in range(len(new_board)):
            row_list = [x for x in new_board[i] if x != 0]
            if len(row_list) != len(new_board[i]):
                return False
            for j in range(len(row_list) - 1):
                if row_list[j] == row_list[j + 1]:
                    return False
        new_board_clone = []
        for i in range(self.side_length):
            new_board_clone.append([])
            for j in range(self.side_length):
                new_board_clone[i].append(new_board[j][i])
            new_board_clone[i] = [x for x in new_board_clone[i] if x != 0]
            new_board_clone[i] += [0 for x in range(self.side_length - len(new_board_clone[i]))]
        new_board = new_board_clone[:]
        for i in range(len(new_board)):
            row_list = [x for x in new_board[i] if x != 0]
            if len(row_list) != len(new_board[i]):
                return False
            for j in range(len(row_list) - 1):
                if row_list[j] == row_list[j + 1]:
                    return False
        return True

    def do_transition(self, old, new, action):
        self.transition_delay = True
        self.transition_step = 0
        self.transition_way = []
        if action == 'up':
            for i in range(self.side_length):
                minus = 0
                flag = False
                for j in range(self.side_length):
                    if old[j][i] == 0:
                        minus += 1
                        continue
                    self.transition_way.append({'value': old[j][i],
                                                'i_1': j, 'j_1': i,
                                                'i_2': j - minus, 'j_2': i})
                    if flag:
                        flag = False
                    elif old[j][i] != new[j - minus][i]:
                        minus += 1
                        flag = True
        elif action == 'down':
            for i in range(self.side_length - 1, -1, -1):
                plus = 0
                flag = False
                for j in range(self.side_length - 1, -1, -1):
                    if old[j][i] == 0:
                        plus += 1
                        continue
                    self.transition_way.append({'value': old[j][i],
                                                'i_1': j, 'j_1': i,
                                                'i_2': j + plus, 'j_2': i})
                    if flag:
                        flag = False
                    elif old[j][i] != new[j + plus][i]:
                        plus += 1
                        flag = True
        elif action == 'left':
            for i in range(self.side_length):
                minus = 0
                flag = False
                for j in range(self.side_length):
                    if old[i][j] == 0:
                        minus += 1
                        continue
                    self.transition_way.append({'value': old[i][j],
                                                'i_1': i, 'j_1': j,
                                                'i_2': i, 'j_2': j - minus})
                    if flag:
                        flag = False
                    elif old[i][j] != new[i][j - minus]:
                        minus += 1
                        flag = True
        elif action == 'right':
            for i in range(self.side_length - 1, -1, -1):
                plus = 0
                flag = False
                for j in range(self.side_length - 1, -1, -1):
                    if old[i][j] == 0:
                        plus += 1
                        continue
                    self.transition_way.append({'value': old[i][j],
                                                'i_1': i, 'j_1': j,
                                                'i_2': i, 'j_2': j + plus})
                    if flag:
                        flag = False
                    elif old[i][j] != new[i][j + plus]:
                        plus += 1
                        flag = True


try:
    data = read_json_file()
    data['score']
    data['grid']
    data['records']
except Exception:
    data = {
        'score': 0,
        'grid': [],
        'records': [],
    }
if len(data['grid']) != settings.SIDE_LENGTH:
    data = {
        'score': 0,
        'grid': [],
        'records': [],
    }
pygame.init()
pygame.display.set_caption('')
size = width, height = 600, 800
score = data['score']
if data['records']:
    record = sorted(data['records'], key=lambda x: x['score'], reverse=True)[0]['score']
else:
    record = 0
screen = pygame.display.set_mode(size)
board = Board()
meta = MetaInfo()
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_DOWN:
                board.do_move('down')
            elif event.key == pygame.K_UP:
                board.do_move('up')
            elif event.key == pygame.K_LEFT:
                board.do_move('left')
            elif event.key == pygame.K_RIGHT:
                board.do_move('right')
            elif event.key == pygame.K_SPACE:
                board.new_game()
    screen.fill('#FFFFFF')
    meta.render()
    board.render()
    pygame.display.flip()
    pygame.time.delay(1000 // settings.FPS)
