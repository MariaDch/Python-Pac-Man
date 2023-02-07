# Pac-Man game project for Python course in FMI
from boards import boards
import pygame
import math

pygame.init()

WIDTH = 750
HEIGHT = 780
screen = pygame.display.set_mode([WIDTH, HEIGHT])
timer = pygame.time.Clock()
fps = 60
my_font = pygame.font.SysFont('arial', 20)
level = boards  # [active_level]
color = 'blue'
PI = math.pi
player_images = []
ghosts_images = []
for i in range(1, 5):
    player_images.append(pygame.transform.scale(pygame.image.load(f'asserts/player/{i}_stage.png'), (35, 35)))
pinky_image = pygame.transform.scale(pygame.image.load(f'asserts/ghosts/1.png'), (35, 35))
blinky_image = pygame.transform.scale(pygame.image.load(f'asserts/ghosts/2.png'), (35, 35))
inky_image = pygame.transform.scale(pygame.image.load(f'asserts/ghosts/3.png'), (35, 35))
clyde_image = pygame.transform.scale(pygame.image.load(f'asserts/ghosts/4.png'), (35, 35))
dead_image = pygame.transform.scale(pygame.image.load(f'asserts/ghosts/5.png'), (35, 35))
eyes_image = pygame.transform.scale(pygame.image.load(f'asserts/ghosts/6.png'), (35, 35))
player_x = 365
player_y = 522
direction = 0
counter = 0
blinky_x = 50
blinky_y = 58
blinky_direction = 0
inky_x = 362
inky_y = 300
inky_direction = 2
pinky_x = 362
pinky_y = 345
pinky_direction = 2
clyde_x = 362
clyde_y = 345
clyde_direction = 2
flicker = False
can_turn_to = [False, False, False, False]  # R, L, U, D
direction_command = 0
player_speed = 2
score = 0
powerUp = 0
powerCount = 0
eaten_ghosts = [False, False, False, False]
ghost_targets = [(player_x, player_y), (player_x, player_y), (player_x, player_y), (player_x, player_y)]
blinky_dead = False
inky_dead = False
clyde_dead = False
pinky_dead = False
blinky_in_box = False
inky_in_box = False
clyde_in_box = False
pinky_in_box = False
ghost_speed = 2
startup_counter = 0
moving = False
lives = 3


class Ghost:
    def __init__(self, x_coord, y_coord, target, speed, image, direct, is_dead, is_in_box, id):
        self._x_pos = x_coord
        self._y_pos = y_coord
        self._center_x = self._x_pos + 18
        self._center_y = self._y_pos + 18
        self._target = target
        self._speed = speed
        self._image = image
        self._direction = direct
        self._is_dead = is_dead
        self._is_in_box = is_in_box
        self._id = id
        self._turns, self._is_in_box = self.check_collisions()
        self._rect = self.draw()

    def draw(self):
        if (not powerUp and not self._is_dead) or (eaten_ghosts[self._id] and powerUp and not self._is_dead):
            screen.blit(self._image, (self._x_pos, self._y_pos))
        elif powerUp and not self._is_dead and not eaten_ghosts[self._id]:
            screen.blit(dead_image, (self._x_pos, self._y_pos))
        else:
            screen.blit(eyes_image, (self._x_pos, self._y_pos))
        ghost_rect = pygame.rect.Rect((self._center_x - 14, self._center_y - 14), (28, 28))
        return ghost_rect

    def check_collisions(self):
        num1 = (HEIGHT - 50) // 32
        num2 = WIDTH // 30
        num3 = 11
        self._turns = [False, False, False, False]
        if 0 < self._center_x // 30 < 29:
            if level[(self._center_y - num3) // num1][self._center_x // num2] == 9:
                self._turns[2] = True
            if level[self._center_y // num1][(self._center_x - num3) // num2] < 3 \
                    or (level[self._center_y // num1][(self._center_x - num3) // num2] == 9 and (
                    self._is_in_box or self._is_dead)):
                self._turns[1] = True
            if level[self._center_y // num1][(self._center_x + num3) // num2] < 3 \
                    or (level[self._center_y // num1][(self._center_x + num3) // num2] == 9 and (
                    self._is_in_box or self._is_dead)):
                self._turns[0] = True
            if level[(self._center_y + num3) // num1][self._center_x // num2] < 3 \
                    or (level[(self._center_y + num3) // num1][self._center_x // num2] == 9 and (
                    self._is_in_box or self._is_dead)):
                self._turns[3] = True
            if level[(self._center_y - num3) // num1][self._center_x // num2] < 3 \
                    or (level[(self._center_y - num3) // num1][self._center_x // num2] == 9 and (
                    self._is_in_box or self._is_dead)):
                self._turns[2] = True

            if self._direction == 2 or self._direction == 3:
                if 8 <= self._center_x % num2 <= 14:
                    if level[(self._center_y + num3) // num1][self._center_x // num2] < 3 \
                            or (level[(self._center_y + num3) // num1][self._center_x // num2] == 9 and (
                            self._is_in_box or self._is_dead)):
                        self._turns[3] = True
                    if level[(self._center_y - num3) // num1][self._center_x // num2] < 3 \
                            or (level[(self._center_y - num3) // num1][self._center_x // num2] == 9 and (
                            self._is_in_box or self._is_dead)):
                        self._turns[2] = True
                if 8 <= self._center_y % num1 <= 14:
                    if level[self._center_y // num1][(self._center_x - num2) // num2] < 3 \
                            or (level[self._center_y // num1][(self._center_x - num2) // num2] == 9 and (
                            self._is_in_box or self._is_dead)):
                        self._turns[1] = True
                    if level[self._center_y // num1][(self._center_x + num2) // num2] < 3 \
                            or (level[self._center_y // num1][(self._center_x + num2) // num2] == 9 and (
                            self._is_in_box or self._is_dead)):
                        self._turns[0] = True

            if self._direction == 0 or self._direction == 1:
                if 8 <= self._center_x % num2 <= 14:
                    if level[(self._center_y + num3) // num1][self._center_x // num2] < 3 \
                            or (level[(self._center_y + num3) // num1][self._center_x // num2] == 9 and (
                            self._is_in_box or self._is_dead)):
                        self._turns[3] = True
                    if level[(self._center_y - num3) // num1][self._center_x // num2] < 3 \
                            or (level[(self._center_y - num3) // num1][self._center_x // num2] == 9 and (
                            self._is_in_box or self._is_dead)):
                        self._turns[2] = True
                if 12 <= self._center_y % num1 <= 18:
                    if level[self._center_y // num1][(self._center_x - num3) // num2] < 3 \
                            or (level[self._center_y // num1][(self._center_x - num3) // num2] == 9 and (
                            self._is_in_box or self._is_dead)):
                        self._turns[1] = True
                    if level[self._center_y // num1][(self._center_x + num3) // num2] < 3 \
                            or (level[self._center_y // num1][(self._center_x + num3) // num2] == 9 and (
                            self._is_in_box or self._is_dead)):
                        self._turns[0] = True
        else:
            self._turns[0] = True
            self._turns[1] = True
        if 340 < self._x_pos < 540 and 300 < self._y_pos < 410:
            self._is_in_box = True
        else:
            self._is_in_box = False
        return self._turns, self._is_in_box


def display_score():
    score_text = my_font.render(f'Score: {score}', True, 'white')
    screen.blit(score_text, (10, 720))
    if powerUp:
        pygame.draw.circle(screen, 'blue', (140, 730), 15)
    for i in range(lives):
        screen.blit(pygame.transform.scale(player_images[0], (25, 25)), (600 + i * 30, 720))


def check_collisions(_score, power_up, power_count, eatenGhosts):
    num1 = (HEIGHT - 50) // 32
    num2 = WIDTH // 30
    if 0 < player_x < 720:
        if level[center_y // num1][center_x // num2] == 1:
            level[center_y // num1][center_x // num2] = 0
            _score += 10
        if level[center_y // num1][center_x // num2] == 2:
            level[center_y // num1][center_x // num2] = 0
            _score += 50
            power_up = True
            power_count = 0
            eatenGhosts = [False, False, False, False]
    return _score, power_up, power_count, eatenGhosts


def draw_board(lvl, v_color):
    num1 = (HEIGHT - 50) // 32
    num2 = WIDTH // 30
    for i in range(len(lvl)):
        for j in range(len(lvl[i])):
            if lvl[i][j] == 1:
                pygame.draw.circle(screen, 'white', (j * num2 + 0.5 * num2, i * num1 + 0.5 * num1), 3)
            if lvl[i][j] == 2 and not flicker:
                pygame.draw.circle(screen, 'white', (j * num2 + 0.5 * num2, i * num1 + 0.5 * num1), 8)
            if lvl[i][j] == 3:
                pygame.draw.line(screen, v_color, (j * num2 + 0.5 * num2, i * num1), (j * num2 + 0.5 * num2,
                                                                                      i * num1 + num1), 2)
            if lvl[i][j] == 4:
                pygame.draw.line(screen, v_color, (j * num2, i * num1 + 0.5 * num1), (j * num2 + num2,
                                                                                      i * num1 + 0.5 * num1), 2)
            if lvl[i][j] == 5:
                pygame.draw.arc(screen, v_color, [(j * num2 - num2 * 0.4) - 2, i * num1 + 0.5 * num1, num2, num1]
                                , 0, PI / 2, 2)
            if lvl[i][j] == 6:
                pygame.draw.arc(screen, v_color, [j * num2 + num2 * 0.5, i * num1 + 0.5 * num1, num2, num1]
                                , PI / 2, PI, 2)
            if lvl[i][j] == 7:
                pygame.draw.arc(screen, v_color, [j * num2 + num2 * 0.5, i * num1 - 0.4 * num1, num2, num1]
                                , PI, 3 * PI / 2, 2)
            if lvl[i][j] == 8:
                pygame.draw.arc(screen, v_color, [(j * num2 - num2 * 0.4) - 2, i * num1 - 0.4 * num1, num2, num1]
                                , 3 * PI / 2, 2 * PI, 2)
            if lvl[i][j] == 9:
                pygame.draw.line(screen, 'white', (j * num2, i * num1 + 0.5 * num1), (j * num2 + num2,
                                                                                      i * num1 + 0.5 * num1), 2)


def draw_player():
    if direction == 0:  # RIGHT
        screen.blit(player_images[counter // 5], (player_x, player_y))
    elif direction == 1:  # LEFT
        screen.blit(pygame.transform.flip(player_images[counter // 5], True, False), (player_x, player_y))
    elif direction == 2:  # UP
        screen.blit(pygame.transform.rotate(player_images[counter // 5], 90), (player_x, player_y))
    elif direction == 3:  # DOWN
        screen.blit(pygame.transform.rotate(player_images[counter // 5], 270), (player_x, player_y))


def check_position(centerX, centerY, lvl):
    turns = [False, False, False, False]
    num1 = (HEIGHT - 50) // 32
    num2 = (WIDTH // 30)
    num3 = 11
    # check collisions based on center x and center y of player +/- fudge number
    if centerX // 30 < 29:
        if direction == 0:
            if level[centerY // num1][(centerX - num3) // num2] < 3:
                turns[1] = True
        if direction == 1:
            if level[centerY // num1][(centerX + num3) // num2] < 3:
                turns[0] = True
        if direction == 2:
            if level[(centerY + num3) // num1][centerX // num2] < 3:
                turns[3] = True
        if direction == 3:
            if level[(centerY - num3) // num1][centerX // num2] < 3:
                turns[2] = True

        if direction == 2 or direction == 3:
            if 12 <= centerX % num2 <= 18:
                if level[(centerY + num3) // num1][centerX // num2] < 3:
                    turns[3] = True
                if level[(centerY - num3) // num1][centerX // num2] < 3:
                    turns[2] = True
            if 12 <= centerY % num1 <= 18:
                if level[centerY // num1][(centerX - num2) // num2] < 3:
                    turns[1] = True
                if level[centerY // num1][(centerX + num2) // num2] < 3:
                    turns[0] = True
        if direction == 0 or direction == 1:
            if 8 <= centerX % num2 <= 14:
                if level[(centerY + num1) // num1][centerX // num2] < 3:
                    turns[3] = True
                if level[(centerY - num1) // num1][centerX // num2] < 3:
                    turns[2] = True
            if 8 <= centerY % num1 <= 14:
                if level[centerY // num1][(centerX - num3) // num2] < 3:
                    turns[1] = True
                if level[centerY // num1][(centerX + num3) // num2] < 3:
                    turns[0] = True
    else:
        turns[0] = True
        turns[1] = True

    return turns


def move_player(pl_x, pl_y):
    # R, L, U, D
    if direction == 0 and can_turn_to[0]:
        pl_x += player_speed
    elif direction == 1 and can_turn_to[1]:
        pl_x -= player_speed
    elif direction == 2 and can_turn_to[2]:
        pl_y -= player_speed
    elif direction == 3 and can_turn_to[3]:
        pl_y += player_speed
    return pl_x, pl_y


run = True
while run:
    timer.tick(fps)
    if counter < 19:
        counter += 1
        if counter > 10:
            flicker = False

    else:
        counter = 0
        flicker = True

    if powerUp and powerCount < 600:
        powerCount += 1
    elif powerUp and powerCount >= 600:
        powerCount = 0
        powerUp = False
        eaten_ghosts = [False, False, False, False]
    if startup_counter < 180:
        moving = False
        startup_counter += 1
    else:
        moving = True

    screen.fill('black')
    draw_board(level, color)
    draw_player()
    blinky = Ghost(blinky_x, blinky_y, ghost_targets[0], ghost_speed, blinky_image, blinky_direction, blinky_dead,
                   blinky_in_box, 0)
    inky = Ghost(inky_x, inky_y, ghost_targets[1], ghost_speed, inky_image, inky_direction, inky_dead,
                 inky_in_box, 1)
    pinky = Ghost(pinky_x, pinky_y, ghost_targets[2], ghost_speed, pinky_image, pinky_direction, pinky_dead,
                  pinky_in_box, 2)
    clyde = Ghost(clyde_x, clyde_y, ghost_targets[3], ghost_speed, clyde_image, clyde_direction, clyde_dead,
                  clyde_in_box, 0)
    display_score()
    center_x = player_x + 18
    center_y = player_y + 18
    pygame.draw.circle(screen, 'white', (center_x, center_y), 2)
    can_turn_to = check_position(center_x, center_y, level)
    if moving:
        player_x, player_y = move_player(player_x, player_y)
    score, powerUp, powerCount, eaten_ghosts = check_collisions(score, powerUp, powerCount, eaten_ghosts)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                direction_command = 0
            if event.key == pygame.K_LEFT:
                direction_command = 1
            if event.key == pygame.K_UP:
                direction_command = 2
            if event.key == pygame.K_DOWN:
                direction_command = 3
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_RIGHT and direction_command == 0:
                direction_command = direction
            if event.key == pygame.K_LEFT and direction_command == 1:
                direction_command = direction
            if event.key == pygame.K_UP and direction_command == 2:
                direction_command = direction
            if event.key == pygame.K_DOWN and direction_command == 3:
                direction_command = direction

    for i in range(0, 4):
        if direction_command == i and can_turn_to[i]:
            direction = i

    if player_x >= 700:
        player_x = 30
    elif player_x < -30:
        player_x = 700

    pygame.display.flip()
pygame.quit()
