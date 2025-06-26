import pygame
import random

pygame.init()

white = (255, 255, 255) #Цвета по RGB
black = (0, 0, 0)
red = (255, 0, 0)
grey = (100,100,100)
green = (0,100,0)
purple = (155,0,155)
dark_grey = (20,20,20)

dis_x = 1280 #Размер игрового поля по оси x
dis_y = 720 #Размер игрового поля по оси y
dis=pygame.display.set_mode((dis_x, dis_y))  #Создаём экран размером (dis_x, dis_y)
pygame.display.set_caption('Snake') #Название окна игры
snake_block=10 #Размер блока змея окоянного
snake_speed=15 #Кол-во обновлений игры в секунду (тиков в секунду) (FPS)
font_style = pygame.font.SysFont("bahnschrift", 50, False, True) #Задаём стиль текста(Шрифт, размер, Жирный?, Курсив?)
clock = pygame.time.Clock() #Переменная отвечающая за подсчёт времени

ap_texture = pygame.image.load("./textures/apple.png").convert() #Загружаем и конвертируем(в удобный формат) изображения(текстуры).
tutorial_texture = pygame.image.load("./textures/tutorial.png").convert()
info_texture = pygame.image.load("./textures/info.png").convert()

def net(): #Функция для рисования сетки
    for x in range(0, dis_x, snake_block):
        pygame.draw.line(dis, dark_grey, (x, 50), (x, dis_y))
    for y in range(50, dis_y, snake_block):
        pygame.draw.line(dis, dark_grey, (0, y), (dis_x, y))

def score(score): #Функция подсчёта и вывода счёта(длина змея - начальная длина змея)
   value = font_style.render("Ваш счёт: " + str(int((score-2)//3)), True, black, grey)
   dis.blit(value, [dis_x/2, 0])

def message(msg,x,y): #Функция для вывода сообщений на игровой экран
   mesg = font_style.render(msg, True, black, grey)
   dis.blit(mesg, [x, y])

def our_snake(snake_block, snake_list): #Функция для рисования змея окоянного
   for x in snake_list:
        if x==snake_list[len(snake_list)-1]:
            pygame.draw.rect(dis, white, [x[0]-1, x[1]-1, snake_block+3, snake_block+3])  #Рисую голову змея белым
        else:
            pygame.draw.rect(dis, grey, [x[0], x[1], snake_block, snake_block])  #Рисую хвост змея серым

def tutorial(): #Функия для вывода обучения, и последующего запуска игры
    learning_end = False #флаг того, что обучение не нужно закрывать
    while not learning_end:
        dis.blit(tutorial_texture, (0, 0))  #Выводим обучение (картинку)
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  #Выход через закрытие окна
                learning_end = True
                event.type = pygame.QUIT
            if event.type == pygame.KEYDOWN:  #Выбираем из взаимодействий игрока только нажатия клавиш.
                if event.key == pygame.K_ESCAPE:  #Завершение игры через Escape.
                    learning_end = True
                    event.type = pygame.K_ESCAPE
                if event.key == pygame.K_SPACE or event.key == pygame.K_i:  #Закрываем окно обучения при нажатии space или i
                    learning_end = True

def game(): #Игровая логика
    game_end=False #Флаг для закрытия игры
    defeat=False #Флаг означающий поражение игрока
    x1 = dis_x/2 #Указываем начальную координату положения змея по оси х
    y1 = dis_y/2 #Указываем начальную координату положения змея по оси y
    x1_change = 0 #Переменная, которой в цикле while будут присваиваться значения изменения положения змея по оси х
    y1_change = 0 #Переменная, которой в цикле while будут присваиваться значения изменения положения змея по оси y
    foodx = round(random.randrange(0 + snake_block*2, dis_x - snake_block*2) / 10.0) * 10.0 #Переменная, которая будет указывать расположение еды по оси х
    foody = round(random.randrange(0 + snake_block*8, dis_y - snake_block*2) / 10.0) * 10.0 #Переменная, которая будет указывать расположение еды по оси y
    snake_list = [] #Хвост змея окоянного
    snake_len = 2 #Длина змея окоянного
    stop=True #Флаг, означающий что змей стоит
    previous_key = '' #Переменная содержащая последнюю нажатую клавишу действия
    move_accept = False #Переменная для ограничения кол-во действий в тик
    portal_xy = [dis_x/2,dis_y/2] #Координаты портала
    dot_portal = False #Переменная означающая что портал используется в данный момент
    xt = dis_x/2 #Переменная входной точки портала
    yt = dis_y/2 #Переменная входной точки портала
    xtemp = 0 #Переменная хранящая координаты курсора
    ytemp = 0 #Переменная хранящая координаты курсора

    while not game_end: #Основной цикл
        for event in pygame.event.get(): #Цикл для считывания действий игрока
            #print(event) #Вывод действия игрока на консоль
            if (event.type==pygame.QUIT): #Выход через закрытие окна
                game_end=True

            if (event.type == pygame.MOUSEMOTION): #Считываем координаты курсора
                xtemp, ytemp = event.pos
            if (dot_portal == False):  #Записываем координаты курсора в переменные
                    xt=(xtemp//10)*10
                    yt=(ytemp//10)*10

            if (event.type == pygame.KEYDOWN): #Выбираем из взаимодействий игрока только нажатия клавиш.
                if event.key==pygame.K_ESCAPE: #Завершение игры через Escape.
                    game_end=True
                if event.key==pygame.K_SPACE: #Перезапуск игры через Space
                    #print("restart") #Вывод в консоль сообщения о рестарте
                    defeat=False #Сброс ключевых переменных
                    x1 = dis_x/2 
                    y1 = dis_y/2
                    x1_change = 0
                    y1_change = 0
                    snake_len = 2
                    snake_list = []
                    stop=True
                    previous_key = ''
                    move_accept = False
                    dot_portal=False
                    portal_xy = [dis_x/2,dis_y/2]
                if (defeat==False): #Проверка на то, что игра не проиграна (пользователь не может двигать змея, когда игра проиграна)
                    if event.key == pygame.K_a and previous_key != 'd' and move_accept == False: #влево a
                        move_accept = True
                        previous_key = 'a'
                        stop=False
                        x1_change = -snake_block
                        y1_change = 0
                    elif event.key == pygame.K_d and previous_key != 'a' and move_accept == False: #вправо d
                        move_accept = True
                        previous_key = 'd'
                        stop=False
                        x1_change = snake_block
                        y1_change = 0
                    elif event.key == pygame.K_w and previous_key != 's' and move_accept == False: #вверх w
                        move_accept = True
                        previous_key = 'w'
                        stop=False
                        y1_change = -snake_block
                        x1_change = 0
                    elif event.key == pygame.K_s and previous_key != 'w' and move_accept == False: #вниз s
                        move_accept = True
                        previous_key = 's'
                        stop=False
                        y1_change = snake_block
                        x1_change = 0
                    elif event.key == pygame.K_x: #стоп x
                        previous_key = ''
                        stop=True
                        y1_change = 0
                        x1_change = 0
                    elif event.key == pygame.K_f and dot_portal == False: #Телепорт в начало space
                        portal_time = 0
                        portal_xy = [x1,y1]
                        dot_portal = True
                        stop=False
                        x1=xt
                        y1=yt
                if event.key == pygame.K_i: #Вывод обучения i
                    tutorial()


        if (defeat==False): 
            x1 += x1_change #Записываем новое значение положения змейки по оси х.
            y1 += y1_change #Записываем новое значение положения змейки по оси y.

        if (x1 >= dis_x-snake_block) or (x1 < 0+snake_block) or (y1 >= dis_y-snake_block) or (y1 < 0+snake_block + 50):
            defeat=True  #Поражение, если координаты головы змея окоянного выходят за границы поля

        snake_head = [x1,y1] #голова змея окоянного
        snake_list.append(snake_head) #Добавляем координату головы змея в список координат тела(для продвижения змея вперёд) #здесь можно добавить if, чтоб змей не уходил в себя при поражении

        if len(snake_list) > snake_len: #Убираем старые координаты из координат тела змея
            del snake_list[0]

        if stop == False: #поражение при столкновении головы змея с телом
            for x in snake_list[:-1]:
                if x == snake_head:
                    defeat = True 
        
        if x1 == foodx and y1 == foody: #Собираем еду, если голова змея на клетке еды
            foodx = round(random.randrange(0 + snake_block*2, dis_x - snake_block*2) / 10.0) * 10.0 #Создаём переменную, которая будет указывать расположение еды по оси х
            foody = round(random.randrange(0 + snake_block*2 + 50, dis_y - snake_block*2) / 10.0) * 10.0 #Создаём переменную, которая будет указывать расположение еды по оси y
            snake_len += 3 #Добавляем длину змею
        
        move_accept = False #Возвращаем возможность двигаться в конце каждого тика


        dis.fill(black) #Красим игровое поле в black
        net() #Рисуем сетку
        
        dis.blit(ap_texture, (foodx-4, foody-4)) #Рисуем текстуру еды
        if dot_portal == True: #Рисуем портал
            pygame.draw.rect(dis, purple, [portal_xy[0]-3, portal_xy[1]-3, snake_block+6, snake_block+6])
            pygame.draw.rect(dis, purple, [xt-3, yt-3, snake_block+6, snake_block+6])
            portal_time +=1
            if  portal_time == snake_len:
                dot_portal = False
        our_snake(snake_block, snake_list) #Рисуем змея окоянного

        pygame.draw.rect(dis, grey, [0, 0, dis_x, 50]) #Рисуем серый прямоугольник сверху
        dis.blit(info_texture, (1210, 0)) #Рисуем текстуру подсказки кнопки обучения
        score(snake_len) #Выводим счёт
        if (defeat==True): #Выводим сообщение о проигрыше
            message("Вы проиграли.",0,0)

        pygame.display.update() #Обновляем экран
        clock.tick(snake_speed) #Ограничиваем скорость обновлений


    pygame.quit() #Закрываем PyGame


game() #Запускаем основную функцию
pygame.quit #На всякий случай ещё раз закрываем PyGame
