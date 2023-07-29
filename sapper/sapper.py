from random import randint
import pygame_gui
import pygame
import os, sys

SIZE_SP = 50

def load_image(name, colorkey=None) -> pygame.Surface:
    pygame.init()
    fullname = os.path.join('data', name)
    # если файл не существует, то выходим
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    if colorkey is not None:
        # image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
            image.set_colorkey(colorkey)
        else:
            image = image.convert_alpha()
    return image

def start_screen():
    global level, level_map, min, max_x, max_y, screen
    razmer = 250,200
    manager = pygame_gui.UIManager(razmer)
    easy_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((10 , 10, 115, 30)),text='Лёгкий')
    standart_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((130 , 10, 115, 30)),text='Средний')
    hard_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((70 , 50, 115, 30)),text='Сложный')
    rezult_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((10 , 90, 115, 30)),text='Результаты')
    nastr_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((130 , 90, 115, 30)),text='Параметры')
    button = True
    clock = pygame.time.Clock()
    while button:
        time_delta = clock.tick(60) /1000.0
        screen.fill(pygame.Color('white'))
        for event in pygame.event.get():
            manager.process_events(event)
            if event.type == pygame.QUIT:
                terminate()
                button = False
            if event.type == pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_element == easy_button:
                    level = 1
                    button = False
                    max_x = 15
                    max_y = 15
                    min = 45
                    create_level(max_x, max_y)
                    screen = pygame.display.set_mode(((max_x + 1) * SIZE_SP, (max_y + 1) * SIZE_SP))
                    print (level_map)
                if event.ui_element == standart_button:
                    level = 2
                    button = False
                    min = 100
                    create_level(max_x, max_y)
                    screen = pygame.display.set_mode(((max_x + 1) * SIZE_SP, (max_y + 1) * SIZE_SP))
                if event.ui_element == hard_button:
                    level = 3
                    button = False
                    min = 145
                    create_level(max_x, max_y)
                    screen = pygame.display.set_mode(((max_x + 1) * SIZE_SP, (max_y + 1) * SIZE_SP))
                if event.ui_element == rezult_button:
                    level = 4
                if event.ui_element == nastr_button:
                    level = 5
        manager.draw_ui(screen)    
        pygame.display.update()
        manager.update(time_delta)

def terminate():
    print(123)
    sys.exit

def create_level(w, h):
    global level_map, min
    cor = [[-1,1], [0,1] ,[1,1] , [1,0] ,[1,-1], [0,-1], [-1,-1], [-1,0] ]   
    level_map = ['0'] * w 
    for i in range(h): 
        level_map[i] = [0] * w

    for _ in range(min):
        y = randint(0, h-1)
        x = randint(0, w-1)
        while level_map[x][y] == '*':
            y = randint(0, h-1)
            x = randint(0, w-1)
        level_map[x][y] = '*'

        for  cord in cor:
            x1 = x + cord[0]
            y1 = y + cord[1]
            if x1 < 0 or y1 < 0 or x1 + 1 > len(level_map) or y1 + 1 > len(level_map) or level_map[x1][y1] == '*':
                continue
            
            else:
                level_map[x1][y1] += 1

if __name__ == '__main__':
    pygame.init()
    SCORE = 0
    #my_font = pygame.font.SysFont(None, 30)
    screen = pygame.display.set_mode((250, 200))
    start_screen()