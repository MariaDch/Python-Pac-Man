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
font = pygame.font.get_default_font()
level = boards  # [active_level]
color = 'blue'
PI = math.pi
player_images = []
ghosts_images = []
for i in range(1, 5):
    player_images.append(pygame.transform.scale(pygame.image.load(f'asserts/player/{i}_stage.png'), (37, 37)))
player_x = 365
player_y = 522
direction = 0
counter = 0
flicker = False
can_turn_to = [False, False, False, False]  # R, L, U, D
direction_command = 0
player_speed = 2

for i in range(1, 6):
    ghosts_images.append(pygame.transform.scale(pygame.image.load(f'asserts/ghosts/{i}.png'), (37, 37)))


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
    num3 = 15
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
            if 12 <= centerX % num2 <= 18:
                if level[(centerY + num1) // num1][centerX // num2] < 3:
                    turns[3] = True
                if level[(centerY - num1) // num1][centerX // num2] < 3:
                    turns[2] = True
            if 12 <= centerY % num1 <= 18:
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
    screen.fill('black')
    draw_board(level, color)
    draw_player()
    center_x = player_x + 18
    center_y = player_y + 18
    pygame.draw.circle(screen, 'white', (center_x, center_y), 2)
    can_turn_to = check_position(center_x, center_y, level)
    player_x, player_y = move_player(player_x, player_y)

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

    if direction_command == 0 and can_turn_to[0]:
        direction = 0
    if direction_command == 1 and can_turn_to[1]:
        direction = 1
    if direction_command == 2 and can_turn_to[2]:
        direction = 2
    if direction_command == 3 and can_turn_to[3]:
        direction = 3

    if player_x >= 700:
        player_x = 30
    elif player_x < -30:
        player_x = 700

    pygame.display.flip()
pygame.quit()
