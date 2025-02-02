import sys
import pygame
import random
import os

from pygame import K_SPACE

speed = 1
score = 0
y = 0
x = 450

pipeSpeed = 3


class G:
    def __init__(self, x):
        size = 700, 700
        s = 60
        screen = pygame.display.set_mode(size)
        pygame.display.set_caption("Flappy bird")
        self.background_image = load_image("backgr.webp")
        bird_image = load_image("bird.png")
        pipe1_image = load_image("pipek.png")
        pipe2_image = load_image("pipek2.png")
        line_image = load_image("line.png")
        self.image = x
        screen = pygame.display.set_mode(size)
        pygame.display.set_caption("Flappy bird")
        clock = pygame.time.Clock()

#создаем класс труб
class Pipe(pygame.sprite.Sprite):
    def __init__(self, x_pos, y_pos, pipe, type, bird, alive, score, pipes):
        #Инициализируем спрайт
        pygame.sprite.Sprite.__init__(self)
        self.image = pipe
        self.rect = self.image.get_rect()

        #Получаем координаты трубы
        self.rect.x = x_pos
        self.rect.y = y_pos

        #Фиксируем тип трубы(нижняя или верхняя)
        self.type = type
        self.bird = bird

        #Фиксируем проход через трубы
        self.enter = False
        self.exit = False
        self.passed = False

        #Жива птица или нет
        self.alive = alive

        self.score = score
        self.pipes = pipes

        #Инициализируем скорость трубы
        self.pipeSpeed = 1

    #Оюновляем трубы и их скорость
    def update(self):
        #Проверяем, что птица жива
        if self.alive is True:
            if len(self.pipes) < 5:
                #ускоряем скорость трубы
                self.pipeSpeed = 1 + self.score // 3
            self.rect.x -= self.pipeSpeed

            #Если труба выходит за пределы экрана, то удаляем ее
            if self.rect.x <= - 800:
                self.kill()
            #делаем глобальной переменную подсчета очков
            global score
            #Узнаем какой тип трубы
            if self.type == 'bottom':

                #Проверяем, что птица перешла через трубу
                if self.rect.topleft[0] < self.bird.x and not self.passed:
                    self.enter = True
                    if self.rect.topright[0] < self.bird.x and not self.passed:
                        self.exit = True

                #Если она прошла окончательно, то прибаляем очко
                if self.enter and self.exit and not self.passed:
                    #Добавляем очко
                    score += 1
                    self.passed = True

#Загружаем изображения,
#убираем фон, если необходимо
def load_image(name, color_key=None):
    #Соединяем изображение с путем
    fullname = os.path.join(r'C:\Users\79774\PycharmProjects\data', name)
    try:
        #Пробуем его загрузить
        image = pygame.image.load(fullname).convert_alpha()

    #Если изображения нет, то выдает ошибку
    except pygame.error as message:
        print(f'Картинка {name} не найдена')
        raise SystemExit(message)

    #Если изображение с фоном
    if color_key is not None:
        if color_key == -1:
            #Получаем rgb цветов изображения
            r, g, b, old_alpha = image.get_at((0, 0))
            if old_alpha > 0:
                image.set_at((20, 20), (r, g, b, 255))
                image.set_colorkey(color_key)

                #Конвертируем изображение
                image = image.convert_alpha()

    else:
        image = image.convert_alpha()
    #Возвращаем изображение
    return image

#Создаем землю
class Background(pygame.sprite.Sprite):
    def __init__(self, x, y, z, alive):
        #Инициализируем группу спрайтов
        pygame.sprite.Sprite.__init__(self)
        self.image = z

        #Создаем прямоугольник по заднему фону
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = x, y
        self.alive = alive

    #Обновляем фон каждый раз
    def update(self):
        if self.alive is True:
            #Двигаем полосу влево, по координает х
            self.rect.x = self.rect.x - speed

            #Если полоса выходит за рамки экрана, удаляем ее
            if self.rect.x <= -700:
                self.kill()


#Главная функция
def main(screen):
    pygame.init()
    pygame.font.init()

    #Устанавливаем размеры
    size = 769, 1000
    s = 60
    alive = True
    moving = False

    #Устанавливаем шрифт для инструкции
    font = pygame.font.Font(None, 30)

    #Устанавливаем заголовок
    pygame.display.set_caption("Flappy bird")

    #Загружаем все изображения
    background_image = load_image("background.jpg")
    bird_image1 = load_image("bird_down.png")
    bird_image2 = load_image("bird_up.png")
    pipe1_image = load_image("pipos2.png")
    pipe2_image = load_image("pipos.png")
    line_image = load_image("line.png")
    game_over = load_image("game_over.png")


    #screen.fill((0, 0, 0))
    #screen.blit(background_image, (0, 0))

    #Создаем группу спрайтов
    line = pygame.sprite.Group()

    #добавляем в нее наше изображение
    line.add(Background(0, 920, line_image, alive))


    bird_animation = []
    #Добавляем в список изображния птицы с махающими крыльями
    bird_animation.append(bird_image1)
    bird_animation.append(bird_image1)
    bird_animation.append(bird_image1)

    bird_animation.append(bird_image2)
    bird_animation.append(bird_image2)
    bird_animation.append(bird_image2)

    #Создаем группу спрайтов для труб
    pipes = pygame.sprite.Group()
    clock2 = 0

    #Устанавливаем время
    clock = pygame.time.Clock()

    bird = pygame.Rect(350, 500, 50, 50)
    bird_y = 500
    bird_speed = 0
    bird_speedup = 0

    running = True
    position = 0
    clock1 = 0

    over = False
    f = 0

    #Делаем переменную очки глобальной
    global score
    score = 0
    clock3 = 0
    k = 0
    playing = False
    j = True

    #Начинаем основной игровой цикл
    while running:
        playing = True

        #Заливаем цветом экран
        screen.fill((0, 0, 0))

        #Устанавливаем задний фон
        screen.blit(background_image, (-8, 0))

        #Проверяем все события
        for event in pygame.event.get():
            #Проверяем, если нажат крестик
            if event.type == pygame.QUIT:
                running = False
            #Проверяем, если нажат пробел
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    playing = False
                    #Обнуляем очки
                    score = 0
                    #Обращаемся к функции для начала игры
                    restart(playing, screen, background_image, running)
                    j = False
                    #Останавливаем цикл
                    break

        #Получаем список всех нажатий, которые были задействованы
        keys = pygame.key.get_pressed()
        pressed = pygame.mouse.get_pressed()

        f += 1

        #screen.fill((0, 0, 0))

        #screen.blit(background_image, (0, 0))

        #Проверяем. что птица жива
        if alive is True:
            if position == 1:

                #Если нажат пробел:
                if pressed[0] or keys[pygame.K_SPACE]:
                    #Птица падает
                    bird_speedup = -2
                else:
                    #Если же ничего не нажато, то птица не двигается
                    bird_speedup = 0

                bird_y += bird_speed
                #меняем скорость птицы
                bird_speed = (bird_speed + bird_speedup + 0.5) * 0.98
                bird.y = bird_y

                #роверяем, если птица упала на землю
                if bird.bottom > 1000 or bird.top < 0:
                    position = -1
                #Перебираем трубы
                for i in pipes:
                    enter = False
                    exit = False

                    #Проверяем на столкновение с трубой
                    if bird.colliderect(i) or bird.bottom > 1000 or bird.top < 0:
                        k = -1
                        #Меняем флаг на отрицательный
                        alive = False

                        #Меняем позицию на отрицательную
                        position = -1
                        w = 1
                        #Вызываем функцию для записи в файл
                        writing(w)
                        seeing(score)
                        #dead(screen, game_over)

            #Если птица еще не начала двигаться
            if position == 0:
                #Проверяем зажата ли правая кнопка мыши
                if pressed[0]:
                    #меняем позицию и разрешаем двигаться
                    position = 1
                    moving = True
                #меняем координаты птица по у
                bird_y += (400 - bird_y) * 0.1
                bird.y = bird_y

            if position == -1:
                print('g')
                if j is False:
                    #Если птица упала, то вызываем функцию начала игры
                    restart(playing, screen, background_image)

                if keys[pygame.K_SPACE]:
                    score = 0
                    print('h')
                bird_speed = 0
                bird_speedup = 0
                alive = False

            #Если заканчивается спрайты с изображениями линий, то добавляем новые
            if len(line) <= 2 and moving is True:
                line.add(Background(0, 920, line_image, alive))
        #Рисуем эти линии
        line.draw(screen)
        #Проверяем если птица жива и двигается, то обновляем задний фон
        if alive and moving is True:
            line.update()

        #Птица ударилась о землю, то показываем изображение о завершении игры
        if k == -1:
            screen.blit(game_over, (290, 380))

        #Обновляем трубы
        if clock1 <= 0 and alive is True and moving is True:
            x1, x2, y1, y2 = update_pipe(pipe1_image, score)
            #Добавление верхней трубы
            pipes.add(Pipe(x1, y1, pipe2_image, 'top', bird, alive, score, pipes))
            #обавление нижней трубы
            pipes.add(Pipe(x2, y2, pipe1_image, 'bottom', bird, alive, score, pipes))
            clock1 = random.randint(190, 280)
        clock1 -= 1

        #вырисовываем трубы
        pipes.draw(screen)

        #если птица жива и двигается, то обновляем трубы
        if alive and moving is True:
            pipes.update()

        #Создаем анимацию махания крыльев
        if alive is True and moving is True:
            screen.blit(bird_animation[f % 6], bird)
        else:
            #Если же птица врезалась в трубу, останавливаем анимацию
            x, y = bird.x, bird.y
            screen.blit(bird_animation[0], (x, y))

        #Создаем подсчет очков и выставляем на экран
        message = font.render("Score: " + str(score), 1, pygame.Color('black'))
        screen.blit(message, (10, 10))

        #Обновляем экран
        pygame.display.update()
        clock.tick(60)


#Функция для создания труб
def update_pipe(pipe1_image, score):
    global x
    #Устанавливаем координаты труб
    top_pipe_x = 750
    bottom_pipe_x = 750
    #Создаем трубы различной длины
    top_pipe_y = random.randint(-600, -500)

    #Создаем значение для пространства, которое будет уменьшаться с каждыми 4 очками
    x -= (30 * score // 4)
    if x > 370:
        #Создаем переменную для пространства между трубами
        space = random.randint(370, x)
    else:
        space = random.randint(300, 330)
    print(space)

    #Записываем высоту трубы
    height = pipe1_image.get_height()

    #Вычисляем нижнюю точку у нижней трубы
    bottom_pipe_y = top_pipe_y + height + space

    #Возвращаем координаты труб
    return (top_pipe_x, bottom_pipe_x, top_pipe_y, bottom_pipe_y)


#Функция для вызова изображение об окончании игры
def dead(screen, game_over):
    screen.blit(game_over, (500, 500))
    pygame.display.flip()


#Функция для обновления экрана по окончанию игры
def restart(playing, screen, background_image, running):
    while playing is False:
        #Проверяем все нажатия пользователем
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        playing = True
        running = True

        #Вызываем основную функцию
        main(screen)


#Функция для записи очков в файл
def writing(w):

    #Вычисляем количество попыток
    global y
    y += 1
    if w == 1:
        #Записываем в файл
        with open('score_counter.txt', 'a', encoding='utf8') as o:
            o.write(f'{str(y)} попытка; счет - {str(score)}')
            o.write("\n")
            #Закрываем файл
            o.close()
            w = 0


def seeing(score):
    a = score + 1


#Создаем частоту обновления
FPS = 50


#Функция для завершения программы
def terminate():
    pygame.quit()
    sys.exit()


#Функция для создания заставки игры
def start_screen():
    pygame.font.init()
    #Установка эрана для заставки
    screen = pygame.display.set_mode((759, 1000))


    #Инструкция для игры
    intro_text = ["Правила игры",
                  "Для того, чтобы удержать птицу в полете, ",
                  "периодически нажимайте левой кнопкой мыши на экран.",
                  "Избегайте препятствий, такие как трубы."]

    #Загрузка изображения
    fon1 = load_image("fon.jpg")
    #Удаление фона
    fon1.convert_alpha()
    fon = pygame.transform.scale(fon1, (759, 1000))

    #отображение заставки
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 30)
    text_coord = 50

    #вывод инструкции на экран
    for line in intro_text:
        #Установка цвета
        string_rendered = font.render(line, 1, pygame.Color('black'))
        intro_rect = string_rendered.get_rect()

        #установка координат
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 10
        text_coord += intro_rect.height

        #Вывод текста
        screen.blit(string_rendered, intro_rect)

    #Проверка на закрытие экрана
    while True:
        #Перебор всех событий
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                #Вызов функции о завершении игры
                terminate()

            #Проверка на нажатие клавиши Escape
            elif event.type == pygame.KEYDOWN or \
                    event.type == pygame.K_ESCAPE:
                return main(screen)
        #Отрисовка изображений
        pygame.display.flip()


if __name__ == '__main__':
    #инициализирование пигейма
    pygame.init()
    #Вызов функции для отображения заставки
    start_screen()