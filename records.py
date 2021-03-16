import pygame
import json

import settings


def read_json_file():
    with open(settings.DATA, 'r', encoding='utf-8') as JSONFile:
        return json.load(JSONFile)


class Records:
    def __init__(self):
        self.top = 20
        self.left = width // 2
        if len(data['records']) > 10:
            self.records = list(sorted(data['records'], key=lambda x: x['score'], reverse=True))[:10]
        else:
            self.records = (list(sorted(data['records'], key=lambda x: x['score'], reverse=True)) +
                            [{'score': '-', 'date': '-'} for i in range(10 - len(data['records']))])

    def render(self):
        font = pygame.font.Font(None, 50)
        title = font.render('Топ 10 ваших лучших рекордов', True, pygame.Color('#444444'))
        title_x = self.left - title.get_width() // 2
        title_y = self.top + 40
        screen.blit(title, (title_x, title_y))

        font = pygame.font.Font(None, 36)
        table_title_place = font.render('Место', True, pygame.Color('#444444'))
        table_title_place_x = self.left - 250
        table_title_place_y = self.top + 90
        screen.blit(table_title_place, (table_title_place_x, table_title_place_y))

        table_title_1 = font.render('Очки', True, pygame.Color('#444444'))
        table_title_1_x = self.left - 100
        table_title_1_y = self.top + 90
        screen.blit(table_title_1, (table_title_1_x, table_title_1_y))

        table_title_2 = font.render('Дата и время', True, pygame.Color('#444444'))
        table_title_2_x = self.left + 100
        table_title_2_y = self.top + 90
        screen.blit(table_title_2, (table_title_2_x, table_title_2_y))

        font = pygame.font.Font(None, 30)
        for i in range(len(self.records)):
            pygame.draw.rect(screen, pygame.Color('#000000'), (self.left - 300, self.top + 130 + 40 * i - 12, 600, 2), 0)
            if str(i + 1) in settings.RECORDS_COLOR:
                place = str(i + 1)
            else:
                place = 'other'
            record_place = font.render(str(i + 1) + '.', True, pygame.Color(settings.RECORDS_COLOR[place]))
            record_place_x = self.left - 250
            record_place_y = self.top + 130 + 40 * i
            screen.blit(record_place, (record_place_x, record_place_y))

            record_score = font.render(str(self.records[i]['score']), True, pygame.Color(settings.RECORDS_COLOR[place]))
            record_score_x = self.left - 100
            record_score_y = self.top + 130 + 40 * i
            screen.blit(record_score, (record_score_x, record_score_y))

            record_date = font.render(str(self.records[i]['date']), True, pygame.Color(settings.RECORDS_COLOR[place]))
            record_date_x = self.left + 100
            record_date_y = self.top + 130 + 40 * i
            screen.blit(record_date, (record_date_x, record_date_y))




try:
    data = read_json_file()
    data['records']
except Exception:
    data = {
        'records': [{'score': '-', 'date': '-'}]
    }
pygame.init()
pygame.display.set_caption('')
size = width, height = 800, 600
screen = pygame.display.set_mode(size)
records = Records()
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    screen.fill('#FFFFFF')
    records.render()
    pygame.display.flip()
    pygame.time.delay(1000 // settings.FPS)
