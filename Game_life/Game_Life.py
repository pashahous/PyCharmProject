import pygame as pygame
import random
import copy

WIN_WIDTH = 640
WIN_HEIGHT = 480
CELL_SIZE = 10
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
clist = []
HEIGHT_INFORM_PANEL = 0 # размер информационной панели
blue_cell = False  # set True if want play life with blue cell


# blue cell create when neigbour = 4


class GameOfLife:
    def __init__(self, widht=640, height=480, cell_size=10, speed=10):
        self.width = widht
        self.height = height
        self.cell_size = cell_size
        self.generation = 0

        # Setup window size
        self.screen_size = widht, height + HEIGHT_INFORM_PANEL # create  window with size w,h + iform panel

        # create new window
        self.screen = pygame.display.set_mode(self.screen_size)

        # calculate num of cells on vertical and horizontal
        self.cell_width = self.width // self.cell_size
        self.cell_height = self.height // self.cell_size

        # speed of game
        self.speed = speed

    # def draw_information_panel(self):
    #     """ Write on bottom information"""
    #     input1 = pygame.InputBox(50, self.height + 25, 75, self.height+35)

    def draw_grid(self):
        for x in range(0, self.width, self.cell_size):
            pygame.draw.line(self.screen, pygame.Color('black'),
                             (x, 0), (x, self.width))
        for y in range(0, self.height + 1 * self.cell_size, self.cell_size):
            pygame.draw.line(self.screen, pygame.Color('black'),
                             (0, y), (self.height, y))

    def cell_list(self, randomize=False):
        """
         Создание списка клеток.

         Клетка считается живой, если ее значение равно  1.
         В противном случае клетка считается мертвой, то
         есть ее значение равно 0.
         Если параметр randomize = True, то создается список, где
         каждая клетка может быть равновероятно живой или мертвой.
         """
        cellist = []
        if randomize:
            for x in range(self.width // self.cell_size):
                cellist.append([])
                for y in range(self.height // self.cell_size):
                    cellist[x].append(random.choice([0, 1]))
            return cellist
        else:
            return [[0] * (self.height // self.cell_size) for i in range(self.width // self.cell_size)]
            # return [[0, 0, 0, 0, 0], [0, 0, 1, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0]]

    def draw_cell_list(self, rects):
        for row in range(len(rects)):
            for col in range(len(rects[row])):
                if rects[row][col] == 1:
                    pygame.draw.rect(self.screen, GREEN, (
                        col * self.cell_size + 1, row * self.cell_size + 1, self.cell_size - 1, self.cell_size - 1))
                elif rects[row][col] == 0:
                    pygame.draw.rect(self.screen, WHITE, (
                        col * self.cell_size + 1, row * self.cell_size + 1, self.cell_size - 1, self.cell_size - 1))
                elif rects[row][col] == 2 and blue_cell:
                    pygame.draw.rect(self.screen, BLUE, (
                        col * self.cell_size + 1, row * self.cell_size + 1, self.cell_size - 1, self.cell_size - 1))

    def click_cell(self, x, y, cell_list):
        self.x = x
        self.y = y
        if cell_list[self.y // self.cell_size][self.x // self.cell_size] == 1:
            cell_list[self.y // self.cell_size][self.x // self.cell_size] = 0
        else:
            cell_list[self.y // self.cell_size][self.x // self.cell_size] = 1
            # print('xi = {}  yj = {} '.format(self.x // self.cell_size, self.y // self.cell_size))

    def new_random_live_cell(self, clist, n_cell):
        # create ner random green cell
        # clist : list when append cell
        # n_cell: number of cell for apend per generation
        t = False
        while t:
            for _ in range(n_cell):
                col = int(random.random() * self.width // self.cell_size)
                row = int(random.random() * self.height // self.cell_size)
                if clist[col][row] == 0:
                    # print('col {} row {}'.format(col,row))
                    clist[row][col] = 1
                    t = False
                    pygame.draw.rect(self.screen, RED, (
                        col * self.cell_size + 1, row * self.cell_size + 1, self.cell_size - 1, self.cell_size - 1))
        pygame.display.flip()

    def get_neighbours(self, cell_list):
        row = len(cell_list)
        column = len(cell_list[0])
        new_cell_list = [[0] * column for i in range(row)]
        for i in range(len(cell_list) - 1):
            for j in range(len(cell_list[i]) - 1):
                neigbours = 0
                neigbours_blue = 0
                for n, m in [(-1, 1), (-1, -1), (-1, 0), (1, 1), (0, -1), (0, 1), (1, -1), (1, 0)]:
                    if cell_list[i + n][j + m] == 1:
                        neigbours += 1
                    if cell_list[i + n][j + m] == 2:  # blue
                        neigbours_blue += 1
                if neigbours == 3:
                    new_cell_list[i][j] = 1
                elif neigbours == 2 and cell_list[i][j] == 1:
                    new_cell_list[i][j] = 1
                elif neigbours == 4 and blue_cell:
                    new_cell_list[i][j] = 2
                else:
                    new_cell_list[i][j] = 0

        return new_cell_list

    def flag_play(self):
        self.flag = 0

    def print_list(self, list):
        for i in list:
            for j in i:
                print(j, end=' ')
        print('')

    def run(self):

        pygame.init()
        clock = pygame.time.Clock()
        # self.draw_information_panel() // панель для вывода информации
        pygame.display.set_caption('Game of Life')
        self.screen.fill(pygame.Color('white'))
        running = True
        clist = self.cell_list(randomize=True)
        paused = True
        time_for_new_cell = 0
        n_cell = (self.height // self.cell_size * self.width // self.cell_size) // 5000  # num of new cell in cel
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        self.click_cell(event.pos[0], event.pos[1], clist)
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_p:
                        if paused:
                            paused = False
                        else:
                            paused = True

            self.draw_grid()
            self.draw_cell_list(clist)
            pygame.display.flip()

            if not paused:
                clist = copy.copy(self.get_neighbours(clist))
                time_for_new_cell += 50

            if time_for_new_cell > 100:
                time_for_new_cell = 0
                self.new_random_live_cell(clist, n_cell)  # CREATE new rand GREEN cell

            clock.tick(self.speed)
        pygame.quit()


if __name__ == '__main__':
    game = GameOfLife(400, 400, 20, speed=20)
    game.run()
