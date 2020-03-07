import pygame
import random
from Settings import *
import time


def possible(list_of_num, n, x, y): # is possible for num in cell
    for i in range(0, 9):
        if list_of_num[y][i] == n:
            return False
    for i in range(0, 9):
        if list_of_num[i][x] == n:
            return False
    x0 = (x // 3) * 3
    y0 = (y // 3) * 3
    for i in range(0, 3):
        for j in range(0, 3):
            if list_of_num[y0 + i][x0 + j]:
                return False
    return True


class Sudoky():
    def __init__(self, cell_size=20):
        self.cell_size = cell_size
        self.win_width = self.cell_size * 9
        self.win_height = self.cell_size * 9

        self.screen = pygame.display.set_mode((self.win_width + 2, self.win_height + 2))

    def rand_num(self, list_of_num):
        num = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        e = 0
        while e < 9:
            i = random.randint(0, 8)
            j = random.randint(0, 8)
            if list_of_num[i][j] == '':
                list_of_num[i][j] = num.pop()
                e += 1

    # def create_fill(self):
    #     for i in range(9):
    #         list_of_num.append([])
    #         for j in range(9):
    #             if i == j:
    #                 list_of_num[i].append(random.randint(1, 9))
    #             else: list_of_num[i].append('')

    def draw_grid(self):
        for x in range(0, self.win_width + self.cell_size, self.cell_size):
            if x % 3 == 0:
                line_width = 4
            else:
                line_width = 1
            pygame.draw.line(self.screen, BLACK, (x, 0), (x, self.win_width), line_width)
        for y in range(0, self.win_height + self.cell_size, self.cell_size):
            if y % 3 == 0:
                line_width = 4
            else:
                line_width = 1
            pygame.draw.line(self.screen, BLACK, (0, y), (self.win_width, y), line_width)

    def next_num(self):
        pass

    def draw_field(self, list_of_num): # рисуем поле
        for i in range(9):
            for j in range(9):
                self.draw_num(list_of_num[i][j], i * self.cell_size + self.cell_size / 2,
                              j * self.cell_size + self.cell_size / 2)

    def draw_num(self, num, x, y): # печать числа в клетке
        text = font.render(str(num), 0, GREEN)
        place = text.get_rect(center=(x, y))
        self.screen.blit(text, place)

    def draw_selected_cell(self, x, y): # выделение выбранной клетки
        xx = (x // self.cell_size) * self.cell_size
        yy = (y // self.cell_size) * self.cell_size
        pygame.draw.rect(self.screen, GREEN, (xx, yy, self.cell_size , self.cell_size ))

    def filling_fill(self): # заполнение матрици числами
        global list_of_num
        num = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        for y in range(9):
            for x in range(9):
                if list_of_num[y][x] == '':
                    for n in num:
                        if possible(list_of_num, n, y, x):
                            list_of_num[y][x] = n
                            print('True n ={}  y ={}  x ={}'.format(n,y,x))


    def run(self):
        global font
        global list_of_num
        pygame.init()
        clock = pygame.time.Clock()
        font = pygame.font.SysFont('arial', self.cell_size)
        pygame.display.set_caption('Sudoky')
        self.screen.fill(pygame.Color('white'))
        # self.create_fill()
        list_of_num = [['' for j in range(9)] for i in range(9)] # генерируем матрицу
        self.rand_num(list_of_num)
        running = True
        cd = True
        x, y = 0, 0
        selected = False
        while running:
            self.screen.fill(pygame.Color('white'))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:  # нажата клавиша
                    if event.key == pygame.K_n:
                        list_of_num = [['' for j in range(9)] for i in range(9)]
                        self.rand_num(list_of_num)
                    elif event.key == pygame.K_RIGHT:
                        self.next_num()
                    elif event.key == pygame.K_f:
                        self.filling_fill()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        x, y = (event.pos[0], event.pos[1])
                        if list_of_num[x//self.cell_size][y//self.cell_size] == '':
                            selected = True
                        else:
                            selected = False

            if selected:
                self.draw_selected_cell(x, y)
            self.draw_field(list_of_num)
            self.draw_grid()
            pygame.display.flip()
            clock.tick(15)

    pygame.quit()


if __name__ == '__main__':
    game = Sudoky(50)
    game.run()
