import pygame
from pygame.locals import *
from random import randint


pygame.init()

res = (600, 600)
win = pygame.display.set_mode(res)
pygame.display.set_caption('SNAKE')

red = (255, 0, 0)
grn = (0, 255, 0)
wht = (255, 255, 255)
black = (0, 0, 0)

score = 0

x, y, fontSize = 20, 550, 40
text = 'Score: '
myFont = pygame.font.SysFont('None', fontSize)
death_x, death_y, deathSize = 100, 200, 100
fin_score_x, fin_score_y, fin_scoreSize = 120, 270, 50


class Snake:
    def __init__(self):
        self.head_pos = (300, 300)
        self.body_pos = [(300, 300), (300, 320), (300, 340)]  # 280, 300)
        self.speed = 20
        self.direction = 'up'
        self.color = red
        self.width = 20
        self.new_body = False

    def move(self):
        if self.direction == 'up':
            self.head_pos = (self.head_pos[0], self.head_pos[1] - self.speed)

        elif self.direction == 'down':
            self.head_pos = (self.head_pos[0], self.head_pos[1] + self.speed)

        elif self.direction == 'left':
            self.head_pos = (self.head_pos[0] - self.speed, self.head_pos[1])

        elif self.direction == 'right':
            self.head_pos = (self.head_pos[0] + self.speed, self.head_pos[1])

        if self.head_pos[0] <= 0:  # WALL COLLISION CHECK
            self.head_pos = (590, self.head_pos[1])

        elif self.head_pos[0] >= 600:
            self.head_pos = (10, self.head_pos[1])

        if self.head_pos[1] <= 0:
            self.head_pos = (self.head_pos[0], 590)

        elif self.head_pos[1] >= 600:
            self.head_pos = (self.head_pos[0], 10)

        self.body_pos.insert(0, self.head_pos)
        if not self.new_body:  # don't delete if need to add new
            self.body_pos.pop(-1)
        else:
            self.new_body = False

    def draw_body(self):
        for block in self.body_pos:
            block_rect = pygame.Rect(block[0], block[1], self.width, self.width)
            pygame.draw.rect(win, self.color, block_rect)


class Food:
    def __init__(self):
        self.food_pos = (randint(20, 580), randint(20, 580))
        self.color = grn
        self.width = 20

    def draw_food(self):
            pygame.draw.rect(win, self.color, (self.food_pos[0], self.food_pos[1], self.width, self.width))


food = Food()
food_eaten = False
snake = Snake()
working = True


def controls():
    global working
    for event in pygame.event.get():
        if event.type == QUIT:
            working = False
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                working = False
            if event.key == K_RIGHT:
                if snake.direction != 'left':
                    snake.direction = 'right'
            elif event.key == K_LEFT:
                if snake.direction != 'right':
                    snake.direction = 'left'
            elif event.key == K_UP:
                if snake.direction != 'down':
                    snake.direction = 'up'
            elif event.key == K_DOWN:
                if snake.direction != 'up':
                    snake.direction = 'down'


def death():
    win.fill(black)
    death_text = 'YOU DIED'
    score_text = 'Your score is '
    death_font = pygame.font.SysFont('None', deathSize)
    death_image = death_font.render(death_text, 5, red)
    score_font = pygame.font.SysFont('None', fin_scoreSize)
    fin_score_image = score_font.render(score_text + str(score), 5, wht)
    win.blit(death_image, (death_x, death_y))
    win.blit(fin_score_image, (fin_score_x, fin_score_y))


def game():
    global food
    global food_eaten
    global working
    global score

    win.fill(wht)
    text_image = myFont.render(text + str(score), 5, black)
    win.blit(text_image, (x, y))

    snake.draw_body()
    snake.move()

    if food_eaten:
        food = Food()
        food_eaten = False
    food.draw_food()

    pygame.display.update()
    if (pygame.Rect(snake.head_pos[0], snake.head_pos[1], snake.width, snake.width)).colliderect(pygame.Rect(food.food_pos[0], food.food_pos[1], food.width, food.width)):
        snake.new_body = True
        food_eaten = True
        score += 10
    head = True
    for body in snake.body_pos:
        if (pygame.Rect(snake.head_pos[0], snake.head_pos[1], snake.width, snake.width)).colliderect(pygame.Rect(body[0], body[1], snake.width, snake.width)) and not head:
            working = False
            pygame.time.delay(2000)
            death()
            pygame.display.update()
            pygame.time.delay(3000)
        else:
            head = False


while working:
    pygame.time.Clock().tick(15)
    controls()
    game()
pygame.quit()
