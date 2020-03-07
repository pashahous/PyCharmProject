import pygame
import time
# import os
import random
import math

FPS = 50
WIN_WIDTH = 500
WIN_HEIGHT = 500
COLOR = ['YELLOW', 'RED', 'GREEN', 'WHITE', 'BLUE']
NUM_BULLS = 2
balls = []
MAX_SPEED = 7
MIN_SPEED = -7
T = True


def main():
    pygame.init()
    win = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
    clock = pygame.time.Clock()

    run = True
    for i in range(NUM_BULLS):
        balls.append(Ball())

    while run:
        win.fill((255, 255, 255))
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            elif event.type == pygame.KEYDOWN:  # проверка нажатия клавиш
                pass

        pressed = pygame.mouse.get_pressed()
        pos = pygame.mouse.get_pos()
        if pressed[0]:
            for ball in balls:
                rasst = math.sqrt(pow((ball.x - pos[0]), 2) + pow((ball.y - pos[1]), 2))
                if rasst <= ball.R:
                    ball.x = pos[0]
                    ball.y = pos[1]
                    if time.time() - ball.last_time_selected > 0.3 and ball.selected == False:
                        ball.selected = True
                        ball.last_time_selected = time.time()
                        print('True')
                    elif time.time() - ball.last_time_selected > 0.3 and ball.selected == True:
                        ball.selected = False
                        ball.last_time_selected = time.time()
                        print('False')

        for ball in balls:
            ball.draw(win)
            ball.move()

            if ball.x - ball.R < 0 or ball.x + ball.R > WIN_WIDTH:
                ball.speed_x = -ball.speed_x
            if ball.y - ball.R < 0 or ball.y + ball.R > WIN_HEIGHT:
                ball.speed_y = -ball.speed_y
        pygame.display.update()

    pygame.quit()
    # quit()


def click_on_ball():
    pass


def draw_window(win):
    pass


class Ball:
    def __init__(self):
        self.x = random.randrange(0, WIN_WIDTH)
        self.y = random.randrange(0, WIN_HEIGHT)
        self.R = 30
        self.color = (random.randrange(0, 255), random.randrange(0, 255), random.randrange(0, 255))
        self.speed_x = random.randrange(MIN_SPEED, MAX_SPEED)
        self.speed_y = random.randrange(MIN_SPEED, MAX_SPEED)
        self.selected = False  # выделен ли шар
        self.last_time_selected = 0
        self.friction = 0.1

    def move(self):
        self.x = self.x + self.speed_x - self.friction
        self.y = self.x + self.speed_y - self.friction

    def draw(self, win):
        if self.selected:
            pygame.draw.circle(win, self.color, (int(self.x), int(self.y)), self.R, self.R - 25)
        else:
            pygame.draw.circle(win, self.color, (int(self.x), int(self.y)), self.R, self.R)


if __name__ == "__main__":
    main()
