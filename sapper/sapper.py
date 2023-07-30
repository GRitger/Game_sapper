from random import randint
import pygame_gui
import pygame
import os, sys
import time

SIZE_SP = 30

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

def drow_map():
    global level, level_map, min, max_x, max_y, screen
    screen.fill(pygame.Color('white'))
    pygame.draw.rect(screen, (0, 0, 0), (15, 3 * SIZE_SP, max_x  * SIZE_SP, max_y * SIZE_SP), 2)
    for i in range(max_x):
        for j in range(max_y):
            pygame.draw.rect(screen, (0, 0, 0), (15 + i * SIZE_SP, 3 * SIZE_SP + j * SIZE_SP, SIZE_SP, SIZE_SP), 2)
            pygame.draw.rect(screen, (190, 190, 190), (15 + i * SIZE_SP, 3 * SIZE_SP + j * SIZE_SP, SIZE_SP-2, SIZE_SP-2))

    pygame.display.flip()
    game()

def game():
    start = time.time()
    global col_flag, sec
    run = True
    sec = 0                    
    flag = pygame.transform.scale(load_image('flag.png', -1), (SIZE_SP - 2, SIZE_SP - 2))
    mina = pygame.transform.scale(load_image('mine.jpg', -1), (SIZE_SP - 10, SIZE_SP - 10))
    vopros = pygame.transform.scale(load_image('vopros.jpg', -1), (SIZE_SP - 2, SIZE_SP - 2))
    smail = pygame.transform.scale(load_image('smail.jpg', -1), (50, 50))
    screen.blit(smail, (200, 20))
    Pause = False
    while run: 
        tim = flag_font.render(str(sec), False, (0, 0, 0))
        pygame.draw.rect(screen, (255, 255, 255), (300, 20, 50, 40))
        screen.blit(tim, (300, 20))
        pygame.display.update()
        for event in pygame.event.get():
            tim = flag_font.render(str(sec), False, (0, 0, 0))
            pygame.draw.rect(screen, (255, 255, 255), (330, 20, 50, 40))
            screen.blit(tim, (300, 20))
            pygame.draw.rect(screen, (255, 255, 255), (20, 20, 50, 50))
            text = flag_font.render(str(col_flag), False, (0, 0, 0))
            screen.blit(text, (20, 20))
            pygame.display.update()
            if event.type == pygame.QUIT:
                terminate()
                run = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_p:
                if Pause == False:
                    Pause = True
                    
                else:
                    Pause = False
                    start = time.time() - sec

            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                if 200 < x  < 250 and 20 < y < 70:
                    game_over(x, y, mina)
                    run = False
                    break 
                if event.button == 1:
                    y = (y - 3 * SIZE_SP) // SIZE_SP 
                    x = (x -15) // SIZE_SP
                    if y < 0 or x < 0 or y > 14 or x > 14:
                        continue 
                    pygame.draw.rect(screen, (255, 255, 255), (15 + x * SIZE_SP, 3 * SIZE_SP + y * SIZE_SP, SIZE_SP-2, SIZE_SP-2))
                    if level_map[y][x] == '*':
                        pygame.draw.rect(screen, (255, 0, 0), (15 + x * SIZE_SP, 3 * SIZE_SP + y * SIZE_SP, SIZE_SP-2, SIZE_SP-2))
                        screen.blit(mina, (19 +  SIZE_SP * x, SIZE_SP * (y + 3) + 4))
                        pygame.display.update()
                        game_over(x, y, mina)
                        run = False
                        break   
                    else:
                        text = my_font.render(level_map[y][x], False, (0, 0, 0)) 
                        screen.blit(text, (23 +  SIZE_SP * x, SIZE_SP * (y + 3) - 4))
                    pygame.display.update()
                if event.button == 3:
                    y = (y - 3 * SIZE_SP) // SIZE_SP 
                    x = (x -15) // SIZE_SP
                    if y < 0 or x < 0 or y > 14 or x > 14:
                        continue 
                    if map [y][x] == 0:
                        screen.blit(flag, (15 +  SIZE_SP * x, SIZE_SP * (y + 3)))
                        col_flag -=1
                        pygame.display.update()
                        map [y][x] = (map [y][x] + 1) % 3
                    elif map [y][x] == 1:
                        screen.blit(vopros, (15 +  SIZE_SP * x, SIZE_SP * (y + 3)))
                        col_flag +=1
                        pygame.display.update()
                        map [y][x] = (map [y][x] + 1) % 3
                    elif map [y][x] == 2:
                        pygame.draw.rect(screen, (190, 190, 190), (15 + x * SIZE_SP, 3 * SIZE_SP + y * SIZE_SP, SIZE_SP-2, SIZE_SP-2))
                        pygame.display.update()
                        map [y][x] = (map [y][x] + 1) % 3
            if Pause == False: 
                end = time.time() - start
                sec = round(end)
        if Pause == False:
            end = time.time() - start
            sec = round(end)

def game_over(x, y, mina):
    global screen
    q = True
    while q:
        for i in range(max_x):
            for j in range(max_y):
                if level_map[j][i] == '*' and i != y and j != x:
                    pygame.draw.rect(screen, (255, 255, 255), (15 + i * SIZE_SP, 3 * SIZE_SP + j * SIZE_SP, SIZE_SP-2, SIZE_SP-2))
                    screen.blit(mina, (19 +  SIZE_SP * i, SIZE_SP * (j + 3) + 4))
                    pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.KEYDOWN:
                screen = pygame.display.set_mode((250, 200))
                q = False
                break
    #while True:
        #pass
                


def start_screen():
    global level, level_map, min, max_x, max_y, screen, col_flag
    
    
    razmer = 250,200
    manager = pygame_gui.UIManager(razmer)
    while True:
        easy_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((10 , 10, 115, 30)),text='Лёгкий')
        standart_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((130 , 10, 115, 30)),text='Средний')
        hard_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((70 , 50, 115, 30)),text='Сложный')
        rezult_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((10 , 90, 115, 30)),text='Результаты')
        nastr_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((130 , 90, 115, 30)),text='Параметры')
        clock = pygame.time.Clock()
        time_delta = clock.tick(60) /1000.0
        manager.update(time_delta)
        manager.draw_ui(screen)        
        pygame.display.update()
        button = True
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
                        min = col_flag = 45
                        create_level(max_x, max_y)
                    if event.ui_element == standart_button:
                        level = 2
                        button = False
                        min = col_flag = 100
                        create_level(max_x, max_y)
                    if event.ui_element == hard_button:
                        level = 3
                        button = False
                        min = col_flag = 145
                        create_level(max_x, max_y)
                    if event.ui_element == rezult_button:
                        level = 4
                    if event.ui_element == nastr_button:
                        level = 5
            manager.draw_ui(screen)    
            pygame.display.update()
            manager.update(time_delta)
        for i in range(max_x):
            for j in range(max_y):
                level_map[i][j] = str(level_map[i][j])
    
        drow_map()
        manager.clear_and_reset()

def terminate():
    pygame.quit()
    sys.exit

def create_level(w, h):
    global level_map, min, map
    cor = [[-1,1], [0,1] ,[1,1] , [1,0] ,[1,-1], [0,-1], [-1,-1], [-1,0] ]

    map = [0] * w
    for i in range(h): 
        map[i] = [0] * w

    level_map = [0] * w 
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
    screen = pygame.display.set_mode(((max_x + 1) * SIZE_SP, (max_y + 4) * SIZE_SP))

if __name__ == '__main__':
    pygame.init()
    my_font = pygame.font.SysFont("arial", 30)
    flag_font = pygame.font.SysFont("arial", 40)
    screen = pygame.display.set_mode((250, 200))
    max_x = 15
    max_y = 15
    start_screen()
    